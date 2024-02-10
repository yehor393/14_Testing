from unittest.mock import patch

from app.repositories.user import UserRepo
from app.services.users import UserServices
from app.schemas.user import User, RolesEnum, UserActivation

from app.models.users import UserDB


def test_create_success(default_user, mock_db):
    with patch("app.services.users.UserRepo") as mock_repo:
        user_service = UserServices(mock_db)
        mock_repo.return_value.create.return_value = UserDB(
            username="test@mail.com",
            password='1321ased',
            role=RolesEnum.USER,
            is_active=False,
            otp="123456",
            image="https://picsum.photos/200/300"
        )
        result = user_service.create_new(default_user)
        assert result.is_active == False
        assert result.otp
        assert result.otp != default_user.otp


def test_activation_success(activation_data, mock_db):
    with patch("app.services.users.UserRepo") as mock_repo:
        mock_repo.return_value.get_by_username.return_value = UserDB(
            username="test@mail.com",
            password='1321ased',
            role=RolesEnum.USER,
            is_active=True,
            otp="111222",
            image="https://picsum.photos/200/300"
        )

        mock_repo.return_value.update.return_value = UserDB(
            username="test@mail.com",
            password='1321ased',
            role=RolesEnum.USER,
            is_active=True,
            otp="111222",
            image="https://picsum.photos/200/300"
        )

        user_service = UserServices(mock_db)
        result = user_service.activate_user(activation_data)
        assert result.is_active is True
        mock_repo.return_value.update.assert_called()


def test_activation_not_success(activation_data, mock_db):
    with patch("app.services.users.UserRepo") as mock_repo:
        mock_repo.return_value.get_by_username.return_value = UserDB(
            username="test@mail.com",
            password='1321ased',
            role=RolesEnum.USER,
            is_active=False,
            otp="123456",
            image="https://picsum.photos/200/300"
        )

        mock_repo.return_value.update.return_value = UserDB(
            username="test@mail.com",
            password='1321ased',
            role=RolesEnum.USER,
            is_active=False,
            otp="123456",
            image="https://picsum.photos/200/300"
        )

        user_service = UserServices(mock_db)
        result = user_service.activate_user(activation_data)
        assert result.is_active is False
        mock_repo.return_value.update.assert_not_called()


def test_update_user(default_user, admin_user, mock_db):
    with patch('app.repositories.user.UserRepo') as mock_repo:
        mock_db.query.return_value.filter.return_value.delete.return_value = None
        mock_repo.return_value.create.return_value = admin_user

        user_service = UserRepo(mock_db)

        updated_user = user_service.update(default_user)

        mock_db.query.assert_called_with(UserDB)
        # mock_db.query.return_value.filter.assert_called_with(updated_user == default_user)
        mock_db.query.return_value.filter.return_value.delete.assert_called_once()

        # mock_repo.return_value.create.assert_called_with(default_user)

        assert updated_user.username == default_user.username
        assert updated_user.role == default_user.role
