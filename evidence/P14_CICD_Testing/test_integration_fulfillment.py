import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User, Role, Robot, InventoryItem, CustomerOrder, WarehouseTask
from backend.schemas import OrderCreate, OrderItemCreate, TaskAssign
from backend.services import FulfillmentService, TaskService

def get_test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_order_fulfillment_pipeline():
    db = get_test_db()
    # Roles & Users
    role_c = Role(name="Customer"); role_a = Role(name="Administrator")
    db.add_all([role_c, role_a]); db.commit()
    cust = User(username="cust1", hashed_password="pw", role_id=role_c.id)
    admin = User(username="admin1", hashed_password="pw", role_id=role_a.id)
    db.add_all([cust, admin]); db.commit()

    # Robot & Item
    robot = Robot(robot_code="RBT-01", name="Robot 1", status="IDLE", battery_level=100.0, current_location="DOCK", secret_key="secret123")
    item = InventoryItem(sku="SKU-101", name="LiDAR", location="AISLE-1", quantity=50, unit_price=200.0)
    db.add_all([robot, item]); db.commit()

    # 1. Create Order
    order_req = OrderCreate(items=[OrderItemCreate(item_id=item.id, quantity=5)])
    order = FulfillmentService.create_customer_order(db, order_req, cust)
    assert order.status == "PROCESSING"

    # Check Task Created
    task = db.query(WarehouseTask).filter(WarehouseTask.order_id == order.id).first()
    assert task is not None
    assert task.status == "PENDING"

    # 2. Assign Robot to Task
    assigned_task = TaskService.assign_robot_to_task(db, TaskAssign(task_id=task.id, robot_id=robot.id), admin)
    assert assigned_task.assigned_robot_id == robot.id
    assert assigned_task.status == "ASSIGNED"
    assert robot.status == "BUSY"
