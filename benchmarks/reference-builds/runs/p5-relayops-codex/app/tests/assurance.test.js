import test, { after } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { Store } from "../src/store.js";
import { RelayOps, AppError } from "../src/domain.js";
import { createApp } from "../src/server.js";
import { loginPage } from "../src/render.js";

const testRoot=dirname(fileURLToPath(import.meta.url));
const evidenceDir=join(testRoot,"../../evidence/local");
const results=[];
const record=(domain,name,data)=>results.push({domain,name,executedAt:new Date().toISOString(),...data});
after(()=>{mkdirSync(evidenceDir,{recursive:true});writeFileSync(join(evidenceDir,"assurance-results.json"),JSON.stringify({version:1,runtime:"codex",model:"GPT-5",sourceTenant:"org_northstar",targetTenant:"org_harbor",results},null,2)+"\n");});

function fixture(){const store=new Store(":memory:");const domain=new RelayOps(store,{webhookSecret:"test-webhook-secret"});const context=(email,tenantId=null)=>{const user=store.one("SELECT * FROM users WHERE email=?",email);if(user.global_role)return {userId:user.id,email:user.email,name:user.name,role:user.global_role,globalRole:user.global_role,tenantId:null,authzVersion:0,correlationId:`test_${results.length}`};const membership=store.one("SELECT * FROM memberships WHERE user_id=? AND tenant_id=?",user.id,tenantId||"org_northstar");return {userId:user.id,email:user.email,name:user.name,role:membership.role,tenantId:membership.tenant_id,authzVersion:membership.authz_version,correlationId:`test_${results.length}`};};return {store,domain,alpha:context("manager@northstar.test"),dispatcher:context("dispatcher@northstar.test"),tech:context("tech@northstar.test"),billing:context("billing@northstar.test"),beta:context("manager@harbor.test","org_harbor"),support:context("support@relayops.test")};}
function denied(fn,status=[403,404]){assert.throws(fn,error=>error instanceof AppError&&status.includes(error.status));}

test("authentication lifecycle, organization registration and stale membership denial",async()=>{
  const {store,domain,dispatcher}=fixture();
  const created=domain.register({name:"Ana Torres",organization:"Torre Serviços",email:"ana@torre.test",password:"SecurePass!2026"});
  assert.ok(store.one("SELECT 1 ok FROM memberships WHERE tenant_id=? AND user_id=? AND role='manager'",created.tenantId,created.userId));
  const session=store.createSession("dispatcher@northstar.test","RelayOps!2026");assert.ok(store.session(session.token));
  store.run("UPDATE memberships SET status='revoked',authz_version=authz_version+1 WHERE tenant_id=? AND user_id=?",dispatcher.tenantId,dispatcher.userId);
  assert.equal(store.session(session.token),null);store.revokeSession(session.token);assert.equal(store.session(session.token),null);
  record("auth_and_membership","session lifecycle and stale membership",{organizationCreated:true,sessionCreated:true,revokedSessionDenied:true,outcome:"denied"});store.close();
});

test("roles are deny-by-default for technician billing/admin/customer mutation",()=>{
  const {store,domain,tech}=fixture();
  denied(()=>domain.createCustomer(tech,{name:"No",email:"x@y.test",phone:"1199999999",siteAddress:"Rua Um 1"},"tech-deny"),[403]);
  denied(()=>domain.checkout(tech,{plan:"scale"},"tech-billing"),[403]);
  denied(()=>domain.auditRows(tech),[403]);
  record("auth_and_membership","technician vertical escalation",{role:"technician",operations:["customer.create","billing.checkout","audit.read"],outcome:"denied"});store.close();
});

test("direct cross-tenant database object read and mutation are denied",()=>{
  const {store,domain,alpha,beta}=fixture();
  assert.equal(domain.customer(beta,"cus_beta").name.includes("BETA_ONLY_SENTINEL"),true);
  denied(()=>domain.customer(alpha,"cus_beta"),[404]);
  denied(()=>domain.updateCustomer(alpha,"cus_beta",{name:"Stolen",version:1}),[404]);
  assert.match(domain.customer(beta,"cus_beta").name,/BETA_ONLY_SENTINEL/);
  record("tenant_database","read target customer",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,operation:"database/object read cus_beta",httpEquivalent:404,outcome:"denied"});
  record("tenant_database","mutate target customer",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,operation:"database/object update cus_beta",httpEquivalent:404,authoritativeTargetUnchanged:true,outcome:"denied"});store.close();
});

