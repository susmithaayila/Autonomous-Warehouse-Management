# P16_Final_Review Data View

## Sheet: Final Security Review

| Review Area | Observation / Finding | Risk Level | Control Implemented |
| --- | --- | --- | --- |
| Command Security | Unauthorized robot execution prevented | HIGH | HMAC-SHA256 signing and Nonce verification |
| Data Concurrency | Race conditions in inventory balance prevented | HIGH | SQLAlchemy row locking & transaction reservation |
| Authentication | Brute-force protection enabled | MEDIUM | Account lockout after 5 failed attempts & audit logging |


