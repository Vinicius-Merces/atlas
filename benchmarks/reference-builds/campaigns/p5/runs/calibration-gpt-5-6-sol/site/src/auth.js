const crypto = require('node:crypto');

function hashPassword(password, salt = crypto.randomBytes(16).toString('hex')) {
  const hash = crypto.scryptSync(String(password), salt, 32).toString('hex');
  return { salt, hash };
}

function verifyPassword(password, salt, expectedHex) {
  const actual = crypto.scryptSync(String(password), salt, 32);
  const expected = Buffer.from(expectedHex, 'hex');
  return actual.length === expected.length && crypto.timingSafeEqual(actual, expected);
}

function newSessionToken() {
  return crypto.randomBytes(32).toString('base64url');
}

function tokenDigest(token) {
  return crypto.createHash('sha256').update(String(token)).digest('hex');
}

function parseCookies(header = '') {
  const out = {};
  for (const pair of String(header).split(';')) {
    const index = pair.indexOf('=');
    if (index < 0) continue;
    const key = pair.slice(0, index).trim();
    const value = pair.slice(index + 1).trim();
    if (key) out[key] = decodeURIComponent(value);
  }
  return out;
}

module.exports = {
  hashPassword,
  verifyPassword,
  newSessionToken,
  tokenDigest,
  parseCookies,
};
