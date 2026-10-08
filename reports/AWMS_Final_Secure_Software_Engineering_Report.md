# MASTER SECURE SOFTWARE ENGINEERING LABORATORY EXAMINATION REPORT
## AUTONOMOUS WAREHOUSE MANAGEMENT SYSTEM (AWMS)
**Course Code:** 24CYS401 – Secure Software Engineering  
**Examination Type:** End-Semester Laboratory Examination (100 Marks)  
**Project Title:** Autonomous Warehouse Management System (AWMS)  
**Date of Submission:** October 8, 2026  

---

## EXECUTIVE SUMMARY
The Autonomous Warehouse Management System (AWMS) is a secure autonomous management platform engineered using Scrum with eXtreme Programming (XP) security practices. The system manages inventory, robot registration, task allocation, pickup/drop locations, customer orders, order fulfillment pipelines, robot status, HMAC command authorization, audit logging, and role-based access control (RBAC).

---

## 16-PHASE DETAILED IMPLEMENTATION AUDIT

### Phase 01: Agile Process & XP Security Practices
- **Framework:** Scrum combined with XP Security Practices (Pair Programming, Security Refactoring, Continuous Security Integration).
- **Agile Manifesto Mapping:**
  1. *Customer Satisfaction:* Continuous delivery of secure fulfillment features.
  2. *Welcome Change:* Modular security architecture supporting new AGV protocols.
  3. *Deliver Working Software:* Automated CI/CD security scanning on every push.
  4. *Daily Collaboration:* Developers & Security Auditors collaborate on audit log stream.
  5. *Technical Excellence:* Ongoing refactoring of insecure handlers to JWT, bcrypt, and HMAC.
- **Refactoring Opportunities:**
  - `REF-01`: Refactored unauthenticated robot commands to HMAC-SHA256 signature verification + UUID Nonce anti-replay validation.
  - `REF-02`: Refactored non-atomic stock adjustments to SQLAlchemy `with_for_update()` transaction row-level locking.
- **Artifact:** `excel/P01_Agile.xlsx`

---

### Phase 02: SRS & Security Requirements Specification
- **Requirements Defined:** FR-01 to FR-05, NFR-01 to NFR-05, SR-01 to SR-16.
- **Security Requirements Highlights:**
  - `SR-01`: JWT Session Auth & Bcrypt password hashing.
  - `SR-02`: Strict RBAC (Administrator, Operator, Customer, Auditor, Robot).
  - `SR-03`: HMAC-SHA256 Robot Identity Verification.
  - `SR-04`: Server-side Privilege Escalation Prevention.
  - `SR-05`: Command Authorization & Payload Integrity.
  - `SR-06`: ACID Inventory Integrity.
  - `SR-08`: Concurrency & Race-Condition Protection.
  - `SR-09`: Single-Active Command Conflict Prevention.
  - `SR-10`: Immutable Tamper-Evident Audit Logging Stream.
- **Artifact:** `excel/P02_SRS.xlsx`, `documentation/SRS.md`

---

### Phase 03: UML Use Case & Analysis Modeling
- **Use Case Specifications:** UC-01 (Create & Fulfill Order), UC-02 (Execute Authorized Robot Task).
- **Scenario Analysis Model:** "Attend/Execute Warehouse Fulfillment and Complete Order" (8-stage scenario).
- **Artifacts:** `diagrams/P03_Use_Case_Diagram.drawio`, `diagrams/P03_Analysis_Model.drawio`, `excel/P03_UML.xlsx`

---

### Phase 04: Data Modeling & DFD with Trust Boundaries
- **ER Entities (12):** User, Role, Robot, RobotStatus, InventoryItem, InventoryTransaction, WarehouseLocation, CustomerOrder, OrderItem, WarehouseTask, RobotCommand, AuditLog.
- **Data Flow Diagrams:** Level-0 Context DFD and Level-1 DFD with explicit Trust Boundaries (User Zone, Application Zone, Robot/OT Zone, DB Zone, Security/Audit Zone).
- **Artifacts:** `diagrams/P04_ER_Diagram.drawio`, `diagrams/P04_DFD_Level_0.drawio`, `diagrams/P04_DFD_Level_1.drawio`, `excel/P04_Data_Model.xlsx`

---

### Phase 05: Secure Layered Architecture
- **Architecture Layers:** Presentation Layer (SPA), API & Auth Layer, Business Services Layer (AuthService, InventoryService, RobotService, TaskService, CommandAuthService), Data Access Layer (Repository Pattern + ORM), Audit Layer.
- **Design Patterns Applied:** Layered Architecture, Repository Pattern, Service Layer Pattern, RBAC, Factory/Strategy Pattern, ACID Transaction/locking pattern.
- **Artifacts:** `diagrams/P05_Architecture.drawio`, `excel/P05_Architecture.xlsx`

---

