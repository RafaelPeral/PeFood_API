from src.model.settings.db_connection_handler import DBConectionHandler
from asyncio import run
from dotenv import load_dotenv

load_dotenv()


async def main():
    db_connection_handler = DBConectionHandler()
    await db_connection_handler.connect_db()


run(main())
