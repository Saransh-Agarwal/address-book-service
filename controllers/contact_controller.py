from flask import Blueprint, request, jsonify
from typing import List, Dict, Any
from services.contact_service import ContactService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContactController:
    """
    Controller for handling contact API endpoints.
    Manages HTTP requests/responses and delegates business logic to service layer.
    """
    
    def __init__(self, contact_service: ContactService):
        self.contact_service = contact_service
        self.blueprint = Blueprint('contacts', __name__)
        self._register_routes()
    
    def _register_routes(self):
        """Register all contact-related routes"""
        self.blueprint.add_url_rule('/create', 'create_contacts', 
                                   self.create_contacts, methods=['POST'])
        self.blueprint.add_url_rule('/update', 'update_contacts', 
                                   self.update_contacts, methods=['PUT'])
        self.blueprint.add_url_rule('/delete', 'delete_contacts', 
                                   self.delete_contacts, methods=['DELETE'])
        self.blueprint.add_url_rule('/search', 'search_contacts', 
                                   self.search_contacts, methods=['POST'])
    
    def create_contacts(self):
        """
        POST /create
        Create one or more contacts.
        
        Expected request body: List of contact objects
        Returns: List of created contacts with generated IDs
        """
        try:
            # Validate request data
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            contact_data_list = request.get_json()
            
            if not isinstance(contact_data_list, list):
                return jsonify({"error": "Request body must be a list"}), 400
            
            if not contact_data_list:
                return jsonify({"error": "Request body cannot be empty"}), 400
            
            # Create contacts
            created_contacts = self.contact_service.create_contacts(contact_data_list)
            
            # Convert to response format
            response_data = [contact.to_dict() for contact in created_contacts]
            
            logger.info(f"Created {len(created_contacts)} contacts")
            return jsonify(response_data), 201
            
        except ValueError as e:
            logger.error(f"Validation error in create_contacts: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error in create_contacts: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    def update_contacts(self):
        """
        PUT /update
        Update one or more contacts.
        
        Expected request body: List of objects with id and fields to update
        Returns: List of updated contacts
        """
        try:
            # Validate request data
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            update_data_list = request.get_json()
            
            if not isinstance(update_data_list, list):
                return jsonify({"error": "Request body must be a list"}), 400
            
            if not update_data_list:
                return jsonify({"error": "Request body cannot be empty"}), 400
            
            # Update contacts
            updated_contacts = self.contact_service.update_contacts(update_data_list)
            
            # Convert to response format
            response_data = [contact.to_dict() for contact in updated_contacts]
            
            logger.info(f"Updated {len(updated_contacts)} contacts")
            return jsonify(response_data), 200
            
        except ValueError as e:
            logger.error(f"Validation error in update_contacts: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error in update_contacts: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    def delete_contacts(self):
        """
        DELETE /delete
        Delete one or more contacts by IDs.
        
        Expected request body: List of contact IDs
        Returns: Object with count of deleted contacts
        """
        try:
            # Validate request data
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            contact_ids = request.get_json()
            
            if not isinstance(contact_ids, list):
                return jsonify({"error": "Request body must be a list"}), 400
            
            if not contact_ids:
                return jsonify({"error": "Request body cannot be empty"}), 400
            
            # Validate all items are strings
            for contact_id in contact_ids:
                if not isinstance(contact_id, str):
                    return jsonify({"error": "All contact IDs must be strings"}), 400
            
            # Delete contacts
            deleted_count = self.contact_service.delete_contacts(contact_ids)
            
            logger.info(f"Deleted {deleted_count} contacts")
            return jsonify({"deleted": deleted_count}), 200
            
        except Exception as e:
            logger.error(f"Unexpected error in delete_contacts: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    def search_contacts(self):
        """
        POST /search
        Search contacts by query string.
        
        Expected request body: Object with 'query' field
        Returns: List of matching contacts
        """
        try:
            # Validate request data
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            search_data = request.get_json()
            
            if not isinstance(search_data, dict):
                return jsonify({"error": "Request body must be an object"}), 400
            
            if 'query' not in search_data:
                return jsonify({"error": "Missing 'query' field"}), 400
            
            query = search_data['query']
            if not isinstance(query, str):
                return jsonify({"error": "'query' must be a string"}), 400
            
            # Search contacts
            matching_contacts = self.contact_service.search_contacts(query)
            
            # Convert to response format
            response_data = [contact.to_dict() for contact in matching_contacts]
            
            logger.info(f"Search for '{query}' returned {len(matching_contacts)} contacts")
            return jsonify(response_data), 200
            
        except Exception as e:
            logger.error(f"Unexpected error in search_contacts: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500 