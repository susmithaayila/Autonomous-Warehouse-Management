# Traceability_Matrix Data View

## Sheet: Traceability Matrix

| Requirement ID | Requirement Description | Use Case | DFD Process | Asset | Threat | Jira Story | Sprint | Implementation Module | Test ID | Docker Control | Kubernetes Control |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SR-01 | JWT Auth & Bcrypt | UC-01 | P1: Authentication | User Credentials | TH-01 | AWMS-01 | Sprint 1 | AuthService / security.py | UT-01 | Non-root user | Secret env mapping |
| SR-02 | RBAC Control | UC-01 | P1: Authentication | User Roles | TH-06 | AWMS-02 | Sprint 1 | require_roles dependency | UT-01 | Controlled ports | Namespace isolation |
| SR-03 | Robot Identity Verification | UC-02 | P5: Robot Control | Robot Credentials | TH-01 | AWMS-05 | Sprint 1 | RobotService / HMAC | UT-02 | Minimal base image | Secret management |
| SR-04 | Privilege Escalation Block | UC-01 | P1: Authentication | User Roles | TH-06 | AWMS-02 | Sprint 1 | UserService.assign_role | UT-01 | Non-root user | Resource limits |
| SR-05 | Robot Command Authorization | UC-02 | P5: Robot Control | Robot Commands | TH-07 | AWMS-06 | Sprint 2 | CommandAuthorizationService | IT-01 | Controlled ports | Pod Security Context |
| SR-06 | Inventory Integrity | UC-01 | P2: Inventory Mgt | Inventory Data | TH-02 | AWMS-04 | Sprint 1 | InventoryService / ACID | UT-02 | No secrets in image | ConfigMap mounting |
| SR-08 | Race-condition Protection | UC-01 | P2: Inventory Mgt | Inventory Data | TH-08 | AWMS-04 | Sprint 1 | SQLAlchemy with_for_update | UT-02 | Minimal base image | Resource limits |
| SR-09 | Command Conflict Prevention | UC-02 | P5: Robot Control | Robot Status | TH-09 | AWMS-10 | Sprint 2 | CommandAuthorizationService | E2E-01 | Non-root user | Restricted exposure |
| SR-10 | Audit Logging | UC-01/UC-02 | P7: Audit & Mon | Audit Logs | TH-03 | AWMS-14 | Sprint 2 | security.py / log_audit_event | IT-01 | Controlled ports | Log volume mount |


