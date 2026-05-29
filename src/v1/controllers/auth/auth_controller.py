from sqlalchemy.orm import Session

from services.auth.auth_service import AuthService


class AuthController:

    def __init__(self):
        self.service = AuthService()

    async def signup(
            self,
            db: Session,
            name: str,
            email: str,
            password: str
    ):

        return await self.service.signup(db, name, email, password)

    async def login(
            self,
            db: Session,
            email: str,
            password: str
    ):

        return await self.service.login(db, email, password)