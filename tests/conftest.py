from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.main import app
from app.database import Base, get_db
import pytest
from app.models.user import User


TEST_DATABASE_URL = "postgresql://localhost/escalation_tracker_test"


engine=create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    new_user = User(
        name = "test_user",
        email = "test@123.com",
        hashed_password = pwd_context.hash("test_password")
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user

@pytest.fixture
def test_token(client, test_user):
    response = client.post("/auth/login", data={
        "username": test_user.email, 
        "password": "test_password"
    })

    token = response.json()["access_token"]

    return token

