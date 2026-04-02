from sqlalchemy.orm import Session
from db.models import User
from fastapi import HTTPException

def get_user_role_from_db(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.role