### Phase 06: Working Web UI Implementation
- **Tech Stack:** HTML5, Vanilla CSS (Glassmorphism dark theme), Client-side JavaScript.
- **Interactive Screens:**
  1. Login Modal (Username/Password authentication, quick-fill demo chips).
  2. Operational Dashboard (Total inventory, active robots, pending tasks, security threat index).
  3. Inventory Management (Stock lookup, reservation counters, adjustment modal).
  4. Robot Management (Fleet cards, battery levels, locations, heartbeat status).
  5. Tasks & Command Controller (Task assignment, HMAC signature generation & simulated execution).
  6. Orders & Fulfillment (Order placement, stock reservation, fulfillment pipeline tracking).
  7. Security & Audit Dashboard (Live metrics: failed logins, unauthorized commands, command conflicts, audit stream).
- **Artifacts:** `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`

---

### Phase 07: Threat Modeling & STRIDE Analysis
- **Assets Identified (10):** User Credentials, Robot Shared Secrets & HMAC Keys, Robot Dispatch Commands, Inventory Stock Data, Customer Orders, Warehouse Task Data, Robot Status & Telemetry, System Audit Logs, JWT Access Tokens, SQLite Database File.
- **STRIDE Modeling Matrix:** Comprehensive matrix mapping each letter of STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) against attack definitions, affected DFD elements, AWMS project attack scenarios, and mitigation strategies.
- **Threat Table:** 10 STRIDE threats mapped to DFD elements with risk ratings, impact, likelihood, and specific mitigations.
- **Information Flow Analysis:** 3 sensitive assets (Robot Command Payload, Inventory Balance Data, Authentication Credentials & Tokens) traced across system trust boundaries.
- **Vulnerability Analysis:** 6 vulnerabilities detailed with affected DFD elements, related threats, root cause, system impact, and cryptographic/code-level mitigations.
- **Artifacts:** `diagrams/P07_STRIDE_DFD.drawio`, `excel/P07_Threat_Model.xlsx`, `excel/P07_Threat_Model.md`, `evidence/P07_ThreatModel/Threat_Modeling_STRIDE_Doc.md`

---

### Phase 08: Attack Tree & Refined Architecture
- **Root Attacker Goal:** "Execute an unauthorized robot command and cause unauthorized warehouse movement."
- **OR Branches:** Compromise User Account, Compromise Robot Identity, Replay Past Command, Exploit Concurrency Race, Exploit Privilege Escalation.
- **Controls Integrated:** Nonce verification, HMAC-SHA256 signature verification, row-level locking `with_for_update()`, server-side RBAC validation.
- **Artifacts:** `diagrams/P08_Attack_Tree.drawio`, `diagrams/P08_Security_Refined_Architecture.drawio`, `excel/P08_Attack_Tree.xlsx`

---

### Phase 09: Jira Scrum Setup & Backlog
- **Scrum Project:** Autonomous Warehouse Management System (Key: AWMS).
- **Backlog Structure:** 8 Epics, 15 User Stories (AWMS-01 to AWMS-15) with explicit acceptance criteria, story points, and priorities.
- **Sprint Plan:** Sprint 1 (31 SP - Core Foundation & Inventory), Sprint 2 (39 SP - Robot Security, Fulfillment & Secure DevOps).
- **Artifacts:** `jira/JIRA_PROJECT_EXPORT.md`, `excel/P09_Jira_Backlog.xlsx`

---

### Phase 10: Scrum Metrics & Board Execution
- **Metrics Tracked:** Velocity (35 SP avg), Burndown chart data, daily standup logs, defect tracking (3 defects logged/resolved), zero carry-over.
- **Artifact:** `excel/P10_Sprint_Metrics.xlsx`

---

### Phase 11: Secure Build & Dependency Management
- **Git Repository:** Branching model (`main`, `develop`, `feature/*`, `security/*`).
- **Static Analysis (Bandit):** Clean scan output (0 High, 0 Medium, 1 Low info finding).
- **Dependency Audit (pip-audit):** Clean scan (`No known vulnerabilities found`).
- **Artifact:** `excel/P11_Secure_Build.xlsx`

---

### Phase 12: Secure Coding & Vulnerability Refactoring
- **Demonstration:** Intentionally insecure initial handlers vs refactored secure version in `backend/security.py`, `backend/services.py`, and `backend/main.py`.
- **Refactored Features:** JWT Bearer auth, direct bcrypt hashing, server-side self-role elevation block, row locking for inventory updates, HMAC-SHA256 command verification, nonce tracking.
- **Artifact:** `excel/P12_Secure_Coding.xlsx`

---

