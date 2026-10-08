import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User, Role, InventoryItem
from backend.schemas import InventoryUpdate
from backend.services import InventoryService
from fastapi import HTTPException

def get_test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_inventory_update_success():
    db = get_test_db()
    role = Role(name="Operator")
    db.add(role); db.commit()
    user = User(username="op1", hashed_password="pw", role_id=role.id)
    db.add(user); db.commit()

    item = InventoryItem(sku="SKU-TEST-01", name="Test Sensor", location="A1", quantity=100, unit_price=50.0)
    db.add(item); db.commit()

    update_data = InventoryUpdate(item_id=item.id, quantity_change=-20, reason="Dispatch")
    updated = InventoryService.update_inventory(db, update_data, user)
    assert updated.quantity == 80

def test_inventory_negative_stock_prevented():
    db = get_test_db()
    role = Role(name="Operator")
    db.add(role); db.commit()
    user = User(username="op1", hashed_password="pw", role_id=role.id)
    db.add(user); db.commit()

    item = InventoryItem(sku="SKU-TEST-02", name="Test Motor", location="A2", quantity=10, unit_price=150.0)
    db.add(item); db.commit()

    update_data = InventoryUpdate(item_id=item.id, quantity_change=-50, reason="Excessive Deduction")
    with pytest.raises(HTTPException) as exc_info:
        InventoryService.update_inventory(db, update_data, user)
    assert exc_info.value.status_code == 400
    assert "Insufficient stock" in exc_info.value.detail
