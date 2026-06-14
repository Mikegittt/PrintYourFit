from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DEBUG: bool = Field(default=True)
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./dev.db")
    SECRET_KEY: str = Field(default="dev-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200
    CLOUDINARY_CLOUD_NAME: str = Field(default="")
    CLOUDINARY_API_KEY: str = Field(default="")
    CLOUDINARY_API_SECRET: str = Field(default="")
    PAYSTACK_SECRET_KEY: str = Field(default="")
    PAYSTACK_BASE_URL: str = "https://api.paystack.co"
    FRONTEND_URL: str = "http://localhost:5173"
    PRINT_SHOP_ONBOARDING_FEE_NAIRA: int = 10000
    VTPASS_API_KEY: str = Field(default="")
    VTPASS_URL: str = "https://vtpass.com/api"
    HF_MODEL: str = Field(default="stabilityai/stable-diffusion-2")
    HF_API_TOKEN: str = Field(default="")
    DEFAULT_PRINT_SHOP_ID: str = Field(default="dev")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
