from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from typing import Optional

def create_task(db: Session, task: TaskCreate) -> Task:
    """ Creates new task in the db and returns the new task. """
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()  # Commits the new task to the db immediately
    db.refresh(db_task)  # Updates db_task with the latest db state (like git pull)
    return db_task

def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Returns the first match or None if no match found. """
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """ Returns max 100 rows. """
    return db.query(Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """ Given an id, updates the corresponding task. Returns the updated task or None if no match found. """
    db_task = get_task(db, task_id)
    
    if not db_task:
        return None  
    
		# Only update fields the client explicitly sent (exclude_unset=True)
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()  # Commits changes to the db immediately
    db.refresh(db_task)  # Updates db_task with the latest db state (like git pull)
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    """ Given an id, deletes the corresponding task. Returns True if successful, False if no match found. """
    db_task = get_task(db, task_id)
    
    if not db_task:
        return False 

    db.delete(db_task)
    db.commit()  # Commits deletion to the db immediately
    return True