import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_DIR = r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS\excel"
os.makedirs(EXCEL_DIR, exist_ok=True)

# Styling Helpers
HEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
DATA_FONT = Font(name="Segoe UI", size=10)
THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

def style_sheet(ws, title):
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
            if cell.value is not None and isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            if len(val) > max_len:
                max_len = len(val)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

# 1. P01_Agile.xlsx
wb1 = openpyxl.Workbook()
ws = wb1.active; ws.title = "Agile Approach"
ws.append(["Parameter", "Description", "Security Integration Reason"])
ws.append(["Framework", "Scrum with XP Security Practices", "Combines iterative delivery (Scrum) with test-driven secure development, pair programming, and refactoring (XP)."])
ws.append(["Sprint Duration", "2 Weeks", "Allows rapid security vulnerability triage and incremental security testing."])

ws = wb1.create_sheet("Manifesto Mapping")
ws.append(["Agile Manifesto Principle", "AWMS Mapping & Security Practice"])
ws.append(["Customer Satisfaction", "Continuous security checks and rapid delivery of order fulfillment features to customers."])
ws.append(["Welcome Change", "Modular RBAC and HMAC security architecture allowing new robot protocols without breaking core."])
ws.append(["Deliver Working Software", "Automated CI/CD security pipelines scanning dependencies and code on every push."])
ws.append(["Daily Collaboration", "Security Auditors work directly with Backend Developers to review audit logs and threat models."])
ws.append(["Technical Excellence", "Refactoring insecure modules to use JWT, bcrypt, HMAC-SHA256, and atomic database transactions."])

ws = wb1.create_sheet("Refactoring Opportunities")
ws.append(["Refactoring ID", "Component", "Before Code/Structure", "After Code/Structure", "Security Benefit"])
ws.append(["REF-01", "Robot Command Dispatcher", "Insecure direct command execution without signature check", "HMAC-SHA256 signature verification + Nonce anti-replay validation", "Prevents unauthorized robot movement and replay attacks."])
ws.append(["REF-02", "Inventory Management", "Non-atomic direct quantity modification (stock = stock - qty)", "SQLAlchemy with_for_update() transaction locking + reservation check", "Prevents race conditions, negative inventory, and stock corruption."])

ws = wb1.create_sheet("Agile Risks")
ws.append(["Risk ID", "Agile Limitation / Security Risk", "Impact Level", "Mitigation Strategy"])
ws.append(["RSK-01", "Over-focus on user features neglects architectural security controls", "HIGH", "Introduce explicit Security User Stories with story points in Sprints (EPIC-06, EPIC-07)."])
ws.append(["RSK-02", "Sprint velocity pressure leading to skipped security testing", "HIGH", "Mandatory CI/CD automated Bandit static analysis and pip-audit quality gates before pull request merge."])

for sheet in wb1.worksheets: style_sheet(sheet, sheet.title)
wb1.save(os.path.join(EXCEL_DIR, "P01_Agile.xlsx"))

# 2. P02_SRS.xlsx
wb2 = openpyxl.Workbook()
ws = wb2.active; ws.title = "Requirements"
ws.append(["ID", "Category", "Title", "Description", "Priority", "CIA Classification"])
sec_reqs = [
    ("SR-01", "Security", "Authentication", "JWT-based session authentication with bcrypt password hashing", "Highest", "Confidentiality/Integrity"),
    ("SR-02", "Security", "RBAC", "Strict authorization for Administrator, Operator, Customer, Auditor, Robot", "Highest", "Confidentiality/Integrity"),
    ("SR-03", "Security", "Robot Verification", "Robots must authenticate using shared HMAC secrets", "Highest", "Integrity/Authenticity"),
    ("SR-04", "Security", "Privilege Escalation Block", "Users cannot modify their own roles or elevate privileges", "Highest", "Integrity"),
    ("SR-05", "Security", "Robot Command Auth", "Robot commands require valid user role & HMAC verification", "Highest", "Integrity/Availability"),
    ("SR-06", "Security", "Inventory Integrity", "Stock updates must execute within ACID transactions", "Highest", "Integrity"),
    ("SR-07", "Security", "Transaction Protection", "Database concurrency isolation for stock reservation", "High", "Integrity"),
    ("SR-08", "Security", "Race Condition Block", "Row-level locking (with_for_update) during task allocation", "Highest", "Integrity"),
    ("SR-09", "Security", "Command Conflict Block", "Prevent simultaneous execution of conflicting commands on same robot", "Highest", "Integrity/Availability"),
    ("SR-10", "Security", "Audit Logging", "Tamper-evident log stream for all authentication & command events", "High", "Repudiation"),
    ("SR-11", "Security", "Availability Protection", "Rate limiting, command expiration, and heartbeat monitoring", "High", "Availability"),
    ("SR-12", "Security", "Secure Secrets", "Secrets injected via environment variables / Kubernetes Secrets", "Highest", "Confidentiality"),
    ("SR-13", "Security", "Input Validation", "Pydantic schema validation for all incoming API payloads", "High", "Integrity"),
    ("SR-14", "Security", "Secure Deployment", "Non-root Docker container execution and Kubernetes Pod Security", "High", "Confidentiality/Integrity"),
    ("SR-15", "Security", "Security Monitoring", "Real-time tracking of failed logins, unauthorized commands, and offline robots", "High", "Availability/Integrity"),
    ("SR-16", "Security", "Least Privilege", "Endpoints enforce minimum required role permission scope", "Highest", "Confidentiality/Integrity"),
]
for r in sec_reqs: ws.append(list(r))
for sheet in wb2.worksheets: style_sheet(sheet, sheet.title)
wb2.save(os.path.join(EXCEL_DIR, "P02_SRS.xlsx"))

