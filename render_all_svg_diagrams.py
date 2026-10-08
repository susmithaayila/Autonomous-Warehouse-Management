import os
import shutil

BASE_DIR = r"C:\Users\ayila\.gemini\antigravity-ide\scratch\AWMS"
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence")

def create_svg(filename, title, svg_elements, width=1000, height=700):
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .title {{ font-family: system-ui, sans-serif; font-size: 20px; font-weight: bold; fill: #1e3a8a; text-anchor: middle; }}
    .sub {{ font-family: system-ui, sans-serif; font-size: 12px; fill: #64748b; text-anchor: middle; }}
    .box-blue {{ fill: #dbeafe; stroke: #2563eb; stroke-width: 2; rx: 8; ry: 8; }}
    .box-amber {{ fill: #fef3c7; stroke: #d97706; stroke-width: 2; rx: 8; ry: 8; }}
    .box-rose {{ fill: #fee2e2; stroke: #dc2626; stroke-width: 2; rx: 8; ry: 8; }}
    .box-green {{ fill: #dcfce7; stroke: #16a34a; stroke-width: 2; rx: 8; ry: 8; }}
    .box-purple {{ fill: #f3e8ff; stroke: #7c3aed; stroke-width: 2; rx: 8; ry: 8; }}
    .box-slate {{ fill: #f8fafc; stroke: #475569; stroke-width: 2; rx: 8; ry: 8; }}
    .label {{ font-family: system-ui, sans-serif; font-size: 13px; font-weight: 600; fill: #0f172a; text-anchor: middle; }}
    .label-sm {{ font-family: system-ui, sans-serif; font-size: 11px; fill: #334155; text-anchor: middle; }}
    .line {{ stroke: #475569; stroke-width: 2; marker-end: url(#arrow); }}
    .actor {{ fill: #e2e8f0; stroke: #334155; stroke-width: 2; }}
  </style>

  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="{width/2}" y="35" class="title">{title}</text>
  
  {svg_elements}
</svg>"""
    filepath = os.path.join(DIAGRAMS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Created SVG: {filename}")

# 1. P03_Use_Case_Diagram.svg
uc_svg = """
<rect x="220" y="60" width="560" height="600" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" rx="12" />
<text x="500" y="85" class="label" fill="#475569">AWMS Boundary</text>

<!-- Actors -->
<circle cx="100" cy="180" r="20" class="actor" />
<path d="M 100 200 L 100 250 M 70 220 L 130 220 M 100 250 L 75 300 M 100 250 L 125 300" class="line" />
<text x="100" y="320" class="label">Customer</text>

<circle cx="100" cy="420" r="20" class="actor" />
<path d="M 100 440 L 100 490 M 70 460 L 130 460 M 100 490 L 75 540 M 100 490 L 125 540" class="line" />
<text x="100" y="560" class="label">Warehouse Admin</text>

<circle cx="900" cy="300" r="20" class="actor" />
<path d="M 900 320 L 900 370 M 870 340 L 930 340 M 900 370 L 875 420 M 900 370 L 925 420" class="line" />
<text x="900" y="440" class="label">Autonomous AGV</text>

<!-- Use Cases -->
<ellipse cx="360" cy="150" rx="100" ry="30" class="box-blue" />
<text x="360" y="155" class="label">UC-01: Create Order</text>

<ellipse cx="360" cy="260" rx="100" ry="30" class="box-blue" />
<text x="360" y="265" class="label">View &amp; Adjust Inventory</text>

<ellipse cx="360" cy="370" rx="100" ry="30" class="box-amber" />
<text x="360" y="375" class="label">UC-02: Issue Robot Cmd</text>

<ellipse cx="360" cy="480" rx="100" ry="30" class="box-rose" />
<text x="360" y="485" class="label">Assign User Roles (RBAC)</text>

<ellipse cx="640" cy="370" rx="110" ry="35" class="box-purple" />
<text x="640" y="370" class="label">HMAC &amp; Nonce Auth</text>
<text x="640" y="388" class="label-sm">&lt;&lt;include&gt;&gt;</text>

<!-- Connector lines -->
<line x1="130" y1="220" x2="260" y2="150" class="line" />
<line x1="130" y1="460" x2="260" y2="370" class="line" />
<line x1="130" y1="460" x2="260" y2="480" class="line" />
<line x1="460" y1="370" x2="530" y2="370" class="line" />
<line x1="750" y1="370" x2="870" y2="340" class="line" />
"""
create_svg("P03_Use_Case_Diagram.svg", "AWMS Use Case Diagram", uc_svg)

# 2. P03_Analysis_Model.svg
an_svg = """
<rect x="50" y="100" width="200" height="60" class="box-blue" />
<text x="150" y="135" class="label">1. Customer Order Placed</text>

<line x1="250" y1="130" x2="330" y2="130" class="line" />

<rect x="330" y="100" width="240" height="60" class="box-blue" />
<text x="450" y="135" class="label">2. Verify Stock &amp; Reserve Qty</text>

<line x1="570" y1="130" x2="650" y2="130" class="line" />

<rect x="650" y="100" width="250" height="60" class="box-blue" />
<text x="775" y="135" class="label">3. Create Task (PICK/MOVE/DROP)</text>

<line x1="775" y1="160" x2="775" y2="240" class="line" />

<rect x="650" y="240" width="250" height="60" class="box-amber" />
<text x="775" y="275" class="label">4. Assign Available AGV (IDLE)</text>

<line x1="650" y1="270" x2="570" y2="270" class="line" />

<rect x="330" y="240" width="240" height="60" class="box-amber" />
<text x="450" y="275" class="label">5. Issue HMAC Signed Command</text>

<line x1="330" y1="270" x2="250" y2="270" class="line" />

<rect x="50" y="240" width="200" height="60" class="box-rose" />
<text x="150" y="265" class="label">6. Verify HMAC &amp; Nonce</text>
<text x="150" y="285" class="label-sm">(Replay Protection)</text>

<line x1="150" y1="300" x2="150" y2="380" class="line" />

<rect x="50" y="380" width="200" height="60" class="box-green" />
<text x="150" y="415" class="label">7. Move Item to Packing Zone</text>

<line x1="250" y1="410" x2="330" y2="410" class="line" />

<rect x="330" y="380" width="280" height="60" class="box-green" />
<text x="470" y="415" class="label">8. Order Status: FULFILLED</text>
"""
create_svg("P03_Analysis_Model.svg", "AWMS Warehouse Fulfillment Scenario Analysis Model", an_svg)

# 3. P04_ER_Diagram.svg
er_svg = """
<!-- Entities -->
<g transform="translate(60, 100)">
  <rect width="200" height="150" class="box-slate" />
  <rect width="200" height="30" fill="#334155" rx="8" ry="8" />
  <text x="100" y="20" fill="#fff" class="label">User</text>
  <text x="15" y="50" class="label-sm" text-anchor="start">+ id (PK)</text>
  <text x="15" y="70" class="label-sm" text-anchor="start">+ username</text>
  <text x="15" y="90" class="label-sm" text-anchor="start">+ hashed_password</text>
  <text x="15" y="110" class="label-sm" text-anchor="start">+ role_id (FK)</text>
  <text x="15" y="130" class="label-sm" text-anchor="start">+ is_active</text>
</g>

<g transform="translate(60, 320)">
  <rect width="200" height="100" class="box-slate" />
  <rect width="200" height="30" fill="#334155" rx="8" ry="8" />
  <text x="100" y="20" fill="#fff" class="label">Role</text>
  <text x="15" y="50" class="label-sm" text-anchor="start">+ id (PK)</text>
  <text x="15" y="70" class="label-sm" text-anchor="start">+ name</text>
  <text x="15" y="90" class="label-sm" text-anchor="start">+ description</text>
</g>

<g transform="translate(400, 100)">
  <rect width="200" height="150" class="box-slate" />
  <rect width="200" height="30" fill="#334155" rx="8" ry="8" />
  <text x="100" y="20" fill="#fff" class="label">InventoryItem</text>
  <text x="15" y="50" class="label-sm" text-anchor="start">+ id (PK)</text>
  <text x="15" y="70" class="label-sm" text-anchor="start">+ sku</text>
  <text x="15" y="90" class="label-sm" text-anchor="start">+ name</text>
  <text x="15" y="110" class="label-sm" text-anchor="start">+ quantity</text>
  <text x="15" y="130" class="label-sm" text-anchor="start">+ reserved_quantity</text>
</g>

<g transform="translate(740, 100)">
  <rect width="200" height="150" class="box-slate" />
  <rect width="200" height="30" fill="#334155" rx="8" ry="8" />
  <text x="100" y="20" fill="#fff" class="label">Robot (AGV)</text>
  <text x="15" y="50" class="label-sm" text-anchor="start">+ id (PK)</text>
  <text x="15" y="70" class="label-sm" text-anchor="start">+ robot_code</text>
  <text x="15" y="90" class="label-sm" text-anchor="start">+ name</text>
  <text x="15" y="110" class="label-sm" text-anchor="start">+ status</text>
  <text x="15" y="130" class="label-sm" text-anchor="start">+ secret_key</text>
</g>

<g transform="translate(400, 320)">
  <rect width="200" height="150" class="box-slate" />
  <rect width="200" height="30" fill="#334155" rx="8" ry="8" />
  <text x="100" y="20" fill="#fff" class="label">WarehouseTask</text>
  <text x="15" y="50" class="label-sm" text-anchor="start">+ id (PK)</text>
  <text x="15" y="70" class="label-sm" text-anchor="start">+ task_code</text>
  <text x="15" y="90" class="label-sm" text-anchor="start">+ order_id (FK)</text>
  <text x="15" y="110" class="label-sm" text-anchor="start">+ item_id (FK)</text>
  <text x="15" y="130" class="label-sm" text-anchor="start">+ assigned_robot_id (FK)</text>
</g>

<line x1="160" y1="250" x2="160" y2="320" class="line" />
<line x1="500" y1="250" x2="500" y2="320" class="line" />
<line x1="740" y1="175" x2="600" y2="395" class="line" />
"""
create_svg("P04_ER_Diagram.svg", "AWMS Entity Relationship Diagram (ERD)", er_svg)

# 4. P04_DFD_Level_0.svg
dfd0_svg = """
<rect x="80" y="200" width="180" height="80" class="box-slate" />
<text x="170" y="245" class="label">Customer / Operator / Admin</text>

<circle cx="500" cy="240" r="100" class="box-blue" />
<text x="500" y="235" class="label">0.0 AWMS Core System</text>
<text x="500" y="255" class="label-sm">(Autonomous Warehouse Mgt)</text>

<rect x="740" y="200" width="180" height="80" class="box-slate" />
<text x="830" y="245" class="label">Autonomous Robot (AGV)</text>

<line x1="260" y1="220" x2="400" y2="220" class="line" />
<text x="330" y="210" class="label-sm">Orders &amp; Commands</text>

<line x1="400" y1="260" x2="260" y2="260" class="line" />
<text x="330" y="280" class="label-sm">Status &amp; Inventory Data</text>

<line x1="600" y1="220" x2="740" y2="220" class="line" />
<text x="670" y="210" class="label-sm">HMAC Signed Cmd</text>

<line x1="740" y1="260" x2="600" y2="260" class="line" />
<text x="670" y="280" class="label-sm">Robot Heartbeat/Status</text>
"""
create_svg("P04_DFD_Level_0.svg", "AWMS Context Level-0 Data Flow Diagram", dfd0_svg)

# 5. P04_DFD_Level_1.svg
dfd1_svg = """
<!-- Trust Boundaries -->
<rect x="40" y="80" width="220" height="540" fill="#eff6ff" stroke="#93c5fd" stroke-dasharray="6,6" rx="8" />
<text x="150" y="110" class="label" fill="#1e40af">User Zone (External)</text>

<rect x="300" y="80" width="400" height="540" fill="#f0fdf4" stroke="#86efac" stroke-dasharray="6,6" rx="8" />
<text x="500" y="110" class="label" fill="#166534">Application Zone (AWMS Backend)</text>

<rect x="740" y="80" width="220" height="540" fill="#fffbeb" stroke="#fde047" stroke-dasharray="6,6" rx="8" />
<text x="850" y="110" class="label" fill="#854d0e">Robot OT Zone</text>

<!-- Processes inside App Zone -->
<circle cx="400" cy="180" r="45" class="box-blue" />
<text x="400" y="185" class="label-sm">1.0 Auth Service</text>

<circle cx="600" cy="180" r="45" class="box-blue" />
<text x="600" y="185" class="label-sm">2.0 Inventory Mgt</text>

<circle cx="400" cy="340" r="45" class="box-blue" />
<text x="400" y="345" class="label-sm">3.0 Order Fulfillment</text>

<circle cx="600" cy="340" r="45" class="box-amber" />
<text x="600" y="345" class="label-sm">4.0 Cmd Auth</text>

<circle cx="500" cy="500" r="45" class="box-purple" />
<text x="500" y="505" class="label-sm">5.0 Security Audit</text>
"""
create_svg("P04_DFD_Level_1.svg", "AWMS Level-1 DFD with Trust Boundaries", dfd1_svg)

# 6. P05_Architecture.svg
arch_svg = """
<rect x="100" y="90" width="800" height="60" class="box-blue" />
<text x="500" y="125" class="label">Presentation Layer (Single Page Web Application UI)</text>

<rect x="100" y="180" width="800" height="60" class="box-rose" />
<text x="500" y="215" class="label">Authentication &amp; RBAC Authorization Middleware (JWT + Role Checking)</text>

<rect x="100" y="270" width="800" height="80" class="box-amber" />
<text x="500" y="305" class="label">Business Services Layer</text>
<text x="500" y="330" class="label-sm">(AuthService, InventoryService, RobotService, TaskService, CommandAuthorizationService)</text>

<rect x="100" y="380" width="800" height="60" class="box-green" />
<text x="500" y="415" class="label">Data Access Layer (SQLAlchemy ORM + ACID Concurrency Locks with_for_update)</text>

<path d="M 400 480 C 400 460 600 460 600 480 L 600 550 C 600 570 400 570 400 550 Z" class="box-slate" />
<text x="500" y="520" class="label">Database (SQLite)</text>

<line x1="500" y1="150" x2="500" y2="180" class="line" />
<line x1="500" y1="240" x2="500" y2="270" class="line" />
<line x1="500" y1="350" x2="500" y2="380" class="line" />
<line x1="500" y1="440" x2="500" y2="470" class="line" />
"""
create_svg("P05_Architecture.svg", "AWMS Secure Layered Architecture", arch_svg)

# 7. P07_STRIDE_DFD.svg
stride_svg = """
<rect x="100" y="100" width="220" height="60" class="box-rose" />
<text x="210" y="125" class="label">[T-01] Robot Identity Spoofing</text>
<text x="210" y="145" class="label-sm">Mitigation: HMAC-SHA256 Secret</text>

<rect x="390" y="100" width="220" height="60" class="box-rose" />
<text x="500" y="125" class="label">[T-02] Inventory Tampering</text>
<text x="500" y="145" class="label-sm">Mitigation: Row Locking &amp; RBAC</text>

<rect x="680" y="100" width="220" height="60" class="box-rose" />
<text x="790" y="125" class="label">[T-07] Replay Command Attack</text>
<text x="790" y="145" class="label-sm">Mitigation: Nonce Verification</text>

<rect x="100" y="240" width="220" height="60" class="box-rose" />
<text x="210" y="265" class="label">[T-06] Privilege Escalation</text>
<text x="210" y="285" class="label-sm">Mitigation: Self-Role Block</text>

<rect x="390" y="240" width="220" height="60" class="box-rose" />
<text x="500" y="265" class="label">[T-09] Command Conflict</text>
<text x="500" y="285" class="label-sm">Mitigation: State Machine Check</text>

<rect x="680" y="240" width="220" height="60" class="box-rose" />
<text x="790" y="265" class="label">[T-10] Audit Log Tampering</text>
<text x="790" y="285" class="label-sm">Mitigation: Append-only Stream</text>
"""
create_svg("P07_STRIDE_DFD.svg", "AWMS STRIDE Threat Model Diagram", stride_svg)

# 8. P08_Attack_Tree.svg
at_svg = """
<rect x="300" y="80" width="400" height="60" fill="#990000" stroke="#660000" rx="8" ry="8" />
<text x="500" y="115" class="label" fill="#ffffff">ROOT GOAL: Unauthorized Robot Operation</text>

<ellipse cx="500" cy="180" rx="25" ry="20" class="box-amber" />
<text x="500" y="185" class="label">OR</text>

<g transform="translate(40, 240)">
  <rect width="200" height="60" class="box-rose" />
  <text x="100" y="35" class="label">Compromise User Account</text>
  <rect y="90" width="200" height="50" class="box-green" />
  <text x="100" y="120" class="label-sm">Control: Bcrypt + Lockout</text>
</g>

<g transform="translate(280, 240)">
  <rect width="200" height="60" class="box-rose" />
  <text x="100" y="35" class="label">Spoof Robot Identity</text>
  <rect y="90" width="200" height="50" class="box-green" />
  <text x="100" y="120" class="label-sm">Control: HMAC-SHA256</text>
</g>

<g transform="translate(520, 240)">
  <rect width="200" height="60" class="box-rose" />
  <text x="100" y="35" class="label">Replay Past Command</text>
  <rect y="90" width="200" height="50" class="box-green" />
  <text x="100" y="120" class="label-sm">Control: UUID Nonce Check</text>
</g>

<g transform="translate(760, 240)">
  <rect width="200" height="60" class="box-rose" />
  <text x="100" y="35" class="label">Exploit Race Condition</text>
  <rect y="90" width="200" height="50" class="box-green" />
  <text x="100" y="120" class="label-sm">Control: Row Locking</text>
</g>

<line x1="500" y1="140" x2="500" y2="160" class="line" />
<line x1="500" y1="200" x2="140" y2="240" class="line" />
<line x1="500" y1="200" x2="380" y2="240" class="line" />
<line x1="500" y1="200" x2="620" y2="240" class="line" />
<line x1="500" y1="200" x2="860" y2="240" class="line" />
"""
create_svg("P08_Attack_Tree.svg", "AWMS Security Attack Tree Diagram", at_svg)

# 9. P08_Security_Refined_Architecture.svg
ref_svg = """
<rect x="100" y="100" width="800" height="90" class="box-rose" />
<text x="500" y="135" class="label">Security Protection Shield</text>
<text x="500" y="160" class="label-sm">(HMAC Verification Engine + UUID Nonce Anti-Replay + Immutable Audit Stream)</text>

<line x1="500" y1="190" x2="500" y2="250" class="line" />

<rect x="100" y="250" width="800" height="90" class="box-blue" />
<text x="500" y="285" class="label">AWMS Core Application Engine</text>
<text x="500" y="310" class="label-sm">(ACID Concurrency Locking + RBAC Authorization + Fulfillment Pipeline)</text>
"""
create_svg("P08_Security_Refined_Architecture.svg", "AWMS Security Refined Architecture", ref_svg)

# Copy all SVGs to corresponding evidence folders
for svg_file in os.listdir(DIAGRAMS_DIR):
    if svg_file.endswith(".svg"):
        s_src = os.path.join(DIAGRAMS_DIR, svg_file)
        if "P03" in svg_file:
            shutil.copy2(s_src, os.path.join(EVIDENCE_DIR, "P03_UML", svg_file))
        elif "P04" in svg_file:
            shutil.copy2(s_src, os.path.join(EVIDENCE_DIR, "P04_DataFlow", svg_file))
        elif "P05" in svg_file:
            shutil.copy2(s_src, os.path.join(EVIDENCE_DIR, "P05_Architecture", svg_file))
        elif "P07" in svg_file:
            shutil.copy2(s_src, os.path.join(EVIDENCE_DIR, "P07_ThreatModel", svg_file))
        elif "P08" in svg_file:
            shutil.copy2(s_src, os.path.join(EVIDENCE_DIR, "P08_AttackTree", svg_file))

print("Rendered all 9 vector SVG diagrams successfully!")
