from api import app, get_db
from api.database import schema, models
from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import Depends, Response, Request
from typing import List
from datetime import datetime

# list all projects the current user is in 
@app.get("/project/all", response_model=List[schema.ProjectOut])
async def get_all_projects(request: Request, db: Session = Depends(get_db)):
    _user_projects = db.query(models.Project).join(models.UserXProject).filter(models.UserXProject.uid == request.state.payload['uid']).all()
    return _user_projects

# add user to project
@app.post("/project/adduser/{email}/{project_id}")
async def link_project(email:str,project_id:str,request: Request, db: Session = Depends(get_db)):
    user:models.User|None = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        return Response("User doesnt exist",status_code=403)

    if db.query(models.Project).filter(and_(
        models.Project.pid == project_id,
        models.Project.uid == request.state.payload['uid']
    )).first() is None:
        return Response("Forbidden, you dont own this project",status_code=403)
    
    if db.query(models.UserXProject).filter(and_(
        models.UserXProject.pid == project_id,
        models.UserXProject.uid == user.uid
    )).first() is not None:
        return Response("User already added in this project",status_code=403)

    _project:models.Project|None = db.query(models.Project).filter(models.Project.pid == project_id).first()
    if _project is None:
        return Response("Project doesnt exist", 403)
    
    db.add(models.UserXProject(
        uid = user.uid,
        pid = project_id
    ))

    db.add(models.Notification(
        uid = user.uid,
        tid = None,
        pid = project_id,
        content = f"You have been added to a project : {_project.name} ",
        date_added = (datetime.now().timestamp()*1000).__floor__()
    ))

    db.commit()
    return Response(status_code=200)

# remove user from project
@app.post("/project/removeuser/{email}/{project_id}")
async def unlink_project(email:str,project_id:str,request:Request, db: Session = Depends(get_db)):
    user:models.User|None = db.query(models.User).filter(models.User.email == email).first()
    
    if user is None:
        return Response("User doesnt exist",status_code=403)

    if db.query(models.Project).filter(and_(
        models.Project.pid == project_id,
        models.Project.uid == request.state.payload['uid']
    )).first() is None:
        return Response("Forbidden, you dont own this project",status_code=403)

    _project:models.Project|None = db.query(models.Project).filter(models.Project.pid == project_id).first()
    if _project is None:
        return Response("Project doesnt exist", 403)
        
    if _project.uid == user.uid:
        return Response("Owner cannot be removed from project",status_code=403)

    db.add(models.Notification(
        uid = user.uid,
        tid = None,
        pid = project_id,
        content = f"You have been removed from a project : {_project.name} ",
        date_added = (datetime.now().timestamp()*1000).__floor__()
    ))

    # remove the link between user and project
    db.query(models.UserXProject).filter(and_(
        models.UserXProject.pid == project_id,
        models.UserXProject.uid == user.uid
        )).delete()
        
    # delete all tasks of user linked to the project
    db.query(models.Task).filter(and_(
        models.Task.pid == project_id,
        models.Task.uid == user.uid
        )).delete()
    # commit 
    db.commit()

    return Response(status_code=200)

# get project members
@app.get("/project/members/{pid}", response_model=List[schema.UserOut])
async def get_project_members(pid:str, db:Session = Depends(get_db)):
    _project = db.query(models.UserXProject).filter(models.UserXProject.pid == pid).all()
    return [entry.users for entry in _project]