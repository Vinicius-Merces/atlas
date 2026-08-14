const { RelayStore: BaseRelayStore, ForbiddenError, ValidationError } = require('./store');

class RelayStore extends BaseRelayStore {
  search(actor, query) {
    this.authorize(actor);
    const q = `%${String(query || '').trim()}%`;
    const customers = this.db.prepare(`
      SELECT id, name, email
      FROM customer
      WHERE tenant_id = ? AND (name LIKE ? OR email LIKE ?)
      ORDER BY name
      LIMIT 20
    `).all(actor.tenantId, q, q);
    const workOrders = this.db.prepare(`
      SELECT w.id, w.title, w.status
      FROM work_order w
      JOIN customer c ON c.id = w.customer_id AND c.tenant_id = w.tenant_id
      WHERE w.tenant_id = ? AND (w.title LIKE ? OR c.name LIKE ?)
      ORDER BY w.updated_at DESC
      LIMIT 20
    `).all(actor.tenantId, q, q);
    return { customers, workOrders };
  }

  exportCustomers(actor) {
    this.authorize(actor, ['manager', 'dispatcher', 'billing']);
    const rows = this.db.prepare(`
      SELECT name, email, COALESCE(phone, '') AS phone
      FROM customer
      WHERE tenant_id = ?
      ORDER BY name
    `).all(actor.tenantId);
    const escape = (value) => `"${String(value).replaceAll('"', '""')}"`;
    return ['name,email,phone', ...rows.map((row) => [row.name, row.email, row.phone].map(escape).join(','))].join('\n') + '\n';
  }
}

module.exports = { RelayStore, ForbiddenError, ValidationError };
