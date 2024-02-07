# import urllib
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.todo_items import router as todo_router
from api.users import router as user_router
from services.users import UserServices
from models import todo
from dependencies.auth import create_access_token
from dependencies.database import engine, SessionLocal, get_db
# from fastapi_sso.sso.google import GoogleSSO
from schemas.user import Email

todo.BaseModel.metadata.create_all(bind=engine)

app = FastAPI()

# Додавання CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
)

app.include_router(todo_router, prefix="/todo")
app.include_router(user_router, prefix="/users")

GSSO_CLIENT_SECRET = "YOUR SECRET"
GSSO_CLIENT_ID = "YOUR CLIENT ID"

REDIRECT_URI = "http://localhost:8000/google/callback"


@app.get("/")
async def health_check():
    print()
    return {"OK": True}


@app.post("/get_acces_token")
async def complete_google_login(login: Email, db: SessionLocal = Depends(get_db)):
    user_service = UserServices(db)
    user = user_service.get_by_username(login.email)
    access_token = create_access_token(username=user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}
