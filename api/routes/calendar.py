from api import app, get_db
from api.database import schema, models
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import Depends, Request
from typing import List

@app.get("/calendar/task/{start}/{end}", response_model=List[schema.TaskOut])
async def tasks_in_range(start: int, end:int,request: Request, db: Session = Depends(get_db)):
    if start == end:
        return db.query(models.Task).filter(and_(
            models.Task.uid == request.state.payload['uid'],
            models.Task.deadline == start,
        )).all()
   
    return db.query(models.Task).filter(and_(
        models.Task.uid == request.state.payload['uid'],
        models.Task.deadline >= start,
        models.Task.deadline < end
    )).all()
