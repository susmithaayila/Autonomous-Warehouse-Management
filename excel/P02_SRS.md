# P02_SRS Data View

## Sheet: Requirements

| ID | Category | Title | Description | Priority | CIA Classification |
| --- | --- | --- | --- | --- | --- |
| SR-01 | Security | Authentication | JWT-based session authentication with bcrypt password hashing | Highest | Confidentiality/Integrity |
| SR-02 | Security | RBAC | Strict authorization for Administrator, Operator, Customer, Auditor, Robot | Highest | Confidentiality/Integrity |
| SR-03 | Security | Robot Verification | Robots must authenticate using shared HMAC secrets | Highest | Integrity/Authenticity |
| SR-04 | Security | Privilege Escalation Block | Users cannot modify their own roles or elevate privileges | Highest | Integrity |
| SR-05 | Security | Robot Command Auth | Robot commands require valid user role & HMAC verification | Highest | Integrity/Availability |
| SR-06 | Security | Inventory Integrity | Stock updates must execute within ACID transactions | Highest | Integrity |
| SR-07 | Security | Transaction Protection | Database concurrency isolation for stock reservation | High | Integrity |
| SR-08 | Security | Race Condition Block | Row-level locking (with_for_update) during task allocation | Highest | Integrity |
| SR-09 | Security | Command Conflict Block | Prevent simultaneous execution of conflicting commands on same robot | Highest | Integrity/Availability |
| SR-10 | Security | Audit Logging | Tamper-evident log stream for all authentication & command events | High | Repudiation |
| SR-11 | Security | Availability Protection | Rate limiting, command expiration, and heartbeat monitoring | High | Availability |
| SR-12 | Security | Secure Secrets | Secrets injected via environment variables / Kubernetes Secrets | Highest | Confidentiality |
| SR-13 | Security | Input Validation | Pydantic schema validation for all incoming API payloads | High | Integrity |
| SR-14 | Security | Secure Deployment | Non-root Docker container execution and Kubernetes Pod Security | High | Confidentiality/Integrity |
| SR-15 | Security | Security Monitoring | Real-time tracking of failed logins, unauthorized commands, and offline robots | High | Availability/Integrity |
| SR-16 | Security | Least Privilege | Endpoints enforce minimum required role permission scope | Highest | Confidentiality/Integrity |


