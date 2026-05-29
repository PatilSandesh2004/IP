import hashlib
import hmac
import uuid

from sqlalchemy.orm import Session

from models.user_model import User


class AuthService:

    def _hash_password(self, password: str, salt: str | None = None):

        salt = salt or uuid.uuid4().hex
        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            120000
        ).hex()

        return f"{salt}${derived_key}"

    def _verify_password(self, password: str, stored_hash: str):

        salt, _, _ = stored_hash.partition("$")
        recalculated = self._hash_password(password, salt)

        return hmac.compare_digest(recalculated, stored_hash)

    async def signup(
            self,
            db: Session,
            name: str,
            email: str,
            password: str
    ):

        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            name=name,
            email=email,
            password_hash=self._hash_password(password),
            auth_token=str(uuid.uuid4())
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    async def login(
            self,
            db: Session,
            email: str,
            password: str
    ):

        user = db.query(User).filter(User.email == email).first()

        if not user or not self._verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        user.auth_token = str(uuid.uuid4())
        db.commit()
        db.refresh(user)

        return user