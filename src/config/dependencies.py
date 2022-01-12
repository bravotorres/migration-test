from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.data.base import SessionLocal
from src.data.models import Commerce


# In this case, HTTP Basic security
security = HTTPBasic()


def get_db():
    """
    Generate a DataBase session as a coroutine to can use as a Dependency.
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_api_key(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    # In this simple case, the username contain an API key saved as an attribute of Commerce
    api_key = credentials.username
    commerce = db.query(Commerce).filter(Commerce.api_key == api_key).first()

    if not commerce:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access is not valid.")

    return commerce
