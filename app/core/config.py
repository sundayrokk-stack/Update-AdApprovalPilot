from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    RENDER_EXTERNAL_URL: str
    ADMIN_ID: int = 6941833127
    ADMIN_USERNAME: str = "@BlockSavvyMx"
    
    class Config:
        env_file = ".env"

settings = Settings()
