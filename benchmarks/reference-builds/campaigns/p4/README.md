# P4 Live Reference Build Campaign

P4 runs the `premium-marketing-site` fixture as a controlled live campaign.

Implementation code is not merged into `main` before target results are frozen. Every runtime starts from the same recorded base commit and works on an isolated `bench/p4-asteria-{target_id}` branch.

Targets are a diagnostic GPT-5.6 Sol calibration plus Codex and Claude Code comparison targets. The calibration validates the live path but is never relabeled as either target runtime.

Protocol: freeze base commit; create isolated run branch; record manifest; build from the canonical fixture; collect browser/deployment/security/performance evidence; freeze implementation and evidence; obtain independent review; score with P3; preserve the first result before remediation; compare target runs only after both are frozen.
