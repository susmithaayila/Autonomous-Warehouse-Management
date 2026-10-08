import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from backend.models import (
    User, Role, Robot, RobotStatus, InventoryItem, InventoryTransaction,
    CustomerOrder, OrderItem, WarehouseTask, RobotCommand, AuditLog
)
from backend.schemas import (
    LoginRequest, UserCreate, RoleAssignRequest, RobotRegister, RobotStatusUpdate,
    InventoryCreate, InventoryUpdate, OrderCreate, TaskCreate, TaskAssign,
    CommandIssue, CommandExecute
)
from backend.security import (
    verify_password, get_password_hash, create_access_token, log_audit_event,
    verify_robot_hmac, compute_robot_hmac
)
from backend.config import settings

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, login_data: LoginRequest, ip_address: str = "127.0.0.1"):
        user = db.query(User).filter(User.username == login_data.username).first()
        if not user:
            log_audit_event(db, login_data.username, "UNKNOWN", "USER_LOGIN", "AUTH", "FAILED", "WARNING", ip_address, "User not found")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        if not user.is_active:
            log_audit_event(db, user.username, user.role.name, "USER_LOGIN", "AUTH", "DENIED", "HIGH", ip_address, "Account disabled")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

        if user.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
            log_audit_event(db, user.username, user.role.name, "USER_LOGIN", "AUTH", "DENIED", "CRITICAL", ip_address, "Account locked due to excessive failed attempts")
            raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Account locked. Contact security administrator.")

        if not verify_password(login_data.password, user.hashed_password):
            user.failed_login_attempts += 1
            db.commit()
            log_audit_event(db, user.username, user.role.name, "USER_LOGIN", "AUTH", "FAILED", "WARNING", ip_address, f"Failed attempt {user.failed_login_attempts}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        # Reset failed attempts on success
        user.failed_login_attempts = 0
        db.commit()

        token = create_access_token({"sub": user.username, "role": user.role.name, "id": user.id})
        log_audit_event(db, user.username, user.role.name, "USER_LOGIN", "AUTH", "SUCCESS", "INFO", ip_address, "Successful login")
        return {
            "access_token": token,
            "token_type": "bearer",  # nosec B105
            "user_id": user.id,
            "username": user.username,
            "role": user.role.name
        }

class UserService:
    @staticmethod
    def create_user(db: Session, data: UserCreate, current_user: User):
        existing = db.query(User).filter(User.username == data.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        role = db.query(Role).filter(Role.name == data.role_name).first()
        if not role:
            raise HTTPException(status_code=400, detail=f"Role '{data.role_name}' does not exist")

        new_user = User(
            username=data.username,
            hashed_password=get_password_hash(data.password),
            role_id=role.id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        log_audit_event(db, current_user.username, current_user.role.name, "CREATE_USER", f"User:{new_user.username}", "SUCCESS", "INFO", details=f"Created user with role {data.role_name}")
        return new_user

    @staticmethod
    def assign_role(db: Session, data: RoleAssignRequest, current_user: User):
        # SR-04 Privilege Escalation Prevention
        if current_user.id == data.user_id:
            log_audit_event(db, current_user.username, current_user.role.name, "ASSIGN_ROLE", f"User:{data.user_id}", "DENIED", "CRITICAL", details="Self privilege escalation attempt blocked")
            raise HTTPException(status_code=403, detail="Self-privilege escalation is strictly prohibited")

        target_user = db.query(User).filter(User.id == data.user_id).first()
        if not target_user:
            raise HTTPException(status_code=444, detail="Target user not found")

        new_role = db.query(Role).filter(Role.name == data.new_role_name).first()
        if not new_role:
            raise HTTPException(status_code=400, detail=f"Invalid role '{data.new_role_name}'")

        old_role_name = target_user.role.name
        target_user.role_id = new_role.id
        db.commit()

        log_audit_event(db, current_user.username, current_user.role.name, "ASSIGN_ROLE", f"User:{target_user.username}", "SUCCESS", "HIGH", details=f"Role changed from {old_role_name} to {new_role.name}")
        return target_user

class InventoryService:
    @staticmethod
    def update_inventory(db: Session, data: InventoryUpdate, current_user: User):
        # SR-06 Inventory Integrity & SR-08 Race condition protection
        item = db.query(InventoryItem).filter(InventoryItem.id == data.item_id).with_for_update(nowait=False).first()
        if not item:
            raise HTTPException(status_code=404, detail="Inventory item not found")

        prev_qty = item.quantity
        new_qty = prev_qty + data.quantity_change
        if new_qty < 0:
            log_audit_event(db, current_user.username, current_user.role.name, "UPDATE_INVENTORY", f"Item:{item.sku}", "FAILED", "WARNING", details="Attempted negative stock balance")
            raise HTTPException(status_code=400, detail="Insufficient stock available for deduction")

        item.quantity = new_qty
        txn = InventoryTransaction(
            item_id=item.id,
            user_id=current_user.id,
            transaction_type="ADJUSTMENT" if data.quantity_change >= 0 else "DEDUCTION",
            change_qty=data.quantity_change,
            previous_qty=prev_qty,
            new_qty=new_qty
        )
        db.add(txn)
        db.commit()
        db.refresh(item)

        log_audit_event(db, current_user.username, current_user.role.name, "UPDATE_INVENTORY", f"Item:{item.sku}", "SUCCESS", "INFO", details=f"Qty changed by {data.quantity_change} (Reason: {data.reason})")
        return item

class RobotService:
    @staticmethod
    def register_robot(db: Session, data: RobotRegister, current_user: User):
        # SR-03 Robot identity verification
        existing = db.query(Robot).filter(Robot.robot_code == data.robot_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Robot with this code already registered")

        robot = Robot(
            robot_code=data.robot_code,
            name=data.name,
            secret_key=data.secret_key,
            status="IDLE",
            battery_level=100.0,
            current_location="DOCK-01"
        )
        db.add(robot)
        db.commit()
        db.refresh(robot)

        log_audit_event(db, current_user.username, current_user.role.name, "REGISTER_ROBOT", f"Robot:{robot.robot_code}", "SUCCESS", "HIGH", details=f"Registered robot {robot.name}")
        return robot

    @staticmethod
    def update_robot_status(db: Session, data: RobotStatusUpdate, current_user: User):
        robot = db.query(Robot).filter(Robot.robot_code == data.robot_code).first()
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")

        robot.status = data.status
        robot.battery_level = data.battery_level
        robot.current_location = data.location
        robot.last_heartbeat = datetime.datetime.utcnow()

        status_entry = RobotStatus(
            robot_id=robot.id,
            status=data.status,
            battery_level=data.battery_level,
            location=data.location
        )
        db.add(status_entry)
        db.commit()
        return robot

class TaskService:
    @staticmethod
    def assign_robot_to_task(db: Session, data: TaskAssign, current_user: User):
        task = db.query(WarehouseTask).filter(WarehouseTask.id == data.task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        robot = db.query(Robot).filter(Robot.id == data.robot_id).first()
        if not robot:
            raise HTTPException(status_code=404, detail="Robot not found")

        if robot.status != "IDLE":
            log_audit_event(db, current_user.username, current_user.role.name, "ASSIGN_TASK", f"Task:{task.task_code}", "DENIED", "WARNING", details=f"Robot {robot.robot_code} is not IDLE (Status: {robot.status})")
            raise HTTPException(status_code=400, detail=f"Robot {robot.robot_code} is not available (Status: {robot.status})")

        task.assigned_robot_id = robot.id
        task.status = "ASSIGNED"
        robot.status = "BUSY"
        db.commit()

        log_audit_event(db, current_user.username, current_user.role.name, "ASSIGN_TASK", f"Task:{task.task_code}", "SUCCESS", "INFO", details=f"Assigned Robot {robot.robot_code}")
        return task

class CommandAuthorizationService:
    @staticmethod
    def issue_command(db: Session, data: CommandIssue, current_user: User):
        # SR-05 & SR-09 Command Conflict Prevention
        robot = db.query(Robot).filter(Robot.id == data.robot_id).first()
        if not robot or not robot.is_active:
            raise HTTPException(status_code=400, detail="Target robot inactive or not found")

        # Check for active executing commands on this robot
        active_cmd = db.query(RobotCommand).filter(
            RobotCommand.robot_id == robot.id,
            RobotCommand.status.in_(["ISSUED", "EXECUTING"])
        ).first()
        if active_cmd:
            log_audit_event(db, current_user.username, current_user.role.name, "ISSUE_COMMAND", f"Robot:{robot.robot_code}", "DENIED", "HIGH", details="Command conflict detected: Robot is already executing another command")
            raise HTTPException(status_code=409, detail="Command Conflict: Robot is currently executing another active command")

        # SR-11 Replay Protection (Nonce check)
        existing_nonce = db.query(RobotCommand).filter(RobotCommand.nonce == data.nonce).first()
        if existing_nonce:
            log_audit_event(db, current_user.username, current_user.role.name, "ISSUE_COMMAND", f"Robot:{robot.robot_code}", "DENIED", "CRITICAL", details="Replay Attack Detected: Nonce already used")
            raise HTTPException(status_code=400, detail="Replay Attack Protection: Nonce has already been processed")

        cmd_id = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        signature = compute_robot_hmac(robot.secret_key, f"{cmd_id}:{data.command_type}:{data.payload}:{data.nonce}")

        command = RobotCommand(
            command_id=cmd_id,
            task_id=data.task_id,
            robot_id=robot.id,
            command_type=data.command_type,
            payload=data.payload,
            nonce=data.nonce,
            signature=signature,
            status="ISSUED"
        )
        db.add(command)
        db.commit()
        db.refresh(command)

        log_audit_event(db, current_user.username, current_user.role.name, "ISSUE_COMMAND", f"Cmd:{cmd_id}", "SUCCESS", "INFO", details=f"Issued command {data.command_type} to Robot {robot.robot_code}")
        return command

    @staticmethod
    def execute_command(db: Session, data: CommandExecute):
        # SR-03 & SR-05 Robot Identity Verification
        command = db.query(RobotCommand).filter(RobotCommand.command_id == data.command_id).first()
        if not command:
            raise HTTPException(status_code=404, detail="Command not found")

        if command.status in ["SUCCESS", "REJECTED"]:
            # SR-11 Replay Attack attempt on executed command
            log_audit_event(db, data.robot_code, "ROBOT", "EXECUTE_COMMAND", f"Cmd:{data.command_id}", "DENIED", "CRITICAL", details="Replay attack attempt on already completed command")
            raise HTTPException(status_code=400, detail="Replay Attack: Command already completed")

        robot = db.query(Robot).filter(Robot.id == command.robot_id, Robot.robot_code == data.robot_code).first()
        if not robot:
            raise HTTPException(status_code=403, detail="Robot identity mismatch")

        # HMAC Verification
        expected_sig = compute_robot_hmac(robot.secret_key, f"{command.command_id}:{command.command_type}:{command.payload}:{command.nonce}")
        if not verify_robot_hmac(robot.secret_key, f"{command.command_id}:{command.command_type}:{command.payload}:{command.nonce}", data.signature):
            command.status = "REJECTED"
            db.commit()
            log_audit_event(db, robot.robot_code, "ROBOT", "EXECUTE_COMMAND", f"Cmd:{command.command_id}", "DENIED", "CRITICAL", details="Invalid HMAC signature detected")
            raise HTTPException(status_code=401, detail="Invalid HMAC command signature")

        # Execute Task State Transition
        task = db.query(WarehouseTask).filter(WarehouseTask.id == command.task_id).first()
        if task:
            if command.command_type == "PICK":
                task.status = "PICKING"
                robot.status = "BUSY"
            elif command.command_type == "MOVE":
                task.status = "MOVING"
                robot.current_location = task.drop_location
            elif command.command_type == "DROP":
                task.status = "COMPLETED"
                task.completed_at = datetime.datetime.utcnow()
                robot.status = "IDLE"

                # Check if order is fulfilled
                order = db.query(CustomerOrder).filter(CustomerOrder.id == task.order_id).first()
                if order:
                    all_tasks = db.query(WarehouseTask).filter(WarehouseTask.order_id == order.id).all()
                    if all(t.status == "COMPLETED" for t in all_tasks):
                        order.status = "FULFILLED"

        command.status = "SUCCESS"
        command.executed_at = datetime.datetime.utcnow()
        db.commit()

        log_audit_event(db, robot.robot_code, "ROBOT", "EXECUTE_COMMAND", f"Cmd:{command.command_id}", "SUCCESS", "INFO", details=f"Command {command.command_type} executed successfully")
        return command

class FulfillmentService:
    @staticmethod
    def create_customer_order(db: Session, order_data: OrderCreate, current_user: User):
        # Full end-to-end order fulfillment pipeline initiation
        if not order_data.items:
            raise HTTPException(status_code=400, detail="Order must contain at least one item")

        # Check Inventory & Reserve Stock
        for item_req in order_data.items:
            inv_item = db.query(InventoryItem).filter(InventoryItem.id == item_req.item_id).first()
            if not inv_item:
                raise HTTPException(status_code=404, detail=f"Inventory item ID {item_req.item_id} not found")
            if (inv_item.quantity - inv_item.reserved_quantity) < item_req.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient available stock for item '{inv_item.name}'")

        order_num = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        order = CustomerOrder(order_number=order_num, customer_id=current_user.id, status="PROCESSING")
        db.add(order)
        db.commit()
        db.refresh(order)

        # Create Order Items and Warehouse Tasks
        for item_req in order_data.items:
            inv_item = db.query(InventoryItem).filter(InventoryItem.id == item_req.item_id).first()
            inv_item.reserved_quantity += item_req.quantity

            ord_item = OrderItem(order_id=order.id, item_id=inv_item.id, quantity=item_req.quantity, status="RESERVED")
            db.add(ord_item)

            task_code = f"TASK-{uuid.uuid4().hex[:8].upper()}"
            task = WarehouseTask(
                task_code=task_code,
                order_id=order.id,
                item_id=inv_item.id,
                quantity=item_req.quantity,
                pickup_location=inv_item.location,
                drop_location="PACKING-ZONE-A",
                status="PENDING"
            )
            db.add(task)

        db.commit()
        log_audit_event(db, current_user.username, current_user.role.name, "CREATE_ORDER", f"Order:{order_num}", "SUCCESS", "INFO", details=f"Order created with {len(order_data.items)} item(s)")
        return order

class AuditService:
    @staticmethod
    def get_security_metrics(db: Session):
        failed_logins = db.query(AuditLog).filter(AuditLog.action == "USER_LOGIN", AuditLog.result.in_(["FAILED", "DENIED"])).count()
        unauth_cmds = db.query(AuditLog).filter(AuditLog.action.in_(["ISSUE_COMMAND", "EXECUTE_COMMAND"]), AuditLog.result.in_(["DENIED", "REJECTED"])).count()
        priv_changes = db.query(AuditLog).filter(AuditLog.action == "ASSIGN_ROLE").count()
        inv_mods = db.query(AuditLog).filter(AuditLog.action == "UPDATE_INVENTORY").count()
        robots_offline = db.query(Robot).filter(Robot.status == "OFFLINE").count()
        cmd_conflicts = db.query(AuditLog).filter(AuditLog.details.like("%conflict%")).count()
        total_logs = db.query(AuditLog).count()
        failed_logs = db.query(AuditLog).filter(AuditLog.result != "SUCCESS").count()
        error_rate = (failed_logs / total_logs * 100.0) if total_logs > 0 else 0.0

        return {
            "failed_login_count": failed_logins,
            "unauthorized_command_count": unauth_cmds,
            "privilege_changes_count": priv_changes,
            "inventory_modification_rate": float(inv_mods),
            "robot_offline_count": robots_offline,
            "command_conflict_count": cmd_conflicts,
            "api_error_rate": round(error_rate, 2)
        }
