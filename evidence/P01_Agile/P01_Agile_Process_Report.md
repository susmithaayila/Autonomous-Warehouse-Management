# Phase 01: Agile Process & XP Security Practices

## 1. Scrum with XP Security Practices
The AWMS project adopts Scrum integrated with Extreme Programming (XP) security practices:
- **Test-Driven Secure Development (TDD):** Security unit tests (JWT auth, negative inventory block, HMAC validation) written before feature deployment.
- **Pair Programming & Code Review:** Peer review of authorization logic and input validation.
- **Security Refactoring:** Continuous improvement of legacy insecure modules to secure patterns.

## 2. Agile Manifesto Principles Mapping
1. **Customer Satisfaction:** Delivering secure customer order fulfillment continuously.
2. **Welcome Changing Requirements:** Modular RBAC and HMAC secret handling allow adding new AGV protocols without breaking existing interfaces.
3. **Deliver Working Software Frequently:** Automated CI/CD security pipelines scanning dependencies and code on every push.
4. **Daily Collaboration:** Security Auditors work directly with Developers to inspect audit streams.
5. **Technical Excellence:** Continuous refactoring to eliminate insecure practices.

## 3. Refactoring Opportunities (Before vs After)
- **REF-01 (Robot Command Dispatcher):**
  - *Before:* Unauthenticated direct robot movement call (`execute_cmd(cmd_type)`).
  - *After:* HMAC-SHA256 signature calculation + UUID Nonce anti-replay verification.
- **REF-02 (Inventory Stock Balance):**
  - *Before:* Direct non-atomic balance modification (`stock = stock - qty`).
  - *After:* SQLAlchemy `with_for_update()` transaction locking + reservation counter deduction.

## 4. Agile Limitations / Security Risks & Mitigations
- **Risk 1:** Feature velocity pressure leading to skipped security checks.
  - *Mitigation:* Mandatory automated Bandit static analysis and pip-audit quality gates in CI/CD.
- **Risk 2:** Sprint backlog ignoring non-functional security requirements.
  - *Mitigation:* Explicit Security User Stories in Epics EPIC-06 and EPIC-07 with allocated story points.
