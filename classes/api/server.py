"""
Flask server implementation for the Everything API.
"""
import os
import logging
from flask import Flask, jsonify, request, Response
from typing import Dict, Any, Optional, Tuple, Union

from classes.core.search import SearchService
from classes.utils.config import Config

logger = logging.getLogger(__name__)


class EverythingAPIServer:
    """
    Flask server for the Everything API.
    """
    def __init__(self, config: Config, search_service: SearchService):
        """
        Initialize the API server.

        Args:
            config: Configuration object
            search_service: Search service for performing searches
        """
        self.config = config
        self.search_service = search_service
        self.app = Flask(__name__)
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self) -> None:
        """
        Register API routes.
        """
        @self.app.route('/everything-search-api/search', methods=['GET'])
        def search() -> Union[Response, Tuple[Dict[str, Any], int]]:
            """
            Handle search requests.
            
            Returns:
                JSON response with search results
            """
            # Get query parameter
            query = request.args.get('q')
            if not query:
                return jsonify({"error": "Missing query parameter 'q'"}), 400
            
            # Validate total search terms length
            search_terms = [term.strip() for term in query.split() if term.strip()]
            total_chars = sum(len(term) for term in search_terms)
            
            if total_chars < 3:
                return jsonify({
                    "error": f"Total length of search terms must be at least 3 characters. Current length: {total_chars}"
                }), 400
            
            # Get limit parameter
            try:
                limit = int(request.args.get('limit', self.config.get_int('Search', 'max_results')))
                if limit <= 0:
                    return jsonify({"error": "Limit must be a positive integer"}), 400
            except ValueError:
                return jsonify({"error": "Invalid limit parameter"}), 400
            
            # Get match_all parameter (default is true)
            match_all_param = request.args.get('match_all', 'true').lower()
            match_all = match_all_param not in ('false', '0', 'no')
            
            try:
                # Perform search
                response = self.search_service.search(query, limit, match_all)
                
                # Return results
                return jsonify(response.to_dict())
            except Exception as e:
                logger.error(f"Search failed: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.errorhandler(404)
        def not_found(e) -> Tuple[Dict[str, Any], int]:
            """
            Handle 404 errors.
            
            Returns:
                JSON response with error message
            """
            return jsonify({"error": "Endpoint not found"}), 404
        
        @self.app.errorhandler(500)
        def server_error(e) -> Tuple[Dict[str, Any], int]:
            """
            Handle 500 errors.
            
            Returns:
                JSON response with error message
            """
            logger.error(f"Server error: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    def run(self) -> None:
        """
        Run the Flask server.
        """
        host = self.config.get('Server', 'host')
        port = self.config.get_int('Server', 'port')
        
        logger.info(f"Starting Everything API server on {host}:{port}")
        self.app.run(host=host, port=port)
