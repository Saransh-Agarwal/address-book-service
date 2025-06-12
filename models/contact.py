from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Contact:
    """
    Contact model representing an address book entry.
    
    Attributes:
        id: Unique identifier (UUID string)
        name: Contact's full name
        phone: Contact's phone number
        email: Contact's email address
    """
    name: str
    phone: str
    email: str
    id: Optional[str] = None
    
    def __post_init__(self):
        """Generate UUID if not provided"""
        if self.id is None:
            self.id = str(uuid.uuid4())
    
    def to_dict(self) -> dict:
        """Convert contact to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }
    
    def update_fields(self, **kwargs) -> None:
        """Update contact fields with provided values"""
        for field, value in kwargs.items():
            if hasattr(self, field) and field != 'id':
                setattr(self, field, value) 