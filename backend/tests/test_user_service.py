from unittest.mock import MagicMock

import pytest

from app.schemas.user import UserCreate
from app.services.user_service import (
    create_user,
    hash_password,
    verify_password
)
from app.models.user import User


class TestUserService:

    def test_hash_password(self):
        password = "Test@123"

        hashed_password = hash_password(password)

        assert hashed_password != password
        assert hashed_password.startswith("$2")

    def test_verify_password_success(self):
        password = "Test@123"

        hashed_password = hash_password(password)

        assert verify_password(
            password,
            hashed_password
        ) is True

    def test_verify_password_failure(self):
        password = "Test@123"

        hashed_password = hash_password(password)

        assert verify_password(
            "WrongPassword",
            hashed_password
        ) is False

    def test_create_user_success(self):
        db = MagicMock()

        db.query.return_value.filter.return_value.first.return_value = None

        user_data = UserCreate(
            name="Test User",
            email="testuser@example.com",
            password="Test@123"
        )

        user = create_user(db, user_data)

        assert user.name == "Test User"
        assert user.email == "testuser@example.com"
        assert user.role == "user"
        assert user.password_hash != "Test@123"

        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(user)

    def test_create_user_duplicate_email(self):
        db = MagicMock()

        existing_user = User(
            user_id=1,
            name="Existing User",
            email="existing@example.com",
            password_hash="hashed-password",
            role="user"
        )

        db.query.return_value.filter.return_value.first.return_value = (
            existing_user
        )

        user_data = UserCreate(
            name="New User",
            email="existing@example.com",
            password="Test@123"
        )

        with pytest.raises(
            ValueError,
            match="Email already registered"
        ):
            create_user(db, user_data)