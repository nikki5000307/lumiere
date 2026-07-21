from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.wishlist import WishlistCreate, WishlistResponse, WishlistItem
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.database.database import get_db
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/wishlists", tags=["wishlists"])

@router.get("/", response_model=List[WishlistResponse])
def get_user_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all wishlist items for current user"""
    wishlist_items = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    return wishlist_items

@router.post("/", response_model=WishlistResponse)
def add_to_wishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a product to wishlist"""
    product = db.query(Product).filter(Product.id == wishlist.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == wishlist.product_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already in wishlist")
    
    new_wishlist = Wishlist(user_id=current_user.id, product_id=wishlist.product_id)
    db.add(new_wishlist)
    db.commit()
    db.refresh(new_wishlist)
    return new_wishlist

@router.delete("/{wishlist_id}")
def remove_from_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a product from wishlist"""
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")
    
    if wishlist_item.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Item removed from wishlist"}

@router.delete("/product/{product_id}")
def remove_product_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a specific product from user's wishlist"""
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()
    
    if not wishlist_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not in wishlist")
    
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Product removed from wishlist"}
