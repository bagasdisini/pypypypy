from fastapi import FastAPI

from api.users import users_router
from core.config import config
from db.postgresql import init_db

app = FastAPI()

init_db()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(users_router, tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)