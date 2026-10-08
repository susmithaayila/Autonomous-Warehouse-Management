import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS"
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence", "P07_ThreatModel")
os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)

HEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
SUBHEADER_FONT = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
DATA_FONT = Font(name="Segoe UI", size=10)
THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

def style_sheet(ws, col_widths=None):
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "A2"
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = DATA_FONT
            cell.border = THIN_BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    
    for i, col in enumerate(ws.columns, 1):
        col_letter = get_column_letter(i)
        if col_widths and col_letter in col_widths:
            ws.column_dimensions[col_letter].width = col_widths[col_letter]
        else:
            ws.column_dimensions[col_letter].width = 24

wb = openpyxl.Workbook()

# Sheet 1: Assets & CIA
ws1 = wb.active
ws1.title = "Assets & CIA"
ws1.append(["Asset ID", "Asset Name", "Asset Category", "Confidentiality", "Integrity", "Availability", "Owner", "Impact of Compromise"])
assets_data = [
    ("AST-01", "User Credentials & Passwords", "Authentication", "CRITICAL", "HIGH", "MEDIUM", "User Service", "Unauthorized system login, identity theft, privilege escalation"),
    ("AST-02", "Robot Shared Secrets & HMAC Keys", "Robot Identity", "CRITICAL", "CRITICAL", "HIGH", "Robot Service", "Attacker can forge physical robot commands and cause AGV collisions"),
    ("AST-03", "Robot Dispatch Commands", "Operational Control", "HIGH", "CRITICAL", "CRITICAL", "Command Service", "Disruption of warehouse physical movement, equipment damage"),
    ("AST-04", "Inventory Stock Data", "Business Data", "MEDIUM", "CRITICAL", "HIGH", "Inventory Service", "Inventory corruption, double-selling stock, financial discrepancy"),
    ("AST-05", "Customer Orders", "Business Data", "HIGH", "HIGH", "HIGH", "Order Service", "Order tampering, shipment delays, customer data exposure"),
    ("AST-06", "Warehouse Task Data", "Operations", "MEDIUM", "HIGH", "HIGH", "Task Service", "Incorrect order picking execution, operational workflow failure"),
    ("AST-07", "Robot Status & Telemetry", "Telemetry", "LOW", "HIGH", "CRITICAL", "Robot Service", "False AGV position data leading to missed tasks or route blocks"),
    ("AST-08", "System Audit Logs", "Compliance", "HIGH", "CRITICAL", "HIGH", "Audit Service", "Loss of forensic trace, inability to investigate security incidents"),
    ("AST-09", "JWT Access Tokens", "Session", "CRITICAL", "HIGH", "HIGH", "Auth Service", "Session hijacking, API abuse under compromised user context"),
    ("AST-10", "SQLite Database File & Schema", "Data Store", "CRITICAL", "CRITICAL", "CRITICAL", "Database Layer", "Total system data loss, database corruption, full disclosure")
]
for a in assets_data:
    ws1.append(list(a))
style_sheet(ws1, {"A": 12, "B": 28, "C": 18, "D": 16, "E": 14, "F": 14, "G": 18, "H": 40})


