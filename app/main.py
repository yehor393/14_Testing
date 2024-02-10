# import urllib
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.todo_items import router as todo_router
from app.api.users import router as user_router
from app.services.users import UserServices
from app.models import todo
from app.dependencies.auth import create_access_token
from app.dependencies.database import engine, SessionLocal, get_db
# from fastapi_sso.sso.google import GoogleSSO
from app.schemas.user import Email

todo.BaseModel.metadata.create_all(bind=engine)

app = FastAPI()

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
    """
    Checks the health of the service.

    This endpoint function is used to perform a liveness check of the web service.
    Returns a status indicating that the service is functioning properly.

    :return: A dictionary confirming that the service is operational.
    :rtype: dict
    """
    return {"OK": True}


@app.post("/get_acces_token")
async def complete_google_login(login: Email, db: SessionLocal = Depends(get_db)):
    """
    Completes the Google login process by generating an access token for the user.

    Receives an email object and a database session, finds the user in the database by their email,
    and generates an access token based on the user's username and role.

    :param login: An object containing the user's email.
    :type login: Email
    :param db: The database session, by default obtained through dependency.
    :type db: SessionLocal
    :return: A dictionary containing the access token and the token type.
    :rtype: dict
    """
    user_service = UserServices(db)
    user = user_service.get_by_username(login.email)
    access_token = create_access_token(username=user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}