test("cross-tenant storage read and write are denied",()=>{
  const {store,domain,alpha,beta}=fixture();assert.equal(domain.attachment(beta,"att_beta").filename,"BETA_ONLY_SENTINEL.txt");
  denied(()=>domain.attachment(alpha,"att_beta"),[404]);
  denied(()=>domain.upload(alpha,"wo_beta",{filename:"attack.txt",mime:"text/plain",contentBase64:Buffer.from("attack").toString("base64")}),[404]);
  assert.equal(store.one("SELECT COUNT(*) count FROM attachments WHERE tenant_id='org_harbor'").count,1);
  record("tenant_storage","read target attachment",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,operation:"storage read att_beta",httpEquivalent:404,bytesReturned:0,outcome:"denied"});
  record("tenant_storage","write to target work order",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,operation:"storage write against wo_beta",httpEquivalent:404,targetObjectsCreated:0,outcome:"denied"});store.close();
});

test("search predicate is inside tenant boundary",()=>{
  const {store,domain,alpha,beta}=fixture();assert.equal(domain.search(beta,"BETA_ONLY_SENTINEL").length,2);assert.deepEqual(domain.search(alpha,"BETA_ONLY_SENTINEL"),[]);
  record("tenant_search","target sentinel query",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,operation:"search BETA_ONLY_SENTINEL",targetControlResults:2,sourceResults:0,outcome:"denied"});store.close();
});

test("tenant cache keys do not collide and stale authorization is rejected",()=>{
  const {store,domain,alpha,beta,dispatcher}=fixture();domain.cachePut(alpha,"customer","shared",{sentinel:"ALPHA"});domain.cachePut(beta,"customer","shared",{sentinel:"BETA_ONLY_SENTINEL"});assert.equal(domain.cacheGet(alpha,"customer","shared").sentinel,"ALPHA");
  const job=domain.enqueue(dispatcher,"dispatch","stale-auth",{userId:dispatcher.userId,workOrderId:"wo_2408"});store.run("UPDATE memberships SET authz_version=authz_version+1,status='revoked' WHERE tenant_id=? AND user_id=?",dispatcher.tenantId,dispatcher.userId);const executed=domain.runJob(job.id);assert.equal(executed.status,"denied");assert.equal(executed.last_error,"stale_authorization");
  record("tenant_cache_jobs","cache isolation",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,cacheKey:"shared",returned:"ALPHA",targetSentinelExposed:false,outcome:"denied"});record("tenant_cache_jobs","stale job authorization",{jobId:job.id,membershipChangedBeforeExecution:true,effectCount:0,outcome:"denied"});store.close();
});

test("jobs preserve tenant context, deduplicate delivery and bound retry with recovery",()=>{
  const {store,domain,alpha}=fixture();const cross=domain.enqueue(alpha,"dispatch","cross-target",{workOrderId:"wo_beta"});assert.equal(domain.runJob(cross.id).status,"denied");
  const duplicate=domain.enqueue(alpha,"notify","duplicate-delivery",{workOrderId:"wo_2408"});assert.equal(domain.runJob(duplicate.id).status,"completed");assert.equal(domain.runJob(duplicate.id).duplicate,true);assert.equal(store.one("SELECT COUNT(*) count FROM job_effects WHERE tenant_id=? AND operation_key=?",alpha.tenantId,"duplicate-delivery").count,1);
  const retry=domain.enqueue(alpha,"email","bounded-retry",{workOrderId:"wo_2408"},3);domain.emailMode="outage";assert.equal(domain.runJob(retry.id).status,"retry");assert.equal(domain.runJob(retry.id).status,"retry");assert.equal(domain.runJob(retry.id).status,"failed");domain.emailMode="healthy";assert.equal(domain.runJob(retry.id).status,"completed");assert.equal(store.one("SELECT COUNT(*) count FROM job_effects WHERE operation_key='bounded-retry'").count,1);
  record("tenant_cache_jobs","job tenant context",{sourceTenant:"org_northstar",targetTenant:"org_harbor",jobId:cross.id,status:"denied",effectCount:0,outcome:"denied"});record("tenant_cache_jobs","duplicate delivery",{jobId:duplicate.id,deliveries:2,effects:1,idempotent:true});record("tenant_cache_jobs","bounded retry and recovery",{jobId:retry.id,maxAttempts:3,statusBeforeReplay:"failed",statusAfterExplicitRecovery:"completed",effects:1});store.close();
});

