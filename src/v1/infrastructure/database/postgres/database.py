from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dependencies import SYSTEM


DATABASE_URL = f"postgresql://{SYSTEM.POSTGRES_USER}:{SYSTEM.POSTGRES_PASSWORD}@{SYSTEM.POSTGRES_HOST}:{SYSTEM.POSTGRES_PORT}/{SYSTEM.POSTGRES_DB}"




engine=create_engine(
    DATABASE_URL
)


SessionLocal=sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
)