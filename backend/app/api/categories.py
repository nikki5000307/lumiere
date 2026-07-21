from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.core.auth import get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    """Get all product categories"""
    return {"message": "Get all categories"}

@router.post("/")
def create_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new category (admin only)"""
    return {"message": "Category created"}

@router.put("/{category_id}")
def update_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a category (admin only)"""
    return {"message": "Category updated"}

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a category (admin only)"""
    return {"message": "Category deleted"}
