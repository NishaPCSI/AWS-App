from api import app, get_db
from fastapi import Depends, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.database import models, schema
from datetime import datetime
from typing import List

# get notifications
@app.get("/notification/all", response_model=List[schema.NotificationOut])
async def get_notifications(request: Request, db:Session = Depends(get_db)):
    _resp = db.query(models.Notification).filter(and_(
        models.Notification.uid == request.state.payload['uid'],
        models.Notification.date_added <= (datetime.now().timestamp()*1000).__floor__(),
        )).all()
    return _resp

# remove notification
@app.post("/notification/remove/{nid}")
async def remove_task(nid: str, db: Session = Depends(get_db)):
    db.query(models.Notification).filter(models.Notification.nid == nid).delete()
    db.commit()
    return Response(status_code=200)
