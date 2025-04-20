from fastapi import UploadFile, File, Response
from api import app, get_db
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from api.database import models
from io import BytesIO

AVATAR_PATH = "api/static/avatars"

@app.post("/upload")
async def upload_avatar(request:Request ,file: UploadFile = File(...), db: Session = Depends(get_db)):
    # images must be png only
    if not file.filename.endswith(".png"):
        return Response("Only PNG images are allowed.",status_code=403)
    try:
        downloaded_content = BytesIO()
        while contents := file.file.read(1024 * 1024):
            # ONLY READ IN 1 MB CHUNKS to stop shitting the server on troll files of 50GB
            if downloaded_content.tell() > 1048576: 
                # THROW ERROR if the file size exceeds 1MB
                del downloaded_content
                return Response('File larger than 1MB size limit',status_code=419)
            downloaded_content.write(contents)
        
        with open(f'{AVATAR_PATH}/{request.state.payload["uid"]}.png', 'wb') as f:
            f.write(downloaded_content.getbuffer())

        db.query(models.User).filter(models.User.uid == request.state.payload['uid']).update(values={'avatar':True})
        db.commit()
    except Exception as e:
        print(e)
        return Response(f'There was an error uploading the file: {e}',status_code=409)
    finally:
        await file.close()

    return Response('Success')
