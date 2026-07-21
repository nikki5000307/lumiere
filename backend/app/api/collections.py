from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.auth import get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/collections", tags=["collections"])

@router.get("/")
def get_collections(db: Session = Depends(get_db)):
    """Get all collections"""
    return {"message": "Get all collections"}

@router.post("/")
def create_collection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new collection (admin only)"""
    return {"message": "Collection created"}

@router.put("/{collection_id}")
def update_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a collection (admin only)"""
    return {"message": "Collection updated"}

@router.delete("/{collection_id}")
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a collection (admin only)"""
    return {"message": "Collection deleted"}
