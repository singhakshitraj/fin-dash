from collections import defaultdict
from fastapi import APIRouter,Depends,Query,status,HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.connection import newSession
from db.models import FinancialRecord,TransactionType,UserRole
from auth.token import JWTTokenClass
from utils.get_user_role import get_user_role_from_db

router=APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary",summary='Permission Level-ADMIN/ANALYST/VIEWER')
def get_summary(username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession)):
    
    rows=db.query(
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total"),
        func.count(FinancialRecord.id).label("count"),
    ).group_by(FinancialRecord.type).all()
    total_income=0.0
    total_expenses=0.0
    record_count=0
    
    for row in rows:
        if row.type==TransactionType.INCOME:
            total_income=float(row.total or 0)
        elif row.type==TransactionType.EXPENSE:
            total_expenses=float(row.total or 0)
        record_count +=row.count

    return {
        "message":"summary fetched successfully",
        "details":{
            "total_income":total_income,
            "total_expenses":total_expenses,
            "net_balance":round(total_income - total_expenses,2),
            "record_count":record_count,
        }
    }

@router.get("/recent",summary='Permission Level-ADMIN/ANALYST/VIEWER')
def get_recent(n:int=Query(default=10,ge=1,le=20),username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession)):

    records=db.query(FinancialRecord).order_by(FinancialRecord.date.desc()).limit(n).all()
    return {
        "message":"recent records fetched successfully",
        "count":len(records),
        "details":[
            {
                "id":r.id,
                "amount":r.amount,
                "type":r.type,
                "category":r.category,
                "description":r.description,
                "date":r.date,
            }
            for r in records
        ]
    }

@router.get("/categorywise",summary='Permission Level-ADMIN/ANALYST')
def get_by_category(username:str=Depends(JWTTokenClass.get_user),db:Session=Depends(newSession)):
    role=get_user_role_from_db(username,db)
    if role not in (UserRole.ANALYST,UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Category breakdown is available to analysts and admins only."
        )

    rows=db.query(
        FinancialRecord.category,
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total"),
    ).group_by(FinancialRecord.category,FinancialRecord.type).all()

    data=defaultdict(lambda:{"total_income":0.0,"total_expenses":0.0})

    for row in rows:
        cat=row.category.value
        if row.type==TransactionType.INCOME:
            data[cat]["total_income"] +=float(row.total or 0)
        else:
            data[cat]["total_expenses"] +=float(row.total or 0)

    breakdown=[
        {
            "category":cat,
            "total_income":round(vals["total_income"],2),
            "total_expenses":round(vals["total_expenses"],2),
            "net":round(vals["total_income"] - vals["total_expenses"],2),
        }
        for cat,vals in sorted(data.items())
    ]

    return {
        "message":"categorywise breakdown fetched",
        "details":breakdown
    }