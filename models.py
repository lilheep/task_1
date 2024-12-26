from peewee import Model, MySQLDatabase, IntegrityError, CharField, MySQLDatabase, AutoField

db_connection = MySQLDatabase(
    'users_1',
    user='root', 
    password='root', 
    host='localhost',
    port=3306
)

def initialize_database():
    import pymysql
    connection = pymysql.connect(
        host='localhost',
        user='root', 
        password='root' 
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS users_1")
    cursor.close()
    connection.close()

    db_connection.init(
        'users_1', 
        user='root',
        password='root',
        host='localhost',
        port=3306
    )
    
class BaseModel(Model):
    class Meta:
        database = db_connection

class Users(BaseModel):
    id = AutoField()
    user_name = CharField(max_length=20, unique=True)
    password = CharField(max_length=50, unique=True)

if __name__ == '__main__':
    initialize_database()
    db_connection.connect()
    
    db_connection.create_tables([Users], safe=True)

    if not Users.select().exists():
        
            Users.create(user_name='Vitaliy Mashkov', password='aboba1337')
            Users.create(user_name='Kirill Nasekomoe', password='1Cnepython')

    db_connection.close()
