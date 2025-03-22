# tasks/task_manager.py

from db.init_db import SessionLocal
from db.models import Task

# CRUD básico para Tasks

def create_task(data):
    with SessionLocal() as session:
        task = Task(**data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def get_task_by_id(task_id):
    with SessionLocal() as session:
        return session.query(Task).filter(Task.id == task_id).first()

def update_task(task_id, update_data):
    with SessionLocal() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            for key, value in update_data.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            session.commit()
            session.refresh(task)
            return task
        return None

def delete_task(task_id):
    with SessionLocal() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
            return True
        return False

def list_tasks():
    with SessionLocal() as session:
        return session.query(Task).all()
