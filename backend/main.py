import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import engine, Base, get_db
from backend.models import User, Role, Robot, InventoryItem, AuditLog, WarehouseTask, CustomerOrder, RobotCommand
from backend.schemas import (
    Token, LoginRequest, UserCreate, UserResponse, RoleAssignRequest,
    RobotRegister, RobotResponse, RobotStatusUpdate, InventoryCreate, InventoryUpdate,
    InventoryResponse, OrderCreate, OrderResponse, TaskCreate, TaskAssign, TaskResponse,
    CommandIssue, CommandExecute, CommandResponse, AuditLogResponse, MetricsResponse
)
from backend.security import get_current_user, require_roles, get_password_hash, log_audit_event
from backend.services import (
    AuthService, UserService, InventoryService, RobotService, TaskService,
    CommandAuthorizationService, FulfillmentService, AuditService
)

# Initialize DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Secure Autonomous Warehouse Management System API"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed Database
def seed_initial_data():
    db = next(get_db())

    # Roles
    role_names = ["Administrator", "Operator", "Customer", "Auditor", "Robot"]
    roles = {}
    for r_name in role_names:
        role = db.query(Role).filter(Role.name == r_name).first()
        if not role:
            role = Role(name=r_name, description=f"{r_name} role in AWMS")
            db.add(role)
            db.commit()
            db.refresh(role)
        roles[r_name] = role

    # Users
    users_data = [
        ("admin", "AdminPass123!", "Administrator"),
        ("operator", "OperatorPass123!", "Operator"),
        ("customer", "CustomerPass123!", "Customer"),
        ("auditor", "AuditorPass123!", "Auditor"),
    ]
    for u_name, u_pass, r_name in users_data:
        usr = db.query(User).filter(User.username == u_name).first()
        if not usr:
            usr = User(
                username=u_name,
                hashed_password=get_password_hash(u_pass),
                role_id=roles[r_name].id
            )
            db.add(usr)
            db.commit()

    # Robots
    robots_data = [
        ("ROBOT-01", "Robot Alpha", "DOCK-01", "robot_secret_alpha_99"),
        ("ROBOT-02", "Robot Beta", "DOCK-02", "robot_secret_beta_88"),
        ("ROBOT-03", "Robot Gamma", "CHARGING-01", "robot_secret_gamma_77"),
    ]
    for r_code, r_name, loc, sec in robots_data:
        rbt = db.query(Robot).filter(Robot.robot_code == r_code).first()
        if not rbt:
            rbt = Robot(
                robot_code=r_code,
                name=r_name,
                status="IDLE",
                battery_level=100.0,
                current_location=loc,
                secret_key=sec
            )
            db.add(rbt)
            db.commit()

    # Inventory Items
    items_data = [
        ("SKU-1001", "High-Speed Electric Motor", "AISLE-A1", 50, 299.99),
        ("SKU-1002", "Autonomous Controller Board", "AISLE-A2", 30, 450.00),
        ("SKU-1003", "Lithium Battery Pack 48V", "AISLE-B1", 20, 650.00),
        ("SKU-1004", "LiDAR Optical Sensor", "AISLE-C3", 15, 890.00),
    ]
    for sku, name, loc, qty, price in items_data:
        itm = db.query(InventoryItem).filter(InventoryItem.sku == sku).first()
        if not itm:
            itm = InventoryItem(
                sku=sku,
                name=name,
                location=loc,
                quantity=qty,
                reserved_quantity=0,
                unit_price=price
            )
            db.add(itm)
            db.commit()

seed_initial_data()

# Root & Health Endpoints
@app.get("/api/health")
def health_check():
    return {"status": "HEALTHY", "system": settings.PROJECT_NAME, "version": settings.VERSION}

# Authentication Endpoints
@app.post("/api/auth/login", response_model=Token)
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    return AuthService.authenticate_user(db, login_data, client_ip)

@app.get("/api/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# User & RBAC Management
@app.post("/api/users", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    return UserService.create_user(db, user_data, current_user)

@app.post("/api/users/assign-role", response_model=UserResponse)
def assign_role(
    role_data: RoleAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    return UserService.assign_role(db, role_data, current_user)

@app.get("/api/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Auditor"]))
):
    users = db.query(User).all()
    return users

# Inventory Endpoints
@app.get("/api/inventory", response_model=List[InventoryResponse])
def get_inventory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(InventoryItem).all()

@app.post("/api/inventory", response_model=InventoryResponse)
def create_inventory_item(
    item_data: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Operator"]))
):
    existing = db.query(InventoryItem).filter(InventoryItem.sku == item_data.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    item = InventoryItem(**item_data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    log_audit_event(db, current_user.username, current_user.role.name, "CREATE_INVENTORY", f"SKU:{item.sku}", "SUCCESS", "INFO")
    return item

@app.post("/api/inventory/update", response_model=InventoryResponse)
def update_inventory(
    update_data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Operator"]))
):
    return InventoryService.update_inventory(db, update_data, current_user)

# Robot Management Endpoints
@app.get("/api/robots", response_model=List[RobotResponse])
def list_robots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Robot).all()

@app.post("/api/robots", response_model=RobotResponse)
def register_robot(
    robot_data: RobotRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    return RobotService.register_robot(db, robot_data, current_user)

@app.post("/api/robots/status")
def update_robot_status(
    status_data: RobotStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RobotService.update_robot_status(db, status_data, current_user)

# Warehouse Task Management
@app.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WarehouseTask).all()

@app.post("/api/tasks/assign", response_model=TaskResponse)
def assign_task(
    assign_data: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Operator"]))
):
    return TaskService.assign_robot_to_task(db, assign_data, current_user)

# Order & Fulfillment Endpoints
@app.get("/api/orders", response_model=List[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name == "Customer":
        return db.query(CustomerOrder).filter(CustomerOrder.customer_id == current_user.id).all()
    return db.query(CustomerOrder).all()

@app.post("/api/orders", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Customer", "Administrator", "Operator"]))
):
    return FulfillmentService.create_customer_order(db, order_data, current_user)

# Secure Robot Command Control
@app.get("/api/commands", response_model=List[CommandResponse])
def list_commands(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Operator", "Auditor"]))
):
    return db.query(RobotCommand).all()

@app.post("/api/commands/issue", response_model=CommandResponse)
def issue_command(
    cmd_data: CommandIssue,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Operator"]))
):
    return CommandAuthorizationService.issue_command(db, cmd_data, current_user)

@app.post("/api/commands/execute", response_model=CommandResponse)
def execute_command(
    exec_data: CommandExecute,
    db: Session = Depends(get_db)
):
    return CommandAuthorizationService.execute_command(db, exec_data)

# Audit & Monitoring Endpoints
@app.get("/api/audit/logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Auditor"]))
):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(200).all()

@app.get("/api/audit/metrics", response_model=MetricsResponse)
def get_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "Auditor"]))
):
    return AuditService.get_security_metrics(db)

# Mount Frontend static files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")
