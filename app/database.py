from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "zettelkasten"


settings = Settings()
client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db]
