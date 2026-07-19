from fastapi import APIRouter, Depends, UploadFile, File
import os
from pathlib import Path

from typing import List

from backend.api.dependencies import get_application, get_current_user
from backend.api.schemas.document import UploadResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post("", response_model=UploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    application=Depends(get_application),
    current_user=Depends(get_current_user),
):
    # Save the files to backend/documents/
    documents_dir = Path("backend/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)
    
    total_chunks = 0
    
    for file in files:
        file_path = documents_dir / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())
            
        # Ingest it
        result = application.ingestion_service.ingest(str(file_path))
        total_chunks += result.chunks
    
    # Save the knowledge base so it persists
    application.ingestion_service.document_store.save()
    
    return UploadResponse(
        documents=len(files),
        chunks=total_chunks
    )

@router.delete("")
async def clear_documents(
    application=Depends(get_application),
    current_user=Depends(get_current_user)
):
    documents_dir = Path("backend/documents")
    if documents_dir.exists():
        for item in documents_dir.glob("*.pdf"):
            item.unlink()
            
    application.ingestion_service.document_store.clear()
    application.ingestion_service.document_store.save()
    
    if application.ingestion_service.keyword_search:
        application.ingestion_service.keyword_search.build_index()
        
    return {"message": "Knowledge base cleared."}