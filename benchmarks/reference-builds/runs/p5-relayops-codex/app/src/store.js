import { DatabaseSync } from "node:sqlite";
import { chmodSync, mkdirSync, readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { randomUUID, scryptSync, timingSafeEqual, createHash, randomBytes } from "node:crypto";

const schema = readFileSync(fileURLToPath(new URL("./schema.sql", import.meta.url)), "utf8");
const iso = () => new Date().toISOString();
export const hash = value => createHash("sha256").update(String(value)).digest("hex");
export const id = prefix => `${prefix}_${randomUUID()}`;

export function passwordHash(password, salt = randomBytes(16).toString("hex")) {
  return `${salt}:${scryptSync(password, salt, 32).toString("hex")}`;
}
export function passwordValid(password, encoded) {
  const [salt, digest] = String(encoded).split(":");
  if (!salt || !digest) return false;
  return timingSafeEqual(Buffer.from(digest, "hex"), scryptSync(password, salt, 32));
}

export class Store {
  constructor(path = ":memory:", { seed = true } = {}) {
    if (path !== ":memory:") mkdirSync(dirname(path), { recursive: true });
    this.db = new DatabaseSync(path);
    this.db.exec("PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON;");
    this.db.exec(schema);
    if (path !== ":memory:") chmodSync(path, 0o600);
    if (seed) this.seed();
  }

  tx(fn) {
    this.db.exec("BEGIN IMMEDIATE");
    try { const value = fn(); this.db.exec("COMMIT"); return value; }
    catch (error) { this.db.exec("ROLLBACK"); throw error; }
  }

  seed() {
    if (this.db.prepare("SELECT COUNT(*) count FROM organizations").get().count) return;
    const now = iso();
    const orgs = [
      ["org_northstar", "northstar", "Northstar Elevadores"],
      ["org_harbor", "harbor", "Harbor Climatização"]
    ];
    const users = [
      ["usr_nm", "manager@northstar.test", "Marina Costa", "manager", "org_northstar", "RelayOps!2026", null],
      ["usr_nd", "dispatcher@northstar.test", "Diego Alves", "dispatcher", "org_northstar", "RelayOps!2026", null],
      ["usr_nt", "tech@northstar.test", "Lia Rocha", "technician", "org_northstar", "RelayOps!2026", null],
      ["usr_nb", "billing@northstar.test", "Bruno Mota", "billing", "org_northstar", "RelayOps!2026", null],
      ["usr_hm", "manager@harbor.test", "Helena Park", "manager", "org_harbor", "RelayOps!2026", null],
      ["usr_support", "support@relayops.test", "Sara Lima", null, null, "Support!2026", "support"]
    ];
    this.tx(() => {
      for (const [oid, slug, name] of orgs) this.db.prepare("INSERT INTO organizations VALUES (?,?,?,?,?)").run(oid, slug, name, "active", now);
      for (const [uid,email,name,role,tenant,password,globalRole] of users) {
        this.db.prepare("INSERT INTO users VALUES (?,?,?,?,?,?)").run(uid,email,name,passwordHash(password, hash(email).slice(0,32)),globalRole,now);
        if (tenant) this.db.prepare("INSERT INTO memberships VALUES (?,?,?,?,?)").run(tenant,uid,role,"active",1);
      }
      const customers = [
        ["cus_nova", "org_northstar", "NS-100", "Nova Diagnósticos", "operacoes@novadiag.test", "+55 11 3020-1100", "Av. Angélica, 820 — São Paulo"],
        ["cus_orion", "org_northstar", "NS-101", "Orion Office Park", "facilities@orion.test", "+55 11 3030-1188", "Rua Verbo Divino, 1488 — São Paulo"],
        ["cus_beta", "org_harbor", "HB-900", "BETA_ONLY_SENTINEL Harbor Pier", "private@harbor.test", "+55 21 3000-9900", "Cais Privado 9 — Rio de Janeiro"]
      ];
      for (const c of customers) this.db.prepare("INSERT INTO customers(id,tenant_id,external_ref,name,email,phone,site_address,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,'active',?,?)").run(...c,now,now);
      const orders = [
        ["wo_2408", "org_northstar", "cus_nova", "Inspeção preventiva — elevador B", "Ruído intermitente no conjunto de tração.", "scheduled", "high", "usr_nt", "2026-08-14T15:00:00.000Z"],
        ["wo_2411", "org_northstar", "cus_orion", "Falha no painel do lobby", "Display reinicia após pico de energia.", "new", "urgent", null, "2026-08-14T17:30:00.000Z"],
        ["wo_beta", "org_harbor", "cus_beta", "BETA_ONLY_SENTINEL compressor", "Informação restrita do tenant Harbor.", "in_progress", "urgent", "usr_hm", now]
      ];
      for (const w of orders) this.db.prepare("INSERT INTO work_orders(id,tenant_id,customer_id,title,description,status,priority,assigned_user_id,scheduled_at,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)").run(...w,now,now);
      this.db.prepare("INSERT INTO attachments VALUES (?,?,?,?,?,?,?,?,?,?,?)").run("att_beta","org_harbor","wo_beta","org_harbor/private-beta.txt","BETA_ONLY_SENTINEL.txt","text/plain",18,hash("BETA_ONLY_SENTINEL"),Buffer.from("BETA_ONLY_SENTINEL").toString("base64"),"usr_hm",now);
      for (const tenant of ["org_northstar","org_harbor"]) {
        this.db.prepare("INSERT INTO subscriptions VALUES (?,?,?,?,?,?,?,?)").run(tenant,`sub_${tenant}`,"active","active","scale",100,1,now);
        this.db.prepare("INSERT INTO entitlements VALUES (?,?,?,?,?,?,?)").run(tenant,"operations",1,"reconciliation","provider active",1,now);
      }
    });
  }

  one(sql, ...args) { return this.db.prepare(sql).get(...args); }
  all(sql, ...args) { return this.db.prepare(sql).all(...args); }
  run(sql, ...args) { return this.db.prepare(sql).run(...args); }
  close() { this.db.close(); }

  audit({ tenantId = null, actorId = null, role = "anonymous", action, resource, resourceId = null, result, reason = null, correlationId, details = {} }) {
    const auditId = id("aud");
    this.run("INSERT INTO audit_log VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", auditId,tenantId,actorId,role,action,resource,resourceId,result,reason,correlationId,JSON.stringify(details),iso());
    return auditId;
  }

  createSession(email, password, tenantId = null) {
    const user = this.one("SELECT * FROM users WHERE lower(email)=lower(?)", email);
    if (!user || !passwordValid(password, user.password_hash)) return null;
    let tenant = tenantId;
    if (!user.global_role) {
      const membership = tenant
        ? this.one("SELECT * FROM memberships WHERE user_id=? AND tenant_id=? AND status='active'", user.id, tenant)
        : this.one("SELECT * FROM memberships WHERE user_id=? AND status='active' ORDER BY tenant_id", user.id);
      if (!membership) return null;
      tenant = membership.tenant_id;
    }
    const token = randomBytes(32).toString("base64url");
    this.run("INSERT INTO sessions VALUES (?,?,?,?,?,?)", hash(token),user.id,tenant,new Date(Date.now()+8*60*60*1000).toISOString(),null,iso());
    return { token, user, tenantId: tenant };
  }

  session(token) {
    if (!token) return null;
    const row = this.one(`SELECT s.*,u.email,u.name,u.global_role,m.role,m.status membership_status,m.authz_version,o.name tenant_name
      FROM sessions s JOIN users u ON u.id=s.user_id
      LEFT JOIN memberships m ON m.user_id=s.user_id AND m.tenant_id=s.tenant_id
      LEFT JOIN organizations o ON o.id=s.tenant_id
      WHERE s.token_hash=? AND s.revoked_at IS NULL AND s.expires_at>?`, hash(token),iso());
    if (!row || (!row.global_role && row.membership_status !== "active")) return null;
    return { userId:row.user_id,email:row.email,name:row.name,globalRole:row.global_role,tenantId:row.tenant_id,tenantName:row.tenant_name,role:row.global_role || row.role,authzVersion:row.authz_version || 0,tokenHash:row.token_hash };
  }

  revokeSession(token) { if (token) this.run("UPDATE sessions SET revoked_at=? WHERE token_hash=?", iso(), hash(token)); }
}

export { iso };
