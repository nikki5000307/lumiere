from typing import List, Dict, Any
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Requirements:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is valid"

def paginate(items: List[Any], skip: int = 0, limit: int = 10) -> List[Any]:
    """Paginate a list of items"""
    return items[skip:skip + limit]

def get_pagination_params(skip: int = 0, limit: int = 10) -> Dict[str, int]:
    """Get pagination parameters"""
    return {
        "skip": max(0, skip),
        "limit": min(100, max(1, limit))
    }

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency"""
    return f"{currency} {amount:,.2f}"

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def truncate_text(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix

def clean_dict(data: dict) -> dict:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}

def merge_dicts(*dicts) -> dict:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result