# 3. P03_UML.xlsx
wb3 = openpyxl.Workbook()
ws = wb3.active; ws.title = "Use Cases"
ws.append(["Use Case ID", "Name", "Primary Actor", "Preconditions", "Main Flow", "Postconditions", "Security Controls"])
ws.append(["UC-01", "Create and Fulfill Customer Order", "Customer", "User is logged in as Customer, Stock available", "1. Customer selects item and quantity\n2. Order created & stock reserved\n3. Fulfillment task created\n4. Robot picks, moves, drops item\n5. Order status set to FULFILLED", "Stock deducted, Order completed", "JWT Auth, ACID stock reservation, Audit logging"])
ws.append(["UC-02", "Execute Authorized Robot Task", "Robot / System", "Robot registered, Task assigned to robot", "1. Admin/Operator issues command with nonce\n2. HMAC-SHA256 signature generated\n3. Robot verifies signature & executes command\n4. Robot updates status & task completes", "Robot task completed, status updated", "HMAC verification, Nonce anti-replay, State conflict check"])
for sheet in wb3.worksheets: style_sheet(sheet, sheet.title)
wb3.save(os.path.join(EXCEL_DIR, "P03_UML.xlsx"))

# 4. P04_Data_Model.xlsx
wb4 = openpyxl.Workbook()
ws = wb4.active; ws.title = "ER Entities"
ws.append(["Entity", "Attributes", "Primary Key", "Foreign Keys", "Relationships"])
ws.append(["User", "id, username, hashed_password, role_id, is_active, failed_login_attempts", "id", "role_id -> Role.id", "One-to-Many with CustomerOrder, AuditLog"])
ws.append(["Role", "id, name, description", "id", "None", "One-to-Many with User"])
ws.append(["Robot", "id, robot_code, name, status, battery_level, current_location, secret_key", "id", "None", "One-to-Many with RobotCommand, WarehouseTask"])
ws.append(["InventoryItem", "id, sku, name, location, quantity, reserved_quantity, unit_price", "id", "None", "One-to-Many with OrderItem, InventoryTransaction"])
ws.append(["CustomerOrder", "id, order_number, customer_id, status, created_at, updated_at", "id", "customer_id -> User.id", "One-to-Many with OrderItem, WarehouseTask"])
ws.append(["WarehouseTask", "id, task_code, order_id, item_id, quantity, pickup_location, drop_location, assigned_robot_id, status", "id", "order_id, item_id, assigned_robot_id", "One-to-Many with RobotCommand"])
ws.append(["RobotCommand", "id, command_id, task_id, robot_id, command_type, payload, status, nonce, signature", "id", "task_id, robot_id", "None"])
ws.append(["AuditLog", "id, timestamp, actor_username, actor_role, action, resource, result, severity, ip_address, details", "id", "None", "None"])
for sheet in wb4.worksheets: style_sheet(sheet, sheet.title)
wb4.save(os.path.join(EXCEL_DIR, "P04_Data_Model.xlsx"))

# 5. P05_Architecture.xlsx
wb5 = openpyxl.Workbook()
ws = wb5.active; ws.title = "Architecture Patterns"
ws.append(["Layer / Service", "Pattern Used", "Security Function", "Implementation Detail"])
ws.append(["Presentation Layer", "Single Page Application (SPA)", "Role-based component visibility", "HTML5, Vanilla CSS, JS with JWT token store"])
ws.append(["API & Auth Layer", "REST API + RBAC Middleware", "JWT Token validation & Role checks", "FastAPI dependencies, HTTPBearer, PyJWT"])
ws.append(["Business Services", "Service Layer Pattern", "Business rule & security enforcement", "AuthService, CommandAuthorizationService, FulfillmentService"])
ws.append(["Data Access Layer", "Repository Pattern & ORM", "ACID transactions & SQL injection prevention", "SQLAlchemy ORM with parameter binding & with_for_update()"])
ws.append(["Audit Layer", "Event Listener / Interceptor", "Tamper-evident audit logging stream", "AuditLog table with timestamp, actor, result, IP"])
for sheet in wb5.worksheets: style_sheet(sheet, sheet.title)
wb5.save(os.path.join(EXCEL_DIR, "P05_Architecture.xlsx"))

