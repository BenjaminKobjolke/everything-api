"""
Core search functionality for the Everything API.
"""
import os
import logging
from typing import List, Optional

from classes.external.everything import Everything, Request
from classes.core.models import SearchResult, SearchResponse

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for performing searches using the Everything SDK.
    """
    def __init__(self, dll_path: str):
        """
        Initialize the SearchService.

        Args:
            dll_path: Path to the Everything64.dll file
        """
        self.dll_path = dll_path
        try:
            self.everything = Everything(dll_path)
            logger.info("Everything SDK initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Everything SDK: {e}")
            raise

    def search(self, query: str, max_results: int = 100, match_all: bool = True) -> SearchResponse:
        """
        Perform a search using the Everything SDK.

        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 100)
            match_all: Whether to match all words in the query (default: True)

        Returns:
            A SearchResponse object containing the search results

        Raises:
            Exception: If the search fails
        """
        # Store original query
        original_query = query
        
        # Get search terms for filtering
        search_terms = [term.strip().lower() for term in query.split() if term.strip()]
        
        logger.info(f"Performing search with query: '{query}', max_results: {max_results}, match_all: {match_all}")
        
        # Set search options - use original query without modification
        self.everything.set_search(query)
        self.everything.set_request_flags(
            Request.FullPathAndFileName | Request.DateModified | Request.Size
        )
        
        # Execute the search
        if not self.everything.query():
            error = self.everything.get_last_error()
            logger.error(f"Search failed: {error}")
            raise Exception(f"Search failed: {error}")
        
        # Get initial results from Everything SDK
        initial_results = []
        total_initial_results = len(self.everything)
        logger.info(f"Found {total_initial_results} initial results from Everything SDK")
        
        # Process all results first
        for i in range(total_initial_results):
            try:
                item = self.everything[i]
                
                # Get filename with error handling
                try:
                    raw_filename = item.get_filename()
                    filename = os.path.basename(raw_filename) if raw_filename else ""
                    path = raw_filename or ""
                except Exception as e:
                    logger.warning(f"Error getting filename for result {i}: {e}")
                    filename = f"Error retrieving filename: {str(e)[:50]}"
                    path = "Unknown path"
                
                # Get size with error handling
                try:
                    size = item.get_size()
                except Exception as e:
                    logger.warning(f"Error getting size for result {i}: {e}")
                    size = None
                
                # Get date_modified with error handling
                try:
                    date_modified = item.get_date_modified()
                except Exception as e:
                    logger.warning(f"Error getting date_modified for result {i}: {e}")
                    date_modified = None
                
                # Create SearchResult object
                result = SearchResult(
                    filename=filename,
                    path=path,
                    size=size,
                    date_modified=date_modified
                )
                initial_results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing search result {i}: {e}")
                # Add a placeholder result to maintain the count
                initial_results.append(SearchResult(
                    filename=f"Error processing result {i}",
                    path="Error",
                    size=0,
                    date_modified=None
                ))
        
        # Apply filtering if match_all is True
        results = []
        if match_all and search_terms:
            logger.info(f"Filtering results to match all search terms: {search_terms}")
            for result in initial_results:
                # Convert path to lowercase for case-insensitive comparison
                path_lower = result.path.lower() if result.path else ""
                
                # Check if all search terms are in the path
                if all(term in path_lower for term in search_terms):
                    results.append(result)
            
            logger.info(f"After filtering: {len(results)} of {len(initial_results)} results match all terms")
        else:
            # If match_all is False, use all results
            results = initial_results
        
        # Limit the number of results
        if len(results) > max_results:
            results = results[:max_results]
            logger.info(f"Limited to {max_results} results")
        
        # Use filtered count for the response
        filtered_count = len(results)
        
        return SearchResponse(
            results=results,
            query=query,
            count=filtered_count,
            total_count=total_initial_results,
            original_query=original_query if match_all else None
        )
