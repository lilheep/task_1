"""Создание модуля"""
from peewee import SqliteDatabase, Model, TimeField, IntegerField, TextField,\
                    ForeignKeyField, CharField

db = SqliteDatabase('sqlite.db')

class DB(Model):
    """class DB(Model)"""
    class Meta:
        """class Meta"""
        database = db
        
class Users(DB):
    """Таблица хранения пользователей"""
    id = IntegerField(primary_key=True)
    user_name = CharField(max_length=20)
    password = CharField(max_length=50) 
    
db.connect()
db.create_tables([Users], safe=True)
db.close()
