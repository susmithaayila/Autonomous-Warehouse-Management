from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4)

# User Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role_name: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RoleAssignRequest(BaseModel):
    user_id: int
    new_role_name: str

# Robot Schemas
class RobotRegister(BaseModel):
    robot_code: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    secret_key: str = Field(..., min_length=8)

class RobotResponse(BaseModel):
    id: int
    robot_code: str
    name: str
    status: str
    battery_level: float
    current_location: str
    last_heartbeat: datetime
    is_active: bool

    class Config:
        from_attributes = True

class RobotStatusUpdate(BaseModel):
    robot_code: str
    status: str
    battery_level: float
    location: str

# Inventory Schemas
class InventoryCreate(BaseModel):
    sku: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    location: str
    quantity: int = Field(..., ge=0)
    unit_price: float = Field(..., ge=0.0)

class InventoryUpdate(BaseModel):
    item_id: int
    quantity_change: int
    reason: str

class InventoryResponse(BaseModel):
    id: int
    sku: str
    name: str
    location: str
    quantity: int
    reserved_quantity: int
    min_threshold: int
    unit_price: float

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Task Schemas
class TaskCreate(BaseModel):
    order_id: int
    item_id: int
    quantity: int = Field(..., gt=0)
    pickup_location: str
    drop_location: str

class TaskAssign(BaseModel):
    task_id: int
    robot_id: int

class TaskResponse(BaseModel):
    id: int
    task_code: str
    order_id: int
    item_id: int
    quantity: int
    pickup_location: str
    drop_location: str
    assigned_robot_id: Optional[int] = None
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Robot Command Schemas
class CommandIssue(BaseModel):
    task_id: int
    robot_id: int
    command_type: str  # PICK, MOVE, DROP, STOP
    payload: str
    nonce: str

class CommandExecute(BaseModel):
    command_id: str
    robot_code: str
    signature: str

class CommandResponse(BaseModel):
    id: int
    command_id: str
    task_id: int
    robot_id: int
    command_type: str
    status: str
    nonce: str
    timestamp: datetime
    executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Audit & Monitoring Schemas
class AuditLogResponse(BaseModel):
    id: int
    timestamp: datetime
    actor_username: str
    actor_role: str
    action: str
    resource: str
    result: str
    severity: str
    ip_address: str
    details: Optional[str] = None

    class Config:
        from_attributes = True

class MetricsResponse(BaseModel):
    failed_login_count: int
    unauthorized_command_count: int
    privilege_changes_count: int
    inventory_modification_rate: float
    robot_offline_count: int
    command_conflict_count: int
    api_error_rate: float
