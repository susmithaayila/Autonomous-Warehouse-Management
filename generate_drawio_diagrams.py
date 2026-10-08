import os
import xml.etree.ElementTree as ET

DIAGRAMS_DIR = r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS\diagrams"
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def create_drawio_file(filename, diagram_title, xml_body):
    content = f"""<mxfile host="app.diagrams.net" modified="2026-10-08T10:00:00.000Z" agent="Antigravity IDE" version="21.0.0" type="device">
  <diagram id="{filename.replace('.', '_')}" name="{diagram_title}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {xml_body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    filepath = os.path.join(DIAGRAMS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename}")

# 1. P03_Use_Case_Diagram.drawio
uc_body = """
<mxCell id="title" value="AWMS - Secure Use Case Diagram" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="400" y="20" width="360" height="40" as="geometry" />
</mxCell>

<!-- System Boundary -->
<mxCell id="boundary" value="Autonomous Warehouse Management System (AWMS)" style="shape=swimlane;whiteSpace=wrap;html=1;startSize=30;fontSize=14;fontStyle=1;fillColor=#f8fafc;strokeColor=#64748b;" vertex="1" parent="1">
  <mxGeometry x="250" y="80" width="660" height="680" as="geometry" />
</mxCell>

<!-- Actors -->
<mxCell id="actor_customer" value="Customer" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#e2e8f0;strokeColor=#334155;" vertex="1" parent="1">
  <mxGeometry x="80" y="140" width="40" height="80" as="geometry" />
</mxCell>
<mxCell id="actor_operator" value="Warehouse Operator" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#e2e8f0;strokeColor=#334155;" vertex="1" parent="1">
  <mxGeometry x="80" y="320" width="40" height="80" as="geometry" />
</mxCell>
<mxCell id="actor_admin" value="Warehouse Admin" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#e2e8f0;strokeColor=#334155;" vertex="1" parent="1">
  <mxGeometry x="80" y="520" width="40" height="80" as="geometry" />
</mxCell>

<mxCell id="actor_auditor" value="Security Auditor" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#e2e8f0;strokeColor=#334155;" vertex="1" parent="1">
  <mxGeometry x="960" y="200" width="40" height="80" as="geometry" />
</mxCell>
<mxCell id="actor_robot" value="Autonomous Robot" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#e2e8f0;strokeColor=#334155;" vertex="1" parent="1">
  <mxGeometry x="960" y="450" width="40" height="80" as="geometry" />
</mxCell>

<!-- Use Cases inside boundary -->
<mxCell id="uc_login" value="UC-00: Authenticate &amp; Login" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;" vertex="1" parent="boundary">
  <mxGeometry x="220" y="40" width="200" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_order" value="UC-01: Create &amp; Track Order" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="boundary">
  <mxGeometry x="50" y="100" width="200" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_inv_view" value="View Inventory" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#475569;" vertex="1" parent="boundary">
  <mxGeometry x="50" y="180" width="180" height="45" as="geometry" />
</mxCell>
<mxCell id="uc_inv_update" value="Manage Inventory (ACID Update)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#475569;" vertex="1" parent="boundary">
  <mxGeometry x="50" y="250" width="220" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_task_assign" value="Assign Robot to Task" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#475569;" vertex="1" parent="boundary">
  <mxGeometry x="50" y="330" width="200" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_robot_cmd" value="UC-02: Issue &amp; Execute Robot Cmd" style="ellipse;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;fontStyle=1;" vertex="1" parent="boundary">
  <mxGeometry x="380" y="360" width="240" height="60" as="geometry" />
</mxCell>
<mxCell id="uc_robot_reg" value="Register Autonomous Robot" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#475569;" vertex="1" parent="boundary">
  <mxGeometry x="50" y="420" width="210" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_role_assign" value="Assign User Roles (RBAC)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="boundary">
  <mxGeometry x="50" y="500" width="210" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_audit" value="View Security Audit Logs" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#7c3aed;" vertex="1" parent="boundary">
  <mxGeometry x="380" y="160" width="210" height="50" as="geometry" />
</mxCell>
<mxCell id="uc_monitor" value="Monitor Security Metrics" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#7c3aed;" vertex="1" parent="boundary">
  <mxGeometry x="380" y="240" width="210" height="50" as="geometry" />
