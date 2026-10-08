# Phase 12 – Secure Coding and Refactoring Report

## Autonomous Warehouse Management System (AWMS)
**Course:** 24CYS401 – Secure Software Engineering  
**Phase:** 12 – Secure Coding and Refactoring [4 Marks]

---

## 1. Executive Summary & Module Scope
Phase 12 demonstrates secure software engineering implementation across core AWMS modules:
- **Authentication & Authorization Module:** `backend/security.py`, `backend/services.py` (`AuthService`)
- **Inventory & Reservation Module:** `backend/services.py` (`InventoryService`)
- **Robot Command & Cryptographic HMAC Module:** `backend/services.py` (`CommandAuthService`)
- **User Management & Self-Escalation Protection:** `backend/services.py` (`UserService`)

---

## 2. Identified Security Weaknesses (Before Refactoring)

### Weakness 1: Unauthenticated Robot Command Dispatcher & Replay Attack Vulnerability
- **Initial Insecure Pattern:**
  ```python
  # INSECURE INITIAL VERSION
  def execute_robot_command_insecure(robot_id: int, command_type: str):
      robot = db.query(Robot).get(robot_id)
      robot.status = f"EXECUTING_{command_type}"
      db.commit()
      return {"status": "SUCCESS"}
  ```
- **Security Flaw:** Any user or network eavesdropper could send unauthenticated REST calls to dispatch physical AGVs without proof of origin or freshness. Past intercepted commands could be replayed infinitely to cause physical collision hazards.

### Weakness 2: Non-Atomic Inventory Balance Modification & Race Condition
- **Initial Insecure Pattern:**
  ```python
  # INSECURE INITIAL VERSION
  def update_inventory_stock_insecure(item_id: int, qty_change: int):
      item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
      item.quantity = item.quantity + qty_change  # Can drop below zero!
      db.commit()
  ```
- **Security Flaw:** Under concurrent order fulfillment requests, parallel worker threads reading `item.quantity` simultaneously experience lost updates, leading to negative stock balances and stock allocation corruption.

### Weakness 3: Missing Server-Side Self-Role Change Verification
- **Initial Insecure Pattern:**
  ```python
  # INSECURE INITIAL VERSION
  def update_user_role_insecure(user_id: int, new_role_id: int):
      user = db.query(User).get(user_id)
      user.role_id = new_role_id
      db.commit()
  ```
- **Security Flaw:** Lacked server-side enforcement preventing an logged-in user from sending a PUT request to change their own role ID to 1 (Administrator).

---

## 3. Secure Refactored Code Implementation

### Refactoring 1: HMAC-SHA256 Command Authentication with Nonce Anti-Replay (`CommandAuthService`)
```python
class CommandAuthService:
    @staticmethod
    def issue_command(db: Session, robot_id: int, command_type: str, payload: str, issued_by_id: int):
        robot = db.query(Robot).filter(Robot.id == robot_id).first()
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")
        
        # Check single-active command constraint
        active_cmd = db.query(RobotCommand).filter(
            RobotCommand.robot_id == robot_id,
            RobotCommand.status.in_(["PENDING", "EXECUTING"])
        ).first()
        if active_cmd:
            raise HTTPException(status_code=400, detail="Robot already has an active command in progress")
        
        nonce = str(uuid.uuid4())
        raw_payload = f"{robot.robot_code}:{command_type}:{payload}:{nonce}"
        signature = compute_robot_hmac(settings.ROBOT_HMAC_SECRET, raw_payload)
        
        command = RobotCommand(
            robot_id=robot_id,
            command_type=command_type,
            payload=payload,
            nonce=nonce,
            hmac_signature=signature,
            issued_by_id=issued_by_id,
            status="PENDING"
        )
        db.add(command)
        db.commit()
        return command

    @staticmethod
    def execute_command(db: Session, command_id: int, provided_signature: str, provided_nonce: str):
        command = db.query(RobotCommand).filter(RobotCommand.id == command_id).first()
        if not command:
            raise HTTPException(status_code=404, detail="Command not found")
        
        # Verify Nonce Uniqueness & Anti-Replay
        if command.nonce != provided_nonce or command.status != "PENDING":
            log_audit_event(db, "ROBOT", "Robot", "REPLAY_ATTEMPT", f"RobotCommand:{command_id}", "REJECTED", "HIGH")
            raise HTTPException(status_code=400, detail="Command replay detected or invalid nonce")
        
        # Verify Cryptographic HMAC Signature
        robot = db.query(Robot).filter(Robot.id == command.robot_id).first()
        raw_payload = f"{robot.robot_code}:{command.command_type}:{command.payload}:{provided_nonce}"
        if not verify_robot_hmac(settings.ROBOT_HMAC_SECRET, raw_payload, provided_signature):
            log_audit_event(db, "ROBOT", "Robot", "HMAC_FAILED", f"RobotCommand:{command_id}", "REJECTED", "HIGH")
            raise HTTPException(status_code=401, detail="Invalid HMAC signature")
        
        command.status = "COMPLETED"
        command.executed_at = datetime.datetime.utcnow()
        robot.status = "IDLE"
        db.commit()
        return command
```

### Refactoring 2: Atomic Row Locking & Negative Stock Guard (`InventoryService`)
```python
class InventoryService:
    @staticmethod
    def adjust_stock(db: Session, item_id: int, quantity_change: int, reason: str, user: User):
        # Apply SQLAlchemy pessimistic row-level lock
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).with_for_update().first()
        if not item:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        
        new_quantity = item.quantity + quantity_change
        if new_quantity < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Adjustment failed: Insufficient stock. Current: {item.quantity}, Requested change: {quantity_change}"
            )
        
        item.quantity = new_quantity
        tx = InventoryTransaction(
            item_id=item_id,
            user_id=user.id,
            transaction_type="ADJUSTMENT",
            quantity=quantity_change,
            reason=reason
        )
        db.add(tx)
        db.commit()
        return item
```

---

## 4. Demonstration of Four Pillars of Secure Coding

### 1. Input Validation (Pydantic V2 Schemas)
- Strict typed schemas validate all incoming REST JSON bodies in `backend/schemas.py`.
- Validation annotations enforce positive quantities (`@field_validator(gt=0)`), string lengths, and enum values.

### 2. Authorization (FastAPI RBAC)
- Role-based dependencies (`require_roles(["Administrator", "Operator"])`) inspect JWT claims on every endpoint call.
- Direct object reference access controls (IDOR protection) restrict Customers to viewing only their own orders.

### 3. Comprehensive Error Handling
- Detailed standard `HTTPException` responses return appropriate status codes (400, 401, 403, 404, 409) without leaking internal stack trace details or database paths.

### 4. Sensitive Data Handling
- Password Hashing: Direct Bcrypt salt generation and verification (`verify_password`).
- Access Tokens: Signed JWTs (`HS256`) with strict 60-minute expiration.
- Database Credentials & Cryptographic Keys: Loaded via OS environment variables.

---

## 5. Summary Checklist of Deliverables

- [x] Implemented Core Authentication, Inventory, and Robot Modules
- [x] Identified at least 2 Security Weaknesses (HMAC Absence, Inventory Race Condition, Self-Role Escalation)
- [x] Applied Refactoring with Complete Code Improvements & Explanations
- [x] Demonstrated Input Validation, RBAC Authorization, Error Handling, and Sensitive Data Protection
