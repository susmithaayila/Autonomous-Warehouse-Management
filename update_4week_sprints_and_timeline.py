import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS"
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
JIRA_DIR = os.path.join(BASE_DIR, "jira")

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
        cell.fill = HEADER_FILL; cell.font = HEADER_FONT; cell.alignment = Alignment(horizontal="center", vertical="center")
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = DATA_FONT; cell.border = THIN_BORDER
    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 22

# Update P10_Sprint_Metrics.xlsx with 4-week Sprints
wb10 = openpyxl.Workbook()
ws10 = wb10.active; ws10.title = "Sprint Metrics"
ws10.append(["Metric / Parameter", "Sprint 1 (4 Weeks)", "Sprint 2 (4 Weeks)", "Total Project"])
ws10.append(["Sprint Name", "Sprint 1 – Core Operations", "Sprint 2 – Security & DevOps", "8 Weeks Total"])
ws10.append(["Sprint Duration", "4 Weeks (Oct 8 - Nov 5, 2026)", "4 Weeks (Nov 6 - Dec 4, 2026)", "8 Weeks"])
ws10.append(["Committed Story Points", 31, 39, 70])
ws10.append(["Completed Story Points", 31, 39, 70])
ws10.append(["Velocity", 31, 39, 35.0])
ws10.append(["Defects Logged", 1, 2, 3])
ws10.append(["Defects Resolved", 1, 2, 3])
style_sheet(ws10, ws10.title)
wb10.save(os.path.join(EXCEL_DIR, "P10_Sprint_Metrics.xlsx"))

# Update P09_Jira_Backlog.xlsx with Timings and Assignee
wb9 = openpyxl.Workbook()
ws9 = wb9.active; ws9.title = "Jira Backlog"
ws9.append(["Issue Key", "Issue Type", "Summary", "Epic", "Assignee", "Priority", "Points", "Sprint", "Start Date", "End Date"])
stories_timeline = [
    ("AWMS-01", "User Story", "Secure User Login", "EPIC-01 Auth & RBAC", "Assigned to User", "Highest", 3, "Sprint 1 (4 Wks)", "2026-10-08", "2026-10-18"),
    ("AWMS-02", "User Story", "Role Assignment & RBAC", "EPIC-01 Auth & RBAC", "Assigned to User", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-12", "2026-10-22"),
    ("AWMS-03", "User Story", "View Inventory Balance", "EPIC-02 Inventory", "Assigned to User", "High", 3, "Sprint 1 (4 Wks)", "2026-10-15", "2026-10-25"),
    ("AWMS-04", "User Story", "Secure Inventory Update", "EPIC-02 Inventory", "Assigned to User", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-18", "2026-10-28"),
    ("AWMS-05", "User Story", "Register Autonomous Robot", "EPIC-03 Robot Mgt", "Assigned to User", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-20", "2026-11-01"),
    ("AWMS-06", "User Story", "Robot Command Authorization", "EPIC-06 Robot Control", "Assigned to User", "Highest", 8, "Sprint 2 (4 Wks)", "2026-11-06", "2026-11-20"),
    ("AWMS-07", "User Story", "Monitor Robot Status", "EPIC-03 Robot Mgt", "Assigned to User", "High", 3, "Sprint 1 (4 Wks)", "2026-10-25", "2026-11-05"),
    ("AWMS-08", "User Story", "Create Warehouse Task", "EPIC-04 Task Mgt", "Assigned to User", "High", 5, "Sprint 1 (4 Wks)", "2026-10-25", "2026-11-05"),
    ("AWMS-09", "User Story", "Assign AGV to Task", "EPIC-04 Task Mgt", "Assigned to User", "Highest", 5, "Sprint 1 (4 Wks)", "2026-10-28", "2026-11-05"),
    ("AWMS-10", "User Story", "Prevent Command Conflict", "EPIC-06 Robot Control", "Assigned to User", "Highest", 8, "Sprint 2 (4 Wks)", "2026-11-12", "2026-11-25"),
    ("AWMS-11", "User Story", "Prevent Replay Attack", "EPIC-06 Robot Control", "Assigned to User", "Highest", 5, "Sprint 2 (4 Wks)", "2026-11-15", "2026-11-28"),
    ("AWMS-12", "User Story", "Customer Order Placement", "EPIC-05 Order Fulfillment", "Assigned to User", "High", 5, "Sprint 1 (4 Wks)", "2026-10-20", "2026-11-05"),
    ("AWMS-13", "User Story", "Update Order Status via Tasks", "EPIC-05 Order Fulfillment", "Assigned to User", "High", 5, "Sprint 2 (4 Wks)", "2026-11-06", "2026-11-20"),
    ("AWMS-14", "User Story", "Security Audit Stream", "EPIC-07 Audit & Mon", "Assigned to User", "High", 5, "Sprint 2 (4 Wks)", "2026-11-20", "2026-12-01"),
    ("AWMS-15", "User Story", "Automated Security CI/CD", "EPIC-08 Secure DevOps", "Assigned to User", "High", 5, "Sprint 2 (4 Wks)", "2026-11-25", "2026-12-04")
]
for s in stories_timeline: ws9.append(list(s))
style_sheet(ws9, ws9.title)
wb9.save(os.path.join(EXCEL_DIR, "P09_Jira_Backlog.xlsx"))

# Copy to evidence folder
shutil.copy2(os.path.join(EXCEL_DIR, "P09_Jira_Backlog.xlsx"), os.path.join(BASE_DIR, "evidence", "P09_Jira", "P09_Jira_Backlog.xlsx"))
shutil.copy2(os.path.join(EXCEL_DIR, "P10_Sprint_Metrics.xlsx"), os.path.join(BASE_DIR, "evidence", "P10_ScrumMetrics", "P10_Sprint_Metrics.xlsx"))

print("Updated 4-week Sprint metrics and Jira backlog timeline tables!")
