import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import BaseModel
from app.schemas.user import User, RolesEnum, UserActivation

TEST_DATABASE_URL = "sqlite:///"


@pytest.fixture
def mock_db():
    return {}


@pytest.fixture
def test_db():
    # Create an engine that connects to the test database
    engine = create_engine(TEST_DATABASE_URL)

    # Create all tables
    BaseModel.metadata.create_all(engine)

    # Create a new session for the test
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()

    yield db  # this is where the testing happens

    # Tear down: Drop all data after each test
    BaseModel.metadata.drop_all(bind=engine)
    db.close()


@pytest.fixture
def default_user():
    return User(
        username="test@mail.com",
        password='1321ased',
        role=RolesEnum.USER,
        is_active=True,
        otp="123456",
        image="https://picsum.photos/200/300"
    )


@pytest.fixture
def admin_user():
    return User(
        username="admin@mail.com",
        password='1321ased',
        role=RolesEnum.ADMIN,
        is_active=True,
        otp="123456",
        image="https://picsum.photos/200/300"
    )


@pytest.fixture
def activation_data():
    return UserActivation(Email="test@mail.com", otp='111222')
