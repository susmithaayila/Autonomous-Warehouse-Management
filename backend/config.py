import os

class Settings:
    PROJECT_NAME: str = "Autonomous Warehouse Management System (AWMS)"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "awms_super_secure_jwt_secret_key_2026_cys401")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./awms.db")
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    ENFORCE_ROBOT_NONCE: bool = True

settings = Settings()
