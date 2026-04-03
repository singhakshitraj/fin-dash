import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from main import app
from db.connection import newSession
from db.models import Base, User, UserRole
from auth.password import PasswordHelpers
from auth.token import JWTTokenClass

os.environ["SECRET_KEY"] = "testsecret"
os.environ["ALGORITHM"] = "HS256"
os.environ["ADMIN_USERNAME"] = "admin"

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[newSession] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_user(db_session):
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    user = User(
        username=admin_username,
        password=PasswordHelpers.hash_password("adminpass"),
        role=UserRole.ADMIN
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    token = JWTTokenClass.generate_token({"username": user.username})
    return {"user": user, "token": token, "headers": {"Authorization": f"Bearer {token}"}}

@pytest.fixture
def regular_user(db_session):
    user = User(
        username="testuser",
        password=PasswordHelpers.hash_password("testpass"),
        role=UserRole.VIEWER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    token = JWTTokenClass.generate_token({"username": user.username})
    return {"user": user, "token": token, "headers": {"Authorization": f"Bearer {token}"}}
