from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone
import os
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='auth/login')

class JWTTokenClass:
    @staticmethod
    def generate_token(user):
        #print(str(user.id),user.username,datetime.now(timezone.utc),datetime.now(timezone.utc) + timedelta(minutes=60))
        payload={
            "username":user['username'],
            "iat":datetime.now(timezone.utc),
            "exp":datetime.now(timezone.utc) + timedelta(minutes=60)
        }
        token=jwt.encode(
            payload,
            os.environ.get('SECRET_KEY'),
            algorithm=os.environ.get('ALGORITHM')
        )
        return token
    @staticmethod
    def get_user(token:str=Depends(oauth2_scheme)):
        try:
            payload=jwt.decode(
                token,
                os.environ.get('SECRET_KEY'),
                algorithms=[os.environ.get('ALGORITHM')]
            )

            username=payload.get("username")

            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token:missing subject"
                )
            return username

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )