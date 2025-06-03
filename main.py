from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
import uvicorn

DATABASE_URL = "postgresql://bisan_unsa_user:Du1q6HeIUWxIqL4qSK4nNO6BegSMoDsm@dpg-d05n0c3uibrs73fs4eo0-a.oregon-postgres.render.com/bisan_unsa"
engine = create_engine(DATABASE_URL, client_encoding='utf8')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str 

class Task(BaseModel):
    task: str
    deadline: str 
    user: str

@app.post("/login/")
async def user_login(user: User):
    with engine.begin() as conn:
        query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        result = conn.execute(query, {"username": user.username, "password": user.password}).fetchone()
        if result:
            return {"status": "Logged in"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/create_user/")
async def create_user(user: User):
    with engine.begin() as conn:
        # Check if user exists
        query = text("SELECT * FROM users WHERE username = :username")
        result = conn.execute(query, {"username": user.username}).fetchone()
        if result:
            raise HTTPException(status_code=400, detail="User already exists")

        try:
            query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            conn.execute(query, {"username": user.username, "password": user.password})
            return {"status": "User Created"}
        except IntegrityError:
            raise HTTPException(status_code=500, detail="Error creating user")

@app.post("/create_task/")
async def create_task(task: Task):
    with engine.begin() as conn:
        try:
            query = text("INSERT INTO tasks (task, deadline, user) VALUES (:task, :deadline, :user)")
            conn.execute(query, {"task": task.task, "deadline": task.deadline, "user": task.user})
            return {"status": "Task Created"}
        except IntegrityError:
            raise HTTPException(status_code=500, detail="Error creating task")

@app.get("/get_tasks/")
async def get_tasks(name: str):
    with engine.begin() as conn:
        query = text("SELECT task, deadline FROM tasks WHERE user = :username")
        result = conn.execute(query, {"username": name}).fetchall()
        tasks = [{"task": row[0], "deadline": row[1]} for row in result]
        return {"tasks": tasks}
