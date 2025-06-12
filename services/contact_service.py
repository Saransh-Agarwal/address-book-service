from typing import List, Dict, Any, Optional
from models.contact import Contact
from storage.memory_store import MemoryStore


class ContactService:
    """
    Business logic layer for contact operations.
    Handles validation, business rules, and storage operations.
    """
    
    def __init__(self, store: MemoryStore):
        self._store = store
    
    def create_contacts(self, contact_data_list: List[Dict[str, Any]]) -> List[Contact]:
        """
        Create multiple contacts from input data.
        
        Args:
            contact_data_list: List of dictionaries containing contact data
            
        Returns:
            List of created Contact objects
            
        Raises:
            ValueError: If contact data is invalid
        """
        created_contacts = []
        
        for contact_data in contact_data_list:
            # Validate required fields
            self._validate_contact_data(contact_data)
            
            # Create contact object
            contact = Contact(
                name=contact_data['name'],
                phone=contact_data['phone'],
                email=contact_data['email']
            )
            
            # Store contact
            created_contact = self._store.create_contact(contact)
            created_contacts.append(created_contact)
        
        return created_contacts
    
    def update_contacts(self, update_data_list: List[Dict[str, Any]]) -> List[Contact]:
        """
        Update multiple contacts with new data.
        
        Args:
            update_data_list: List of dictionaries containing id and fields to update
            
        Returns:
            List of updated Contact objects
            
        Raises:
            ValueError: If contact ID not found or update data is invalid
        """
        updated_contacts = []
        
        for update_data in update_data_list:
            # Validate ID is present
            if 'id' not in update_data:
                raise ValueError("Contact ID is required for update")
            
            contact_id = update_data['id']
            
            # Get current contact
            current_contact = self._store.get_contact(contact_id)
            if not current_contact:
                raise ValueError(f"Contact with ID {contact_id} not found")
            
            # Extract update fields (exclude id)
            update_fields = {k: v for k, v in update_data.items() if k != 'id'}
            
            # Validate update fields
            if update_fields:
                self._validate_update_fields(update_fields)
            
            # Update contact
            updated_contact = self._store.update_contact(contact_id, **update_fields)
            if updated_contact:
                updated_contacts.append(updated_contact)
        
        return updated_contacts
    
    def delete_contacts(self, contact_ids: List[str]) -> int:
        """
        Delete multiple contacts by IDs.
        
        Args:
            contact_ids: List of contact IDs to delete
            
        Returns:
            Number of contacts successfully deleted
        """
        deleted_count = 0
        
        for contact_id in contact_ids:
            if self._store.delete_contact(contact_id):
                deleted_count += 1
        
        return deleted_count
    
    def search_contacts(self, query: str) -> List[Contact]:
        """
        Search contacts by query string.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Contact objects
        """
        if not query or not query.strip():
            return []
        
        return self._store.search_contacts(query)
    
    def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get a single contact by ID"""
        return self._store.get_contact(contact_id)
    
    def get_all_contacts(self) -> List[Contact]:
        """Get all contacts"""
        return self._store.get_all_contacts()
    
    def _validate_contact_data(self, contact_data: Dict[str, Any]) -> None:
        """Validate contact data for creation"""
        required_fields = ['name', 'phone', 'email']
        
        for field in required_fields:
            if field not in contact_data:
                raise ValueError(f"Missing required field: {field}")
            
            value = contact_data[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Field '{field}' must be a non-empty string")
        
        # Additional validation
        self._validate_email(contact_data['email'])
        self._validate_phone(contact_data['phone'])
    
    def _validate_update_fields(self, update_fields: Dict[str, Any]) -> None:
        """Validate fields for contact update"""
        valid_fields = {'name', 'phone', 'email'}
        
        for field, value in update_fields.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field for update: {field}")
            
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Field '{field}' must be a non-empty string")
        
        # Additional validation for specific fields
        if 'email' in update_fields:
            self._validate_email(update_fields['email'])
        
        if 'phone' in update_fields:
            self._validate_phone(update_fields['phone'])
    
    def _validate_email(self, email: str) -> None:
        """Basic email validation"""
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise ValueError(f"Invalid email format: {email}")
    
    def _validate_phone(self, phone: str) -> None:
        """Basic phone validation"""
        # Remove common separators and check if remaining characters are digits
        clean_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if not clean_phone.isdigit() or len(clean_phone) < 10:
            raise ValueError(f"Invalid phone format: {phone}") 