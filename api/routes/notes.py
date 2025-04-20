from api import app, get_db
from typing import List
from api.database import schema,models
from fastapi import Request, Depends, Response
from sqlalchemy.orm import  Session

# get all notes
@app.get("/note/all", response_model=List[schema.NoteOut])
async def get_all_notes(request: Request, db: Session = Depends(get_db)):
    _user_notes = db.query(models.Notes).filter(models.Notes.uid == request.state.payload['uid']).all()
    return _user_notes

# add notes
@app.post("/note/add")
async def add_note(note: schema.NoteIn, request: Request, db: Session = Depends(get_db)):
    note_dict = note.dict()
    note_dict.update({'uid':request.state.payload['uid']})
    db.add(models.Notes(**note_dict))
    db.commit()
    return note_dict

# remove note
@app.post("/note/remove/{nid}")
async def remove_note(nid: str, db: Session = Depends(get_db)):
    db.query(models.Notes).filter(models.Notes.nid == nid).delete()
    db.commit()
    return Response(status_code=200)

# change note 
@app.post("/note/change")
async def change_note_details(note:schema.NoteOut, db: Session = Depends(get_db)):
    db.query(models.Notes).filter(models.Notes.nid == note.nid).update(values=note.dict(exclude_unset=True))
    db.commit()
    return Response(status_code=200)

