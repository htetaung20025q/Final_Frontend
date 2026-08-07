import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database import Base
from models.refresh_model import RefreshToken
from models.user_model import User
from schemas.user import UserCreate, UserDelete, UserLogin, UserUpdate
from services import db_auth


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_login_uses_stored_password_hash_and_returns_tokens(db_session):
    user = User(
        username="alice",
        email="alice@example.com",
        hashed_password=db_auth.jwt_ser.hash_password("secret123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = db_auth.login(
        UserLogin(email="alice@example.com", password="secret123"),
        db_session,
    )

    assert response.status_code == 200
    payload = json.loads(response.body.decode("utf-8"))
    assert payload["Message"].startswith("User alice")
    assert payload["access_token"]
    assert payload["refresh_token"]


def test_update_uses_user_id_not_username_for_lookup(db_session):
    user = User(
        username="bob",
        email="bob@example.com",
        hashed_password=db_auth.jwt_ser.hash_password("secret123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    updated = db_auth.update(
        UserUpdate(
            id=user.id,
            username="charlie",
            email="charlie@example.com",
            password="secret123",
        ),
        db_session,
    )

    assert updated["user"]["email"] == "charlie@example.com"
    assert updated["user"]["username"] == "charlie"


def test_delete_removes_user_when_password_matches(db_session):
    user = User(
        username="dave",
        email="dave@example.com",
        hashed_password=db_auth.jwt_ser.hash_password("secret123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    result = db_auth.delete(
        UserDelete(id=user.id, password="secret123"),
        db_session,
    )

    assert result["message"] == "User deleted successfully"
    assert db_session.query(User).filter(User.id == user.id).first() is None
