from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from auth.token import JWTTokenClass
from db.connection import newSession
from db.models import User,UserRole
from utils.get_user_role import get_user_role_from_db
from db.enums import UserRole


router=APIRouter(prefix="/users",tags=["Users"])

@router.get("/{user_id}")
def get_user_by_id(user_id:int,username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession)):
    role=get_user_role_from_db(username,db)
    if role !=UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view other users.",
        )

    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )

    return {
        'id':user.id,
        'username':user.username,
        'role':user.role,
        'is_active':user.is_active
    }

@router.patch("/{user_id}")
def admin_update_user(user_id:int,username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession),role:UserRole|None=None,is_active:bool|None=None):
    user_role=get_user_role_from_db(username,db)
    if user_role !=UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can modify other users.",
        )
    target=db.query(User).filter(User.id==user_id).first()
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    caller=db.query(User).filter(User.username==username).first()
    if caller and caller.id==user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot modify their own role"
        )
    response={
        'message':'Update Successful!',
        'user_id':user_id,
        'updated_fields':{}
    }
    if role is not None:
        target.role=role
        response['updated_fields']['role']=role
    if is_active is not None:
        target.is_active=is_active
        response['updated_fields']['is_active']=is_active
    db.commit()
    db.refresh(target)

    return response


