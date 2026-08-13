---
name: authentication-flow-review
description: "Review sign-in, sign-up, recovery, MFA, SSO/OAuth/OIDC, session creation, and account-linking flows when identity behavior changes or authentication must be production-ready."
---

# Authentication Flow Review

## Purpose

Review authentication as an end-to-end identity flow rather than a login form, verifying that user identity, session establishment, recovery, federation, and account lifecycle behavior remain secure and understandable.

## Trigger conditions

Use when a change adds or modifies sign-in, sign-up, passwordless access, password recovery, MFA, OAuth/OIDC, SSO, account linking, session creation, reauthentication, or identity-provider behavior.

## Inputs

- Authentication architecture and provider configuration
- Routes, callbacks, middleware, token/session handling, cookies, and persistence
- User lifecycle and recovery requirements
- Threat model and trust boundaries
- Relevant tests, logs, and environment configuration

## Dependencies

- Authoritative identity-provider or authentication-library contract for enabled flows
- Product account lifecycle and recovery requirements
- `authorization-boundary-review` when authenticated identities can access protected resources
- `secret-environment-audit` when client/server credentials, signing secrets, or provider configuration change

## Procedure

1. Map every authentication entry point and callback.
2. Separate authentication from authorization. A valid identity must not imply access to every resource.
3. Identify the authoritative user identifier and, for federated identity, the identity-provider namespace that makes it unique.
4. Review sign-up and account-linking behavior for duplicate identity, provider-confusion, and account-takeover paths.
5. Review password, OTP, magic-link, OAuth/OIDC, SSO, and MFA paths that are actually enabled; do not assume unused methods are protected by an enabled provider.
6. Validate redirect/callback targets, state/nonce/PKCE or provider-equivalent protections where applicable, and signature/integrity validation for identity assertions.
7. Review session creation, renewal, expiration, logout, revocation, reauthentication, and privileged-step-up behavior.
8. Review recovery and email/phone change flows as authentication events with takeover risk.
9. Validate cookies/tokens against deployment context: transport security, storage location, exposure to client script, lifetime, rotation, audience/issuer, and replay risk.
10. Confirm rate limiting, abuse controls, and observable security events for high-risk authentication endpoints.
11. Test negative paths: expired tokens, replayed callbacks, wrong audience/issuer, disabled users, stale sessions, duplicate identities, failed MFA, and recovery misuse.
12. Map applicable requirements to the current OWASP ASVS authentication, session, token, OAuth/OIDC, configuration, and logging guidance when the project uses ASVS as an assurance baseline.

## Outputs

- Authentication-flow map
- Trust-boundary findings
- Session/token findings
- Recovery/account-linking findings
- Abuse and observability gaps
- Required mitigations and verification evidence
- Residual risk and review outcome

## Limitations

- Does not replace provider-specific security documentation or penetration testing.
- Does not decide product access policy; use `authorization-boundary-review` for resource permissions.
- Does not treat successful provider authentication as proof that application sessions and callbacks are safe.

## Validation

- Exercise positive and negative authentication flows in the closest safe environment available.
- Verify identity assertions and sessions cannot be accepted with invalid integrity, issuer/audience, expiration, or required state.
- Confirm logout/revocation/recovery behavior with actual session evidence.
- Record any provider controls that cannot be inspected and treat missing mandatory evidence as unresolved risk.
