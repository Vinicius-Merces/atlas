const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { RelayStore } = require('../src/store');

function fixtureStore() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'relayops-p5-'));
  const store = new RelayStore({ filename: ':memory:', storageRoot: path.join(root, 'files') });
  return {
    root,
    store,
    cleanup() {
      store.close();
      fs.rmSync(root, { recursive: true, force: true });
    },
  };
}

function actor(store, email, password = 'relayops-demo') {
  const login = store.login(email, password);
  if (!login) throw new Error(`Unable to seed actor ${email}`);
  return login.actor;
}

function evidenceDir() {
  const dir = process.env.RELAYOPS_EVIDENCE_DIR
    ? path.resolve(process.env.RELAYOPS_EVIDENCE_DIR)
    : path.resolve(__dirname, '../../run/evidence');
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

function writeEvidence(name, payload) {
  const file = path.join(evidenceDir(), `${name}.json`);
  fs.writeFileSync(file, JSON.stringify({ version: 1, generated_at: new Date().toISOString(), ...payload }, null, 2) + '\n');
  return file;
}

module.exports = { fixtureStore, actor, writeEvidence, evidenceDir };
