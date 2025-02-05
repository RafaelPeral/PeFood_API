import logging
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from src.model.entities.address import Address
from src.model.entities.bag import Bag
from src.model.entities.payment_format import PaymentFormat
from src.model.entities.product import Product
from src.model.entities.user import User


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class DBConnectionHandler:
    def __init__(self):
        self.connection_string = os.getenv("DB_CONNECTION_STRING")
        self.__db_name = os.getenv("DB_NAME")

        self.__document_models = [User, Address, PaymentFormat, Product, Bag]

        self.__client = None
        self.__db_connection = None

    async def connect_db(self):
        try:
            self.__client = AsyncIOMotorClient(self.connection_string)
            self.__client.admin.command("ping")
            self.__db_connection = self.__client[self.__db_name]
            await init_beanie(
                database=self.__db_connection, document_models=self.__document_models
            )

        except ServerSelectionTimeoutError as e:
            logger.error(f"Timeout error connecting to MongoDB: {e}")
            raise Exception(
                "Timeout while connecting to MongoDB. Make sure the server is running and accessible."
            )

        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            raise Exception(f"Error connecting to MongoDB: {e}")

        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise Exception(f"Configuration error while initializing Beanie: {e}")

        except Exception as e:
            logger.error(
                f"Unexpected error while connecting to the database: {e}", exc_info=True
            )
            raise Exception(
                "Unexpected error while initializing the database. Check logs for more details."
            )

    def get_client(self):
        if not self.__client:
            raise Exception("Database uninitialized. Call connect_db first.")
        return self.__client

    def get_db_connection(self):
        if not self.__client:
            raise Exception("Database uninitialized. Call connect_db first.")
        return self.__db_connection
