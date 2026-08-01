import bcrypt

from models.current_user import CurrentUser
from services.user_service import UserService


class AuthService:

    @staticmethod
    def login(username, password):

        user = UserService.find_by_username(username)

        if user is None:
            return None

        if not bcrypt.checkpw(
            password.encode(),
            user["password_hash"].encode()
        ):
            return None

        return CurrentUser(
            id=user["id"],
            username=user["username"],
            full_name=user["full_name"],
            role=user["role"]
        )