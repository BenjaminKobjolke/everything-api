"""
Main entry point for the Everything API.
"""
import os
import sys
import argparse
import logging

from classes.utils.config import Config
from classes.utils.logging import setup_logging
from classes.core.search import SearchService
from classes.api.server import EverythingAPIServer


def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Everything Search API")
    
    parser.add_argument(
        "--config", 
        default="settings.ini",
        help="Path to configuration file (default: settings.ini)"
    )
    
    parser.add_argument(
        "--host",
        help="Host to bind the server to (overrides config file)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        help="Port to bind the server to (overrides config file)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (overrides config file)"
    )
    
    parser.add_argument(
        "--log-file",
        help="Path to log file (overrides config file)"
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Load configuration
    config = Config(args.config)
    
    # Override configuration with command line arguments
    if args.host:
        config.set("Server", "host", args.host)
    
    if args.port:
        config.set("Server", "port", args.port)
    
    if args.log_level:
        config.set("Logging", "level", args.log_level)
    
    if args.log_file:
        config.set("Logging", "log_file", args.log_file)
    
    # Save configuration if it doesn't exist
    if not os.path.exists(args.config):
        config.save()
    
    # Set up logging
    log_level = config.get("Logging", "level")
    log_file = config.get("Logging", "log_file")
    setup_logging(log_level, log_file)
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Join with the DLL filename to get the full path
    dll_path = os.path.join(script_dir, "Everything64.dll")
    
    # Check if the DLL exists
    if not os.path.exists(dll_path):
        logging.error(f"Everything64.dll not found at {dll_path}")
        sys.exit(1)
    
    try:
        # Initialize search service
        search_service = SearchService(dll_path)
        
        # Initialize and run the server
        server = EverythingAPIServer(config, search_service)
        server.run()
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
