import pytest
from backend.security import get_password_hash, verify_password, create_access_token, decode_token

def test_password_hashing():
    raw_pass = "SecureAdminPass123!"
    hashed = get_password_hash(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPass123!", hashed) is False

def test_jwt_token_encode_decode():
    data = {"sub": "test_operator", "role": "Operator", "id": 42}
    token = create_access_token(data)
    decoded = decode_token(token)
    assert decoded["sub"] == "test_operator"
    assert decoded["role"] == "Operator"
    assert decoded["id"] == 42