# Sheet 2: STRIDE Matrix (Comprehensive Matrix & Category Breakdown)
ws2 = wb.create_sheet("STRIDE Matrix")
ws2.append(["STRIDE Letter", "STRIDE Category", "Attack Definition", "Affected DFD Elements", "AWMS Project Attack Scenario", "AWMS Project Mitigation Strategy"])
stride_matrix_data = [
    (
        "S", 
        "Spoofing Identity", 
        "An attacker pretends to be a legitimate user, system component, or external AGV robot to gain unauthorized access.", 
        "External Entity (AGV Robot, Web User), Data Flow (Robot API Request), Process (AuthService, RobotCommandAuthService)", 
        "Attacker sends forged HTTP POST commands to `/api/v1/robots/command` using a spoofed Robot ID (`AGV-01`) to trigger unauthorized movement.", 
        "Implement mandatory HMAC-SHA256 signature checks on all robot payloads using per-robot secret keys (SR-03), and enforce JWT token verification for users (SR-01)."
    ),
    (
        "T", 
        "Tampering with Data", 
        "Unauthorized modification of data in transit across network boundaries or at rest within data stores.", 
        "Data Store (SQLite DB, Audit Logs), Data Flow (Command Payloads, DB Queries), Process (FulfillmentService)", 
        "Attacker modifies inventory counts directly via concurrent race condition calls or alters AGV target coordinates in transit from (`Zone-A`) to (`Hazard-Zone`).", 
        "Enforce TLS 1.3 encryption for network payloads; use SQLAlchemy `with_for_update()` pessimistic row locking for atomic stock updates (SR-06, SR-08); use parameterized queries (SR-05)."
    ),
    (
        "R", 
        "Repudiation", 
        "An actor performs an action and denies having done so, due to lack of non-repudiable audit evidence.", 
        "Process (Command Authorization, Fulfillment Service), Data Store (Audit Logs Table), External Entity (Operator User)", 
        "A rogue warehouse operator issues a command to abort an active order dispatch causing shipment loss, then claims the system acted automatically.", 
        "Implement an append-only AuditLog service (SR-10) recording actor user ID, client IP address, UTC timestamp, action payload, and unique UUID nonce."
    ),
    (
        "I", 
        "Information Disclosure", 
        "Exposure of private or sensitive information to unauthorized actors or external systems.", 
        "Data Flow (API HTTP Response), Data Store (Environment Files, SQLite DB), Process (API Gateway, Exception Handlers)", 
        "API exception handlers return unhandled stack trace diagnostic output containing raw database paths, JWT secret keys, or internal schema structures.", 
        "Implement centralized exception sanitization middleware returning generic HTTP error structures (SR-12); store secrets in secure `.env` variables excluded from source control."
    ),
    (
        "D", 
        "Denial of Service (DoS)", 
        "Intentionally flooding or exhausting system resources to make services unavailable to legitimate users and AGVs.", 
        "Process (Robot Dispatcher, Auth API), Data Store (SQLite DB Connection Pool), Data Flow (Network Queue)", 
        "Attacker floods `/api/v1/robots/dispatch` with thousands of rapid invalid requests, filling the DB connection pool and causing real AGVs to miss heartbeats.", 
        "Enforce API rate-limiting middleware (SR-11) (e.g., 100 req/min per IP/token), set connection pool execution timeouts, and implement AGV heartbeat monitor fallbacks."
    ),
    (
        "E", 
        "Elevation of Privilege", 
        "An unprivileged user executes unauthorized commands or elevates their access rights to an administrative tier.", 
        "Process (Role Authorization Middleware, User Role API), Data Store (User Roles Table), Boundary (User -> Admin Zone)", 
        "An Operator user sends `PUT /api/v1/users/self/role` with payload `role: ADMINISTRATOR`, bypassing frontend restrictions and acquiring full system control.", 
        "Enforce strict server-side Role-Based Access Control (RBAC) (SR-04) with hard checks rejecting self-privilege escalation requests (`current_user.id != target_user.id`)."
    )
]
for sm in stride_matrix_data:
    ws2.append(list(sm))
style_sheet(ws2, {"A": 14, "B": 22, "C": 35, "D": 35, "E": 45, "F": 45})


