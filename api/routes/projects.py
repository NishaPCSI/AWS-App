from api import app, get_db
from api.database import schema, models
from sqlalchemy.orm import Session
from fastapi import Depends, Response, Request 
from uuid import uuid4
from typing import List

# make a new project
@app.post("/project/add")
async def add_project(project: schema.ProjectIn, request: Request, db: Session = Depends(get_db)):
    _puuid = str(uuid4())
    _k = project.dict() | { 'uid' : request.state.payload['uid'], 'pid' : _puuid }
    db.add(models.Project(**_k))
    db.add(models.UserXProject(**{'uid':request.state.payload['uid'], 'pid' : _puuid}))
    db.commit()
    return project.dict()

@app.get("/project/owned",response_model=List[schema.ProjectOut])
async def get_owned_projects(request: Request, db: Session = Depends(get_db)):
    _resp = db.query(models.Project).filter(models.Project.uid == request.state.payload['uid']).all()
    return _resp

# remove project
@app.post("/project/remove/{pid}")
async def remove_task(pid: str, db: Session = Depends(get_db)):
    _p = db.query(models.Project).filter(models.Project.pid == pid)
    db.query(models.Task).filter(models.Task.pid == pid).delete()
    _k = db.query(models.UserXProject).filter(models.UserXProject.pid == pid)
    
    for entries in _k:
        db.add(models.Notification(
            uid = entries.users.uid,
            content = f"Project {_p.first().name} was deleted"
        ))
    
    _p.delete()
    _k.delete()
    db.commit()
    return Response(status_code=200)

# change project details
@app.post("/project/change")
async def change_project_details(project:schema.ProjectUpdate, db: Session = Depends(get_db)):
    db.query(models.Project).filter(models.Project.pid == project.pid).update(values=project.dict(exclude_unset=True))
    db.commit()
    return Response(status_code=200)

@app.get("/project/details/{pid}")
async def get_project_details(pid:str, db: Session = Depends(get_db)):
    _resp = {}
    _tasks: List[models.Task] = db.query(models.Task).filter(models.Task.pid == pid).all()
    _chunk_user_tasks = {}
    for task in _tasks:
        if task.users.fullname in _chunk_user_tasks:
            _chunk_user_tasks[task.users.fullname].append(task)
        else:
            _chunk_user_tasks[task.users.fullname] = [task]
    _resp['project'] = db.query(models.Project).filter(models.Project.pid == pid).first()
    _resp['tasks'] = _chunk_user_tasks
    return _resp