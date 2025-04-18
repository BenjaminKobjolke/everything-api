"""
Configuration utilities for the Everything API.
"""
import os
import configparser
from typing import Dict, Any, Optional


class Config:
    """
    Configuration manager for the Everything API.
    """
    def __init__(self, config_file: str = "settings.ini"):
        """
        Initialize the Config object.

        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        # Set default values
        self._set_defaults()
        
        # Load configuration from file if it exists
        if os.path.exists(config_file):
            self.load()
    
    def _set_defaults(self) -> None:
        """
        Set default configuration values.
        """
        self.config["Server"] = {
            "host": "localhost",
            "port": "5000"
        }
        
        self.config["Search"] = {
            "max_results": "100"
        }
        
        self.config["Logging"] = {
            "level": "INFO",
            "log_file": "everything_api.log"
        }
    
    def load(self) -> None:
        """
        Load configuration from the config file.
        """
        try:
            self.config.read(self.config_file)
        except Exception as e:
            raise ValueError(f"Failed to load configuration from {self.config_file}: {e}")
    
    def save(self) -> None:
        """
        Save the current configuration to the config file.
        """
        try:
            with open(self.config_file, "w") as f:
                self.config.write(f)
        except Exception as e:
            raise ValueError(f"Failed to save configuration to {self.config_file}: {e}")
    
    def get(self, section: str, option: str, fallback: Optional[str] = None) -> str:
        """
        Get a configuration value.

        Args:
            section: The configuration section
            option: The configuration option
            fallback: Fallback value if the option is not found

        Returns:
            The configuration value as a string
        """
        return self.config.get(section, option, fallback=fallback)
    
    def get_int(self, section: str, option: str, fallback: Optional[int] = None) -> int:
        """
        Get a configuration value as an integer.

        Args:
            section: The configuration section
            option: The configuration option
            fallback: Fallback value if the option is not found

        Returns:
            The configuration value as an integer
        """
        return self.config.getint(section, option, fallback=fallback)
    
    def get_bool(self, section: str, option: str, fallback: Optional[bool] = None) -> bool:
        """
        Get a configuration value as a boolean.

        Args:
            section: The configuration section
            option: The configuration option
            fallback: Fallback value if the option is not found

        Returns:
            The configuration value as a boolean
        """
        return self.config.getboolean(section, option, fallback=fallback)
    
    def set(self, section: str, option: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            section: The configuration section
            option: The configuration option
            value: The value to set
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, option, str(value))
