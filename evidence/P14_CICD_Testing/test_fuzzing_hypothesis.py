from hypothesis import given, strategies as st
from backend.schemas import LoginRequest, InventoryCreate

@given(st.text(min_size=1, max_size=50), st.text(min_size=1, max_size=100))
def test_login_schema_fuzzing(username, password):
    # Ensure Pydantic handles random text gracefully
    try:
        req = LoginRequest(username=username, password=password)
        assert len(req.username) >= 1
    except ValueError:
        pass

@given(st.text(min_size=3, max_size=20), st.text(min_size=2, max_size=50), st.integers(min_value=0, max_value=100000), st.floats(min_value=0.0, max_value=10000.0))
def test_inventory_create_fuzzing(sku, name, qty, price):
    try:
        inv = InventoryCreate(sku=sku, name=name, location="AISLE-F", quantity=qty, unit_price=price)
        assert inv.quantity >= 0
    except ValueError:
        pass
