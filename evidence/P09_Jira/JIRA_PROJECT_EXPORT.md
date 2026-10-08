# JIRA SCRUM PROJECT EXPORT & BACKLOG DOCUMENTATION
## Autonomous Warehouse Management System (AWMS)
**Project Key:** AWMS  
**Project Type:** Scrum Software Development  
**Project Lead / Scrum Master:** Secure Assistant  

---

### 1. Epics (EPIC-01 to EPIC-08)
- **EPIC-01:** Authentication and RBAC (5 Stories)
- **EPIC-02:** Inventory Management (3 Stories)
- **EPIC-03:** Robot Registration and Management (3 Stories)
- **EPIC-04:** Warehouse Task Management (2 Stories)
- **EPIC-05:** Order Fulfillment (2 Stories)
- **EPIC-06:** Secure Robot Command Control (3 Stories)
- **EPIC-07:** Audit Logging and Security Monitoring (2 Stories)
- **EPIC-08:** Secure DevOps and Deployment (2 Stories)

---

### 2. User Stories (AWMS-01 to AWMS-15)

#### AWMS-01: User Authentication
*As a warehouse user, I want to securely log in, so that only authenticated users can access warehouse operations.*
- **Epic:** EPIC-01 Authentication and RBAC
- **Priority:** Highest | **Story Points:** 3 | **Sprint:** Sprint 1
- **Acceptance Criteria:**
  1. Valid credentials return JWT access token.
  2. Invalid credentials are rejected with 401 Unauthorized.
  3. Passwords hashed using bcrypt.
  4. Failed login attempts recorded in Audit Log; account locks after 5 failed attempts.

#### AWMS-02: Role Assignment & RBAC
*As a warehouse administrator, I want to assign roles to users, so that users receive only the permissions required for their responsibilities.*
- **Epic:** EPIC-01 Authentication and RBAC
- **Priority:** Highest | **Story Points:** 5 | **Sprint:** Sprint 1
- **Acceptance Criteria:**
  1. Only Administrators can assign roles.
  2. Self-privilege escalation attempts are blocked with 403 Forbidden.
  3. All privilege changes are logged with CRITICAL severity in Audit Log.

#### AWMS-03: View Inventory
*As a warehouse operator, I want to view inventory, so that I can determine item availability.*
- **Epic:** EPIC-02 Inventory Management
- **Priority:** High | **Story Points:** 3 | **Sprint:** Sprint 1

#### AWMS-04: Secure Inventory Update
*As a warehouse administrator, I want to update inventory securely, so that stock quantities remain accurate.*
- **Epic:** EPIC-02 Inventory Management
- **Priority:** Highest | **Story Points:** 5 | **Sprint:** Sprint 1
- **Acceptance Criteria:**
  1. ACID database transaction locking (`with_for_update`).
  2. Negative stock balances rejected.
  3. Changes audited.

#### AWMS-05: Robot Registration
*As a warehouse administrator, I want to register robots with unique identities, so that only recognized robots can operate.*
- **Epic:** EPIC-03 Robot Registration and Management
- **Priority:** Highest | **Story Points:** 5 | **Sprint:** Sprint 1

#### AWMS-06: Command Authorization
*As a warehouse administrator, I want robot commands to be authorized, so that unauthorized users cannot control robots.*
- **Epic:** EPIC-06 Secure Robot Command Control
- **Priority:** Highest | **Story Points:** 8 | **Sprint:** Sprint 2
- **Acceptance Criteria:**
  1. HMAC-SHA256 signature verification.
  2. Nonce verification for anti-replay.

#### AWMS-07: Robot Status Monitoring
*As a warehouse operator, I want to monitor robot status, so that I can identify unavailable robots.*
- **Epic:** EPIC-03 Robot Registration and Management
- **Priority:** High | **Story Points:** 3 | **Sprint:** Sprint 2

#### AWMS-08: Warehouse Task Creation
*As a warehouse operator, I want to create and manage warehouse tasks, so that goods can be moved efficiently.*
- **Epic:** EPIC-04 Warehouse Task Management
- **Priority:** High | **Story Points:** 5 | **Sprint:** Sprint 1

#### AWMS-09: Task Assignment to AGV
*As a warehouse administrator, I want to assign available robots to tasks, so that warehouse operations can proceed safely.*
- **Epic:** EPIC-04 Warehouse Task Management
- **Priority:** Highest | **Story Points:** 5 | **Sprint:** Sprint 1

#### AWMS-10: Command Conflict Prevention
*As a warehouse system, I want to prevent conflicting robot commands, so that robots do not execute incompatible simultaneous commands.*
- **Epic:** EPIC-06 Secure Robot Command Control
- **Priority:** Highest | **Story Points:** 8 | **Sprint:** Sprint 2

#### AWMS-11: Replay Attack Protection
*As a warehouse system, I want to prevent replayed robot commands, so that old commands cannot be maliciously reused.*
- **Epic:** EPIC-06 Secure Robot Command Control
- **Priority:** Highest | **Story Points:** 5 | **Sprint:** Sprint 2

#### AWMS-12: Order Creation & Tracking
*As a customer, I want to create and track my warehouse order, so that I know the status of my requested goods.*
- **Epic:** EPIC-05 Order Fulfillment
- **Priority:** High | **Story Points:** 5 | **Sprint:** Sprint 1

#### AWMS-13: Order Status Update via Tasks
*As a warehouse operator, I want completed robot tasks to update order status, so that fulfillment reflects actual warehouse activity.*
- **Epic:** EPIC-05 Order Fulfillment
- **Priority:** High | **Story Points:** 5 | **Sprint:** Sprint 2

#### AWMS-14: Security Audit Review
*As a security auditor, I want to review security-relevant events, so that suspicious warehouse activity can be investigated.*
- **Epic:** EPIC-07 Audit Logging and Security Monitoring
- **Priority:** High | **Story Points:** 5 | **Sprint:** Sprint 2

#### AWMS-15: Automated Security Pipeline
*As a security engineer, I want automated security checks in CI/CD, so that vulnerabilities are detected before deployment.*
- **Epic:** EPIC-08 Secure DevOps and Deployment
- **Priority:** High | **Story Points:** 5 | **Sprint:** Sprint 2

---

### 3. Sprint Breakdown & Velocity
- **Sprint 1 Commitment:** 31 Story Points (AWMS-01, AWMS-02, AWMS-03, AWMS-04, AWMS-05, AWMS-08, AWMS-09, AWMS-12) - **Completed: 31 SP (100%)**
- **Sprint 2 Commitment:** 39 Story Points (AWMS-06, AWMS-07, AWMS-10, AWMS-11, AWMS-13, AWMS-14, AWMS-15) - **Completed: 39 SP (100%)**
- **Total Velocity:** 35 Story Points / Sprint average.
