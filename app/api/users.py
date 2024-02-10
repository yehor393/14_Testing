from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from dependencies.database import get_db, SessionLocal
from dependencies.auth import Token, create_access_token, get_current_user, DefaultUser
from dependencies.rate_limiter import RateLimiter
from schemas.user import User, Email
from services.users import UserServices
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from dependencies.emails import send_email
from dependencies.cloudinary_client import get_uploader

from schemas.user import UserActivation

router = APIRouter()

rate_limiter = RateLimiter(3, 120)


async def rate_limit(request: Request):
    # rate_limiter = RateLimiter(3, 120)
    global rate_limiter
    client_id = request.client.host
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    return True


@router.post("/register/", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: User,
                   db: SessionLocal = Depends(get_db),
                   rl=Depends(rate_limit)):
    user_service = UserServices(db)
    return user_service.create_new(user)


@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: SessionLocal = Depends(get_db)):
    user_service = UserServices(db)
    user = user_service.get_user_for_auth(form_data.username, form_data.password)
    access_token = create_access_token(username=user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected-resource/", response_model=User)
async def protected_resource(current_user: DefaultUser, rl=Depends(rate_limit)):
    return current_user


@router.post("/check_email/", response_model=Email)
async def check_email(email_data: Email,
                      db: SessionLocal = Depends(get_db)):
    send_email("Test", "Hello from FastAPI", email_data.email)
    print(email_data)
    return email_data


@router.post("/activate/", response_model=User)
async def activate(data: UserActivation,
                   db: SessionLocal = Depends(get_db)):
    user_service = UserServices(db)
    return user_service.activate_user(data)


@router.post("/upload_image")
def upload(current_user: DefaultUser,
           file: UploadFile = File(...),
           uploader=Depends(get_uploader),
           db: SessionLocal = Depends(get_db)):
    try:
        user_service = UserServices(db)
        contents = file.file.read()
        responce = uploader.upload(contents, public_id=file.filename)
        responce.get('secure_url')
        user_service.set_image(current_user, responce.get('secure_url'))

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
