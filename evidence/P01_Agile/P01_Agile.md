# P01_Agile Data View

## Sheet: Agile Approach

| Parameter | Description | Security Integration Reason |
| --- | --- | --- |
| Framework | Scrum with XP Security Practices | Combines iterative delivery (Scrum) with test-driven secure development, pair programming, and refactoring (XP). |
| Sprint Duration | 2 Weeks | Allows rapid security vulnerability triage and incremental security testing. |


## Sheet: Manifesto Mapping

| Agile Manifesto Principle | AWMS Mapping & Security Practice |
| --- | --- |
| Customer Satisfaction | Continuous security checks and rapid delivery of order fulfillment features to customers. |
| Welcome Change | Modular RBAC and HMAC security architecture allowing new robot protocols without breaking core. |
| Deliver Working Software | Automated CI/CD security pipelines scanning dependencies and code on every push. |
| Daily Collaboration | Security Auditors work directly with Backend Developers to review audit logs and threat models. |
| Technical Excellence | Refactoring insecure modules to use JWT, bcrypt, HMAC-SHA256, and atomic database transactions. |


## Sheet: Refactoring Opportunities

| Refactoring ID | Component | Before Code/Structure | After Code/Structure | Security Benefit |
| --- | --- | --- | --- | --- |
| REF-01 | Robot Command Dispatcher | Insecure direct command execution without signature check | HMAC-SHA256 signature verification + Nonce anti-replay validation | Prevents unauthorized robot movement and replay attacks. |
| REF-02 | Inventory Management | Non-atomic direct quantity modification (stock = stock - qty) | SQLAlchemy with_for_update() transaction locking + reservation check | Prevents race conditions, negative inventory, and stock corruption. |


## Sheet: Agile Risks

| Risk ID | Agile Limitation / Security Risk | Impact Level | Mitigation Strategy |
| --- | --- | --- | --- |
| RSK-01 | Over-focus on user features neglects architectural security controls | HIGH | Introduce explicit Security User Stories with story points in Sprints (EPIC-06, EPIC-07). |
| RSK-02 | Sprint velocity pressure leading to skipped security testing | HIGH | Mandatory CI/CD automated Bandit static analysis and pip-audit quality gates before pull request merge. |


