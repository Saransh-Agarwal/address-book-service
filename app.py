from flask import Flask, jsonify
from storage.memory_store import MemoryStore
from services.contact_service import ContactService
from controllers.contact_controller import ContactController
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Application factory pattern for creating Flask app.
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Configure Flask
    app.config['JSON_SORT_KEYS'] = False  # Maintain field order in JSON responses
    
    # Initialize storage layer
    memory_store = MemoryStore()
    logger.info("Initialized in-memory storage")
    
    # Initialize service layer
    contact_service = ContactService(memory_store)
    logger.info("Initialized contact service")
    
    # Initialize controller layer
    contact_controller = ContactController(contact_service)
    logger.info("Initialized contact controller")
    
    # Register blueprints
    app.register_blueprint(contact_controller.blueprint)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "Address Book API",
            "version": "1.0.0"
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information"""
        return jsonify({
            "service": "Address Book API",
            "version": "1.0.0",
            "endpoints": {
                "create": "POST /create",
                "update": "PUT /update", 
                "delete": "DELETE /delete",
                "search": "POST /search",
                "health": "GET /health"
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    logger.info("Flask application created successfully")
    return app


if __name__ == '__main__':
    app = create_app()
    
    logger.info("Starting Address Book API server...")
    logger.info("Server will run on http://localhost:5000")
    logger.info("Available endpoints:")
    logger.info("  POST   /create  - Create contacts")
    logger.info("  PUT    /update  - Update contacts")
    logger.info("  DELETE /delete  - Delete contacts")
    logger.info("  POST   /search  - Search contacts")
    logger.info("  GET    /health  - Health check")
    
    # Run the application on port 5000
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False  # Set to False for production
    ) 