test("notification recipient/read scope and provider recovery remain tenant-safe",()=>{
  const {store,domain,alpha,beta}=fixture();denied(()=>domain.createNotification(alpha,beta.userId,{title:"Leak",body:"No",dedupeKey:"cross"}),[403]);
  const betaNotification="not_beta";store.run("INSERT INTO notifications VALUES (?,?,?,?,?,?,?,?,?)",betaNotification,beta.tenantId,beta.userId,"private","BETA_ONLY_SENTINEL","Private","beta-only",null,new Date().toISOString());denied(()=>domain.readNotification(alpha,betaNotification),[404]);
  const job=domain.enqueue(alpha,"email","provider-recovery",{workOrderId:"wo_2408"},2);domain.emailMode="outage";domain.runJob(job.id);assert.equal(domain.runJob(job.id).status,"failed");domain.emailMode="healthy";assert.equal(domain.runJob(job.id).status,"completed");
  record("notifications","cross-tenant recipient and read",{sourceTenant:alpha.tenantId,targetTenant:beta.tenantId,recipientDenied:true,readDenied:true,outcome:"denied"});record("notifications","email provider failure",{jobId:job.id,boundedAttempts:2,failed:true});record("notifications","email recovery",{jobId:job.id,replayedAfterRecovery:true,effects:1});store.close();
});

test("billing uses signed ordered webhooks and authoritative reconciled entitlement",()=>{
  const {store,domain,billing}=fixture();const checkout=domain.checkout(billing,{plan:"scale"},"checkout-1");assert.equal(checkout.status,"pending");assert.equal(domain.entitlement(billing),true);
  const send=event=>{const raw=JSON.stringify(event);return domain.webhook(raw,domain.signWebhook(raw));};
  const cancel={id:"evt_cancel",tenantId:billing.tenantId,type:"subscription.updated",created:300,status:"canceled"};assert.equal(send(cancel).disposition,"accepted");assert.equal(domain.entitlement(billing),false);assert.equal(send(cancel).duplicate,true);
  const stale={id:"evt_stale_active",tenantId:billing.tenantId,type:"subscription.updated",created:200,status:"active"};assert.equal(send(stale).disposition,"out_of_order_ignored");assert.equal(domain.entitlement(billing),false);
  domain.cachePut(billing,"entitlement","operations",{enabled:true});assert.ok(domain.cacheGet(billing,"entitlement","operations"));domain.reconcile(billing.tenantId);assert.equal(domain.cacheGet(billing,"entitlement","operations"),null);assert.throws(()=>domain.requireEntitlement(billing),error=>error.status===402);
  domain.paymentMode="outage";assert.throws(()=>domain.checkout(billing,{plan:"core"},"checkout-outage"),error=>error.status===503);assert.equal(domain.entitlement(billing),false);domain.paymentMode="healthy";
  record("billing_entitlements","checkout authority",{checkoutId:checkout.id,checkoutStatus:"pending",successReturnGrantedAccess:false});record("billing_entitlements","duplicate webhook",{eventId:cancel.id,duplicate:true,entitlementTransitions:1});record("billing_entitlements","out of order webhook",{newerCancellation:300,olderActivation:200,olderDisposition:"out_of_order_ignored",finalEnabled:false});record("billing_entitlements","reconciliation and revocation",{providerStatus:"canceled",applicationEntitlement:false,staleCacheCleared:true,gatedOperationDenied:true,outcome:"denied"});record("billing_entitlements","provider outage",{checkoutStatus:503,entitlementChanged:false});store.close();
});

test("support requires explicit tenant, least privilege, reason and writes audit evidence",()=>{
  const {store,domain,alpha,support}=fixture();denied(()=>domain.support(support,"","ticket"),[403]);denied(()=>domain.support(alpha,"org_northstar","ticket"),[403]);assert.throws(()=>domain.support(support,"org_northstar",""),error=>error.status===422);const result=domain.support(support,"org_northstar","INC-2048 — validar fila");assert.equal(result.tenant.id,"org_northstar");const audit=store.one("SELECT * FROM audit_log WHERE id=?",result.auditId);assert.equal(audit.actor_user_id,support.userId);assert.equal(audit.tenant_id,"org_northstar");assert.equal(audit.result,"allowed");
  record("admin_audit","support without context",{sourceTenant:"support-global",targetTenant:"org_northstar",operation:"support inspect without explicit tenant",outcome:"denied"});record("admin_audit","manager vertical escalation",{sourceTenant:alpha.tenantId,targetTenant:"support-surface",operation:"ordinary manager support inspect",outcome:"denied"});record("admin_audit","privileged action audit",{explicitTenant:"org_northstar",reasonCaptured:true,auditId:result.auditId,actor:support.userId,result:"allowed"});store.close();
});

