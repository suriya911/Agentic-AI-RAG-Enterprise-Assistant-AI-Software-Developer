from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth, database
from ..rag.engine import RAGEngine
from ..config import settings

router = APIRouter()
rag_engine = RAGEngine()

@router.post("/", response_model=schemas.Query)
async def create_query(
    query: schemas.QueryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Get relevant documents from vector store
    relevant_docs = await rag_engine.get_relevant_documents(query.question)
    
    # Generate answer using GPT-4
    answer = await rag_engine.generate_answer(query.question, relevant_docs)
    
    # Store query and answer in database
    db_query = models.Query(
        question=query.question,
        answer=answer,
        user_id=current_user.id
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    return db_query

@router.get("/", response_model=List[schemas.Query])
async def read_queries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    queries = db.query(models.Query)\
        .filter(models.Query.user_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return queries

@router.get("/{query_id}", response_model=schemas.Query)
async def read_query(
    query_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    query = db.query(models.Query)\
        .filter(models.Query.id == query_id)\
        .filter(models.Query.user_id == current_user.id)\
        .first()
    if query is None:
        raise HTTPException(status_code=404, detail="Query not found")
    return query 