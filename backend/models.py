import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from backend.database import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    role = relationship("Role")

class Robot(Base):
    __tablename__ = "robots"
    id = Column(Integer, primary_key=True, index=True)
    robot_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    status = Column(String(50), default="IDLE")  # IDLE, BUSY, CHARGING, OFFLINE, MAINTENANCE
    battery_level = Column(Float, default=100.0)
    current_location = Column(String(50), default="DOCK-01")
    secret_key = Column(String(255), nullable=False)
    last_heartbeat = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

class RobotStatus(Base):
    __tablename__ = "robot_statuses"
    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(Integer, ForeignKey("robots.id"), nullable=False)
    status = Column(String(50), nullable=False)
    battery_level = Column(Float, nullable=False)
    location = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class WarehouseLocation(Base):
    __tablename__ = "warehouse_locations"
    id = Column(Integer, primary_key=True, index=True)
    location_code = Column(String(50), unique=True, nullable=False)
    zone = Column(String(50), nullable=False)
    aisle = Column(String(50), nullable=False)
    rack = Column(String(50), nullable=False)

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(50), nullable=False)
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    min_threshold = Column(Integer, default=5)
    unit_price = Column(Float, default=0.0)

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    transaction_type = Column(String(50), nullable=False)  # RESTOCK, PICK, RESERVATION, ADJUSTMENT
    change_qty = Column(Integer, nullable=False)
    previous_qty = Column(Integer, nullable=False)
    new_qty = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class CustomerOrder(Base):
    __tablename__ = "customer_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="CREATED")  # CREATED, PROCESSING, PICKED, MOVED, DROPPED, PACKING, FULFILLED, CANCELLED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    customer = relationship("User")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("customer_orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), default="PENDING")

    order = relationship("CustomerOrder", back_populates="items")
    item = relationship("InventoryItem")

class WarehouseTask(Base):
    __tablename__ = "warehouse_tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_code = Column(String(50), unique=True, index=True, nullable=False)
    order_id = Column(Integer, ForeignKey("customer_orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    pickup_location = Column(String(50), nullable=False)
    drop_location = Column(String(50), nullable=False)
    assigned_robot_id = Column(Integer, ForeignKey("robots.id"), nullable=True)
    status = Column(String(50), default="PENDING")  # PENDING, ASSIGNED, PICKING, MOVING, DROPPING, COMPLETED, FAILED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class RobotCommand(Base):
    __tablename__ = "robot_commands"
    id = Column(Integer, primary_key=True, index=True)
    command_id = Column(String(100), unique=True, index=True, nullable=False)
    task_id = Column(Integer, ForeignKey("warehouse_tasks.id"), nullable=False)
    robot_id = Column(Integer, ForeignKey("robots.id"), nullable=False)
    command_type = Column(String(50), nullable=False)  # PICK, MOVE, DROP, STOP
    payload = Column(Text, nullable=False)
    status = Column(String(50), default="ISSUED")  # ISSUED, EXECUTING, SUCCESS, REJECTED, FAILED
    nonce = Column(String(100), nullable=False)
    signature = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    actor_username = Column(String(100), nullable=False)
    actor_role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    result = Column(String(50), nullable=False)  # SUCCESS, DENIED, FAILED, WARNING
    severity = Column(String(50), default="INFO")  # INFO, WARNING, HIGH, CRITICAL
    ip_address = Column(String(50), default="127.0.0.1")
    details = Column(Text, nullable=True)