# Sheet 3: STRIDE Threat Table
ws3 = wb.create_sheet("STRIDE Threat Table")
ws3.append(["Threat ID", "DFD Element", "STRIDE Category", "Asset At Risk", "Threat Description", "Impact", "Likelihood", "Risk Level", "Mitigation Control"])
threats = [
    ("TH-01", "Robot Controller Process", "Spoofing", "AST-02 Robot Secrets", "Attacker impersonates a warehouse robot to send fake heartbeats and status", "HIGH", "MEDIUM", "HIGH", "HMAC-SHA256 signature and shared secret verification (SR-03)"),
    ("TH-02", "Inventory DB Data Store", "Tampering", "AST-04 Inventory Data", "Attacker tampers with stock levels directly or via concurrent API requests", "HIGH", "MEDIUM", "HIGH", "SQLAlchemy row locking with_for_update() & RBAC (SR-06, SR-08)"),
    ("TH-03", "Robot Command Queue Flow", "Repudiation", "AST-03 Dispatch Cmds", "Malicious operator denies sending an unauthorized robot move command", "MEDIUM", "LOW", "MEDIUM", "Comprehensive AuditLog capturing actor, IP, timestamp & nonce (SR-10)"),
    ("TH-04", "API Gateway Process", "Information Disclosure", "AST-09 JWT Tokens", "Sensory API leaks internal configuration, stack traces, or secret tokens", "HIGH", "LOW", "HIGH", "Strict error sanitization, secure secret environment injection (SR-12)"),
    ("TH-05", "Robot Dispatcher Process", "Denial of Service", "AST-07 Telemetry", "Flooding robot command endpoints with invalid move signals to stall fleet", "HIGH", "MEDIUM", "HIGH", "Rate limiting, command expiration, heartbeat monitoring (SR-11)"),
    ("TH-06", "User Role Assign API", "Elevation of Privilege", "AST-01 User Credentials", "Operator escalates role to Administrator to bypass authorization controls", "CRITICAL", "LOW", "HIGH", "Strict self-escalation block & Admin role enforcement (SR-04)"),
    ("TH-07", "Robot Command API Flow", "Spoofing / Replay", "AST-03 Dispatch Cmds", "Attacker captures valid command payload and replays it to re-trigger AGV move", "HIGH", "MEDIUM", "HIGH", "Unique UUID nonces and replay detection in CommandAuthService (SR-09)"),
    ("TH-08", "Fulfillment Pipeline", "Tampering / Race", "AST-05 Customer Orders", "Concurrent orders reserve same physical stock simultaneously", "HIGH", "HIGH", "HIGH", "ACID database transaction isolation & reservation counters (SR-07)"),
    ("TH-09", "Robot State Machine", "Denial of Service", "AST-07 Telemetry", "Robot receives conflicting PICK and DROP commands simultaneously", "CRITICAL", "LOW", "HIGH", "State validation preventing concurrent active command status (SR-09)"),
    ("TH-10", "Audit Service Data Store", "Tampering", "AST-08 System Audit Logs", "Attacker deletes audit log entries following unauthorized action", "HIGH", "LOW", "HIGH", "Append-only database triggers and restricted Auditor role access (SR-10)")
]
for t in threats:
    ws3.append(list(t))
style_sheet(ws3, {"A": 12, "B": 24, "C": 20, "D": 22, "E": 40, "F": 12, "G": 12, "H": 12, "I": 40})


# Sheet 4: Information Flow Analysis
ws4 = wb.create_sheet("Information Flow Analysis")
ws4.append(["Flow ID", "Sensitive Asset", "Source Entity", "Flow Path / Processing Nodes", "Destination Entity", "Trust Boundary Crossed", "Security Control In Place"])
flows = [
    ("IF-01", "Robot Command Payload (AST-03)", "CommandAuthorizationService", "API Gateway -> Nonce Validator -> HMAC Signer", "Autonomous AGV Robot", "App Zone -> Robot OT Network Zone", "HMAC-SHA256 Secret Signing & UUID Nonce Verification (SR-03, SR-09)"),
    ("IF-02", "Inventory Balance Data (AST-04)", "FulfillmentService", "Fulfillment Pipeline -> Transaction Manager -> SQLAlchemy ORM", "SQLite Inventory Table", "App Zone -> Database Zone", "SQLAlchemy with_for_update() ACID Row Lock & Isolation (SR-06, SR-07)"),
    ("IF-03", "Auth Credentials & Tokens (AST-01, AST-09)", "Web UI Client", "HTTPS REST API -> Auth Middleware -> Bcrypt Verifier", "AuthService API & Session Store", "User Zone -> App Zone", "TLS 1.3 Encryption, Bcrypt Password Hashing, JWT Expiration (SR-01, SR-02)")
]
for f in flows:
    ws4.append(list(f))
