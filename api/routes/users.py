from api import app, get_db
from api.database import schema, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, Request
from api.utils import jwt_helper,password
from sqlalchemy import and_
from typing import List

@app.get("/user/me", response_model=schema.UserOut)
async def get_user(request: Request , db: Session = Depends(get_db)):
    _user = db.query(models.User).filter(models.User.uid == request.state.payload['uid']).first()
    if _user is None:
        raise HTTPException(status_code=404, detail="User account not found")
    return _user

@app.post("/user/add")
async def add_user(user: schema.UserIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first() is not None:
        raise HTTPException(403,"Email is already used by a registered account.")
    user.password = await password.hash_password(user.password)
    db.add(models.User(**user.dict(exclude_unset=True)))
    db.commit()
    return user

@app.post("/user/login")
async def login_user(user: schema.UserLogin,db: Session = Depends(get_db)):
    user.password = await password.hash_password(user.password)
    _user:models.User|None = db.query(models.User).filter(and_(
                models.User.email == user.email,
                models.User.password == user.password
            )).first()

    if _user is None:
        raise HTTPException(403,"Email and password combination is wrong.")

    jwt_token = jwt_helper.create_jwt({'uid':_user.uid})

    response = Response(status_code=200)
    response.set_cookie('jwt', jwt_token, samesite='lax')
    return response

@app.post("/user/logout")
async def logout_user():
    response = Response()
    response.delete_cookie(key='jwt')
    return response


@app.post("/user/change")
async def change_user_details(request:Request,user:schema.UserUpdate, db: Session = Depends(get_db)):
    if user.uid != request.state.payload['uid']:
        return Response("You can Only change your own details",status_code=403)
    _k = user.dict(exclude_unset=True)
    if 'password' in _k:
        _k['password'] = await password.hash_password(_k['password'])
    db.query(models.User).filter(models.User.uid == user.uid).update(values=_k)
    db.commit()
    return Response(status_code=200)

@app.get("/user/email/{email}", response_model=List[schema.UserOut])
async def get_user_by_email(email:str, db:Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email.ilike(f"%{email}%")).all()