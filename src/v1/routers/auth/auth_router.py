from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from controllers.auth.auth_controller import AuthController
from infrastructure.database.postgres.session import get_db
from schemas.auth.auth_schema import AuthResponseSchema
from schemas.auth.auth_schema import LoginRequestSchema
from schemas.auth.auth_schema import SignupRequestSchema


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

controller = AuthController()


@router.post("/signup", response_model=AuthResponseSchema)
async def signup(
        request: SignupRequestSchema,
        db: Session = Depends(get_db)
):

    try:
        user = await controller.signup(
            db=db,
            name=request.name,
            email=request.email,
            password=request.password
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return AuthResponseSchema(
        user_id=user.id,
        name=user.name,
        email=user.email,
        access_token=user.auth_token
    )


@router.post("/login", response_model=AuthResponseSchema)
async def login(
        request: LoginRequestSchema,
        db: Session = Depends(get_db)
):

    try:
        user = await controller.login(
            db=db,
            email=request.email,
            password=request.password
        )
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))

    return AuthResponseSchema(
        user_id=user.id,
        name=user.name,
        email=user.email,
        access_token=user.auth_token
    )