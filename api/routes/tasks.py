from api import app, get_db
from api.database import schema, models
from sqlalchemy.orm import Session
from fastapi import Depends, Response, Request 
from typing import List
from uuid import uuid4
from datetime import datetime, timedelta

@app.get("/task/all", response_model=List[schema.TaskOut])
async def get_all_task(request: Request, db: Session = Depends(get_db)):
    _user_tasks = db.query(models.Task).filter(models.Task.uid == request.state.payload['uid']).all()
    return _user_tasks

TASK_DEADLINES = {
        models.Priority.Low : 0,
        models.Priority.Medium : 1,
        models.Priority.High : 2,
        models.Priority.Critical : 3,
    }

async def get_offset_timestamp(deadline: int, priority: models.Priority) -> int:
    dt = datetime.fromtimestamp(deadline/1000) 
    delta = timedelta(days = TASK_DEADLINES[priority])
    return ((dt - delta).timestamp()*1000).__floor__()

@app.post("/task/add")
async def add_task(task: schema.TaskIn, request: Request, db: Session = Depends(get_db)):
    task_dict = task.dict()
    print(task_dict)
    _tid = str(uuid4())
    task_dict.update({'uid':request.state.payload['uid'], 'tid': _tid})
    days = TASK_DEADLINES[task_dict['priority']]
    db.add(models.Task(**task_dict))
    db.add(models.Notification(
        content = f"Task is due in {days} days.",
        uid = task_dict['uid'],
        tid = _tid,
        pid = task_dict['pid'],
        date_added = await get_offset_timestamp(task_dict['deadline'],task_dict['priority'])
    ))
    db.commit()
    return task_dict

# remove task
@app.post("/task/remove/{tid}")
async def remove_task(tid: str, db: Session = Depends(get_db)):
    db.query(models.Task).filter(models.Task.tid == tid).delete()
    db.query(models.Notification).filter(models.Notification.tid == tid).delete()
    db.commit()
    return Response(status_code=200)

# change task details 
@app.post("/task/change")
async def change_task_details(task:schema.TaskUpdate, db: Session = Depends(get_db)):

    db.query(models.Task).filter(models.Task.tid == task.tid).update(values=task.dict(exclude_unset=True))
    updated_task = db.query(models.Task).filter(models.Task.tid == task.tid).first()
    assert updated_task is not None
    values = {
            'date_added' : await get_offset_timestamp(updated_task.deadline,updated_task.priority),
            'content' : f"Task is due in {TASK_DEADLINES[updated_task.priority]} days."
            }
    db.query(models.Notification).filter(models.Notification.tid ==  task.tid).update(values=values)
    db.commit()
    return Response(status_code=200)
