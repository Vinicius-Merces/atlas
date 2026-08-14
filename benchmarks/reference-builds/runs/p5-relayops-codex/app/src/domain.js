import { createHmac, timingSafeEqual } from "node:crypto";
import { hash, id, iso, passwordHash } from "./store.js";

export class AppError extends Error {
  constructor(status, code, message, fields = null) { super(message); this.status=status; this.code=code; this.fields=fields; }
}
const fail = (status, code, message, fields) => { throw new AppError(status,code,message,fields); };
const clean = value => String(value ?? "").trim();
const email = value => clean(value).toLowerCase();
const allowed = (ctx, roles) => ctx && roles.includes(ctx.role);
const requireRole = (ctx, roles) => { if (!allowed(ctx,roles)) fail(403,"FORBIDDEN","Seu perfil não permite esta ação."); };
const tenant = ctx => { if (!ctx?.tenantId) fail(403,"TENANT_REQUIRED","Contexto de organização obrigatório."); return ctx.tenantId; };
const correlation = ctx => ctx?.correlationId || id("cor");

export class RelayOps {
  constructor(store, options = {}) {
    this.store=store;
    this.webhookSecret=options.webhookSecret || process.env.RELAYOPS_WEBHOOK_SECRET || "local-webhook-not-for-production";
    this.emailMode="healthy";
    this.paymentMode="healthy";
  }

  audit(ctx, action, resource, resourceId, result, reason, details={}) {
    return this.store.audit({tenantId:ctx?.tenantId,actorId:ctx?.userId,role:ctx?.role || "anonymous",action,resource,resourceId,result,reason,correlationId:correlation(ctx),details});
  }
  denied(ctx, action, resource, resourceId, reason="tenant or role boundary") {
    this.audit(ctx,action,resource,resourceId,"denied",reason); fail(403,"DENIED","Acesso negado.");
  }
  notFound(ctx, action, resource, resourceId) {
    this.audit(ctx,action,resource,resourceId,"denied","object outside trusted tenant scope"); fail(404,"NOT_FOUND","Registro não encontrado.");
  }

