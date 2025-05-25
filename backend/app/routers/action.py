from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth, database
from ..workers.tasks import execute_action
from ..config import settings

router = APIRouter()

@router.post("/", response_model=schemas.Action)
async def create_action(
    action: schemas.ActionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Create action in database
    db_action = models.Action(
        action_type=action.action_type,
        details=action.details,
        status="pending",
        user_id=current_user.id
    )
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    
    # Execute action in background
    background_tasks.add_task(
        execute_action,
        action_id=db_action.id,
        action_type=action.action_type,
        details=action.details
    )
    
    return db_action

@router.get("/", response_model=List[schemas.Action])
async def read_actions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    actions = db.query(models.Action)\
        .filter(models.Action.user_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return actions

@router.get("/{action_id}", response_model=schemas.Action)
async def read_action(
    action_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    action = db.query(models.Action)\
        .filter(models.Action.id == action_id)\
        .filter(models.Action.user_id == current_user.id)\
        .first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

@router.put("/{action_id}/status", response_model=schemas.Action)
async def update_action_status(
    action_id: int,
    status: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    action = db.query(models.Action)\
        .filter(models.Action.id == action_id)\
        .filter(models.Action.user_id == current_user.id)\
        .first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action.status = status
    db.commit()
    db.refresh(action)
    return action 