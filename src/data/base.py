from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.settings import get_api_settings

settings = get_api_settings()
SQLALCHEMY_DATABASE_URL = settings.DATABASE_STRING

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == '__main__':
    from src.data.models import Employee, Commerce

    db = SessionLocal()
    key = "5a25c9f25c334f4197df4d2aafca5fd9"
    # key = "5a25c9f25c334f4197df4d2aafca5fda"
    commerce = db.query(Commerce).filter(Commerce.api_key == key).first()

    if commerce:
        f = commerce.trabajadores
        [print(i.nombre_completo) for i in f]

        print("You are in!")

    else:
        print("Get out here!")
