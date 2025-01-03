from peewee import Model, CharField, AutoField
from database import db_connection

class BaseModel(Model):
    class Meta:
        database = db_connection


class Users(BaseModel):
    id = AutoField()
    user_name = CharField(max_length=20, unique=True)
    password = CharField(max_length=50, unique=True)

class Staffs(BaseModel):
    id = AutoField()
    staff_name = CharField(max_length=20, unique=True)
    staff_password = CharField(max_length=50, unique=True)
    
class Students(BaseModel):
    id = AutoField()
    student_name = CharField(max_length=20, unique=True)
    student_password = CharField(max_length=50, unique=True)


def initialize_tables():
    '''Creating tables if they does not exists'''
    db_connection.create_tables([Users, Staffs, Students], safe=True)
    print('Tables is initialized')

def initialize_data():
    '''Filing test data to tables'''
    if not Users.select().exists():    
        Users.create(user_name='Vitaliy Mashkov', password='aboba1337')
        Users.create(user_name='Kirill Nasekomoe', password='1Cnepython')
    print('Test data has been filled')

# Initialize
try:
    db_connection.connect()
    initialize_tables()
    initialize_data()
except Exception as e:
    print(f'Error initializing tables: {e}')
finally:
    db_connection.close()