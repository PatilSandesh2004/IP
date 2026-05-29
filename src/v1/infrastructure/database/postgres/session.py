from infrastructure.database.postgres.database import (
    SessionLocal
)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()