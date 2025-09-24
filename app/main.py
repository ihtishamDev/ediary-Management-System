from .models import *
from fastapi import FastAPI
from .db import engine, Base
from .auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth as auth_router, entries as entries_router

# Create DB tables (dev convenience)
Base.metadata.create_all(bind=engine)
app = FastAPI(title='E-Diary API')
origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, 
allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(auth_router.router, prefix='/auth', tags=['auth'])
app.include_router(entries_router.router, prefix='/entries', tags=['entries'])
# app.include_router(attachments_router.router, prefix='/attachments',
# tags=['attachments'])
# small /me route
from fastapi import Request
from fastapi.responses import JSONResponse
@app.get('/auth/me')
def me(request: Request):
    user = get_current_user(request)
    return JSONResponse({"id": user.id, "name": user.name, "email": user.email,
"created_at": str(user.created_at)})
