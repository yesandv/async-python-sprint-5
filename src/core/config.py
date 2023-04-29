import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    title: str = "File Storage"
    host: str = "127.0.0.1"
    port: int = 8080
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db: str = base_dir + "/storage.db"
    sqlite_dsn: str = Field("sqlite+aiosqlite:///" + db)
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(..., env="JWT_ALGORITHM")
    jwt_expiration_time: int = Field(..., env="JWT_EXPIRATION_TIME")
    s3_region: str = Field(..., env="S3_REGION")
    s3_key: str = Field(..., env="S3_KEY")
    s3_secret_key: str = Field(..., env="S3_SECRET_KEY")
    s3_bucket: str = Field(..., env="S3_BUCKET")
    s3_endpoint: str = Field(..., env="S3_ENDPOINT")

    class Config:
        env_file = "../.env"


app_settings = Settings()