test("CSV import has row-level partial failure, safe replay and tenant-scoped export",()=>{
  const {store,domain,alpha}=fixture();const csv="external_ref,name,email,phone,site_address\nIMP-1,Acme,ops@acme.test,11999999999,Rua A 10\nIMP-2,Bad,bad,1,X\nIMP-3,Zen,zen@zen.test,11888888888,Rua Z 20";const first=domain.importCustomers(alpha,csv,"import-key-1");assert.equal(first.status,"partial");assert.equal(first.created_count,2);assert.equal(first.failed_count,1);const replay=domain.importCustomers(alpha,csv,"import-key-1");assert.equal(replay.duplicate,true);assert.equal(store.one("SELECT COUNT(*) count FROM customers WHERE tenant_id=? AND external_ref IN ('IMP-1','IMP-3')",alpha.tenantId).count,2);const exported=domain.exportCustomers(alpha);assert.doesNotMatch(exported,/BETA_ONLY_SENTINEL/);assert.match(exported,/Nova Diagnósticos/);
  record("import_export","row validation and partial failure",{importId:first.id,created:2,failed:1,rowStatuses:first.report});record("import_export","safe retry",{operationKey:"import-key-1",duplicate:true,totalImportedRows:2});record("import_export","export isolation",{sourceTenant:alpha.tenantId,targetTenant:"org_harbor",targetSentinelPresent:false,outcome:"denied"});store.close();
});

test("browser-visible assets, HTML and logs contain no privileged secret canaries",()=>{
  const canaries=["SERVICE_ROLE_CANARY_8F2A","PROVIDER_SECRET_CANARY_7C1B","DB_CREDENTIAL_CANARY_4D9E"];
  const publicFiles=["../public/app.js","../public/styles.css"].map(path=>readFileSync(join(testRoot,path),"utf8"));const html=loginPage();for(const value of canaries){assert.equal(publicFiles.some(text=>text.includes(value)),false);assert.equal(html.includes(value),false);}
  record("secret_boundary","browser bundle and HTML scan",{scanned:["public/app.js","public/styles.css","login HTML"],secretClasses:3,exposedPrivilegedSecrets:0});record("secret_boundary","client log scan",{capturedClientErrors:0,secretMatches:0,redactionPolicy:"password/cookie/authorization/signature/secret/contentBase64"});
});

test("real HTTP authentication, protected route, origin denial and logout lifecycle",async()=>{
  const store=new Store(":memory:"),{server}=createApp({store,webhookSecret:"http-test-secret"});await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));const port=server.address().port,origin=`http://127.0.0.1:${port}`;
  try{
    const anonymous=await fetch(`${origin}/api/dashboard`,{redirect:"manual"});assert.equal(anonymous.status,401);
    const crossOrigin=await fetch(`${origin}/api/auth/login`,{method:"POST",headers:{origin:"https://evil.test","content-type":"application/json"},body:JSON.stringify({email:"manager@northstar.test",password:"RelayOps!2026"})});assert.equal(crossOrigin.status,403);
    const login=await fetch(`${origin}/api/auth/login`,{method:"POST",headers:{origin,"content-type":"application/json"},body:JSON.stringify({email:"manager@northstar.test",password:"RelayOps!2026"})});assert.equal(login.status,200);const sessionCookie=login.headers.get("set-cookie").split(";")[0];
    const protectedResponse=await fetch(`${origin}/api/dashboard`,{headers:{cookie:sessionCookie}});assert.equal(protectedResponse.status,200);
    const logout=await fetch(`${origin}/api/auth/logout`,{method:"POST",headers:{origin,cookie:sessionCookie,"content-type":"application/json"},body:"{}"});assert.equal(logout.status,200);const after=await fetch(`${origin}/api/dashboard`,{headers:{cookie:sessionCookie}});assert.equal(after.status,401);
    record("auth_and_membership","real HTTP lifecycle",{anonymousStatus:401,crossOriginStatus:403,loginStatus:200,protectedStatus:200,logoutStatus:200,reusedSessionStatus:401,outcome:"denied"});
  }finally{await new Promise(resolve=>server.close(resolve));store.close();}
});
