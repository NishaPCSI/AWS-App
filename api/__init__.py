# import models to generate tables
from api.database import models
from api.database import Base, engine, SessionLocal
from fastapi import FastAPI, Request, Response, Depends
from sqlalchemy.orm import Session
import jwt
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.mount("/static", StaticFiles(directory="api/static"), name="static")

SECRET_KEY = "testfornow"

NO_AUTH_PATHS = ('/user/login','/user/add','/user/logout','/docs','/openapi.json')

@app.middleware("http")
async def handle_jwt_auth(request: Request, call_next):
    if request.scope['path'] not in NO_AUTH_PATHS:
        token = request.cookies.get('jwt')
        
        if token is None:
            # if token doesnt exist, the user is not logged in, throw unauthenticated error
            return Response("Unauthenticated",status_code=401)

        try:
            # try to extract data from the given jwt token and validate it
            request.state.payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # if the token is expired, throw expired error
            return Response("Expired Token",status_code=403)

        except Exception as e:
            print(e)
            # cookie has invalid token, user should check their security
            return Response("Malformed Token",status_code=403)
        
    response = await call_next(request)

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
