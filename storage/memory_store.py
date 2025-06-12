from typing import Dict, List, Optional, Set
from models.contact import Contact
import threading


class MemoryStore:
    """
    In-memory storage for contacts with O(1) operations.
    
    Uses multiple indexes for efficient searching:
    - Primary index by ID
    - Search indexes by name, phone, email
    """
    
    def __init__(self):
        self._lock = threading.RLock()  # Thread safety for concurrent access
        
        # Primary storage: ID -> Contact
        self._contacts: Dict[str, Contact] = {}
        
        # Search indexes for O(1) lookups
        self._name_index: Dict[str, Set[str]] = {}  # name_word -> set of contact_ids
        self._phone_index: Dict[str, str] = {}      # phone -> contact_id
        self._email_index: Dict[str, str] = {}      # email -> contact_id
    
    def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact with O(1) complexity"""
        with self._lock:
            self._contacts[contact.id] = contact
            self._update_indexes(contact)
            return contact
    
    def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get contact by ID with O(1) complexity"""
        return self._contacts.get(contact_id)
    
    def update_contact(self, contact_id: str, **updates) -> Optional[Contact]:
        """Update contact with O(1) complexity"""
        with self._lock:
            contact = self._contacts.get(contact_id)
            if not contact:
                return None
            
            # Remove old indexes
            self._remove_from_indexes(contact)
            
            # Update contact
            contact.update_fields(**updates)
            
            # Add new indexes
            self._update_indexes(contact)
            
            return contact
    
    def delete_contact(self, contact_id: str) -> bool:
        """Delete contact with O(1) complexity"""
        with self._lock:
            contact = self._contacts.get(contact_id)
            if not contact:
                return False
            
            # Remove from all indexes
            self._remove_from_indexes(contact)
            
            # Remove from primary storage
            del self._contacts[contact_id]
            return True
    
    def search_contacts(self, query: str) -> List[Contact]:
        """
        Search contacts by query string.
        Searches in name, phone, and email fields.
        Returns list of matching contacts.
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        matching_ids: Set[str] = set()
        
        with self._lock:
            # Search in name index (word-based)
            for word, contact_ids in self._name_index.items():
                if query_lower in word.lower():
                    matching_ids.update(contact_ids)
            
            # Search in phone index
            for phone, contact_id in self._phone_index.items():
                if query_lower in phone:
                    matching_ids.add(contact_id)
            
            # Search in email index
            for email, contact_id in self._email_index.items():
                if query_lower in email.lower():
                    matching_ids.add(contact_id)
            
            # Return matching contacts
            return [self._contacts[contact_id] for contact_id in matching_ids 
                   if contact_id in self._contacts]
    
    def get_all_contacts(self) -> List[Contact]:
        """Get all contacts"""
        return list(self._contacts.values())
    
    def _update_indexes(self, contact: Contact) -> None:
        """Update all search indexes for a contact"""
        # Name index (split by words for partial matching)
        name_words = contact.name.lower().split()
        for word in name_words:
            if word not in self._name_index:
                self._name_index[word] = set()
            self._name_index[word].add(contact.id)
        
        # Phone index
        self._phone_index[contact.phone] = contact.id
        
        # Email index
        self._email_index[contact.email.lower()] = contact.id
    
    def _remove_from_indexes(self, contact: Contact) -> None:
        """Remove contact from all search indexes"""
        # Remove from name index
        name_words = contact.name.lower().split()
        for word in name_words:
            if word in self._name_index:
                self._name_index[word].discard(contact.id)
                if not self._name_index[word]:
                    del self._name_index[word]
        
        # Remove from phone index
        if contact.phone in self._phone_index:
            del self._phone_index[contact.phone]
        
        # Remove from email index
        if contact.email.lower() in self._email_index:
            del self._email_index[contact.email.lower()] 