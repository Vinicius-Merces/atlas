import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { existsSync, mkdirSync } from "node:fs";
import { extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { randomUUID } from "node:crypto";
import { Store, hash, iso } from "./store.js";
import { RelayOps, AppError } from "./domain.js";
import { loginPage,registerPage,dashboardPage,customersPage,ordersPage,orderDetailPage,billingPage,dataPage,auditPage,supportPage,notFoundPage } from "./render.js";

const root=fileURLToPath(new URL(".",import.meta.url));
const publicRoot=join(root,"public");
const defaultData=resolve(root,"../data/relayops.sqlite");
const mime={".css":"text/css; charset=utf-8",".js":"text/javascript; charset=utf-8",".svg":"image/svg+xml",".png":"image/png",".webp":"image/webp"};
const roles={manager:"Manager",dispatcher:"Dispatcher",technician:"Technician",billing:"Billing",support:"Support"};

function headers(extra={}){return {"content-security-policy":"default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'","referrer-policy":"strict-origin-when-cross-origin","x-content-type-options":"nosniff","x-frame-options":"DENY","permissions-policy":"camera=(), microphone=(), geolocation=(), payment=()","cross-origin-opener-policy":"same-origin","cross-origin-resource-policy":"same-origin",...extra};}
function send(res,status,body,type="text/html; charset=utf-8",extra={}){res.writeHead(status,headers({"content-type":type,...extra}));res.end(body);}
function json(res,status,data,extra={}){send(res,status,JSON.stringify(data),"application/json; charset=utf-8",{"cache-control":"no-store",...extra});}
function redirect(res,path,extra={}){res.writeHead(303,headers({location:path,"cache-control":"no-store",...extra}));res.end();}
function cookies(req){return Object.fromEntries(String(req.headers.cookie||"").split(";").map(x=>x.trim().split("=")).filter(x=>x[0]).map(([k,...v])=>[k,decodeURIComponent(v.join("="))]));}
function cookie(req,token,clear=false){const secure=String(req.headers["x-forwarded-proto"]||"").includes("https")||String(process.env.PUBLIC_ORIGIN||"").startsWith("https");return `relayops_session=${clear?"":encodeURIComponent(token)}; Path=/; HttpOnly; SameSite=Lax; ${secure?"Secure; ":""}${clear?"Max-Age=0; ":"Max-Age=28800; "}`;}
function requestOrigin(req){return String(req.headers.origin||"").replace(/\/$/,"");}
function expectedOrigin(req){const proto=String(req.headers["x-forwarded-proto"]||"http").split(",")[0],host=String(req.headers["x-forwarded-host"]||req.headers.host||"").split(",")[0];return `${proto}://${host}`;}
function sameOrigin(req){const origin=requestOrigin(req);return Boolean(origin)&&origin===expectedOrigin(req);}
async function body(req,{raw=false,max=300000}={}){const chunks=[];let size=0;for await(const chunk of req){size+=chunk.length;if(size>max)throw new AppError(413,"BODY_TOO_LARGE","Payload excede o limite.");chunks.push(chunk);}const text=Buffer.concat(chunks).toString("utf8");if(raw)return text;try{return text?JSON.parse(text):{};}catch{throw new AppError(400,"INVALID_JSON","JSON inválido.");}}
function log(event,details={}){const clean=JSON.stringify({at:iso(),event,...details},(key,value)=>/password|cookie|authorization|signature|secret|contentBase64/i.test(key)?"[REDACTED]":value);process.stdout.write(`${clean}\n`);}

export function createApp(options={}){
  const store=options.store||new Store(options.dbPath||process.env.RELAYOPS_DB_PATH||(process.env.NODE_ENV==="test"?":memory:":defaultData));
  const domain=new RelayOps(store,options);
  const app=createServer(async(req,res)=>{
    const started=Date.now(),correlationId=String(req.headers["x-correlation-id"]||`cor_${randomUUID()}`),url=new URL(req.url||"/",`http://${req.headers.host||"localhost"}`),path=url.pathname;
    res.setHeader("x-correlation-id",correlationId);
    const token=cookies(req).relayops_session,session=store.session(token),ctx=session?{...session,correlationId}:null;
    try{
      if(req.method==="GET"&&path==="/api/health")return json(res,200,{ok:true,service:"relayops",database:"sqlite",time:iso()});
      if(req.method==="GET"&&path.startsWith("/assets/"))return staticFile(path,res);
      if(req.method==="GET"&&path==="/")return redirect(res,ctx?"/app":"/login");
      if(req.method==="GET"&&path==="/login")return send(res,200,loginPage());
      if(req.method==="GET"&&path==="/register")return send(res,200,registerPage());
      if(req.method==="GET"&&path.startsWith("/demo/")){
        if(process.env.RELAYOPS_DEMO_MODE!=="1")throw new AppError(404,"NOT_FOUND","Rota não encontrada.");
        const map={manager:"manager@northstar.test",dispatcher:"dispatcher@northstar.test",technician:"tech@northstar.test",billing:"billing@northstar.test",support:"support@relayops.test"},which=path.split("/")[2],email=map[which];if(!email)throw new AppError(404,"NOT_FOUND","Perfil de demonstração desconhecido.");const auth=store.createSession(email,which==="support"?"Support!2026":"RelayOps!2026");return redirect(res,which==="support"?"/support":"/app",{"set-cookie":cookie(req,auth.token)});
      }

      if(req.method==="GET"&&path.startsWith("/app")&&!ctx)return redirect(res,"/login");
      if(req.method==="GET"&&path==="/app")return send(res,200,dashboardPage(ctx,domain.dashboard(ctx)));
      if(req.method==="GET"&&path==="/app/customers")return send(res,200,customersPage(ctx,domain.listCustomers(ctx,url.searchParams.get("q")||"",url.searchParams.get("status")||"")));
      if(req.method==="GET"&&path==="/app/work-orders")return send(res,200,ordersPage(ctx,domain.listOrders(ctx,Object.fromEntries(url.searchParams)),domain.listCustomers(ctx)));
      if(req.method==="GET"&&/^\/app\/work-orders\/[^/]+$/.test(path)){const oid=decodeURIComponent(path.split("/").pop()),order=domain.order(ctx,oid),events=store.all("SELECT * FROM work_order_events WHERE tenant_id=? AND work_order_id=? ORDER BY created_at",ctx.tenantId,oid),attachments=store.all("SELECT id,filename,mime,size,created_at FROM attachments WHERE tenant_id=? AND work_order_id=? ORDER BY created_at DESC",ctx.tenantId,oid);return send(res,200,orderDetailPage(ctx,order,events,attachments));}
      if(req.method==="GET"&&path==="/app/billing"){const sub=store.one("SELECT * FROM subscriptions WHERE tenant_id=?",ctx.tenantId),ent=store.one("SELECT * FROM entitlements WHERE tenant_id=? AND feature='operations'",ctx.tenantId);return send(res,200,billingPage(ctx,sub,ent));}
      if(req.method==="GET"&&path==="/app/import-export")return send(res,200,dataPage(ctx));
      if(req.method==="GET"&&path==="/app/audit")return send(res,200,auditPage(ctx,domain.auditRows(ctx)));
      if(req.method==="GET"&&path==="/support"){if(!ctx)return redirect(res,"/login");if(ctx.role!=="support")domain.denied(ctx,"support.page","support",null,"least privilege role denial");return send(res,200,supportPage(ctx,store.all("SELECT id,name,status FROM organizations ORDER BY name")));}

      if(req.method==="POST"&&path==="/api/auth/login"){
        requireOrigin(req);rate(store,`login:${actor(req)}`,"login",8,600000);const input=await body(req),auth=store.createSession(input.email,input.password,input.tenantId||null);if(!auth){store.audit({role:"anonymous",action:"auth.login",resource:"session",result:"denied",reason:"invalid credentials",correlationId});throw new AppError(401,"LOGIN_INVALID","E-mail ou senha inválidos.");}store.audit({tenantId:auth.tenantId,actorId:auth.user.id,role:auth.user.global_role||"member",action:"auth.login",resource:"session",result:"allowed",correlationId});return json(res,200,{ok:true,redirect:auth.user.global_role?"/support":"/app"},{"set-cookie":cookie(req,auth.token)});
      }
      if(req.method==="POST"&&path==="/api/auth/register"){requireOrigin(req);rate(store,`register:${actor(req)}`,"register",4,3600000);const result=domain.register(await body(req));return json(res,201,{ok:true,...result});}
      if(req.method==="POST"&&path==="/api/auth/logout"){requireOrigin(req);store.revokeSession(token);return json(res,200,{ok:true},{"set-cookie":cookie(req,"",true)});}
      if(req.method==="POST"&&path==="/api/invites"){guard(ctx);requireOrigin(req);return json(res,201,domain.createInvite(ctx,await body(req)));}
      if(req.method==="POST"&&path==="/api/invites/accept"){requireOrigin(req);return json(res,200,domain.acceptInvite(await body(req)));}

      guardApi(path,ctx);if(req.method!=="GET"&&path!=="/api/billing/webhook")requireOrigin(req);
      if(req.method==="GET"&&path==="/api/dashboard")return json(res,200,domain.dashboard(ctx));
      if(req.method==="GET"&&path==="/api/customers")return json(res,200,domain.listCustomers(ctx,url.searchParams.get("q")||"",url.searchParams.get("status")||""));
      if(req.method==="POST"&&path==="/api/customers")return json(res,201,domain.createCustomer(ctx,await body(req),String(req.headers["idempotency-key"]||"")));
      if(/^\/api\/customers\/[^/]+$/.test(path)){const cid=decodeURIComponent(path.split("/").pop());if(req.method==="GET")return json(res,200,domain.customer(ctx,cid));if(req.method==="PATCH")return json(res,200,domain.updateCustomer(ctx,cid,await body(req)));if(req.method==="DELETE")return json(res,200,domain.deleteCustomer(ctx,cid));}
      if(req.method==="GET"&&path==="/api/work-orders")return json(res,200,domain.listOrders(ctx,Object.fromEntries(url.searchParams)));
      if(req.method==="POST"&&path==="/api/work-orders")return json(res,201,domain.createOrder(ctx,await body(req),String(req.headers["idempotency-key"]||"")));
      if(/^\/api\/work-orders\/[^/]+$/.test(path)&&req.method==="GET")return json(res,200,domain.order(ctx,decodeURIComponent(path.split("/").pop())));
      if(/^\/api\/work-orders\/[^/]+\/transition$/.test(path)&&req.method==="POST")return json(res,200,domain.transitionOrder(ctx,decodeURIComponent(path.split("/")[3]),await body(req)));
      if(/^\/api\/work-orders\/[^/]+\/attachments$/.test(path)&&req.method==="POST")return json(res,201,domain.upload(ctx,decodeURIComponent(path.split("/")[3]),await body(req)));
      if(/^\/api\/attachments\/[^/]+$/.test(path)&&req.method==="GET"){const attachment=domain.attachment(ctx,decodeURIComponent(path.split("/").pop())),buffer=Buffer.from(attachment.body_base64,"base64");return send(res,200,buffer,attachment.mime,{"content-disposition":`attachment; filename="${attachment.filename.replace(/["\r\n]/g,"")}"`,"content-length":String(buffer.length),"cache-control":"private, no-store"});}
      if(req.method==="GET"&&path==="/api/search"){rate(store,`${ctx.tenantId}:${ctx.userId}`,"search",80,600000);return json(res,200,domain.search(ctx,url.searchParams.get("q")||""));}
      if(req.method==="POST"&&/^\/api\/notifications\/[^/]+\/read$/.test(path))return json(res,200,domain.readNotification(ctx,decodeURIComponent(path.split("/")[3])));
      if(req.method==="POST"&&path==="/api/import/customers"){rate(store,`${ctx.tenantId}:${ctx.userId}`,"import",10,3600000);const input=await body(req);return json(res,200,domain.importCustomers(ctx,input.csv,input.operationKey||String(req.headers["idempotency-key"]||"")));}
      if(req.method==="GET"&&path==="/api/export/customers"){rate(store,`${ctx.tenantId}:${ctx.userId}`,"export",10,3600000);return send(res,200,domain.exportCustomers(ctx),"text/csv; charset=utf-8",{"content-disposition":"attachment; filename=relayops-customers.csv","cache-control":"private, no-store"});}
      if(req.method==="POST"&&path==="/api/billing/checkout")return json(res,201,domain.checkout(ctx,await body(req),String(req.headers["idempotency-key"]||"")));
      if(req.method==="POST"&&path==="/api/billing/webhook"){const raw=await body(req,{raw:true});return json(res,200,domain.webhook(raw,String(req.headers["x-relayops-signature"]||"")));}
      if(req.method==="POST"&&path==="/api/billing/demo-webhook"){if(process.env.RELAYOPS_DEMO_MODE!=="1")throw new AppError(404,"NOT_FOUND","Rota não encontrada.");return json(res,200,domain.demoWebhook(ctx,await body(req)));}
      if(req.method==="POST"&&path==="/api/billing/reconcile")return json(res,200,domain.reconcileFor(ctx));
      if(req.method==="POST"&&path==="/api/support/inspect"){const target=String(req.headers["x-support-tenant"]||"");return json(res,200,domain.support(ctx,target,(await body(req)).reason));}
      throw new AppError(404,"NOT_FOUND","Rota não encontrada.");
    }catch(error){const status=error instanceof AppError?error.status:500,code=error instanceof AppError?error.code:"INTERNAL",message=error instanceof AppError?error.message:"Não foi possível concluir a operação.";log("request",{correlationId,method:req.method,path,status,code,durationMs:Date.now()-started,actor:ctx?hash(ctx.userId).slice(0,12):"anonymous",tenant:ctx?.tenantId||null,error:status===500?String(error.message).slice(0,200):undefined});if(path.startsWith("/api/"))return json(res,status,{ok:false,code,message,fields:error.fields||undefined,correlationId});if(status===404)return send(res,404,notFoundPage());return send(res,status,loginPage({error:message}));}
    finally{if(!res.writableEnded)log("request",{correlationId,method:req.method,path,status:res.statusCode,durationMs:Date.now()-started});}
  });
  return {server:app,store,domain};
}

function guard(ctx){if(!ctx)throw new AppError(401,"AUTH_REQUIRED","Entre para continuar.");}
function guardApi(path,ctx){if(path.startsWith("/api/billing/webhook"))return;guard(ctx);}
function requireOrigin(req){if(!sameOrigin(req))throw new AppError(403,"ORIGIN_DENIED","Origem não autorizada.");}
function actor(req){const raw=process.env.TRUST_PROXY==="true"?String(req.headers["x-forwarded-for"]||"").split(",")[0]:req.socket.remoteAddress||"unknown";return hash(raw).slice(0,24);}
function rate(store,key,scope,maximum,windowMs){const now=Date.now(),start=now-windowMs;store.run("DELETE FROM rate_events WHERE occurred_at<?",start);const count=Number(store.one("SELECT COUNT(*) count FROM rate_events WHERE actor_key=? AND scope=? AND occurred_at>=?",key,scope,start).count);if(count>=maximum)throw new AppError(429,"RATE_LIMITED","Muitas tentativas. Aguarde e tente novamente.");store.run("INSERT INTO rate_events VALUES (?,?,?)",key,scope,now);}
async function staticFile(path,res){const file=resolve(publicRoot,path.slice("/assets/".length));if(!file.startsWith(publicRoot)||!existsSync(file))throw new AppError(404,"NOT_FOUND","Arquivo não encontrado.");return send(res,200,await readFile(file),mime[extname(file)]||"application/octet-stream",{"cache-control":"public, max-age=300"});}

if(process.argv[1]===fileURLToPath(import.meta.url)){
  mkdirSync(resolve(root,"../data"),{recursive:true});const port=Number(process.env.PORT||4173),{server}=createApp();server.listen(port,"0.0.0.0",()=>log("server.ready",{port,node:process.version,roles:Object.keys(roles)}));
}
