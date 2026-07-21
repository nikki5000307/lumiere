from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.auth import get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/banners", tags=["banners"])

@router.get("/")
def get_banners(db: Session = Depends(get_db)):
    """Get all banners"""
    return {"message": "Get all banners"}

@router.post("/")
def create_banner(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new banner (admin only)"""
    return {"message": "Banner created"}

@router.put("/{banner_id}")
def update_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a banner (admin only)"""
    return {"message": "Banner updated"}

@router.delete("/{banner_id}")
def delete_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a banner (admin only)"""
    return {"message": "Banner deleted"}
