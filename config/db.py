from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.tasks import Tasks


async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    await init_beanie(database=client.db_name, document_models=[Tasks])
