import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_DIR = r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS\excel"
os.makedirs(EXCEL_DIR, exist_ok=True)

# Styling Helper
HEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Segoe UI", size=14, bold=True, color="1E3A8A")
DATA_FONT = Font(name="Segoe UI", size=10)
THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

def style_sheet(ws, title):
    ws.views.sheetView[0].showGridLines = True
    # Freeze Header Row
    ws.freeze_panes = "A2"
    
    # Format Headers
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # Format Data Rows
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = DATA_FONT
            cell.border = THIN_BORDER
            if cell.value is not None and isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
    # Auto-adjust column width
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            if len(val) > max_len:
                max_len = len(val)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

# 1. P01_Agile.xlsx
wb1 = openpyxl.Workbook()
ws1_1 = wb1.active
ws1_1.title = "Agile Approach"
ws1_1.append(["Parameter", "Description", "Security Integration Reason"])
ws1_1.append(["Framework", "Scrum with XP Security Practices", "Combines iterative delivery (Scrum) with test-driven secure development, pair programming, and refactoring (XP)."])
ws1_1.append(["Sprint Duration", "2 Weeks", "Allows rapid security vulnerability triage and incremental security testing."])
ws1_1.append(["Roles", "Product Owner, Scrum Master, Developers, Security Auditor", "Security Auditor actively participates in threat modeling and review."])

ws1_2 = wb1.create_sheet(title="Manifesto Mapping")
ws1_2.append(["Agile Manifesto Principle", "AWMS Mapping & Security Practice"])
ws1_2.append(["1. Customer Satisfaction through Early & Continuous Delivery", "Continuous security checks and rapid delivery of order fulfillment features to customers."])
ws1_2.append(["2. Welcome Changing Requirements even late in dev", "Modular RBAC and HMAC security architecture allowing new robot protocols without breaking core."])
ws1_2.append(["3. Deliver Working Software Frequently", "Automated CI/CD security pipelines scanning dependencies and code on every push."])
ws1_2.append(["4. Business People & Developers Work Daily Together", "Security Auditors work directly with Backend Developers to review audit logs and threat models."])
ws1_2.append(["5. Continuous Attention to Technical Excellence & Good Design", "Refactoring insecure modules to use JWT, bcrypt, HMAC-SHA256, and atomic database transactions."])

ws1_3 = wb1.create_sheet(title="Refactoring Opportunities")
ws1_3.append(["Refactoring ID", "Component", "Before Code/Structure", "After Code/Structure", "Security Benefit"])
ws1_3.append(["REF-01", "Robot Command Dispatcher", "Insecure direct command execution without signature check", "HMAC-SHA256 signature verification + Nonce anti-replay validation", "Prevents unauthorized robot movement and replay attacks."])
ws1_3.append(["REF-02", "Inventory Management", "Non-atomic direct quantity modification (`stock = stock - qty`)", "SQLAlchemy `with_for_update()` transaction locking + reservation check", "Prevents race conditions, negative inventory, and stock corruption."])

ws1_4 = wb1.create_sheet(title="Agile Risks")
ws1_4.append(["Risk ID", "Agile Limitation / Security Risk", "Impact Level", "Mitigation Strategy"])
ws1_4.append(["RSK-01", "Over-focus on user features neglects architectural security controls", "HIGH", "Introduce explicit Security User Stories with story points in Sprints (EPIC-06, EPIC-07)."])
ws1_4.append(["RSK-02", "Sprint velocity pressure leading to skipped security testing", "HIGH", "Mandatory CI/CD automated Bandit static analysis and pip-audit quality gates before pull request merge."])

for ws in wb1.worksheets:
    style_sheet(ws, ws.title)
wb1.save(os.path.join(EXCEL_DIR, "P01_Agile.xlsx"))

