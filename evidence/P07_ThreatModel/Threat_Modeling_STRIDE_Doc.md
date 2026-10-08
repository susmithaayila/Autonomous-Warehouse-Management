# Phase 07: Threat Modeling and Security Analysis Report
## Course: 24CYS401 – Secure Software Engineering
**Project:** Autonomous Warehouse Management System (AWMS)

---

### 1. Asset Identification & CIA Classification (10 Assets Identified)

| Asset ID | Asset Name | Asset Category | Confidentiality | Integrity | Availability | Asset Owner | Business Impact of Compromise |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **AST-01** | User Credentials & Passwords | Authentication | **CRITICAL** | **HIGH** | **MEDIUM** | Auth Service | Unauthorized login, identity theft, privilege escalation |
| **AST-02** | Robot Shared Secrets & HMAC Keys | Robot Identity | **CRITICAL** | **CRITICAL** | **HIGH** | Robot Service | Payload forgery, unauthorized AGV control, physical collision |
| **AST-03** | Robot Dispatch Commands | Operational Control | **HIGH** | **CRITICAL** | **CRITICAL** | Command Service | Disruption of warehouse movement, physical equipment damage |
| **AST-04** | Inventory Stock Data | Business Data | **MEDIUM** | **CRITICAL** | **HIGH** | Inventory Service | Inventory balance corruption, double-selling stock, financial loss |
| **AST-05** | Customer Orders | Business Data | **HIGH** | **HIGH** | **HIGH** | Order Service | Order tampering, shipment delays, customer data leakage |
| **AST-06** | Warehouse Task Data | Operations | **MEDIUM** | **HIGH** | **HIGH** | Task Service | Incorrect picking execution, operational workflow failure |
| **AST-07** | Robot Status & Telemetry | Telemetry | **LOW** | **HIGH** | **CRITICAL** | Robot Service | False AGV position reporting leading to route blocks |
| **AST-08** | System Audit Logs | Compliance | **HIGH** | **CRITICAL** | **HIGH** | Audit Service | Loss of forensic trace, inability to investigate security breaches |
| **AST-09** | JWT Access Tokens | Session | **CRITICAL** | **HIGH** | **HIGH** | Auth Service | Session hijacking, API abuse under compromised user context |
| **AST-10** | SQLite Database File & Schema | Data Store | **CRITICAL** | **CRITICAL** | **CRITICAL** | Database Layer | Total system data loss, database corruption, full disclosure |

---

### 2. STRIDE Threat Modeling Matrix (Categorized by Attacks S-T-R-I-D-E)

| Letter | Category | Attack Vector / Definition | Affected DFD Elements | AWMS Project Attack Context | Mitigation Strategy in AWMS |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **S** | **Spoofing Identity** | Impersonating a legitimate user, system component, or AGV robot to gain unauthorized access. | External Entity (AGV, User), Data Flow (REST API), Process (Auth Service, Command Auth) | Attacker sends forged HTTP POST commands to `/api/v1/robots/command` using spoofed Robot ID (`AGV-01`) to cause rogue physical movement. | Enforce mandatory HMAC-SHA256 signature validation using per-robot shared secrets (SR-03); enforce JWT verification on user calls (SR-01). |
| **T** | **Tampering with Data** | Unauthorized modification of data in transit across network boundaries or at rest in databases. | Data Store (SQLite DB, Audit Logs), Data Flow (Command Payload, DB Query), Process (Fulfillment) | Attacker alters AGV target coordinates in transit from (`Zone-A`) to (`Hazard-Zone`), or tampers with inventory stock balance via race condition calls. | Enforce TLS 1.3 network encryption; use SQLAlchemy `with_for_update()` row-level locks for atomic stock updates (SR-06, SR-08); parameterized queries (SR-05). |
| **R** | **Repudiation** | An actor performs an action and denies having done so due to lack of tamper-evident logs. | Process (Command Auth, Fulfillment), Data Store (Audit Logs Table), External Entity (Operator) | Rogue operator issues an unauthorized command aborting an active order shipment, then falsely denies initiating the command. | Implement append-only AuditLog service (SR-10) recording actor user ID, client IP address, UTC timestamp, action payload, and unique UUID nonce. |
| **I** | **Information Disclosure** | Exposure of private or sensitive information to unauthorized external actors. | Data Flow (API Response), Data Store (Environment Config), Process (API Gateway, Handlers) | API exception handlers return raw stack trace diagnostic output exposing internal database paths, secret keys, or schema structures. | Implement centralized exception sanitization middleware returning generic HTTP errors (SR-12); inject secrets via secure `.env` files excluded from VCS. |
| **D** | **Denial of Service (DoS)** | Exhausting system resources to make services unavailable to legitimate AGVs and users. | Process (Robot Dispatcher, Auth API), Data Store (SQLite DB Connection Pool), Data Flow (Network Queue) | Attacker floods `/api/v1/robots/dispatch` with thousands of invalid requests, saturating the DB pool and causing AGVs to miss heartbeats. | Enforce API rate-limiting middleware (SR-11) (100 req/min per IP/token), set connection pool execution timeouts, and implement AGV heartbeat monitor fallbacks. |
| **E** | **Elevation of Privilege** | An unprivileged user executes unauthorized commands or elevates access rights to administrative tier. | Process (Role Authorization Middleware, User API), Data Store (User Roles Table), Boundary (User -> Admin Zone) | Operator user calls `PUT /api/v1/users/self/role` with `role: ADMINISTRATOR`, bypassing UI restrictions to gain full system control. | Enforce strict server-side Role-Based Access Control (RBAC) (SR-04) with hard checks rejecting self-privilege escalation (`current_user.id != target.id`). |