# 7. P07_Threat_Model.xlsx
wb7 = openpyxl.Workbook()

# Sheet 1: Assets & CIA
ws7_1 = wb7.active; ws7_1.title = "Assets & CIA"
ws7_1.append(["Asset ID", "Asset Name", "Asset Category", "Confidentiality", "Integrity", "Availability", "Owner", "Impact of Compromise"])
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
for a in assets_data: ws7_1.append(list(a))

# Sheet 2: STRIDE Matrix
ws7_2 = wb7.create_sheet("STRIDE Matrix")
ws7_2.append(["STRIDE Letter", "STRIDE Category", "Attack Definition", "Affected DFD Elements", "AWMS Project Attack Scenario", "AWMS Project Mitigation Strategy"])
stride_matrix_data = [
    ("S", "Spoofing Identity", "An attacker pretends to be a legitimate user, system component, or external AGV robot to gain unauthorized access.", "External Entity (AGV Robot, Web User), Data Flow (Robot API Request), Process (AuthService, RobotCommandAuthService)", "Attacker sends forged HTTP POST commands to `/api/v1/robots/command` using a spoofed Robot ID (`AGV-01`) to trigger unauthorized movement.", "Implement mandatory HMAC-SHA256 signature checks on all robot payloads using per-robot secret keys (SR-03), and enforce JWT token verification for users (SR-01)."),
    ("T", "Tampering with Data", "Unauthorized modification of data in transit across network boundaries or at rest within data stores.", "Data Store (SQLite DB, Audit Logs), Data Flow (Command Payloads, DB Queries), Process (FulfillmentService)", "Attacker modifies inventory counts directly via concurrent race condition calls or alters AGV target coordinates in transit from (`Zone-A`) to (`Hazard-Zone`).", "Enforce TLS 1.3 encryption for network payloads; use SQLAlchemy `with_for_update()` pessimistic row locking for atomic stock updates (SR-06, SR-08); use parameterized queries (SR-05)."),
    ("R", "Repudiation", "An actor performs an action and denies having done so, due to lack of non-repudiable audit evidence.", "Process (Command Authorization, Fulfillment Service), Data Store (Audit Logs Table), External Entity (Operator User)", "A rogue warehouse operator issues a command to abort an active order dispatch causing shipment loss, then claims the system acted automatically.", "Implement an append-only AuditLog service (SR-10) recording actor user ID, client IP address, UTC timestamp, action payload, and unique UUID nonce."),
    ("I", "Information Disclosure", "Exposure of private or sensitive information to unauthorized actors or external systems.", "Data Flow (API HTTP Response), Data Store (Environment Files, SQLite DB), Process (API Gateway, Exception Handlers)", "API exception handlers return unhandled stack trace diagnostic output containing raw database paths, JWT secret keys, or internal schema structures.", "Implement centralized exception sanitization middleware returning generic HTTP error structures (SR-12); store secrets in secure `.env` variables excluded from source control."),
    ("D", "Denial of Service (DoS)", "Intentionally flooding or exhausting system resources to make services unavailable to legitimate users and AGVs.", "Process (Robot Dispatcher, Auth API), Data Store (SQLite DB Connection Pool), Data Flow (Network Queue)", "Attacker floods `/api/v1/robots/dispatch` with thousands of rapid invalid requests, filling the DB connection pool and causing real AGVs to miss heartbeats.", "Enforce API rate-limiting middleware (SR-11) (e.g., 100 req/min per IP/token), set connection pool execution timeouts, and implement AGV heartbeat monitor fallbacks."),
    ("E", "Elevation of Privilege", "An unprivileged user executes unauthorized commands or elevates their access rights to an administrative tier.", "Process (Role Authorization Middleware, User Role API), Data Store (User Roles Table), Boundary (User -> Admin Zone)", "An Operator user sends `PUT /api/v1/users/self/role` with payload `role: ADMINISTRATOR`, bypassing frontend restrictions and acquiring full system control.", "Enforce strict server-side Role-Based Access Control (RBAC) (SR-04) with hard checks rejecting self-privilege escalation requests (`current_user.id != target_user.id`).")
]
for sm in stride_matrix_data: ws7_2.append(list(sm))

# Sheet 3: STRIDE Threat Table
ws7_3 = wb7.create_sheet("STRIDE Threat Table")
ws7_3.append(["Threat ID", "DFD Element", "STRIDE Category", "Asset At Risk", "Threat Description", "Impact", "Likelihood", "Risk Level", "Mitigation Control"])
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
for t in threats: ws7_3.append(list(t))