# 2. P02_SRS.xlsx
wb2 = openpyxl.Workbook()
ws2_1 = wb2.active
ws2_1.title = "Stakeholders"
ws2_1.append(["ID", "Stakeholder Name", "Role in AWMS", "Security Responsibility"])
ws2_1.append(["STK-01", "Customer", "Places orders, tracks status", "Secure credential management, input validation"])
ws2_1.append(["STK-02", "Warehouse Operator", "Monitors stock, assigns tasks", "Task creation, least privilege operation"])
ws2_1.append(["STK-03", "Warehouse Administrator", "Registers robots, user roles", "Full RBAC control, identity management"])
ws2_1.append(["STK-04", "Security Auditor", "Inspects audit logs, monitoring", "Compliance review, threat analysis"])
ws2_1.append(["STK-05", "Robot (Autonomous AGV)", "Executes pick/move/drop commands", "HMAC signing, nonce tracking, status heartbeats"])

ws2_2 = wb2.create_sheet(title="Functional Requirements")
ws2_2.append(["Req ID", "Description", "Priority", "Mapped Actor"])
ws2_2.append(["FR-01", "System shall allow users to authenticate using credentials", "Highest", "All Users"])
ws2_2.append(["FR-02", "System shall support inventory item lookup and real-time balance tracking", "High", "Operator, Customer"])
ws2_2.append(["FR-03", "System shall generate fulfillment tasks upon order placement", "High", "Customer, System"])
ws2_2.append(["FR-04", "System shall assign available autonomous robots to tasks", "Highest", "Administrator, Operator"])
ws2_2.append(["FR-05", "System shall transmit signed commands (PICK, MOVE, DROP) to robots", "Highest", "Robot, System"])

ws2_3 = wb2.create_sheet(title="Security Requirements")
ws2_3.append(["Req ID", "Title", "Description", "CIA Impact", "Priority"])
reqs_sec = [
    ("SR-01", "Authentication", "JWT-based session authentication with bcrypt password hashing", "Confidentiality/Integrity", "Highest"),
    ("SR-02", "Role-Based Access Control (RBAC)", "Strict authorization for Administrator, Operator, Customer, Auditor, Robot", "Confidentiality/Integrity", "Highest"),
    ("SR-03", "Robot Identity Verification", "Robots must authenticate using shared HMAC secrets", "Integrity/Authenticity", "Highest"),
    ("SR-04", "Privilege Escalation Prevention", "Users cannot modify their own roles or elevate privileges", "Integrity", "Highest"),
    ("SR-05", "Robot Command Authorization", "Robot commands require valid user role & HMAC verification", "Integrity/Availability", "Highest"),
    ("SR-06", "Inventory Integrity", "Stock updates must execute within ACID transactions", "Integrity", "Highest"),
    ("SR-07", "Transaction Protection", "Database concurrency isolation for stock reservation", "Integrity", "High"),
    ("SR-08", "Race-Condition Protection", "Row-level locking (`with_for_update`) during task allocation", "Integrity", "Highest"),
    ("SR-09", "Command Conflict Prevention", "Prevent simultaneous execution of conflicting commands on same robot", "Integrity/Availability", "Highest"),
    ("SR-10", "Audit Logging", "Tamper-evident log stream for all authentication & command events", "Repudiation", "High"),
    ("SR-11", "Availability Protection", "Rate limiting, command expiration, and heartbeat monitoring", "Availability", "High"),
    ("SR-12", "Secure Secrets", "Secrets injected via environment variables / Kubernetes Secrets", "Confidentiality", "Highest"),
    ("SR-13", "Input Validation", "Pydantic schema validation for all incoming API payloads", "Integrity", "High"),
    ("SR-14", "Secure Deployment", "Non-root Docker container execution and Kubernetes Pod Security", "Confidentiality/Integrity", "High"),
    ("SR-15", "Security Monitoring", "Real-time tracking of failed logins, unauthorized commands, and offline robots", "Availability/Integrity", "High"),
    ("SR-16", "Least Privilege", "Endpoints enforce minimum required role permission scope", "Confidentiality/Integrity", "Highest"),
]
for r in reqs_sec:
    ws2_3.append(list(r))

for ws in wb2.worksheets:
    style_sheet(ws, ws.title)
wb2.save(os.path.join(EXCEL_DIR, "P02_SRS.xlsx"))

print("Created P01_Agile.xlsx and P02_SRS.xlsx successfully!")
