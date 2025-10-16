"""
Configuration settings for HelpVia API
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # Application
    APP_NAME: str = "HelpVia API"
    ENVIRONMENT: str = "development"  # development, testing, production
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_TYPE: str = "sqlite"  # sqlite or mysql
    MYSQL_DATABASE_URL: str = "mysql+pymysql://user:password@localhost/helpvia_db"
    SQLITE_DATABASE_URL: str = "sqlite+aiosqlite:///./helpvia.db"
    
    # Security
    SECRET_KEY: str = "njxenkxj3hhuexu"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ]
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    MAX_PAGE_SIZE: int = 100
    DEFAULT_PAGE_SIZE: int = 20
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def database_url(self) -> str:
        """
        Returns the appropriate database URL based on environment.
        """
        if self.ENVIRONMENT == "testing" or self.DATABASE_TYPE == "sqlite":
            return self.SQLITE_DATABASE_URL
        return self.MYSQL_DATABASE_URL
    
    @property
    def async_database_url(self) -> str:
        """
        Returns async database URL.
        """
        if self.ENVIRONMENT == "testing" or self.DATABASE_TYPE == "sqlite":
            return self.SQLITE_DATABASE_URL
        # For MySQL, convert to async driver
        return self.MYSQL_DATABASE_URL.replace("mysql+pymysql", "mysql+aiomysql")


# Create settings instance
settings = Settings()