# P4.2 Controlled Benchmark Deployment

P4.2 normalizes public HTTPS evidence for live reference-build campaigns without giving one coding runtime a privileged hosting path.

## Deployment classes

ATLAS distinguishes two deployment classes:

1. `controlled-preview` — campaign-owned, temporary public HTTPS ingress used to verify externally reachable routes, real TLS, remote browser/network behavior, crawl responses and deployment evidence under the same infrastructure for every target.
2. `claimable-production` — provider-backed deployment with persistent project/domain/environment configuration suitable for satisfying a fixture's production-domain blocker.

A controlled preview is real public HTTPS evidence, but it must not be relabeled as claimable production.

## Default P4.2 adapter

The default adapter is a GitHub Actions runner plus a Cloudflare Quick Tunnel. It requires no target-runtime account or secret, exposes the target server through a temporary `*.trycloudflare.com` URL, and records the public URL, TLS/HTTP probes, response headers and lifecycle metadata as an artifact.

Cloudflare Quick Tunnels are intentionally used only for comparison-grade preview evidence. They are testing/development infrastructure and therefore cannot satisfy `marketing-production-domain` by themselves.

## Claimable production adapter

`deployment-adapter.contract.yaml` keeps a separate `claimable_production` section. A provider may be activated only when the same project topology, credentials, environment rules and cleanup policy can be offered to every compared runtime. Provider-specific convenience available to only one runtime is not comparison-grade.

The first supported production shape is Vercel CLI/API deployment because it can expose immutable HTTPS deployment URLs, environment-scoped configuration and inspectable deployment logs. It remains disabled until campaign-owned credentials/project configuration are available.

## Required lifecycle

1. Checkout the exact frozen implementation commit.
2. Install/build using commands recorded by the run.
3. Start the application on the declared local port.
4. Verify local health before opening public ingress.
5. Open campaign-owned public HTTPS ingress.
6. Verify the public endpoint independently from the application process.
7. Collect public HTTP/TLS/header evidence and the deployment URL.
8. Run portable browser evidence against the public URL when requested.
9. Upload the deployment evidence artifact.
10. Terminate the ingress and application process automatically at job completion.

## Truth rules

- `controlled-preview` may support browser, SEO, network and external-reachability evidence.
- It may not be scored as `marketing-production-domain: pass`.
- `claimable-production` requires a persistent provider deployment, HTTPS, environment configuration evidence and a public URL tied to the frozen run commit.
- Deployment evidence must state its source and class.
- The deployment layer must not mutate fixture source code to make a target deployable.