  register(input) {
    const fields={};
    const name=clean(input.name), orgName=clean(input.organization), userEmail=email(input.email), password=String(input.password||"");
    if(name.length<2) fields.name="Informe seu nome.";
    if(orgName.length<3) fields.organization="Informe o nome da empresa.";
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(userEmail)) fields.email="Use um e-mail válido.";
    if(password.length<10) fields.password="Use pelo menos 10 caracteres.";
    if(Object.keys(fields).length) fail(422,"VALIDATION","Revise os campos.",fields);
    const now=iso(), tenantId=id("org"), userId=id("usr");
    try {
      this.store.tx(()=>{
        this.store.run("INSERT INTO organizations VALUES (?,?,?,?,?)",tenantId,`${orgName.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"")}-${tenantId.slice(-5)}`,orgName,"active",now);
        this.store.run("INSERT INTO users VALUES (?,?,?,?,?,?)",userId,userEmail,name,passwordHash(password),null,now);
        this.store.run("INSERT INTO memberships VALUES (?,?,?,?,?)",tenantId,userId,"manager","active",1);
        this.store.run("INSERT INTO subscriptions VALUES (?,?,?,?,?,?,?,?)",tenantId,null,"trialing","trialing","trial",0,1,now);
        this.store.run("INSERT INTO entitlements VALUES (?,?,?,?,?,?,?)",tenantId,"operations",1,"trial","14-day evaluation",1,now);
      });
    } catch { fail(409,"ACCOUNT_EXISTS","Já existe uma conta com estes dados."); }
    return {tenantId,userId};
  }

  createInvite(ctx, input) {
    requireRole(ctx,["manager"]); const tenantId=tenant(ctx), target=email(input.email), role=clean(input.role);
    if(!["manager","dispatcher","technician","billing"].includes(role)) fail(422,"VALIDATION","Perfil inválido.");
    const tokenValue=`invite_${id("token")}`, inviteId=id("inv");
    this.store.run("INSERT INTO invites VALUES (?,?,?,?,?,?,?)",inviteId,tenantId,target,role,hash(tokenValue),new Date(Date.now()+86400000).toISOString(),null);
    this.enqueue(ctx,"email",`invite:${inviteId}`,{to:target,subject:"Convite para o RelayOps",inviteId});
    this.audit(ctx,"invite.create","membership",inviteId,"allowed",null,{role});
    return {inviteId,token:tokenValue,expiresIn:86400};
  }

  acceptInvite(input) {
    const invite=this.store.one("SELECT * FROM invites WHERE token_hash=?",hash(input.token));
    if(!invite || invite.used_at || invite.expires_at<iso()) fail(410,"INVITE_INVALID","Convite expirado ou já utilizado.");
    const target=email(input.email);
    if(target!==invite.email) fail(403,"INVITE_EMAIL","O convite pertence a outro e-mail.");
    let user=this.store.one("SELECT * FROM users WHERE email=?",target); const now=iso();
    this.store.tx(()=>{
      if(!user){const uid=id("usr");this.store.run("INSERT INTO users VALUES (?,?,?,?,?,?)",uid,target,clean(input.name),passwordHash(String(input.password||"")),null,now);user={id:uid};}
      this.store.run("INSERT INTO memberships VALUES (?,?,?,?,?)",invite.tenant_id,user.id,invite.role,"active",1);
      this.store.run("UPDATE invites SET used_at=? WHERE id=? AND used_at IS NULL",now,invite.id);
    });
    return {tenantId:invite.tenant_id,userId:user.id,role:invite.role};
  }

  dashboard(ctx) {
    const tenantId=tenant(ctx);
    const counts=this.store.all("SELECT status,COUNT(*) count FROM work_orders WHERE tenant_id=? GROUP BY status",tenantId);
    const queue=this.store.all(`SELECT w.*,c.name customer_name,u.name technician_name FROM work_orders w
      JOIN customers c ON c.tenant_id=w.tenant_id AND c.id=w.customer_id LEFT JOIN users u ON u.id=w.assigned_user_id
      WHERE w.tenant_id=? ORDER BY CASE w.priority WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 ELSE 2 END,w.updated_at DESC LIMIT 12`,tenantId);
    const entitlement=this.store.one("SELECT * FROM entitlements WHERE tenant_id=? AND feature='operations'",tenantId);
    return {counts,queue,entitlement,notifications:this.notifications(ctx)};
  }

  listCustomers(ctx, query="", status="") {
    const tenantId=tenant(ctx), q=`%${clean(query).slice(0,80)}%`;
    return this.store.all("SELECT * FROM customers WHERE tenant_id=? AND (?='' OR status=?) AND (name LIKE ? OR email LIKE ? OR external_ref LIKE ?) ORDER BY name LIMIT 100",tenantId,status,status,q,q,q);
  }
  customer(ctx, customerId) { const row=this.store.one("SELECT * FROM customers WHERE tenant_id=? AND id=?",tenant(ctx),customerId); if(!row)this.notFound(ctx,"customer.read","customer",customerId); return row; }
  createCustomer(ctx,input,idemKey) {
    requireRole(ctx,["manager","dispatcher"]); const tenantId=tenant(ctx), fields={};
    const data={name:clean(input.name),email:email(input.email),phone:clean(input.phone),siteAddress:clean(input.siteAddress),externalRef:clean(input.externalRef)||null};
    if(data.name.length<2)fields.name="Nome obrigatório."; if(!data.email.includes("@"))fields.email="E-mail inválido."; if(data.phone.length<8)fields.phone="Telefone inválido."; if(data.siteAddress.length<5)fields.siteAddress="Endereço obrigatório.";
    if(Object.keys(fields).length) fail(422,"VALIDATION","Revise os campos.",fields);
    const key=clean(idemKey); if(key){const prior=this.store.one("SELECT details_json FROM audit_log WHERE tenant_id=? AND action='customer.create' AND correlation_id=? AND result='allowed'",tenantId,key);if(prior)return JSON.parse(prior.details_json).result;}
    const customerId=id("cus"),now=iso();
    try{this.store.run("INSERT INTO customers(id,tenant_id,external_ref,name,email,phone,site_address,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,'active',?,?)",customerId,tenantId,data.externalRef,data.name,data.email,data.phone,data.siteAddress,now,now);}catch{fail(409,"CUSTOMER_CONFLICT","Cliente ou referência já existente.");}
    const result=this.customer(ctx,customerId); this.store.audit({tenantId,actorId:ctx.userId,role:ctx.role,action:"customer.create",resource:"customer",resourceId:customerId,result:"allowed",correlationId:key||correlation(ctx),details:{result}}); return result;
  }
  updateCustomer(ctx,customerId,input) {
    requireRole(ctx,["manager","dispatcher"]); const current=this.customer(ctx,customerId), expected=Number(input.version);
    if(expected!==current.version) fail(409,"VERSION_CONFLICT","O cliente foi atualizado por outra pessoa.");
    const changed=this.store.run("UPDATE customers SET name=?,phone=?,site_address=?,status=?,version=version+1,updated_at=? WHERE tenant_id=? AND id=? AND version=?",clean(input.name)||current.name,clean(input.phone)||current.phone,clean(input.siteAddress)||current.site_address,["active","inactive"].includes(input.status)?input.status:current.status,iso(),ctx.tenantId,customerId,expected);
    if(!changed.changes) fail(409,"VERSION_CONFLICT","Conflito de atualização."); this.audit(ctx,"customer.update","customer",customerId,"allowed"); return this.customer(ctx,customerId);
  }
  deleteCustomer(ctx,customerId){requireRole(ctx,["manager"]);this.customer(ctx,customerId);try{this.store.run("DELETE FROM customers WHERE tenant_id=? AND id=?",ctx.tenantId,customerId);}catch{fail(409,"CUSTOMER_IN_USE","Cliente possui ordens vinculadas.");}this.audit(ctx,"customer.delete","customer",customerId,"allowed");return {deleted:true};}

  listOrders(ctx,{query="",status="",priority=""}={}) {
    const tenantId=tenant(ctx),q=`%${clean(query).slice(0,80)}%`;
    let sql=`SELECT w.*,c.name customer_name,u.name technician_name FROM work_orders w JOIN customers c ON c.tenant_id=w.tenant_id AND c.id=w.customer_id LEFT JOIN users u ON u.id=w.assigned_user_id
      WHERE w.tenant_id=? AND (?='' OR w.status=?) AND (?='' OR w.priority=?) AND (w.title LIKE ? OR c.name LIKE ? OR w.id LIKE ?)`;
    const args=[tenantId,status,status,priority,priority,q,q,q];
    if(ctx.role==="technician"){sql+=" AND w.assigned_user_id=?";args.push(ctx.userId);} sql+=" ORDER BY w.updated_at DESC LIMIT 100"; return this.store.all(sql,...args);
  }
  order(ctx,workOrderId){const row=this.store.one(`SELECT w.*,c.name customer_name,c.site_address,u.name technician_name FROM work_orders w JOIN customers c ON c.tenant_id=w.tenant_id AND c.id=w.customer_id LEFT JOIN users u ON u.id=w.assigned_user_id WHERE w.tenant_id=? AND w.id=?`,tenant(ctx),workOrderId);if(!row)this.notFound(ctx,"work_order.read","work_order",workOrderId);if(ctx.role==="technician"&&row.assigned_user_id!==ctx.userId)this.denied(ctx,"work_order.read","work_order",workOrderId,"technician assignment boundary");return row;}
  createOrder(ctx,input,idemKey) {
    requireRole(ctx,["manager","dispatcher"]); const customer=this.customer(ctx,clean(input.customerId)); const title=clean(input.title); if(title.length<4)fail(422,"VALIDATION","Título obrigatório.",{title:"Use pelo menos 4 caracteres."});
    const workOrderId=id("wo"),now=iso(); this.store.run("INSERT INTO work_orders(id,tenant_id,customer_id,title,description,status,priority,assigned_user_id,scheduled_at,created_at,updated_at) VALUES (?,?,?,?,?,'new',?,?,?,?,?,?)",workOrderId,ctx.tenantId,customer.id,title,clean(input.description),["low","normal","high","urgent"].includes(input.priority)?input.priority:"normal",clean(input.assignedUserId)||null,clean(input.scheduledAt)||null,now,now);
    this.store.run("INSERT INTO work_order_events VALUES (?,?,?,?,?,?,?)",id("evt"),ctx.tenantId,workOrderId,ctx.userId,null,"new",now);
    const result=this.order(ctx,workOrderId);this.audit(ctx,"work_order.create","work_order",workOrderId,"allowed",null,{idempotencyKey:idemKey});this.notifyManagers(ctx,"work_order.created",`Nova ordem ${workOrderId}`,`${customer.name}: ${title}`);return result;
  }
  transitionOrder(ctx,workOrderId,input) {
    requireRole(ctx,["manager","dispatcher","technician"]);const current=this.order(ctx,workOrderId),next=clean(input.status),expected=Number(input.version);
    const paths={new:["scheduled","cancelled"],scheduled:["in_progress","blocked","cancelled"],in_progress:["blocked","completed"],blocked:["in_progress","cancelled"],completed:[],cancelled:[]};
    if(!paths[current.status]?.includes(next))fail(422,"INVALID_TRANSITION",`Transição ${current.status} → ${next} não permitida.`);
    if(ctx.role==="technician"&&!["in_progress","blocked","completed"].includes(next))this.denied(ctx,"work_order.transition","work_order",workOrderId,"technician transition boundary");
    const changed=this.store.run("UPDATE work_orders SET status=?,version=version+1,updated_at=? WHERE tenant_id=? AND id=? AND version=?",next,iso(),ctx.tenantId,workOrderId,expected);if(!changed.changes)fail(409,"VERSION_CONFLICT","A ordem mudou; recarregue e tente novamente.");
    this.store.run("INSERT INTO work_order_events VALUES (?,?,?,?,?,?,?)",id("evt"),ctx.tenantId,workOrderId,ctx.userId,current.status,next,iso());this.audit(ctx,"work_order.transition","work_order",workOrderId,"allowed",clean(input.reason),{from:current.status,to:next});return this.order(ctx,workOrderId);
  }

  upload(ctx,workOrderId,input) {
    requireRole(ctx,["manager","dispatcher","technician"]);this.order(ctx,workOrderId);const filename=clean(input.filename).replace(/[^a-zA-Z0-9._ -]/g,"_").slice(0,100),mime=clean(input.mime),body=Buffer.from(String(input.contentBase64||""),"base64");
    if(!filename||!["text/plain","application/pdf","image/png","image/jpeg"].includes(mime)||!body.length||body.length>262144)fail(422,"INVALID_FILE","Arquivo inválido ou maior que 256 KiB.");
    const attachmentId=id("att"),storageKey=`${ctx.tenantId}/${randomKey()}`;this.store.run("INSERT INTO attachments VALUES (?,?,?,?,?,?,?,?,?,?,?)",attachmentId,ctx.tenantId,workOrderId,storageKey,filename,mime,body.length,hash(body),body.toString("base64"),ctx.userId,iso());this.audit(ctx,"attachment.create","attachment",attachmentId,"allowed");return {id:attachmentId,filename,mime,size:body.length,workOrderId};
  }
  attachment(ctx,attachmentId){const row=this.store.one("SELECT * FROM attachments WHERE tenant_id=? AND id=?",tenant(ctx),attachmentId);if(!row)this.notFound(ctx,"attachment.read","attachment",attachmentId);return row;}

  search(ctx,query){const q=clean(query);if(q.length<2)return [];const like=`%${q.slice(0,80)}%`,tenantId=tenant(ctx);return [
    ...this.store.all("SELECT 'customer' type,id,name label,email detail FROM customers WHERE tenant_id=? AND (name LIKE ? OR email LIKE ? OR external_ref LIKE ?) LIMIT 20",tenantId,like,like,like),
    ...this.store.all("SELECT 'work_order' type,id,title label,status detail FROM work_orders WHERE tenant_id=? AND (title LIKE ? OR description LIKE ? OR id LIKE ?) LIMIT 20",tenantId,like,like,like)
  ];}

  notifyManagers(ctx,kind,title,body){for(const member of this.store.all("SELECT user_id FROM memberships WHERE tenant_id=? AND status='active' AND role IN ('manager','dispatcher')",ctx.tenantId)){const key=`${kind}:${hash(title+body).slice(0,16)}:${member.user_id}`;this.store.run("INSERT OR IGNORE INTO notifications VALUES (?,?,?,?,?,?,?,?,?)",id("not"),ctx.tenantId,member.user_id,kind,title,body,key,null,iso());}}
  notifications(ctx){return this.store.all("SELECT * FROM notifications WHERE tenant_id=? AND user_id=? ORDER BY created_at DESC LIMIT 30",tenant(ctx),ctx.userId);}
  readNotification(ctx,notificationId){const changed=this.store.run("UPDATE notifications SET read_at=? WHERE tenant_id=? AND user_id=? AND id=?",iso(),tenant(ctx),ctx.userId,notificationId);if(!changed.changes)this.notFound(ctx,"notification.read","notification",notificationId);return {read:true};}
  createNotification(ctx,targetUserId,input){requireRole(ctx,["manager","dispatcher"]);const member=this.store.one("SELECT 1 ok FROM memberships WHERE tenant_id=? AND user_id=? AND status='active'",tenant(ctx),targetUserId);if(!member)this.denied(ctx,"notification.create","notification",targetUserId,"recipient outside tenant");const key=clean(input.dedupeKey)||hash(`${targetUserId}:${input.title}`);this.store.run("INSERT OR IGNORE INTO notifications VALUES (?,?,?,?,?,?,?,?,?)",id("not"),ctx.tenantId,targetUserId,"manual",clean(input.title),clean(input.body),key,null,iso());return {created:true};}

  enqueue(ctx,type,operationKey,payload,maxAttempts=3){const tenantId=tenant(ctx);const jobId=id("job"),now=iso();this.store.run("INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,'queued',0,?,?,NULL,NULL,?,?)",jobId,tenantId,type,operationKey,JSON.stringify(payload),maxAttempts,ctx.authzVersion||null,now,now);return this.store.one("SELECT * FROM jobs WHERE tenant_id=? AND type=? AND operation_key=?",tenantId,type,operationKey);}
  runJob(jobId,{providerFail=false}={}) {
    const job=this.store.one("SELECT * FROM jobs WHERE id=?",jobId);if(!job)return null;if(job.status==="completed")return {...job,duplicate:true};
    const payload=JSON.parse(job.payload_json),now=iso();
    if(payload.workOrderId&&!this.store.one("SELECT 1 ok FROM work_orders WHERE tenant_id=? AND id=?",job.tenant_id,payload.workOrderId)){this.store.run("UPDATE jobs SET status='denied',last_error='tenant_context_mismatch',updated_at=? WHERE id=?",now,jobId);return this.store.one("SELECT * FROM jobs WHERE id=?",jobId);}
    if(payload.userId&&job.authz_version!=null){const member=this.store.one("SELECT * FROM memberships WHERE tenant_id=? AND user_id=?",job.tenant_id,payload.userId);if(!member||member.status!=="active"||member.authz_version!==job.authz_version){this.store.run("UPDATE jobs SET status='denied',last_error='stale_authorization',updated_at=? WHERE id=?",now,jobId);return this.store.one("SELECT * FROM jobs WHERE id=?",jobId);}}
    if(providerFail||this.emailMode==="outage") {const attempts=job.attempts+1,status=attempts>=job.max_attempts?"failed":"retry";this.store.run("UPDATE jobs SET status=?,attempts=?,last_error='provider_unavailable',run_after=?,updated_at=? WHERE id=?",status,attempts,new Date(Date.now()+attempts*1000).toISOString(),now,jobId);return this.store.one("SELECT * FROM jobs WHERE id=?",jobId);}
    this.store.tx(()=>{this.store.run("INSERT OR IGNORE INTO job_effects VALUES (?,?,?,?,?)",job.tenant_id,job.operation_key,job.type,id("effect"),now);this.store.run("UPDATE jobs SET status='completed',attempts=attempts+1,last_error=NULL,updated_at=? WHERE id=?",now,jobId);});return this.store.one("SELECT * FROM jobs WHERE id=?",jobId);
  }

  cachePut(ctx,scope,key,value,ttl=60){this.store.run("INSERT OR REPLACE INTO cache_entries VALUES (?,?,?,?,?,?)",tenant(ctx),scope,key,JSON.stringify(value),ctx.authzVersion,new Date(Date.now()+ttl*1000).toISOString());}
  cacheGet(ctx,scope,key){const row=this.store.one("SELECT * FROM cache_entries WHERE tenant_id=? AND scope=? AND cache_key=? AND expires_at>?",tenant(ctx),scope,key,iso());if(!row||row.authz_version!==ctx.authzVersion)return null;return JSON.parse(row.value_json);}
  entitlement(ctx,feature="operations"){const row=this.store.one("SELECT * FROM entitlements WHERE tenant_id=? AND feature=?",tenant(ctx),feature);return row&&row.enabled===1;}
  requireEntitlement(ctx,feature="operations"){if(!this.entitlement(ctx,feature))fail(402,"ENTITLEMENT_REQUIRED","Assinatura sem acesso a este recurso.");}

  checkout(ctx,input,idemKey){requireRole(ctx,["manager","billing"]);const tenantId=tenant(ctx),plan=clean(input.plan);if(!["core","scale"].includes(plan))fail(422,"PLAN_INVALID","Plano inválido.");if(this.paymentMode==="outage")fail(503,"PAYMENT_PROVIDER_UNAVAILABLE","Cobrança indisponível; nenhum acesso foi alterado.");const prior=this.store.one("SELECT * FROM checkout_sessions WHERE tenant_id=? AND idempotency_key=?",tenantId,idemKey);if(prior)return prior;const row={id:id("chk"),tenantId,plan,status:"pending",idemKey,createdAt:iso()};this.store.run("INSERT INTO checkout_sessions VALUES (?,?,?,?,?,?)",row.id,tenantId,plan,row.status,idemKey,row.createdAt);this.audit(ctx,"billing.checkout","subscription",row.id,"allowed",null,{plan});return row;}
  signWebhook(raw,timestamp=Math.floor(Date.now()/1000)){return `${timestamp}.${createHmac("sha256",this.webhookSecret).update(`${timestamp}.${raw}`).digest("hex")}`;}
  webhook(raw,signature) {
    const [ts,digest]=String(signature||"").split("."),expected=createHmac("sha256",this.webhookSecret).update(`${ts}.${raw}`).digest("hex");
    if(!ts||!digest||Math.abs(Date.now()/1000-Number(ts))>300||digest.length!==expected.length||!timingSafeEqual(Buffer.from(digest),Buffer.from(expected)))fail(401,"WEBHOOK_SIGNATURE","Assinatura inválida ou expirada.");
    let event;try{event=JSON.parse(raw);}catch{fail(400,"WEBHOOK_JSON","Payload inválido.");}
    const existing=this.store.one("SELECT * FROM webhook_events WHERE event_id=?",event.id);if(existing)return {duplicate:true,disposition:existing.disposition};
    const sub=this.store.one("SELECT * FROM subscriptions WHERE tenant_id=?",event.tenantId);if(!sub)fail(404,"SUBSCRIPTION_NOT_FOUND","Assinatura desconhecida.");
    const stale=Number(event.created)<sub.last_provider_ts, disposition=stale?"out_of_order_ignored":"accepted";
    this.store.tx(()=>{this.store.run("INSERT INTO webhook_events VALUES (?,?,?,?,?,?,?)",event.id,event.tenantId,event.type,Number(event.created),hash(raw),disposition,iso());if(!stale)this.store.run("UPDATE subscriptions SET provider_status=?,last_provider_ts=?,updated_at=? WHERE tenant_id=?",event.status,Number(event.created),iso(),event.tenantId);});
    if(!stale)this.reconcile(event.tenantId);return {duplicate:false,disposition};
  }
  reconcile(tenantId){if(this.paymentMode==="outage")fail(503,"PAYMENT_PROVIDER_UNAVAILABLE","Reconciliação agendada para nova tentativa.");const sub=this.store.one("SELECT * FROM subscriptions WHERE tenant_id=?",tenantId);const enabled=["active","trialing"].includes(sub.provider_status)?1:0,newStatus=enabled?"active":"revoked",version=sub.entitlement_version+1;this.store.tx(()=>{this.store.run("UPDATE subscriptions SET app_status=?,entitlement_version=?,updated_at=? WHERE tenant_id=?",newStatus,version,iso(),tenantId);this.store.run("INSERT OR REPLACE INTO entitlements VALUES (?,?,?,?,?,?,?)",tenantId,"operations",enabled,"reconciliation",`provider ${sub.provider_status}`,version,iso());this.store.run("DELETE FROM cache_entries WHERE tenant_id=? AND scope='entitlement'",tenantId);});return this.store.one("SELECT * FROM entitlements WHERE tenant_id=? AND feature='operations'",tenantId);}

  support(ctx,targetTenantId,reason,action="inspect") {
    if(ctx?.role!=="support")this.denied(ctx,"support.access","tenant",targetTenantId,"least privilege role denial");
    if(!targetTenantId)this.denied(ctx,"support.access","tenant",null,"explicit tenant context missing");
    if(!clean(reason))fail(422,"SUPPORT_REASON","Informe o motivo do acesso.");const org=this.store.one("SELECT * FROM organizations WHERE id=?",targetTenantId);if(!org)this.notFound(ctx,"support.access","tenant",targetTenantId);
    const scoped={...ctx,tenantId:targetTenantId},auditId=this.audit(scoped,`support.${action}`,"tenant",targetTenantId,"allowed",clean(reason),{operator:ctx.userId});return {tenant:{id:org.id,name:org.name,status:org.status},counts:{customers:this.store.one("SELECT COUNT(*) count FROM customers WHERE tenant_id=?",targetTenantId).count,orders:this.store.one("SELECT COUNT(*) count FROM work_orders WHERE tenant_id=?",targetTenantId).count},auditId};
  }
  auditRows(ctx){requireRole(ctx,["manager"]);return this.store.all("SELECT * FROM audit_log WHERE tenant_id=? ORDER BY created_at DESC LIMIT 100",tenant(ctx));}

  importCustomers(ctx,csv,operationKey){requireRole(ctx,["manager","dispatcher"]);const tenantId=tenant(ctx),source=String(csv||""),sourceHash=hash(source),prior=this.store.one("SELECT * FROM imports WHERE tenant_id=? AND operation_key=?",tenantId,operationKey);if(prior){if(prior.source_hash!==sourceHash)fail(409,"IDEMPOTENCY_MISMATCH","A chave já foi usada com outro arquivo.");return {...prior,report:JSON.parse(prior.report_json),duplicate:true};}if(Buffer.byteLength(source)>128000)fail(413,"IMPORT_TOO_LARGE","CSV maior que 128 KiB.");const lines=source.trim().split(/\r?\n/),headers=(lines.shift()||"").split(",").map(clean);if(headers.join(",")!=="external_ref,name,email,phone,site_address")fail(422,"IMPORT_HEADERS","Cabeçalhos esperados: external_ref,name,email,phone,site_address.");const report=[],importId=id("imp"),now=iso();let created=0,failed=0;this.store.tx(()=>{for(let i=0;i<lines.length;i++){const parts=lines[i].split(",").map(clean),[externalRef,name,userEmail,phone,siteAddress]=parts;let error=null;if(parts.length!==5)error="column_count";else if(!externalRef||!name||!userEmail.includes("@")||phone.length<8||siteAddress.length<5)error="row_validation";let entityId=null,status="failed";if(!error){const existing=this.store.one("SELECT id FROM customers WHERE tenant_id=? AND external_ref=?",tenantId,externalRef);if(existing){entityId=existing.id;status="duplicate";}else{entityId=id("cus");this.store.run("INSERT INTO customers(id,tenant_id,external_ref,name,email,phone,site_address,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,'active',?,?)",entityId,tenantId,externalRef,name,userEmail.toLowerCase(),phone,siteAddress,now,now);created++;status="created";}}else failed++;const row={row:i+2,status,error,entityId};report.push(row);this.store.run("INSERT INTO import_rows VALUES (?,?,?,?,?,?,?)",importId,tenantId,i+2,hash(lines[i]),status,entityId,error);}const state=failed?(created?"partial":"failed"):"completed";this.store.run("INSERT INTO imports VALUES (?,?,?,?,?,?,?,?,?)",importId,tenantId,operationKey,sourceHash,state,created,failed,JSON.stringify(report),now);});this.audit(ctx,"customers.import","import",importId,"allowed",null,{created,failed});return {...this.store.one("SELECT * FROM imports WHERE id=?",importId),report};}
  exportCustomers(ctx){requireRole(ctx,["manager","dispatcher","billing"]);const rows=this.listCustomers(ctx);const escape=v=>`"${String(v??"").replaceAll('"','""')}"`;const csv=["external_ref,name,email,phone,site_address,status",...rows.map(r=>[r.external_ref,r.name,r.email,r.phone,r.site_address,r.status].map(escape).join(","))].join("\n")+"\n";this.audit(ctx,"customers.export","export",id("exp"),"allowed",null,{rows:rows.length});return csv;}
}

function randomKey(){return `${Date.now().toString(36)}-${id("object")}`;}
