from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.model.entities.user import User
from src.model.entities.address import Address
from src.model.entities.payment_format import PaymentFormat
from src.model.entities.product import Product
from src.model.entities.bag import Bag
import os


class DBConectionHandler:
    def __init__(self):
        self.connection_string = os.getenv("DB_CONNECTION_STRING")
        self.__db_name = os.getenv("DB_NAME")

        self.__document_models = [User, Address, PaymentFormat, Product, Bag]

        self.__client = None
        self.__db = None
        self.__db_connection = None

    async def connect_db(self):
        try:
            self.__client = AsyncIOMotorClient(self.connection_string)
            self.__db = self.__client[self.__db_name]

            await init_beanie(
                database=self.__db, document_models=self.__document_models
            )
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def get_client(self):
        if not self.__client:
            raise Exception("Database uninitialized. Call connect_db first.")
        return self.__client

    def get_db_connection(self):
        if not self.__client:
            raise Exception("Database uninitialized. Call connect_db first.")
        return self.__db_connection
