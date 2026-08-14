import { cpSync, mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";

rmSync("dist", { recursive: true, force: true });
mkdirSync("dist", { recursive: true });
for (const file of ["server.js", "store.js", "domain.js", "render.js"]) {
  execFileSync(process.execPath, ["--check", `src/${file}`], { stdio: "inherit" });
}
cpSync("src", "dist", { recursive: true });
cpSync("public", "dist/public", { recursive: true });
console.log("RelayOps build complete: dependency-free Node SSR bundle.");