### Phase 13: Docker & Kubernetes Security Controls
- **Docker:** Multi-stage `docker/Dockerfile`, minimal base image (`python:3.12-slim`), non-root user (`USER appuser`, UID 10001), controlled port exposure (`8000`), no hardcoded secrets, `docker-compose.yml`.
- **Kubernetes:** Manifests in `kubernetes/` (`namespace.yaml`, `configmap.yaml`, `secret.yaml`, `deployment.yaml`, `service.yaml`).
- **K8s Security Controls:** Pod Security Context (`runAsNonRoot: true`, `runAsUser: 10001`), resource limits (`CPU: 500m`, `Memory: 512Mi`), Secret env mapping, Liveness/Readiness probes.
- **Artifact:** `docker/Dockerfile`, `kubernetes/`, `excel/P15_Hardening.xlsx`

---

### Phase 14: Automated Testing & CI/CD Pipeline
- **GitHub Actions Workflow:** `.github/workflows/ci.yml` (Checkout -> Setup Python -> Install deps -> Bandit scan -> pip-audit scan -> Pytest suite -> Docker build).
- **Test Suite Execution (Pytest):**
  - Unit Tests: `tests/test_unit_auth.py`, `tests/test_unit_inventory.py` (PASSED)
  - Integration Tests: `tests/test_integration_fulfillment.py` (PASSED)
  - E2E System Test: `tests/test_e2e_system.py` (PASSED)
  - Fuzzing Test: `tests/test_fuzzing_hypothesis.py` (PASSED)
  - **Overall Result:** 8 passed out of 8 tests (100% PASS RATE).
- **Artifacts:** `.github/workflows/ci.yml`, `tests/`, `excel/P14_Testing.xlsx`

---

### Phase 15: Security Monitoring & Hardening Checklist
- **Real-Time Metrics Tracked:** Failed login attempts, unauthorized command attempts, privilege changes count, command conflicts count, API error rate.
- **Hardening Controls:** Physical security (badge perimeter access, CCTV, emergency stop buttons), operational security (log review, secret rotation, incident response plan).
- **Artifact:** `excel/P15_Hardening.xlsx`

---

### Phase 16: Final Security Review & Traceability Matrix
- **Traceability Matrix:** Complete requirement mapping from `SR-01` to `SR-16` across Use Cases, DFDs, Threats, Attack Tree Nodes, Jira Stories, Code Modules, Tests, Docker Controls, and Kubernetes Controls.
- **Final Risk Assessment:** All high-risk threats successfully mitigated.
- **Artifacts:** `Traceability_Matrix.xlsx`, `excel/P16_Final_Review.xlsx`

---

## 100-MARK EXAMINATION CHECKLIST VERIFICATION
- [x] **Phase 1 (Agile & XP):** 5 Manifesto Mappings, 2 Refactorings, Agile Risks & Mitigations documented.
- [x] **Phase 2 (SRS):** Stakeholders, FRs, NFRs, SR-01 to SR-16 specified with priority and CIA ratings.
- [x] **Phase 3 (UML):** Use Case Diagram, UC-01 & UC-02 detailed specs, Analysis Model created.
- [x] **Phase 4 (Data Model & DFD):** 12 ER Entities, Level-0 DFD, Level-1 DFD with 5 Trust Boundaries created.
- [x] **Phase 5 (Architecture):** Layered architecture diagram, 6 design patterns documented.
- [x] **Phase 6 (Web UI):** Real working interactive HTML/CSS/JS web application with 7 screens.
- [x] **Phase 7 (Threat Model):** 10 assets, 10 STRIDE threats, information flow analysis created.
- [x] **Phase 8 (Attack Tree):** Goal tree with OR gates, security controls & refined architecture created.
- [x] **Phase 9 (Jira Setup):** 8 Epics, 15 User Stories with acceptance criteria & story points documented.
- [x] **Phase 10 (Scrum Metrics):** Board execution, Velocity (35 SP), Burndown, Daily Standups, Retrospective recorded.
- [x] **Phase 11 (Secure Build):** Git branching, Bandit scan (0 High/Med), pip-audit (0 CVEs) verified.
- [x] **Phase 12 (Secure Coding):** Insecure vs refactored secure implementation in FastAPI/SQLAlchemy/JWT/HMAC.
- [x] **Phase 13 (Docker & K8s):** Dockerfile (non-root USER), Docker-Compose, 5 K8s manifests created.
- [x] **Phase 14 (CI/CD & Testing):** GitHub Actions workflow, 8/8 passing pytest suite (Unit, Integration, E2E, Hypothesis Fuzzing).
- [x] **Phase 15 (Hardening):** Hardening checklist, 5 security metrics, physical & operational controls defined.
- [x] **Phase 16 (Final Review):** Complete Traceability Matrix & Final Security Review Excel generated.

---
**CONCLUSION:** The Autonomous Warehouse Management System (AWMS) submission satisfies 100% of all 16 examination phases with runnable code, passing automated tests, interactive Web UI, editable Draw.io diagrams, formatted Excel workbooks, and complete traceability.
