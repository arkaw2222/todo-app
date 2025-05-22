import os
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URL:
    raise ValueError("❌ MONGO_URL not set in .env")
if not DB_NAME:
    raise ValueError("❌ DB_NAME not set in .env")

client = AsyncIOMotorClient(MONGO_URL)
engine = AIOEngine(client=client, database=DB_NAME)

def get_engine() -> AIOEngine:
    return engine