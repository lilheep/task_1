from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from models import Roles, Users, Staffs, Students, db_connection
from peewee import Model, DoesNotExist, ForeignKeyField
from typing import List, Any, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_to_db():
    if db_connection.is_closed():
        db_connection.connect()
    try:
        yield
    
    finally:
        if not db_connection.is_closed():
            db_connection.close()
        
models_db = {
    'roles': Roles,
    'users': Users,
    'staffs': Staffs,
    'students': Students
}

def validation_data(instance: Model, fields: List[str]) -> Dict[str, Any]:
    data = {}
    
    for field in fields:
        value = getattr(instance, field)
        if isinstance(value, Model):
            value = value.id
        data[field] = value
        
    return data

@app.get('/{table_name}/', response_model=List[Dict[str, Any]])
async def get_all_records(table_name: str, db=Depends(connect_to_db)):
    if table_name not in models_db:
        raise HTTPException(status_code=404, detail=f'Table {table_name} not found!')
    
    model = models_db[table_name]
    fields = [field.name for field in model._meta.sorted_fields]
    records = model.select()
    
    if records.exists():
        return [validation_data(record, fields) for record in records]
        
    return [{'field': field} for field in fields]
    
@app.get('/{table_name}/{record_id}/', response_model=List[Dict[str, Any]])
def get_record(table_name: str, record_id: int, db=Depends(connect_to_db)):
    
    if table_name not in models_db:
        raise HTTPException(status_code=404, detail=f'Table {table_name} not found!')
    
    model = models_db[table_name]
    fields = [field.name for field in model._meta.sorted_fields]
    try:
        record = model.get(model.id == record_id)
        return [validation_data(record, fields)]
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'Record with id {record_id} not found!')
    
@app.post('/{table_name}', response_model=List[Dict[str, Any]])
async def create_record(table_name: str, data: dict = Body(...), db=Depends(connect_to_db)):
    if table_name not in models_db:
        raise HTTPException(status_code=404, detail=f'Table {table_name} not found!')

    model = models_db[table_name]
    fields = [field.name for field in model._meta.sorted_fields if not field.primary_key]

    record_data = {}
    for field in fields:
        if field in data:
            field_value = data[field]

            if isinstance(model._meta.fields[field], ForeignKeyField):
                related_model = model._meta.fields[field].rel_model
                try:
                    field_value = related_model.get(related_model.id == field_value)
                except DoesNotExist:
                    raise HTTPException(status_code=400, detail=f'Invalid foreign key value for {field}!')
            record_data[field] = field_value

    missing_fields = [f for f in fields if f not in record_data or record_data[f] is None]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")

    try:
        record = model.create(**record_data)
        return [validation_data(record, fields)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating record: {str(e)}")

@app.put('/{table_name}/{record_id}/', response_model=List[Dict[str, Any]])
async def update_record(table_name: str, record_id: int, data = Dict[str, Any], db=Depends(connect_to_db)):
    
    if table_name not in models_db:
        raise HTTPException(status_code=404, detail=f'Table {table_name} not found!')
    
    model = models_db[table_name]
    fields = [field.name for field in model._meta.sorted_fields if not field.primary_key]
    
    try:
        record = model.get(model.id == record_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'Record with id {record_id} not found!')
    
    for field in fields:
        if field in data:
            field_value = data[field]
            if isinstance(model._meta.fields[field], Model):
                related_model = model._meta.fields[field].rel_model
                try:
                    field_value = related_model.get(related_model.id == field_value)
                except DoesNotExist:
                    raise HTTPException(status_code=400, detail=f'Invalid foreign key value for {field}!')
            
            setattr(record, field, field_value)
            
    record.save()
    validation_data(record, [field.name for field in model._meta.sorted_fields])
    
@app.delete('/{table_name}/{record_id}/', response_model=List[Dict[str, Any]])
async def delete_record(table_name: str, record_id: int, db=Depends(connect_to_db)):

    if table_name not in models_db:
        raise HTTPException(status_code=404, detail=f'Table {table_name} not found!')
    
    model = models_db[table_name]
    try:
        record = model.get(model.id == record_id)
        record.delete_instance()
        return [{'messsage': 'Record deleted successfully!'}]
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'Record with id {record_id} not found!')
    
@app.get('/')

def root():
    return {'message': 'Welcome!'}