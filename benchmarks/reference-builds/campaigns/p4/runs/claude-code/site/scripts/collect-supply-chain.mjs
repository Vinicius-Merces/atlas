/**
 * supply-chain-risk-audit evidence.
 */
import { execSync } from "node:child_process";
import { writeFileSync, mkdirSync, readFileSync, existsSync } from "node:fs";

const OUT = "../evidence/supply-chain";
mkdirSync(OUT, { recursive: true });

const problems = [];
const pkg = JSON.parse(readFileSync("package.json", "utf8"));

function run(command) {
  try {
    return execSync(command, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
  } catch (error) {
    return error.stdout ?? "";
  }
}

// npm audit
const auditRaw = run("npm audit --json");
let audit = {};
try {
  audit = JSON.parse(auditRaw);
} catch {
  problems.push("npm audit did not return parseable JSON");
}
const vulns = audit?.metadata?.vulnerabilities ?? {};
for (const level of ["critical", "high"]) {
  if ((vulns[level] ?? 0) > 0) problems.push(`${vulns[level]} ${level} vulnerabilities reported by npm audit`);
}

// Full dependency tree
const treeRaw = run("npm ls --all --json");
let tree = {};
try {
  tree = JSON.parse(treeRaw);
} catch {
  problems.push("npm ls did not return parseable JSON");
}

function flatten(node, into = new Map(), depth = 0) {
  for (const [name, info] of Object.entries(node.dependencies ?? {})) {
    const key = `${name}@${info.version}`;
    if (!into.has(key)) into.set(key, { name, version: info.version, depth });
    flatten(info, into, depth + 1);
  }
  return into;
}
const transitive = flatten(tree);

// Lockfile
const hasLockfile = existsSync("package-lock.json");
if (!hasLockfile) problems.push("no package-lock.json — installs are not reproducible");
const lock = hasLockfile ? JSON.parse(readFileSync("package-lock.json", "utf8")) : { packages: {} };

// Packages with install scripts are the highest-risk supply-chain surface.
const withInstallScripts = Object.entries(lock.packages ?? {})
  .filter(([, meta]) => meta.hasInstallScript)
  .map(([path]) => path);

// Registry provenance: everything must resolve to the public npm registry.
const nonRegistry = Object.entries(lock.packages ?? {})
  .filter(([path, meta]) => path && meta.resolved && !meta.resolved.startsWith("https://registry.npmjs.org/"))
  .map(([path, meta]) => ({ path, resolved: meta.resolved }));
if (nonRegistry.length) problems.push(`${nonRegistry.length} packages resolve outside the public npm registry`);

// Integrity hashes present for every resolved package.
const missingIntegrity = Object.entries(lock.packages ?? {})
  .filter(([path, meta]) => path && meta.resolved && !meta.integrity)
  .map(([path]) => path);
if (missingIntegrity.length) problems.push(`${missingIntegrity.length} packages lack an integrity hash`);

// Version pinning discipline of direct dependencies.
const direct = { ...pkg.dependencies, ...pkg.devDependencies };
const unpinned = Object.entries(direct).filter(([, range]) => /^[*x]|latest/.test(range));
if (unpinned.length) problems.push(`unpinned direct dependencies: ${unpinned.map(([n]) => n).join(", ")}`);

const report = {
  generatedAt: new Date().toISOString(),
  runtime: { node: process.version, npm: run("npm --version").trim() },
  directDependencies: pkg.dependencies,
  directDevDependencies: pkg.devDependencies,
  directCount: Object.keys(direct).length,
  transitiveCount: transitive.size,
  transitivePackages: [...transitive.keys()].sort(),
  lockfile: { present: hasLockfile, lockfileVersion: lock.lockfileVersion },
  packagesWithInstallScripts: withInstallScripts,
  packagesOutsidePublicRegistry: nonRegistry,
  packagesMissingIntegrity: missingIntegrity.length,
  auditSummary: vulns,
  auditAdvisories: Object.keys(audit?.vulnerabilities ?? {}),
  notes: [
    "No postinstall build step of our own; no vendored binaries; no container base image in this run.",
    "Runtime dependencies are limited to next, react, react-dom, zod and three self-hosted font packages.",
    "The lead store uses Node's built-in node:sqlite rather than a native addon, which removes a compiled dependency from the supply chain entirely.",
    "No third-party script, font, analytics or tag-manager origin is contacted at runtime (verified in evidence/security).",
  ],
  problems,
};

writeFileSync(`${OUT}/supply-chain.json`, JSON.stringify(report, null, 2));

console.log(`direct dependencies: ${report.directCount}`);
console.log(`transitive packages: ${report.transitiveCount}`);
console.log(`install scripts: ${withInstallScripts.length ? withInstallScripts.join(", ") : "none"}`);
console.log(`audit: ${JSON.stringify(vulns)}`);
console.log(problems.length ? `PROBLEMS:\n- ${problems.join("\n- ")}` : "no problems found");
process.exit(problems.length ? 1 : 0);
