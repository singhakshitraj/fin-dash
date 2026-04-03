from fastapi import FastAPI
from routers import users,auth,records
app =FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)