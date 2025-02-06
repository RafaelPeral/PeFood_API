from src.model.settings.db_connection_handler import DBConnectionHandler
from asyncio import run
from dotenv import load_dotenv
from src.model.entities.address import Address

load_dotenv()


async def main():
    db_connection_handler = DBConnectionHandler()
    await db_connection_handler.connect_db()
    await db_connection_handler.test_connect_db()
    address = Address(
        street="Rua A", number=10, city="Cidade", neighborhood="Bairro", zip_code=1234
    )
    await address.insert()

    await db_connection_handler.disconnect_db()


run(main())
