# Software Requirements Specification (SRS)
## Autonomous Warehouse Management System (AWMS)
**Course:** 24CYS401 – Secure Software Engineering  
**Project:** Autonomous Warehouse Management System (AWMS)  
**Date:** October 8, 2026  

---

### 1. Introduction
The **Autonomous Warehouse Management System (AWMS)** manages automated robots performing goods picking, transport, and fulfillment inside a secure warehouse facility.

### 2. Stakeholders & User Roles
1. **Customer:** Creates orders, views inventory, tracks order fulfillment status.
2. **Warehouse Operator:** Views inventory balance, creates tasks, assigns available robots to tasks.
3. **Warehouse Administrator:** Registers robots, manages user roles, configures RBAC policies.
4. **Security Auditor:** Monitors security log streams, reviews privilege changes, inspects unauthorized access metrics.
5. **Autonomous Robot (AGV):** Authenticates via HMAC-SHA256, executes valid task commands, reports position and battery status.

---

### 3. Functional Requirements (FR-01 to FR-05)
- **FR-01:** System shall authenticate users via JWT session tokens.
- **FR-02:** System shall allow real-time inventory lookup and balance adjustments.
- **FR-03:** System shall automatically generate warehouse tasks for customer orders.
- **FR-04:** System shall assign available IDLE robots to pickup and drop tasks.
- **FR-05:** System shall issue and execute HMAC-SHA256 signed robot commands.

---

### 4. Security Requirements (SR-01 to SR-16)
- **SR-01 Authentication:** JWT tokens with bcrypt password hashing.
- **SR-02 RBAC:** Enforced role permissions (Customer, Operator, Admin, Auditor, Robot).
- **SR-03 Robot Identity Verification:** HMAC secret signing for all robot commands.
- **SR-04 Privilege Escalation Prevention:** Block self-role elevation.
- **SR-05 Robot Command Authorization:** Role & HMAC signature verification.
- **SR-06 Inventory Integrity:** ACID database transactions.
- **SR-07 Transaction Protection:** Isolation level locks during stock updates.
- **SR-08 Race-Condition Protection:** Row locking `with_for_update()` in SQLite/SQLAlchemy.
- **SR-09 Command Conflict Prevention:** Single-active command state machine.
- **SR-10 Audit Logging:** Immutable log stream for all security-sensitive operations.
- **SR-11 Availability Protection:** Heartbeat monitoring and rate limiting.
- **SR-12 Secure Secrets:** Environment variable injection (Secret keys).
- **SR-13 Input Validation:** Pydantic schema validation on API payloads.
- **SR-14 Secure Deployment:** Non-root Docker user and Kubernetes pod security.
- **SR-15 Security Monitoring:** Real-time metrics for failed logins, unauthorized commands, and offline robots.
- **SR-16 Least Privilege:** Role-based endpoint protection.
