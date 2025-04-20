from pydantic import BaseModel, EmailStr
from .models import TaskStatus, ProjectPhase, Priority
from typing import Optional

class AbstractORM(BaseModel):
    class Config:
        orm_mode = True

class UserIn(AbstractORM):
    fullname : str
    email : EmailStr
    password : str
    dob : int 

class UserOut(AbstractORM):
    fullname : str
    email : EmailStr
    dob : int 
    uid: str
    avatar: bool 

class UserUpdate(AbstractORM):
    uid : str
    fullname : Optional[str]
    email : Optional[EmailStr]
    password : Optional[str]
    dob : Optional[int]

class UserLogin(AbstractORM):
    email : EmailStr
    password : str

class TaskIn(AbstractORM):
    name : str
    description : Optional[str]
    deadline : int 
    priority : Priority
    status : TaskStatus
    pid : Optional[str]
    notify : bool


class TaskUpdate(AbstractORM):
    tid: str
    name : Optional[str] 
    description : Optional[str]
    deadline : Optional[int]
    priority : Optional[Priority]
    status : Optional[TaskStatus]
    pid : Optional[str]
    notify : Optional[bool]

class ProjectIn(AbstractORM):
    name: str
    phase : ProjectPhase
    description : str
    # type: ??

class TaskOut(TaskIn):
    tid: str
    project: Optional[ProjectIn]
    users: Optional[UserOut]

class ProjectOut(ProjectIn):
    uid: str
    pid: str

class ProjectUpdate(AbstractORM):
    pid : str
    name: Optional[str]
    phase : Optional[ProjectPhase]
    description : Optional[str]
    # type: ??


class NotificationIn(AbstractORM):
    uid : str
    pid : Optional[str]
    tid : Optional[str]
    content : str

class NotificationOut(NotificationIn):
    nid : str
    date_added: int

class UserXProject(AbstractORM):
    uid : str
    pid : str

class NoteIn(AbstractORM):
    content : str

class NoteOut(NoteIn):
    nid : str