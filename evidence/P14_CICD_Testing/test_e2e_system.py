import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User, Role, Robot, InventoryItem, CustomerOrder, WarehouseTask, RobotCommand
from backend.schemas import CommandIssue, CommandExecute
from backend.services import CommandAuthorizationService, compute_robot_hmac
from fastapi import HTTPException

def get_test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_hmac_command_issue_and_execution_e2e():
    db = get_test_db()
    role = Role(name="Administrator"); db.add(role); db.commit()
    admin = User(username="admin_e2e", hashed_password="pw", role_id=role.id); db.add(admin); db.commit()

    robot = Robot(robot_code="RBT-E2E", name="E2E AGV", status="BUSY", battery_level=95.0, current_location="ZONE-A", secret_key="super_secret_e2e_key")
    item = InventoryItem(sku="SKU-E2E", name="E2E Sensor", location="A1", quantity=10, unit_price=100.0)
    db.add_all([robot, item]); db.commit()

    order = CustomerOrder(order_number="ORD-E2E", customer_id=admin.id, status="PROCESSING"); db.add(order); db.commit()
    task = WarehouseTask(task_code="TASK-E2E", order_id=order.id, item_id=item.id, quantity=1, pickup_location="A1", drop_location="PACKING", assigned_robot_id=robot.id, status="ASSIGNED")
    db.add(task); db.commit()

    # 1. Issue Command
    nonce = f"NONCE-{uuid.uuid4().hex[:8]}"
    cmd_data = CommandIssue(task_id=task.id, robot_id=robot.id, command_type="PICK", payload="TASK-E2E", nonce=nonce)
    issued_cmd = CommandAuthorizationService.issue_command(db, cmd_data, admin)
    assert issued_cmd.status == "ISSUED"

    # 2. Execute Command with valid HMAC
    exec_data = CommandExecute(command_id=issued_cmd.command_id, robot_code=robot.robot_code, signature=issued_cmd.signature)
    exec_res = CommandAuthorizationService.execute_command(db, exec_data)
    assert exec_res.status == "SUCCESS"
    assert task.status == "PICKING"

    # 3. Test Replay Protection
    with pytest.raises(HTTPException) as exc:
        CommandAuthorizationService.execute_command(db, exec_data)
    assert exc.value.status_code == 400
    assert "Replay Attack" in exc.value.detail