</mxCell>
"""
create_drawio_file("P03_Use_Case_Diagram.drawio", "AWMS Use Case Diagram", uc_body)

# 2. P03_Analysis_Model.drawio
analysis_body = """
<mxCell id="title" value="AWMS - Scenario-Based Analysis Model (Warehouse Fulfillment)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="350" y="20" width="460" height="40" as="geometry" />
</mxCell>

<mxCell id="s1" value="1. Customer Places Order" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="60" as="geometry" />
</mxCell>
<mxCell id="s2" value="2. System Verifies Stock &amp; Reserves Qty" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="1">
  <mxGeometry x="360" y="100" width="240" height="60" as="geometry" />
</mxCell>
<mxCell id="s3" value="3. Create Warehouse Task (PICK/MOVE/DROP)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="1">
  <mxGeometry x="660" y="100" width="250" height="60" as="geometry" />
</mxCell>
<mxCell id="s4" value="4. Assign Available Robot (IDLE check)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="660" y="240" width="250" height="60" as="geometry" />
</mxCell>
<mxCell id="s5" value="5. Issue HMAC Signed Robot Command" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;" vertex="1" parent="1">
  <mxGeometry x="360" y="240" width="240" height="60" as="geometry" />
</mxCell>
<mxCell id="s6" value="6. Robot Verifies HMAC &amp; Nonce Anti-Replay" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="240" width="210" height="60" as="geometry" />
</mxCell>
<mxCell id="s7" value="7. Robot Moves Item to Packing Area" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;" vertex="1" parent="1">
  <mxGeometry x="100" y="380" width="210" height="60" as="geometry" />
</mxCell>
<mxCell id="s8" value="8. Task Completed &amp; Order Status Set to FULFILLED" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="360" y="380" width="280" height="60" as="geometry" />
</mxCell>
"""
create_drawio_file("P03_Analysis_Model.drawio", "AWMS Analysis Model", analysis_body)

# 3. P04_ER_Diagram.drawio
er_body = """
<mxCell id="title" value="AWMS - Entity Relationship Diagram (ERD)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="400" y="20" width="400" height="40" as="geometry" />
</mxCell>

<mxCell id="ent_user" value="User&#10;--&#10;+ id (PK)&#10;+ username&#10;+ hashed_password&#10;+ role_id (FK)&#10;+ is_active" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="80" y="100" width="180" height="130" as="geometry" />
</mxCell>
<mxCell id="ent_role" value="Role&#10;--&#10;+ id (PK)&#10;+ name&#10;+ description" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="80" y="300" width="180" height="90" as="geometry" />
</mxCell>
<mxCell id="ent_robot" value="Robot&#10;--&#10;+ id (PK)&#10;+ robot_code&#10;+ name&#10;+ status&#10;+ battery_level&#10;+ secret_key" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="780" y="100" width="180" height="140" as="geometry" />
</mxCell>
<mxCell id="ent_inv" value="InventoryItem&#10;--&#10;+ id (PK)&#10;+ sku&#10;+ name&#10;+ location&#10;+ quantity&#10;+ reserved_qty" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="430" y="100" width="180" height="140" as="geometry" />
</mxCell>
<mxCell id="ent_order" value="CustomerOrder&#10;--&#10;+ id (PK)&#10;+ order_number&#10;+ customer_id (FK)&#10;+ status&#10;+ created_at" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="80" y="460" width="180" height="120" as="geometry" />
</mxCell>
<mxCell id="ent_task" value="WarehouseTask&#10;--&#10;+ id (PK)&#10;+ task_code&#10;+ order_id (FK)&#10;+ item_id (FK)&#10;+ assigned_robot_id (FK)&#10;+ status" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="430" y="460" width="220" height="140" as="geometry" />
</mxCell>
<mxCell id="ent_cmd" value="RobotCommand&#10;--&#10;+ id (PK)&#10;+ command_id&#10;+ task_id (FK)&#10;+ robot_id (FK)&#10;+ nonce&#10;+ signature" style="shape=table;childLayout=tableLayout;collapsible=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#475569;" vertex="1" parent="1">
  <mxGeometry x="780" y="460" width="190" height="140" as="geometry" />