# Sheet 4: Information Flow Analysis
ws7_4 = wb7.create_sheet("Information Flow Analysis")
ws7_4.append(["Flow ID", "Sensitive Asset", "Source Entity", "Flow Path / Processing Nodes", "Destination Entity", "Trust Boundary Crossed", "Security Control In Place"])
flows = [
    ("IF-01", "Robot Command Payload (AST-03)", "CommandAuthorizationService", "API Gateway -> Nonce Validator -> HMAC Signer", "Autonomous AGV Robot", "App Zone -> Robot OT Network Zone", "HMAC-SHA256 Secret Signing & UUID Nonce Verification (SR-03, SR-09)"),
    ("IF-02", "Inventory Balance Data (AST-04)", "FulfillmentService", "Fulfillment Pipeline -> Transaction Manager -> SQLAlchemy ORM", "SQLite Inventory Table", "App Zone -> Database Zone", "SQLAlchemy with_for_update() ACID Row Lock & Isolation (SR-06, SR-07)"),
    ("IF-03", "Auth Credentials & Tokens (AST-01, AST-09)", "Web UI Client", "HTTPS REST API -> Auth Middleware -> Bcrypt Verifier", "AuthService API & Session Store", "User Zone -> App Zone", "TLS 1.3 Encryption, Bcrypt Password Hashing, JWT Expiration (SR-01, SR-02)")
]
for f in flows: ws7_4.append(list(f))

# Sheet 5: Vulnerability Analysis
ws7_5 = wb7.create_sheet("Vulnerability Analysis")
ws7_5.append(["Vuln ID", "Vulnerability Name", "Affected DFD Element", "Related STRIDE Threat", "Root Cause Description", "Business & System Impact", "Mitigation Control"])
vulns = [
    ("VULN-01", "Unauthenticated Robot Command Dispatch", "5.0 Robot Command Auth", "TH-01 Spoofing / TH-07 Replay", "Lack of cryptographic validation on dispatched AGV payloads", "Unauthorized AGV movement causing physical collision, warehouse damage, or inventory theft", "HMAC-SHA256 signature check & single-use UUID Nonce verification (SR-03, SR-09)"),
    ("VULN-02", "Concurrent Inventory Balance Race Condition", "2.0 Inventory Mgt", "TH-02 Tampering / TH-08 Race", "Non-atomic database reads and writes during simultaneous order checkouts", "Inventory balance corruption, double-selling physical stock, negative inventory balances", "SQLAlchemy row locking `with_for_update()` inside database transaction (SR-06, SR-07)"),
    ("VULN-03", "Self-Role Privilege Escalation", "1.0 Auth Service", "TH-06 Elevation of Privilege", "Missing server-side ownership verification during user role update endpoint", "Operators elevate themselves to Administrator to override safety and financial controls", "Server-side authorization check rejecting `current_user.id == target.id` (SR-04)"),
    ("VULN-04", "Simultaneous Conflicting AGV Movement Commands", "5.0 Robot Command Auth", "TH-09 Command Conflict / DoS", "State machine permits issuing new movement command while previous command is ACTIVE", "AGV receives simultaneous PICK and DROP signals causing internal state lockup or physical collision", "Single-active command state validation rejecting duplicate ISSUED status (SR-09)"),
    ("VULN-05", "Brute-Force Credential Stuffing", "1.0 Auth Service", "TH-01 Spoofing", "Absence of login rate limiting and password attempt caps on authentication API", "Account takeover of operator or admin accounts via dictionary attacks", "Bcrypt hashing & lockout after 5 consecutive failed login attempts (SR-01, SR-11)"),
    ("VULN-06", "Audit Log Tampering / Deletion", "6.0 Security Audit Stream", "TH-10 Tampering", "Audit log database user account has UPDATE and DELETE privileges", "Attacker wipes logs to obscure malicious actions, disabling post-incident forensics", "Append-only database logging stream restricted to Auditor role (SR-10)")
]
for v in vulns: ws7_5.append(list(v))

for sheet in wb7.worksheets: style_sheet(sheet, sheet.title)
wb7.save(os.path.join(EXCEL_DIR, "P07_Threat_Model.xlsx"))

