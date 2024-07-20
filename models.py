from peewee import *

db = SqliteDatabase('db/database.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Team(BaseModel):
    name = CharField()
    participants = CharField()
    description = CharField()
    userId = IntegerField()

    class Meta:
        db_table = 'teams'


class User(BaseModel):
    username = CharField(unique=True)
    name = CharField()
    surname = CharField()
    email = CharField(unique=True)
    password = CharField()
    level = IntegerField()
    xp = IntegerField(default=0)
    class Meta:
        db_table = 'users'

class Task(BaseModel):
    name = CharField()
    level_count = IntegerField()
    description = CharField()
    location = CharField()
    status = IntegerField(default=0)
    class Meta:
        db_table = 'tasks'

class Check_Task(BaseModel):
    offer = CharField()
    taskId = IntegerField()
    userId = IntegerField()

    class Meta:
        db_table = "check_task"

class Check_Team(BaseModel):
    offer = CharField()
    teamId = IntegerField()
    userId = IntegerField()
    class Meta:
        db_table = "checkInviteToTeam"


