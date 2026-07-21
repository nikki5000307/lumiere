from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.schemas.wishlist import WishlistCreate

class WishlistService:
    @staticmethod
    def add_to_wishlist(db: Session, user_id: int, product_id: int):
        """Add a product to user's wishlist"""
        # Check if product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None, "Product not found"
        
        # Check if already in wishlist
        existing = db.query(Wishlist).filter(
            and_(
                Wishlist.user_id == user_id,
                Wishlist.product_id == product_id
            )
        ).first()
        
        if existing:
            return None, "Product already in wishlist"
        
        # Add to wishlist
        wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
        db.add(wishlist_item)
        db.commit()
        db.refresh(wishlist_item)
        return wishlist_item, None

    @staticmethod
    def remove_from_wishlist(db: Session, wishlist_id: int):
        """Remove a product from wishlist"""
        wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        if not wishlist_item:
            return False
        
        db.delete(wishlist_item)
        db.commit()
        return True

    @staticmethod
    def remove_product_from_wishlist(db: Session, user_id: int, product_id: int):
        """Remove a specific product from user's wishlist"""
        wishlist_item = db.query(Wishlist).filter(
            and_(
                Wishlist.user_id == user_id,
                Wishlist.product_id == product_id
            )
        ).first()
        
        if not wishlist_item:
            return False
        
        db.delete(wishlist_item)
        db.commit()
        return True

    @staticmethod
    def get_user_wishlist(db: Session, user_id: int):
        """Get all items in user's wishlist"""
        return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()

    @staticmethod
    def get_user_wishlist_with_products(db: Session, user_id: int):
        """Get user's wishlist items with product details"""
        wishlist_items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
        result = []
        for item in wishlist_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            result.append({
                "wishlist_id": item.id,
                "product": product,
                "added_at": item.created_at
            })
        return result

    @staticmethod
    def clear_wishlist(db: Session, user_id: int):
        """Clear all items from user's wishlist"""
        db.query(Wishlist).filter(Wishlist.user_id == user_id).delete()
        db.commit()
        return True

    @staticmethod
    def is_product_in_wishlist(db: Session, user_id: int, product_id: int):
        """Check if a product is in user's wishlist"""
        item = db.query(Wishlist).filter(
            and_(
                Wishlist.user_id == user_id,
                Wishlist.product_id == product_id
            )
        ).first()
        return item is not None
