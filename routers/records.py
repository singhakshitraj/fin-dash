from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy.orm import Session
from db.connection import newSession
from db.models import FinancialRecord,TransactionCategory,TransactionType,UserRole
from db.models import User
from auth.token import JWTTokenClass
from utils.get_user_role import get_user_role_from_db
from utils.validation_models.financial_record import FinancialRecordCreateValidation,FinancialRecordUpdateValidation


router=APIRouter(
    prefix="/records",
    tags=["Financial Records"]
)

@router.post("",status_code=status.HTTP_201_CREATED)
def create_record(record:FinancialRecordCreateValidation,username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession)):

    role=get_user_role_from_db(username,db)
    if role not in (UserRole.ANALYST,UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Viewers cannot create financial records.",
        )

    owner=db.query(User).filter(User.username==username).first()

    record=FinancialRecord(
        user_id=owner.id,
        amount=record.amount,
        type=record.type,
        category=record.category,
        description=record.description,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        'message':'record added successfully',
        'details':{
            'user_id':owner.id,
            'amount':record.amount,
            'type':record.type,
            'category':record.category
        }
    }
    
@router.get("")
def list_records(
    type:TransactionType | None=Query(default=None),
    category:TransactionCategory | None=Query(default=None),
    date_from:datetime | None=Query(default=None),
    date_to:datetime | None=Query(default=None),
    limit:int=Query(default=50,ge=1,le=200),
    offset:int=Query(default=0,ge=0),
    username:str=Depends(JWTTokenClass.get_user),
    db:Session=Depends(newSession),
):
    query=db.query(FinancialRecord)

    if type is not None:
        query=query.filter(FinancialRecord.type==type)
    if category is not None:
        query=query.filter(FinancialRecord.category==category)
    if date_from is not None:
        query=query.filter(FinancialRecord.date>=date_from)
    if date_to is not None:
        query=query.filter(FinancialRecord.date<=date_to)

    records=(
        query.order_by(FinancialRecord.date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "message":"records fetched successfully",
        "count":len(records),
        "details":[
            {
                "id":r.id,
                "created_by_user_id":r.user_id,
                "amount":r.amount,
                "type":r.type,
                "category":r.category,
                "description":r.description,
                "date":r.date,
            }
            for r in records
        ]
    }
    
@router.get("/{record_id}")
def get_record(record_id:int,username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession)):

    record=db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Financial record with id={record_id} not found."
        )

    return {
        "message":"record fetched successfully",
        "details":{
            "id":record.id,
            "user_id":record.user_id,
            "amount":record.amount,
            "type":record.type,
            "category":record.category,
            "description":record.description,
            "date":record.date,
        }
    }


# ---------------------------------------------------------------------------
# PATCH /records/{record_id}  (ADMIN,ANALYST)
# ---------------------------------------------------------------------------
@router.patch("/{record_id}")
def update_record(record_id:int,payload:FinancialRecordUpdateValidation,username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession),):
    role=get_user_role_from_db(username,db)
    if role not in (UserRole.ANALYST,UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Viewers cannot update financial records."
        )

    record=db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Financial record with id={record_id} not found."
        )

    update_data=payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No fields provided for update."
        )

    for field,value in update_data.items():
        setattr(record,field,value)

    db.commit()
    db.refresh(record)

    return {
        "message":"record updated successfully",
        "details":{
            "id":record.id,
            "user_id":record.user_id,
            "amount":record.amount,
            "type":record.type,
            "category":record.category,
            "description":record.description,
            "date":record.date,
        }
    }

@router.delete("/{record_id}")
def delete_record(record_id:int,username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession),):
    role=get_user_role_from_db(username,db)
    if role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete financial records."
        )

    record=db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Financial record with id={record_id} not found."
        )
    db.delete(record)
    db.commit()
    return {
        "message":f"Financial record with id={record_id} has been deleted.",
        "deleted_id":record_id
    }