</mxCell>
"""
create_drawio_file("P04_ER_Diagram.drawio", "AWMS ER Diagram", er_body)

# 4. P04_DFD_Level_0.drawio
dfd0_body = """
<mxCell id="title" value="AWMS - Level 0 Context Data Flow Diagram" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="380" y="20" width="420" height="40" as="geometry" />
</mxCell>

<mxCell id="ext_user" value="Customer / Operator / Admin" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e2e8f0;strokeColor=#334155;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="80" y="240" width="180" height="80" as="geometry" />
</mxCell>
<mxCell id="proc_awms" value="0.0&#10;Autonomous Warehouse&#10;Management System&#10;(AWMS Core)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="440" y="200" width="240" height="160" as="geometry" />
</mxCell>
<mxCell id="ext_robot" value="Autonomous Robot (AGV)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e2e8f0;strokeColor=#334155;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="860" y="240" width="180" height="80" as="geometry" />
</mxCell>
"""
create_drawio_file("P04_DFD_Level_0.drawio", "AWMS DFD Level 0", dfd0_body)

# 5. P04_DFD_Level_1.drawio
dfd1_body = """
<mxCell id="title" value="AWMS - Level 1 DFD with Trust Boundaries" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="400" y="20" width="400" height="40" as="geometry" />
</mxCell>

<!-- Trust Zones -->
<mxCell id="tz_user" value="External / User Zone" style="swimlane;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#93c5fd;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="80" width="220" height="660" as="geometry" />
</mxCell>
<mxCell id="tz_app" value="Application Zone" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f0fdf4;strokeColor=#86efac;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="300" y="80" width="540" height="660" as="geometry" />
</mxCell>
<mxCell id="tz_robot" value="Robot / OT Zone" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#fde047;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="880" y="80" width="220" height="660" as="geometry" />
</mxCell>

<!-- DFD Processes inside App Zone -->
<mxCell id="p1" value="1.0 Auth Service" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="tz_app">
  <mxGeometry x="40" y="60" width="160" height="70" as="geometry" />
</mxCell>
<mxCell id="p2" value="2.0 Inventory Mgt" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="tz_app">
  <mxGeometry x="40" y="180" width="160" height="70" as="geometry" />
</mxCell>
<mxCell id="p3" value="3.0 Order Fulfillment" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="tz_app">
  <mxGeometry x="40" y="300" width="160" height="70" as="geometry" />
</mxCell>
<mxCell id="p4" value="4.0 Task Allocation" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;" vertex="1" parent="tz_app">
  <mxGeometry x="320" y="300" width="160" height="70" as="geometry" />
</mxCell>
<mxCell id="p5" value="5.0 Robot Command Auth" style="ellipse;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;fontStyle=1;" vertex="1" parent="tz_app">
  <mxGeometry x="320" y="440" width="180" height="80" as="geometry" />
</mxCell>
<mxCell id="p6" value="6.0 Security Audit Stream" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#7c3aed;" vertex="1" parent="tz_app">
  <mxGeometry x="40" y="540" width="180" height="70" as="geometry" />
</mxCell>
"""
create_drawio_file("P04_DFD_Level_1.drawio", "AWMS DFD Level 1", dfd1_body)

# 6. P05_Architecture.drawio
arch_body = """
<mxCell id="title" value="AWMS - Secure Layered Architecture" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="400" y="20" width="380" height="40" as="geometry" />
</mxCell>

<mxCell id="l_ui" value="Presentation Layer (Single Page Web App UI / REST API Client)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="150" y="100" width="860" height="60" as="geometry" />
</mxCell>
<mxCell id="l_sec" value="Authentication &amp; RBAC Authorization Middleware (JWT + Security Dependencies)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="150" y="200" width="860" height="60" as="geometry" />
</mxCell>
<mxCell id="l_svc" value="Business Services Layer (AuthService, InventoryService, RobotService, TaskService, CommandAuthService)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="150" y="300" width="860" height="80" as="geometry" />
</mxCell>
<mxCell id="l_data" value="Data Access &amp; Repository Layer (SQLAlchemy ORM + ACID Concurrency Locking)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f0fdf4;strokeColor=#16a34a;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="150" y="420" width="860" height="60" as="geometry" />
</mxCell>
<mxCell id="l_db" value="Database Layer (SQLite DB / Persistent Storage)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e2e8f0;strokeColor=#334155;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="480" y="520" width="200" height="100" as="geometry" />
</mxCell>
"""
create_drawio_file("P05_Architecture.drawio", "AWMS Architecture", arch_body)

# 7. P07_STRIDE_DFD.drawio
stride_body = """
<mxCell id="title" value="AWMS - STRIDE Threat Model Data Flow Diagram" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="380" y="20" width="420" height="40" as="geometry" />
</mxCell>

