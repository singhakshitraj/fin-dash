from fastapi import FastAPI,Depends,HTTPException
from routers import users,auth,records,dashboard
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.connection import newSession

app =FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get('/',summary='Health Check')
def health_check(session: Session = Depends(newSession)):
    try:
        session.execute(text("SELECT 1"))
        return {"api health":"ok","db health": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not reachable")