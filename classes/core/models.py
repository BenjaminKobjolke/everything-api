"""
Data models for the Everything API.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime


class SearchResult:
    """
    Represents a search result from the Everything search engine.
    """
    def __init__(
        self,
        filename: str,
        path: str,
        size: Optional[int] = None,
        date_modified: Optional[datetime] = None
    ):
        """
        Initialize a SearchResult object.

        Args:
            filename: The name of the file or folder
            path: The full path to the file or folder
            size: The size of the file in bytes
            date_modified: The date the file was last modified
        """
        self.filename = filename
        self.path = path
        self.size = size
        self.date_modified = date_modified

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the SearchResult object to a dictionary.

        Returns:
            A dictionary representation of the SearchResult
        """
        try:
            date_modified_str = None
            if self.date_modified:
                try:
                    date_modified_str = self.date_modified.isoformat()
                except Exception as e:
                    # If date conversion fails, log it and use string representation
                    logging.warning(f"Failed to convert date_modified to ISO format: {e}")
                    date_modified_str = str(self.date_modified)
                    
            return {
                "filename": str(self.filename) if self.filename is not None else None,
                "path": str(self.path) if self.path is not None else None,
                "size": self.size,
                "date_modified": date_modified_str
            }
        except Exception as e:
            logging.error(f"Error converting SearchResult to dict: {e}")
            # Return a safe fallback
            return {
                "filename": "Error: Could not process filename",
                "path": "Error: Could not process path",
                "size": 0,
                "date_modified": None
            }


class SearchResponse:
    """
    Represents a response from the search API.
    """
    def __init__(self, results: list[SearchResult], query: str, count: int, 
                 total_count: Optional[int] = None, original_query: Optional[str] = None):
        """
        Initialize a SearchResponse object.

        Args:
            results: List of SearchResult objects
            query: The search query that was used
            count: The number of results after filtering
            total_count: The total number of results before filtering (if applicable)
            original_query: The original query before modification (if any)
        """
        self.results = results
        self.query = query
        self.count = count
        self.total_count = total_count
        self.original_query = original_query

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the SearchResponse object to a dictionary.

        Returns:
            A dictionary representation of the SearchResponse
        """
        try:
            results_dicts = []
            for result in self.results:
                try:
                    results_dicts.append(result.to_dict())
                except Exception as e:
                    logging.error(f"Error converting individual result to dict: {e}")
                    # Add a placeholder for the failed result
                    results_dicts.append({
                        "filename": "Error: Could not process result",
                        "path": "Error: Could not process result",
                        "size": 0,
                        "date_modified": None
                    })
            
            response_dict = {
                "results": results_dicts,
                "query": self.query,
                "count": self.count
            }
            
            # Include total_count if available
            if self.total_count is not None:
                response_dict["total_count"] = self.total_count
            
            # Include original_query if available
            if self.original_query:
                response_dict["original_query"] = self.original_query
                
            return response_dict
        except Exception as e:
            logging.error(f"Error converting SearchResponse to dict: {e}")
            # Return a safe fallback
            fallback = {
                "results": [],
                "query": self.query if hasattr(self, 'query') else "unknown",
                "count": 0,
                "error": "Failed to process search results"
            }
            
            # Include total_count if available
            if hasattr(self, 'total_count') and self.total_count is not None:
                fallback["total_count"] = self.total_count
                
            # Include original_query if available
            if hasattr(self, 'original_query') and self.original_query:
                fallback["original_query"] = self.original_query
                
            return fallback
