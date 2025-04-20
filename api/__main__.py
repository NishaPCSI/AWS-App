import uvicorn
# import routes to add all api routes from route module
from api import routes

uvicorn.run("api:app", host='0.0.0.0',port=8000, log_level="info")