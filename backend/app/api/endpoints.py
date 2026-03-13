from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.api import crud

router = APIRouter(prefix="/tasks", tags=["tasks"])
limiter = Limiter(key_func=get_remote_address)  # Rate limiting applied per IP address

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")  # capped at 10 POST requests/min
def create_task(request: Request, task: TaskCreate, db: Session = Depends(get_db)):
    """ Creates a new task aka POST request. Returns created task with its assigned ID. """
    return crud.create_task(db, task)

@router.get("/{task_id}", response_model=TaskResponse)
@limiter.limit("30/minute")  # capped at 30 single-item GET requests/min (most permissive)
def get_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    """ Returns a task by its ID aka single-item GET. If the task doesn't exist, returns 404 error. """
    db_task = crud.get_task(db, task_id)
    if not db_task:
        # 404 = valid ID valid but missing resource
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")  
    return db_task

@router.get("/", response_model=List[TaskResponse])
@limiter.limit("20/minute")  # capped at 20 list GET requests/min
def get_tasks(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ 
    Returns tasks in paginated form aka list GET.
    `skip` is the number of records to skip, `limit` is the max number of records to return. 
    """
    limit = min(limit, 1000)  # never return >1000 regardless of what client asks
    return crud.get_tasks(db, skip=skip, limit=limit)

@router.put("/{task_id}", response_model=TaskResponse)
@limiter.limit("10/minute")  # capped at 10 PUT requests/min
def update_task(request: Request, task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """ Updates an existing task by its ID aka PUT request. If the task doesn't exist, returns 404 error. """
    db_task = crud.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return db_task

# 204 = response body is empty, a task object won't return
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)  
@limiter.limit("10/minute")
def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    """ Deletes a task by its ID aka DELETE request. If the task doesn't exist, returns 404 error. """
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")