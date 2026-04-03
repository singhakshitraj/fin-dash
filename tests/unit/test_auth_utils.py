import pytest
from auth.password import PasswordHelpers
from auth.token import JWTTokenClass

def test_password_hashing():
    password = "secretpassword"
    hashed = PasswordHelpers.hash_password(password)
    assert hashed != password
    assert PasswordHelpers.verify_password(password, hashed) is True
    assert PasswordHelpers.verify_password("wrongpassword", hashed) is False

def test_token_generation_and_decoding():
    user = {"username": "testuser"}
    token = JWTTokenClass.generate_token(user)
    assert isinstance(token, str)
    
    decoded_username = JWTTokenClass.get_user(token)
    assert decoded_username == "testuser"

def test_invalid_token():
    with pytest.raises(Exception):
        JWTTokenClass.get_user("invalid_token")
