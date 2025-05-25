from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from .. import models, schemas, auth, database
from ..rag.engine import RAGEngine
from ..config import settings

router = APIRouter()
rag_engine = RAGEngine()

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}

def allowed_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/", response_model=schemas.Document)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed"
        )
    
    # Read file content
    content = await file.read()
    
    # Create document in database
    db_document = models.Document(
        title=file.filename,
        content=content.decode(),
        file_path=file.filename,
        file_type=os.path.splitext(file.filename)[1],
        owner_id=current_user.id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Add document to vector store
    await rag_engine.add_document(
        content=content.decode(),
        metadata={
            "document_id": db_document.id,
            "title": file.filename,
            "owner_id": current_user.id
        }
    )
    
    return db_document

@router.get("/", response_model=List[schemas.Document])
async def read_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    documents = db.query(models.Document)\
        .filter(models.Document.owner_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return documents

@router.get("/{document_id}", response_model=schemas.Document)
async def read_document(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    document = db.query(models.Document)\
        .filter(models.Document.id == document_id)\
        .filter(models.Document.owner_id == current_user.id)\
        .first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document 