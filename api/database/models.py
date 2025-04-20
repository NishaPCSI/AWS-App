from . import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from uuid import uuid4
import enum
from datetime import datetime

class ProjectPhase(int, enum.Enum):
    Planning = 0
    Designing = 1
    Implementing = 2
    Testing = 3
    Deployed = 4
    
class TaskStatus(int, enum.Enum):
    NotTouched = 0
    Working = 1
    Finished = 2
    Halted = 3

class Priority(int, enum.Enum):
    Low = 0
    Medium = 1
    High = 2
    Critical = 3

class User(Base):
    __tablename__ = "users"
    uid = Column(String, primary_key=True, index=True, default=lambda:str(uuid4()))
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    dob = Column(Integer)
    avatar = Column(Boolean, default=False)

class Task(Base):
    __tablename__ = "tasks"
    # unique Task id
    tid = Column(String, primary_key=True, default=lambda:str(uuid4()))
    # task name
    name = Column(String(16), nullable=False)
    # task description
    description = Column( String, nullable=True)
    # deadline : timestamp
    deadline = Column( Integer, nullable=True)
    # priority
    priority = Column(Enum(Priority), nullable=False)
    # status 
    status = Column(Enum(TaskStatus), nullable=False)
    # linked project
    pid = Column( ForeignKey('projects.pid'))
    project = relationship('Project', foreign_keys=[pid])
    # notify
    notify = Column(Boolean,nullable=False)
    # which user owns the task : uid (foreign key)
    uid = Column( ForeignKey('users.uid'))
    users = relationship('User', foreign_keys=[uid])


class Project(Base):    
    __tablename__ = 'projects'
    # pid : project id
    pid = Column(String, primary_key=True, default=lambda: str(uuid4()))
    # project name
    name = Column(String(50),nullable=False)
    # phase (enum)
    phase = Column(Enum(ProjectPhase),nullable=False)
    # type (lmao?)
    # owner of the project
    uid = Column(ForeignKey('users.uid'))
    description = Column(String)

class Notification(Base):
    __tablename__ = 'notifications'
    content = Column(String, nullable=False)
    # notification id
    nid = Column(String, primary_key=True, default=lambda:str(uuid4()))
    # user id
    uid = Column(ForeignKey('users.uid'))
    # task id
    tid = Column(ForeignKey('tasks.tid'))
    # project id
    pid = Column(ForeignKey('projects.pid'))
    # date shown
    date_added = Column(Integer, default=lambda:(datetime.now().timestamp()*1000).__floor__())

class UserXProject(Base):
    # link table for users connected with projects
    __tablename__ = 'userxproject'
    # user id 
    uid = Column(ForeignKey('users.uid'), primary_key = True)
    # project id
    pid = Column(ForeignKey('projects.pid'), primary_key = True)
    # user objects
    users = relationship('User', foreign_keys=[uid])

class Notes(Base):
    __tablename__ = 'notes'
    uid = Column(ForeignKey('users.uid'))
    nid = Column(String, primary_key=True, default=lambda:str(uuid4()))
    content = Column(String, nullable=False)