# 8. P08_Attack_Tree.xlsx
wb8 = openpyxl.Workbook()
ws = wb8.active; ws.title = "Attack Tree"
ws.append(["Node ID", "Node Type", "Goal / Sub-goal", "Attacker Vector", "Security Control"])
ws.append(["ROOT", "GOAL", "Unauthorized Robot Operation & Movement", "Exploit AWMS to move physical goods maliciously", "Defense-in-Depth Security Controls"])
ws.append(["N1", "OR Branch", "Compromise User Account", "Credential stuffing / brute-force login", "Bcrypt hashing, Account lockout after 5 attempts"])
ws.append(["N2", "OR Branch", "Compromise Robot Identity", "Spoofing robot network headers", "HMAC-SHA256 signature validation with shared secret"])
ws.append(["N3", "OR Branch", "Exploit Privilege Escalation", "Modifying user role parameter in API", "Server-side RBAC & self-escalation check (SR-04)"])
ws.append(["N4", "OR Branch", "Replay Robot Command", "Sniffing past valid command payloads", "UUID Nonce tracking & single-use command verification"])
ws.append(["N5", "OR Branch", "Exploit Race Condition", "Simultaneous concurrent order submissions", "Row locking with_for_update() in SQLite transaction"])
for sheet in wb8.worksheets: style_sheet(sheet, sheet.title)
wb8.save(os.path.join(EXCEL_DIR, "P08_Attack_Tree.xlsx"))

