from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from peewee import *
import pydantic
from playhouse.shortcuts import model_to_dict
from models import *

import re
class TaskResponse(pydantic.BaseModel):
    id: int
    name: str
    level_count: int
    description: str
    location: str
    status: int

class UserProfile(pydantic.BaseModel):
    id: int
    username: str
    name: str
    surname: str
    email: str
    password: str
    level: int
    xp: int

class TeamResponse(pydantic.BaseModel):
    id: int
    name: str
    description: str
    participants: str


db = SqliteDatabase("db/database.db")

app = FastAPI()

with db:
    db.create_tables([Team, User, Task, Check_Task, Check_Team])

    '''@app.post("/check_user")
    async def check_user(email: str):
        users = User.select()
        all_email = [user.email for user in users]
    '''

    #USER

    @app.post("/authorization")
    def authorization(email: str, password: str):
        if User.select().where(User.email == email):
            if User.select().where(User.password == password):
                for user in User.select().where(User.password == password):
                    return user.id
            else:
                return -1
        else:
            return -2


    @app.post("/register")
    def register(username: str, name: str, surname: str, email: str, password: str):
        pattern = "^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$"
        match = re.fullmatch(pattern, email)
        if match:
            register = [
                 {"username": username, "name": name, "surname": surname, "email": email, "password": password,
                    "level": 1}
            ]
            return model_to_dict(User.insert_many(register).returning(User.id).execute()[0])['id']
        else:
            return 0


    @app.get("/hello")
    def hello():
        return "DONE"

    #TASK

    @app.post("/create_task")
    def create_task(name: str, level_count: int, description: str, location: str):
        task = [
            {"name": name, "level_count": level_count, "description": description, "location": location}
        ]
        Task.insert_many(task).execute()

    @app.post("/change_status")
    def change_status1(id_task: int, status:  int):
        q = Task.update({Task.status: status}).where(Task.id == id_task)
        q.execute()
        return "DONE"


    @app.get("/get_alltasks", response_model=list[TaskResponse])
    def get_all_task():
        return list(map(model_to_dict, Task.select().where(Task.status == 0)))


    #TEAM

    @app.post("/create_team")
    def create_team(name: str, description: str, userId):
        team = [
           {"name": name, "participants": "", "userId": userId, "description": description} # !!! need to add a list of team members
        ]
        Team.insert_many(team).execute()



    @app.get("/get_allteams", response_model=list[TeamResponse])
    def get_all_teams():
        return list(map(model_to_dict, Team.select()))

    @app.post("/invite_team")
    def invite_team(offer: str, teamId: int, userId: int):
        check_team = [
            {"offer": offer, "teamId": teamId, "userId": userId}
        ]
        Check_Team.insert_many(check_team).execute()
        return "lol"

    #CHECK TASK(FOR ADMIN)

    @app.post("/response_task")
    def response_task(offer: str, taskId: int, userId: int):
        check_task = [
            {"offer": offer, "taskId": taskId, "userId": userId}
        ]
        Check_Task.insert_many(check_task).execute()
        q = Task.update({Task.status: 1}).where(Task.id == taskId)
        q.execute()

    @app.post("/check_ready_task")
    def check_ready_task(taskId: int):
        check_ready_task = [
            {"offer": "СДЕЛАНО", "taskId": taskId, "userId": 0}
        ]
        Check_Task.insert_many(check_ready_task).execute()

    @app.post("/get_xp")
    def get_xp(userId: int, taskId: int):
        for task in Task.select().where(Task.id == taskId):
            taskXp = task.level_count
            q = User.update({User.xp: User.xp + taskXp}).where(User.id == userId)
            q.execute()

    @app.get("/check_status", response_model=TaskResponse) #check status for user
    def check_status(taskId: int):
        res = model_to_dict(Task.select().where(Task.id == taskId)[0])
        return res



    @app.get("/get_allchecktasks")
    def get_all_check_task():
        return list(Check_Task.select())

    # USER_PROFILE
    @app.get("/get_user_profile", response_model=UserProfile)
    def get_user_profile(user_id: str):
        res = model_to_dict(User.select().where(User.id == user_id)[0])
        print(res)
        return res

    # PLAY
    @app.get("/get_user_level")
    def get_user_level(user_id: int):
        for user in User.select().where(User.id == user_id):
            print(user.level)
            return user.level

    @app.post("/change_level")
    def change_level(user_id: int):
        q = User.update({User.level: User.level + 1}).where(User.id == user_id)
        q.execute()




    '''@app.post("/files/")
    async def create_file(file: Annotated[bytes, File()]):
        return {"file_size": len(file)}


    @app.post("/uploadfile/")
    async def create_upload_file(file: UploadFile):
        avatar = file.filename'''

