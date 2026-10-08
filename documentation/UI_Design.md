# Phase 06: User Interface Design & Rationale Report
## Course: 24CYS401 – Secure Software Engineering
**Project:** Autonomous Warehouse Management System (AWMS)

---

### 1. Examination Requirement Mapping Matrix
The university examination template rubric maps directly to the AWMS Domain equivalent screens:

| Generic Exam Rubric Term | AWMS Domain Equivalent Screen | Target User Role | Primary Goal |
| :--- | :--- | :--- | :--- |
| **1. Login Screen** | **Secure AWMS Login Modal** | All Users (Admin, Operator, Customer, Auditor) | Authenticate user via JWT, enforce password security, prevent brute-force login. |
| **2. Student Exam Screen (Task Execution)** | **Robot Task Management & Fulfillment Screen** | Robot / Operator / Customer | Execute pickup/drop tasks, issue HMAC signed commands, monitor fulfillment progress. |
| **3. Faculty Examination Management** | **Warehouse & Robot Management Dashboard** | Warehouse Administrator / Operator | Register autonomous AGVs, manage inventory stock, allocate tasks, manage user roles (RBAC). |
| **4. Examination Results** | **Order Fulfillment Status & Security Audit Stream** | Customer / Security Auditor | View completed order status, track item delivery, inspect security events & metrics. |

---

### 2. Detailed Screen Specifications & Security Analysis

#### Screen 1: Secure Login Screen
- **User:** All Users (Customer, Operator, Admin, Auditor).
- **Goal:** Authenticate identity using username and password.
- **Navigation:** Modal popup accessible from top navigation bar.
- **Inputs:** Username (text), Password (masked password).
- **Feedback:** Real-time toast notifications for success/failure, demo account quick-fill buttons.
- **Error Handling:** Invalid credentials return generic "Invalid username or password" (prevents username enumeration). 5 failed attempts trigger account lockout.
- **Security Considerations:** Bcrypt hashed password check, JWT token issuance, HTTPBearer auth header.

#### Screen 2: Robot Task Management & Fulfillment Screen (Examination Equivalent)
- **User:** Operator, Robot, Customer.
- **Goal:** Execute item picking, moving, and dropping to fulfill customer orders.
- **Navigation:** "⚡ Tasks & Commands" tab in top nav bar.
- **Inputs:** Task ID, Robot ID, Command Type (PICK, MOVE, DROP), Nonce.
- **Feedback:** Real-time status badges (`PENDING`, `ASSIGNED`, `PICKING`, `MOVING`, `COMPLETED`).
- **Error Handling:** Rejects unassigned task execution, blocks command conflicts on busy robots (409 Conflict).
- **Security Considerations:** HMAC-SHA256 signature verification, UUID Nonce anti-replay protection.

#### Screen 3: Warehouse & Robot Management Screen (Faculty Equivalent)
- **User:** Warehouse Administrator / Operator.
- **Goal:** Register AGVs, update stock levels, manage user roles.
- **Navigation:** "📦 Inventory" and "🤖 Robots" tabs.
- **Inputs:** SKU, item name, location, quantity adjustment, robot code, secret key.
- **Feedback:** Confirmation modals, updated table rows, stock balance alerts.
- **Error Handling:** Rejects negative stock deductions, blocks self-role elevation (403 Forbidden).
- **Security Considerations:** Server-side RBAC validation, ACID database transaction row locking (`with_for_update`).

#### Screen 4: Order Status & Security Audit Results Screen (Results Equivalent)
- **User:** Customer, Security Auditor, System Admin.
- **Goal:** Review order completion status, verify fulfillment, audit security events.
- **Navigation:** "🛒 Orders" and "🛡️ Security & Audit" tabs.
- **Inputs:** Order ID filter, audit log search.
- **Feedback:** Live security metrics cards (failed logins count, unauthorized commands count, privilege changes count).
- **Error Handling:** Displays meaningful error messages without leaking internal database stack traces.
- **Security Considerations:** Append-only audit log stream, role-restricted endpoint access.

---

### 3. Application of Shneiderman's 8 Golden Rules of Interface Design

1. **Strive for Consistency:** Uniform dark/glassmorphic color palette (`#0a0e17`, `#121a2a`), standard status badge colors (`green=IDLE/SUCCESS`, `amber=BUSY/WARNING`, `red=OFFLINE/FAILED`).
2. **Enable Frequent Users to Use Shortcuts:** Demo account quick-fill chips for instant one-click login testing.
3. **Offer Informative Feedback:** Toast notification system displaying immediate success/error feedback for every user interaction.
4. **Design Dialogs to Yield Closure:** Explicit confirmation popups and order fulfillment status updates upon task completion.
5. **Prevent Errors:** Inputs validate range parameters (e.g. quantity >= 0), buttons disable or prompt for missing parameters before API call.
6. **Permit Easy Reversal of Actions:** Order cancellation options and stock adjustment reverse inputs.
7. **Support Internal Locus of Control:** Users navigate seamlessly across 6 dedicated tabs without losing state.
8. **Reduce Short-term Memory Load:** Key operational metrics (total stock, active AGVs, pending tasks, threat index) prominently displayed on header cards.