---

### 3. Comprehensive STRIDE Threat Table (10 Detailed Threats)

| Threat ID | DFD Element | STRIDE Category | Asset At Risk | Threat Description | Impact | Likelihood | Risk Level | Mitigation Control |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TH-01** | Robot Controller Process | Spoofing | AST-02 Robot Secrets | Attacker impersonates a warehouse robot to send fake heartbeats and status | HIGH | MEDIUM | HIGH | HMAC-SHA256 signature & shared secret verification (SR-03) |
| **TH-02** | Inventory DB Data Store | Tampering | AST-04 Inventory Data | Attacker tampers with stock levels directly or via concurrent API requests | HIGH | MEDIUM | HIGH | SQLAlchemy row locking `with_for_update()` & RBAC (SR-06, SR-08) |
| **TH-03** | Robot Command Queue Flow | Repudiation | AST-03 Dispatch Cmds | Malicious operator denies sending an unauthorized robot move command | MEDIUM | LOW | MEDIUM | Comprehensive AuditLog capturing actor, IP, timestamp & nonce (SR-10) |
| **TH-04** | API Gateway Process | Information Disclosure | AST-09 JWT Tokens | Sensory API leaks internal configuration, stack traces, or secret tokens | HIGH | LOW | HIGH | Strict error sanitization, secure secret environment injection (SR-12) |
| **TH-05** | Robot Dispatcher Process | Denial of Service | AST-07 Telemetry | Flooding robot command endpoints with invalid move signals to stall fleet | HIGH | MEDIUM | HIGH | Rate limiting, command expiration, heartbeat monitoring (SR-11) |
| **TH-06** | User Role Assign API | Elevation of Privilege | AST-01 User Credentials | Operator escalates role to Administrator to bypass authorization controls | CRITICAL | LOW | HIGH | Strict self-escalation block & Admin role enforcement (SR-04) |
| **TH-07** | Robot Command API Flow | Spoofing / Replay | AST-03 Dispatch Cmds | Attacker captures valid command payload and replays it to re-trigger AGV move | HIGH | MEDIUM | HIGH | Unique UUID nonces and replay detection in CommandAuthService (SR-09) |
| **TH-08** | Fulfillment Pipeline | Tampering / Race | AST-05 Customer Orders | Concurrent orders reserve same physical stock simultaneously | HIGH | HIGH | HIGH | ACID database transaction isolation & reservation counters (SR-07) |
| **TH-09** | Robot State Machine | Denial of Service | AST-07 Telemetry | Robot receives conflicting PICK and DROP commands simultaneously | CRITICAL | LOW | HIGH | State validation preventing concurrent active command status (SR-09) |
| **TH-10** | Audit Service Data Store | Tampering | AST-08 System Audit Logs | Attacker deletes audit log entries following unauthorized action | HIGH | LOW | HIGH | Append-only database triggers & restricted Auditor role access (SR-10) |

---

### 4. Information Flow Analysis (3 Sensitive Assets Traced)

1. **Robot Command Payload Flow (AST-03):**  
   `CommandAuthorizationService` ➔ *(Crosses App Zone to Robot OT Zone)* ➔ `Autonomous Robot AGV`  
   *Security Control:* Mandatory HMAC-SHA256 payload secret signing and single-use UUID Nonce verification (SR-03, SR-09).

2. **Inventory Quantity Balance Flow (AST-04):**  
   `FulfillmentService` ➔ *(Crosses App Zone to Database Zone)* ➔ `SQLite Inventory Table`  
   *Security Control:* SQLAlchemy `with_for_update()` transaction row-level lock & isolation (SR-06, SR-07).

3. **Authentication Credentials & Tokens Flow (AST-01, AST-09):**  
   `Web UI Client` ➔ *(Crosses User Zone to App Zone)* ➔ `AuthService API`  
   *Security Control:* TLS 1.3 Encryption, direct bcrypt password verification, JWT access token issuance (SR-01, SR-02).

---

### 5. Vulnerability Analysis (6 Vulnerabilities Identified)

| Vuln ID | Vulnerability Name | Affected DFD Element | Related Threat | Root Cause Description | System & Business Impact | Mitigation Control |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **VULN-01** | Unauthenticated Robot Command Dispatch | 5.0 Robot Cmd Auth | TH-01 / TH-07 | Missing payload signature validation | AGV collision / warehouse damage | HMAC-SHA256 signature check & UUID Nonce validation |
| **VULN-02** | Inventory Balance Race Condition | 2.0 Inventory Mgt | TH-02 / TH-08 | Non-atomic database checkouts | Stock balance corruption & negative inventory | SQLAlchemy row-level `with_for_update()` lock |
| **VULN-03** | Self-Role Privilege Escalation | 1.0 Auth Service | TH-06 | Missing ownership validation on role API | Operator bypasses safety controls as Admin | Server check `current_user.id != target.id` |
| **VULN-04** | Simultaneous Conflicting Commands | 5.0 Robot Cmd Auth | TH-09 | State machine accepts multi active commands | AGV physical crash or lockup | Single-active command state validation check |
| **VULN-05** | Brute-Force Credential Stuffing | 1.0 Auth Service | TH-01 | Lack of authentication rate limiting | Account takeover via dictionary attacks | Bcrypt hashing & lockout after 5 failed attempts |
| **VULN-06** | Audit Log Wiping | 6.0 Security Audit | TH-10 | Permissive UPDATE/DELETE permissions on DB | Attacker wipes post-incident forensics | Append-only database logging stream |
