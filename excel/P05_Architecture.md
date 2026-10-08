# P05_Architecture Data View

## Sheet: Architecture Patterns

| Layer / Service | Pattern Used | Security Function | Implementation Detail |
| --- | --- | --- | --- |
| Presentation Layer | Single Page Application (SPA) | Role-based component visibility | HTML5, Vanilla CSS, JS with JWT token store |
| API & Auth Layer | REST API + RBAC Middleware | JWT Token validation & Role checks | FastAPI dependencies, HTTPBearer, PyJWT |
| Business Services | Service Layer Pattern | Business rule & security enforcement | AuthService, CommandAuthorizationService, FulfillmentService |
| Data Access Layer | Repository Pattern & ORM | ACID transactions & SQL injection prevention | SQLAlchemy ORM with parameter binding & with_for_update() |
| Audit Layer | Event Listener / Interceptor | Tamper-evident audit logging stream | AuditLog table with timestamp, actor, result, IP |


