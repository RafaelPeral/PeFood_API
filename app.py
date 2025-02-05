from src.model.settings.db_connection_handler import DBConnectionHandler
from asyncio import run
from dotenv import load_dotenv

load_dotenv()


async def main():
    db_connection_handler = DBConnectionHandler()
    await db_connection_handler.connect_db()


run(main())
