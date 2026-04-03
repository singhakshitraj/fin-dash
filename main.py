from fastapi import FastAPI
from routers import users,auth,records,dashboard
app =FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)