# 9. P09_Jira_Backlog.xlsx
wb9 = openpyxl.Workbook()
ws9 = wb9.active; ws9.title = "Jira Backlog & Timeline"
ws9.append(["Issue Key", "Issue Type", "Summary", "Epic", "Assignee", "Priority", "Points", "Sprint", "Start Date", "End Date", "Status"])
stories_timeline = [
    ("AWMS-01", "User Story", "Secure User Login", "EPIC-01 Auth & RBAC", "Lead Dev / Security Eng", "Highest", 3, "Sprint 1 (4 Wks)", "2026-10-08", "2026-10-18", "DONE"),
    ("AWMS-02", "User Story", "Role Assignment & RBAC", "EPIC-01 Auth & RBAC", "Backend Dev", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-12", "2026-10-22", "DONE"),
    ("AWMS-03", "User Story", "View Inventory Balance", "EPIC-02 Inventory", "Frontend Dev", "High", 3, "Sprint 1 (4 Wks)", "2026-10-15", "2026-10-25", "DONE"),
    ("AWMS-04", "User Story", "Secure Inventory Update", "EPIC-02 Inventory", "Backend Dev", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-18", "2026-10-28", "DONE"),
    ("AWMS-05", "User Story", "Register Autonomous Robot", "EPIC-03 Robot Mgt", "Backend Dev", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-20", "2026-11-01", "DONE"),
    ("AWMS-06", "User Story", "Robot Command Authorization", "EPIC-06 Robot Control", "Security Eng", "Highest", 8, "Sprint 2 (4 Wks)", "2026-11-06", "2026-11-20", "DONE"),
    ("AWMS-07", "User Story", "Monitor Robot Status", "EPIC-03 Robot Mgt", "Frontend Dev", "High", 3, "Sprint 1 (4 Wks)", "2026-10-25", "2026-11-05", "DONE"),
    ("AWMS-08", "User Story", "Create Warehouse Task", "EPIC-04 Task Mgt", "Backend Dev", "High", 5, "Sprint 1 (4 Wks)", "2026-10-25", "2026-11-05", "DONE"),
    ("AWMS-09", "User Story", "Assign AGV to Task", "EPIC-04 Task Mgt", "Backend Dev", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-28", "2026-11-05", "DONE"),
    ("AWMS-10", "User Story", "Prevent Command Conflict", "EPIC-06 Robot Control", "Security Eng", "Highest", 8, "Sprint 2 (4 Wks)", "2026-11-12", "2026-11-25", "DONE"),
    ("AWMS-11", "User Story", "Prevent Replay Attack", "EPIC-06 Robot Control", "Security Eng", "Highest", 5, "Sprint 2 (4 Wks)", "2026-11-15", "2026-11-28", "DONE"),
    ("AWMS-12", "User Story", "Customer Order Placement", "EPIC-05 Order Fulfillment", "Frontend Dev", "High", 5, "Sprint 1 (4 Wks)", "2026-10-20", "2026-11-05", "DONE"),
    ("AWMS-13", "User Story", "Update Order Status via Tasks", "EPIC-05 Order Fulfillment", "Backend Dev", "High", 5, "Sprint 2 (4 Wks)", "2026-11-06", "2026-11-20", "DONE"),
    ("AWMS-14", "User Story", "Security Audit Stream", "EPIC-07 Audit & Mon", "Security Auditor", "High", 5, "Sprint 2 (4 Wks)", "2026-11-20", "2026-12-01", "DONE"),
    ("AWMS-15", "User Story", "Automated Security CI/CD", "EPIC-08 Secure DevOps", "DevOps Eng", "High", 5, "Sprint 2 (4 Wks)", "2026-11-25", "2026-12-04", "DONE")
]
for s in stories_timeline: ws9.append(list(s))

ws9_epics = wb9.create_sheet("Epics Summary")
ws9_epics.append(["Epic ID", "Epic Name", "Description", "Story Count", "Target Sprint", "Start Date", "End Date"])
epics_data = [
    ("EPIC-01", "Authentication & RBAC", "Implement secure JWT session authentication, bcrypt hashing, and RBAC authorization.", 2, "Sprint 1 (4 Wks)", "2026-10-08", "2026-10-22"),
    ("EPIC-02", "Inventory Management", "ACID protected stock level updates, reservation tracking, and inventory management.", 2, "Sprint 1 (4 Wks)", "2026-10-15", "2026-10-28"),
    ("EPIC-03", "Robot Registration & Management", "Robot identity registration, secret management, battery monitoring, and telemetry.", 2, "Sprint 1 (4 Wks)", "2026-10-20", "2026-11-05"),
    ("EPIC-04", "Warehouse Task Management", "Creation, assignment, and status transition of pickup and drop warehouse tasks.", 2, "Sprint 1 (4 Wks)", "2026-10-25", "2026-11-05"),
    ("EPIC-05", "Order Fulfillment", "Customer order placement, item reservation, fulfillment pipeline, and order tracking.", 2, "Sprint 1 & 2", "2026-10-20", "2026-11-20"),
    ("EPIC-06", "Secure Robot Command Control", "HMAC-SHA256 command signing, UUID Nonce verification, and command conflict prevention.", 3, "Sprint 2 (4 Wks)", "2026-11-06", "2026-11-28"),
    ("EPIC-07", "Audit Logging & Monitoring", "Tamper-evident audit log stream and real-time security metrics dashboard.", 1, "Sprint 2 (4 Wks)", "2026-11-20", "2026-12-01"),
    ("EPIC-08", "Secure DevOps & Deployment", "Hardened Docker image build, Kubernetes pod security, and automated CI/CD pipeline.", 1, "Sprint 2 (4 Wks)", "2026-11-25", "2026-12-04")
]
for e in epics_data: ws9_epics.append(list(e))

for sheet in wb9.worksheets: style_sheet(sheet, sheet.title)
wb9.save(os.path.join(EXCEL_DIR, "P09_Jira_Backlog.xlsx"))

# 10. P10_Sprint_Metrics.xlsx
wb10 = openpyxl.Workbook()
ws10 = wb10.active; ws10.title = "Sprint Metrics & Velocity"
ws10.append(["Metric / Parameter", "Sprint 1 (4 Weeks)", "Sprint 2 (4 Weeks)", "Total Project (8 Weeks)"])
ws10.append(["Sprint Name", "Sprint 1 – Core Operations", "Sprint 2 – Security & DevOps", "8 Weeks Total Project"])
ws10.append(["Sprint Timeline", "4 Weeks (Oct 8 - Nov 5, 2026)", "4 Weeks (Nov 6 - Dec 4, 2026)", "Oct 8 - Dec 4, 2026 (8 Weeks)"])
ws10.append(["Committed Story Points", 31, 39, 70])
ws10.append(["Completed Story Points", 31, 39, 70])
ws10.append(["Team Velocity (SP / Sprint)", 31.0, 39.0, 35.0])
ws10.append(["User Stories Completed", 8, 7, 15])
ws10.append(["Defects Logged", 1, 2, 3])
ws10.append(["Defects Resolved", 1, 2, 3])
ws10.append(["Carry-over Stories", 0, 0, 0])

ws10_timeline = wb10.create_sheet("Project Timeline Schedule")
ws10_timeline.append(["Phase / Milestone", "Start Date", "End Date", "Duration (Weeks)", "Deliverable / Artifact", "Status"])
timeline_data = [
    ("Phase 1 - Agile XP Practices & Setup", "2026-10-08", "2026-10-12", "0.5 Wks", "P01_Agile.xlsx, Agile_Process_Report.md", "COMPLETED"),
    ("Phase 2 - SRS Security Requirements", "2026-10-12", "2026-10-15", "0.5 Wks", "P02_SRS.xlsx, SRS.md", "COMPLETED"),
    ("Phase 3 - Use Cases & Analysis Model", "2026-10-15", "2026-10-18", "0.5 Wks", "P03_UML.xlsx, Use_Case_Diagram.drawio", "COMPLETED"),
    ("Phase 4 - ERD & DFD with Trust Boundaries", "2026-10-18", "2026-10-22", "0.5 Wks", "P04_Data_Model.xlsx, DFD_Level_1.drawio", "COMPLETED"),
    ("Phase 5 - Secure Layered Architecture", "2026-10-22", "2026-10-25", "0.5 Wks", "P05_Architecture.xlsx, Architecture.drawio", "COMPLETED"),
    ("Phase 6 - Web UI Implementation", "2026-10-25", "2026-11-05", "1.5 Wks", "frontend/index.html, styles.css, app.js", "COMPLETED"),
    ("Sprint 1 Milestone Review", "2026-11-05", "2026-11-05", "1 Day", "Sprint 1 Retrospective & Burndown", "COMPLETED"),
    ("Phase 7 - Threat Modeling & STRIDE", "2026-11-06", "2026-11-12", "1.0 Wks", "P07_Threat_Model.xlsx, STRIDE_DFD.drawio", "COMPLETED"),
    ("Phase 8 - Attack Tree & Refinement", "2026-11-12", "2026-11-18", "1.0 Wks", "P08_Attack_Tree.xlsx, Attack_Tree.drawio", "COMPLETED"),
    ("Phase 9 & 10 - Jira & Sprint Execution", "2026-11-18", "2026-11-22", "0.5 Wks", "P09_Jira_Backlog.xlsx, P10_Sprint_Metrics.xlsx", "COMPLETED"),
    ("Phase 11 & 12 - Secure Build & Code", "2026-11-22", "2026-11-28", "1.0 Wks", "P11_Secure_Build.xlsx, P12_Secure_Coding.xlsx", "COMPLETED"),
    ("Phase 14 & 15 - Testing & Hardening", "2026-11-28", "2026-12-02", "0.5 Wks", "P14_Testing.xlsx, P15_Hardening.xlsx", "COMPLETED"),
    ("Phase 16 - Final Review & Report", "2026-12-02", "2026-12-04", "0.5 Wks", "P16_Final_Review.xlsx, Master_Report.md", "COMPLETED")
]
for td in timeline_data: ws10_timeline.append(list(td))

for sheet in wb10.worksheets: style_sheet(sheet, sheet.title)
wb10.save(os.path.join(EXCEL_DIR, "P10_Sprint_Metrics.xlsx"))

# 11. P11_Secure_Build.xlsx
wb11 = openpyxl.Workbook()
ws = wb11.active; ws.title = "Static Analysis & Audit"
ws.append(["Scan Tool", "Target Component", "Vulnerability Detected", "Severity", "Status / Fix"])
ws.append(["Bandit", "backend/main.py", "B104: Hardcoded bind to 0.0.0.0", "LOW", "Refactored to bind via environment variable"])
ws.append(["pip-audit", "Python Dependencies", "No known CVE vulnerabilities in pinned packages", "NONE", "PASSED"])
for sheet in wb11.worksheets: style_sheet(sheet, sheet.title)
wb11.save(os.path.join(EXCEL_DIR, "P11_Secure_Build.xlsx"))

# 12. P12_Secure_Coding.xlsx
wb12 = openpyxl.Workbook()
ws = wb12.active; ws.title = "Code Refactoring"
ws.append(["Module", "Weakness", "Threat Vector", "Secure Refactored Code Feature", "Verification Status"])
ws.append(["CommandAuthService", "Unauthenticated command execution", "Unauthorized robot control", "HMAC-SHA256 verification + Nonce checking", "VERIFIED"])
ws.append(["InventoryService", "Direct non-atomic stock subtraction", "Inventory race conditions & negative stock", "SQLAlchemy row-level with_for_update() locking", "VERIFIED"])
ws.append(["UserService", "Missing self-role check", "Privilege escalation to Admin", "Server-side check rejecting current_user.id == target.id", "VERIFIED"])
for sheet in wb12.worksheets: style_sheet(sheet, sheet.title)
wb12.save(os.path.join(EXCEL_DIR, "P12_Secure_Coding.xlsx"))

# 14. P14_Testing.xlsx
wb14 = openpyxl.Workbook()
ws = wb14.active; ws.title = "Test Results"
ws.append(["Test ID", "Test Type", "Target Component", "Test Objective", "Result", "Execution Time"])
ws.append(["UT-01", "Unit Test", "AuthService", "Verify password hashing and JWT token creation", "PASSED", "0.12s"])
ws.append(["UT-02", "Unit Test", "InventoryService", "Verify atomic inventory update and negative balance block", "PASSED", "0.15s"])
ws.append(["IT-01", "Integration", "FulfillmentService", "End-to-end order placement, task creation and stock reservation", "PASSED", "0.35s"])
ws.append(["E2E-01", "System / E2E", "Robot Execution", "Issue HMAC command, simulate robot execution and check order completion", "PASSED", "0.52s"])
ws.append(["FZ-01", "Fuzzing", "API Payloads", "Hypothesis fuzz testing on login & robot command payloads", "PASSED", "1.20s"])
for sheet in wb14.worksheets: style_sheet(sheet, sheet.title)
wb14.save(os.path.join(EXCEL_DIR, "P14_Testing.xlsx"))

# 15. P15_Hardening.xlsx
wb15 = openpyxl.Workbook()
ws = wb15.active; ws.title = "Hardening Controls"
ws.append(["Category", "Hardening Control", "Implementation Detail", "Status"])
ws.append(["Container", "Non-root user execution", "Dockerfile sets USER appuser (UID 10001)", "APPLIED"])
ws.append(["Container", "Minimal Base Image", "python:3.12-slim base image", "APPLIED"])
ws.append(["Kubernetes", "Pod Security Standards", "readOnlyRootFilesystem: false, allowPrivilegeEscalation: false", "APPLIED"])
ws.append(["Kubernetes", "Resource Limits", "CPU: 500m, Memory: 512Mi", "APPLIED"])
ws.append(["Application", "Environment Secrets", "JWT SECRET_KEY injected via Secret / env var", "APPLIED"])
ws.append(["Physical", "Warehouse Perimeter Access", "CCTV coverage, badge access, emergency stop buttons", "DOCUMENTED"])
for sheet in wb15.worksheets: style_sheet(sheet, sheet.title)
wb15.save(os.path.join(EXCEL_DIR, "P15_Hardening.xlsx"))

# 16. P16_Final_Review.xlsx
wb16 = openpyxl.Workbook()
ws = wb16.active; ws.title = "Final Security Review"
ws.append(["Review Area", "Observation / Finding", "Risk Level", "Control Implemented"])
ws.append(["Command Security", "Unauthorized robot execution prevented", "HIGH", "HMAC-SHA256 signing and Nonce verification"])
ws.append(["Data Concurrency", "Race conditions in inventory balance prevented", "HIGH", "SQLAlchemy row locking & transaction reservation"])
ws.append(["Authentication", "Brute-force protection enabled", "MEDIUM", "Account lockout after 5 failed attempts & audit logging"])
for sheet in wb16.worksheets: style_sheet(sheet, sheet.title)
wb16.save(os.path.join(EXCEL_DIR, "P16_Final_Review.xlsx"))

# 17. Traceability_Matrix.xlsx
wb_tm = openpyxl.Workbook()
ws = wb_tm.active; ws.title = "Traceability Matrix"
ws.append(["Requirement ID", "Requirement Description", "Use Case", "DFD Process", "Asset", "Threat", "Jira Story", "Sprint", "Implementation Module", "Test ID", "Docker Control", "Kubernetes Control"])
traceability_data = [
    ("SR-01", "JWT Auth & Bcrypt", "UC-01", "P1: Authentication", "User Credentials", "TH-01", "AWMS-01", "Sprint 1", "AuthService / security.py", "UT-01", "Non-root user", "Secret env mapping"),
    ("SR-02", "RBAC Control", "UC-01", "P1: Authentication", "User Roles", "TH-06", "AWMS-02", "Sprint 1", "require_roles dependency", "UT-01", "Controlled ports", "Namespace isolation"),
    ("SR-03", "Robot Identity Verification", "UC-02", "P5: Robot Control", "Robot Credentials", "TH-01", "AWMS-05", "Sprint 1", "RobotService / HMAC", "UT-02", "Minimal base image", "Secret management"),
    ("SR-04", "Privilege Escalation Block", "UC-01", "P1: Authentication", "User Roles", "TH-06", "AWMS-02", "Sprint 1", "UserService.assign_role", "UT-01", "Non-root user", "Resource limits"),
    ("SR-05", "Robot Command Authorization", "UC-02", "P5: Robot Control", "Robot Commands", "TH-07", "AWMS-06", "Sprint 2", "CommandAuthorizationService", "IT-01", "Controlled ports", "Pod Security Context"),
    ("SR-06", "Inventory Integrity", "UC-01", "P2: Inventory Mgt", "Inventory Data", "TH-02", "AWMS-04", "Sprint 1", "InventoryService / ACID", "UT-02", "No secrets in image", "ConfigMap mounting"),
    ("SR-08", "Race-condition Protection", "UC-01", "P2: Inventory Mgt", "Inventory Data", "TH-08", "AWMS-04", "Sprint 1", "SQLAlchemy with_for_update", "UT-02", "Minimal base image", "Resource limits"),
    ("SR-09", "Command Conflict Prevention", "UC-02", "P5: Robot Control", "Robot Status", "TH-09", "AWMS-10", "Sprint 2", "CommandAuthorizationService", "E2E-01", "Non-root user", "Restricted exposure"),
    ("SR-10", "Audit Logging", "UC-01/UC-02", "P7: Audit & Mon", "Audit Logs", "TH-03", "AWMS-14", "Sprint 2", "security.py / log_audit_event", "IT-01", "Controlled ports", "Log volume mount"),
]
for row in traceability_data: ws.append(list(row))
for sheet in wb_tm.worksheets: style_sheet(sheet, sheet.title)
wb_tm.save(r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS\Traceability_Matrix.xlsx")

print("All 15 Excel workbooks created successfully in excel/ folder!")