style_sheet(ws4, {"A": 12, "B": 26, "C": 24, "D": 35, "E": 24, "F": 25, "G": 40})


# Sheet 5: Vulnerability Analysis
ws5 = wb.create_sheet("Vulnerability Analysis")
ws5.append(["Vuln ID", "Vulnerability Name", "Affected DFD Element", "Related STRIDE Threat", "Root Cause Description", "Business & System Impact", "Mitigation Control"])
vulns = [
    ("VULN-01", "Unauthenticated Robot Command Dispatch", "5.0 Robot Command Auth", "TH-01 Spoofing / TH-07 Replay", "Lack of cryptographic validation on dispatched AGV payloads", "Unauthorized AGV movement causing physical collision, warehouse damage, or inventory theft", "HMAC-SHA256 signature check & single-use UUID Nonce verification (SR-03, SR-09)"),
    ("VULN-02", "Concurrent Inventory Balance Race Condition", "2.0 Inventory Mgt", "TH-02 Tampering / TH-08 Race", "Non-atomic database reads and writes during simultaneous order checkouts", "Inventory balance corruption, double-selling physical stock, negative inventory balances", "SQLAlchemy row locking `with_for_update()` inside database transaction (SR-06, SR-07)"),
    ("VULN-03", "Self-Role Privilege Escalation", "1.0 Auth Service", "TH-06 Elevation of Privilege", "Missing server-side ownership verification during user role update endpoint", "Operators elevate themselves to Administrator to override safety and financial controls", "Server-side authorization check rejecting `current_user.id == target.id` (SR-04)"),
    ("VULN-04", "Simultaneous Conflicting AGV Movement Commands", "5.0 Robot Command Auth", "TH-09 Command Conflict / DoS", "State machine permits issuing new movement command while previous command is ACTIVE", "AGV receives simultaneous PICK and DROP signals causing internal state lockup or physical collision", "Single-active command state validation rejecting duplicate ISSUED status (SR-09)"),
    ("VULN-05", "Brute-Force Credential Stuffing", "1.0 Auth Service", "TH-01 Spoofing", "Absence of login rate limiting and password attempt caps on authentication API", "Account takeover of operator or admin accounts via dictionary attacks", "Bcrypt hashing & account lockout after 5 consecutive failed login attempts (SR-01, SR-11)"),
    ("VULN-06", "Audit Log Tampering / Deletion", "6.0 Security Audit Stream", "TH-10 Tampering", "Audit log database user account has UPDATE and DELETE privileges", "Attacker wipes logs to obscure malicious actions, disabling post-incident forensics", "Append-only database logging stream restricted to Auditor role (SR-10)")
]
for v in vulns:
    ws5.append(list(v))
style_sheet(ws5, {"A": 12, "B": 28, "C": 22, "D": 22, "E": 35, "F": 38, "G": 40})

# Save Workbook
output_excel_path = os.path.join(EXCEL_DIR, "P07_Threat_Model.xlsx")
wb.save(output_excel_path)
shutil.copy2(output_excel_path, os.path.join(EVIDENCE_DIR, "P07_Threat_Model.xlsx"))
print(f"Saved Excel file to {output_excel_path}")

md_doc_path = os.path.join(EVIDENCE_DIR, "Threat_Modeling_STRIDE_Doc.md")
with open(md_doc_path, "w", encoding="utf-8") as f:
    f.write("""# Phase 07: Threat Modeling and Security Analysis Report
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
""")

print("Updated Phase 7 Threat Modeling report and markdown documentation!")

