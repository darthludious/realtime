"""
Configuration management for the realtime API assistant.
Handles loading and validation of all configuration settings.
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, List, Optional
import os
import json
from pathlib import Path

class FlowiseAgentConfig(BaseModel):
    """Configuration for a single Flowise agent"""
    name: str
    description: str

class FlowiseConfig(BaseModel):
    """Configuration for Flowise AI integration"""
    enabled: bool
    default_agent: str
    agents: Dict[str, FlowiseAgentConfig]

class AppConfig(BaseModel):
    """Main application configuration"""
    browser_urls: List[HttpUrl] = Field(description="List of URLs that can be opened in the browser")
    browser_command: str = Field(description="Command used to open the browser")
    ai_assistant_name: str = Field(description="Name of the AI assistant")
    human_name: str = Field(description="Name of the human user")
    sql_dialect: str = Field(default="duckdb", description="SQL dialect to use")
    system_message_suffix: Optional[str] = Field(description="Optional suffix for system messages")
    flowise_ai: FlowiseConfig = Field(description="Flowise AI configuration")
    
    # Required environment variables
    openai_api_key: str = Field(description="OpenAI API key")
    scratch_pad_dir: str = Field(description="Directory for scratch pad files")
    
    @classmethod
    def load(cls) -> "AppConfig":
        """
        Load configuration from environment variables and personalization.json
        
        Returns:
            AppConfig: Validated configuration object
        
        Raises:
            ValueError: If required configuration is missing
            ValidationError: If configuration is invalid
        """
        # Load environment variables
        env_vars = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "scratch_pad_dir": os.getenv("SCRATCH_PAD_DIR"),
        }
        
        # Check for missing environment variables
        missing_vars = [k for k, v in env_vars.items() if not v]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        # Load personalization.json
        personalization_file = os.getenv("PERSONALIZATION_FILE", "./personalization.json")
        try:
            with open(personalization_file, "r") as f:
                personalization = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Personalization file not found: {personalization_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in personalization file: {personalization_file}")
            
        # Combine configuration
        config_dict = {**personalization, **env_vars}
        
        # Validate and create config object
        return cls(**config_dict)

# Global configuration instance
_config: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """
    Get the global configuration instance.
    Loads configuration if not already loaded.
    
    Returns:
        AppConfig: Validated configuration object
    """
    global _config
    if _config is None:
        _config = AppConfig.load()
    return _config