<mxCell id="t1" value="[T-01] Spoofing Robot ID&#10;(Mitigation: HMAC-SHA256)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="100" y="120" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="t2" value="[T-02] Inventory Tampering&#10;(Mitigation: Row Locking)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="400" y="120" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="t3" value="[T-07] Replay Command Attack&#10;(Mitigation: Nonce Tracking)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="700" y="120" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="t4" value="[T-06] Privilege Escalation&#10;(Mitigation: Server RBAC)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="100" y="240" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="t5" value="[T-09] Robot Command Conflict&#10;(Mitigation: State Machine Check)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="400" y="240" width="240" height="60" as="geometry" />
</mxCell>
"""
create_drawio_file("P07_STRIDE_DFD.drawio", "AWMS STRIDE DFD", stride_body)

# 8. P08_Attack_Tree.drawio
attack_body = """
<mxCell id="title" value="AWMS - Security Attack Tree Diagram" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="400" y="20" width="380" height="40" as="geometry" />
</mxCell>

<mxCell id="root" value="ROOT GOAL:&#10;Unauthorized Robot Operation &amp; Warehouse Movement" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#990000;strokeColor=#660000;fontColor=#ffffff;fontStyle=1;fontSize=14;" vertex="1" parent="1">
  <mxGeometry x="380" y="80" width="400" height="70" as="geometry" />
</mxCell>

<!-- OR Gate -->
<mxCell id="or1" value="OR" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffcc00;strokeColor=#b8860b;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="555" y="180" width="50" height="40" as="geometry" />
</mxCell>

<!-- Branches -->
<mxCell id="b1" value="Compromise User Account&#10;(Brute-Force / Credential Theft)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="60" y="270" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="b2" value="Spoof Robot Identity&#10;(Shared Secret / Token Theft)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="310" y="270" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="b3" value="Replay Past Command&#10;(Network Eavesdropping)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="560" y="270" width="220" height="60" as="geometry" />
</mxCell>
<mxCell id="b4" value="Exploit Concurrency Race&#10;(Simultaneous API Flooding)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;" vertex="1" parent="1">
  <mxGeometry x="810" y="270" width="220" height="60" as="geometry" />
</mxCell>

<!-- Controls -->
<mxCell id="c1" value="Control: Bcrypt Hashing + Account Lockout" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="60" y="380" width="220" height="50" as="geometry" />
</mxCell>
<mxCell id="c2" value="Control: HMAC-SHA256 Secret Signing" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="310" y="380" width="220" height="50" as="geometry" />
</mxCell>
<mxCell id="c3" value="Control: UUID Nonce &amp; Anti-Replay Check" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="560" y="380" width="220" height="50" as="geometry" />
</mxCell>
<mxCell id="c4" value="Control: SQLAlchemy row locking with_for_update()" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="810" y="380" width="240" height="50" as="geometry" />
</mxCell>
"""
create_drawio_file("P08_Attack_Tree.drawio", "AWMS Attack Tree", attack_body)

# 9. P08_Security_Refined_Architecture.drawio
refined_body = """
<mxCell id="title" value="AWMS - Security Refined Architecture (Post Attack Tree Analysis)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="350" y="20" width="460" height="40" as="geometry" />
</mxCell>

<mxCell id="sec_layer" value="Refined Security Shield: Nonce Verification + HMAC Signature Engine + Audit Stream" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#dc2626;fontStyle=1;fontSize=13;" vertex="1" parent="1">
  <mxGeometry x="150" y="100" width="860" height="80" as="geometry" />
</mxCell>
<mxCell id="core_app" value="AWMS Core Application Engine (ACID Transaction Isolation &amp; Concurrency Locks)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="150" y="230" width="860" height="80" as="geometry" />
</mxCell>
"""
create_drawio_file("P08_Security_Refined_Architecture.drawio", "AWMS Refined Architecture", refined_body)

print("All 9 Draw.io diagram files created successfully in diagrams/ folder!")
