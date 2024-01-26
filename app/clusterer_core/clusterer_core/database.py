# Python module to get the data from the mongo DB database
from typing import List, Optional, Dict, Any
from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


class MongoConnector:
    """
    Python class to:
        - Get the data from the database
        - Send the data from the database
    """

    def __init__(self,
                mongo_uri: str = "",
                mongo_database: str = "bible",
                mongo_host: str = "localhost",
                mongo_port: int = 27017,
                mongo_password: str = None,
                mongo_user: str = None) -> None:
        """
        Initializes an object of class DataBaseFiller, using the information of the
        mongo database.

        Args:
            mongo_database (str): Name of the database to connect to
            mongo_host (str): Host of the database
            mongo_port (int): Port exposed by the database
        """
        self.mongo_uri: str = mongo_uri
        self.mongo_port: int = mongo_port
        self.mongo_host: str = mongo_host
        self.mongo_database: str = mongo_database
        self.mongo_password: str = mongo_password
        self.mongo_user: str = mongo_user
        self.async_client: Optional[AsyncIOMotorClient] = None
        self.async_db: Optional[AsyncIOMotorDatabase] = None
        self.text_collection: Optional[AsyncIOMotorCollection] = None
        self.booklists: Optional[AsyncIOMotorCollection] = None
        self.server_info: Optional[dict] = None

    async def connect(self) -> None:
        """
        Connect to an instance of a MongoDb database.
        """
        # Parse config from environment if not provided
        logger.info(
            "Connecting to Mongo database on host"
            f"{self.mongo_host}:{self.mongo_port}"
        )
        mongo_user_password = f"{self.mongo_user}:{self.mongo_password}@" if self.mongo_user else ""
        mongo_user_port = f":{self.mongo_port}" if self.mongo_port else ""
        # If URI has not been specified, then build it
        if not self.mongo_uri:
            self.mongo_uri = f"mongodb://{mongo_user_password}{self.mongo_host}{mongo_user_port}/{self.mongo_database}?authSource=admin"
        # Create asynchronous Mongo client
        self.async_client = AsyncIOMotorClient(
            self.mongo_uri
        )
        self.async_db = self.async_client[self.mongo_database]
        self.texts = self.async_db["Texts"]
        self.chapters = self.async_db["Chapters"]
        self.verses = self.async_db["Verses"]
        self.booklists = self.async_db["BookList"]
        self.bookclasses_nt = self.async_db["BookClassesNT"]
        self.bookclasses_ot = self.async_db["BookClassesOT"]
        self.server_info = await self.async_client.server_info()
        logger.info(
            "Connected to mongodb server version {0}"
            "on host 'mongodb://{1}:{2}'.".format(
                self.server_info["version"], *self.async_client.address
            )
        )
        return self

    async def close(self):
        """
        Close connection to a mongo database.
        """
        self.async_client.close()
        logger.info("Closed connection to mongodb server.")

    async def get_book_lists(self, language: str) -> Dict[str, List[str]]:
        """
        Get all of the books stored into the collection BookList.
        """
        booklist = self.booklists.find({"language": language}, {"_id": 0})
        return {"books": [book["book"] for book in await booklist.to_list(length=100)]}

    async def get_book_classes_nt(self) -> Dict[str, List[str]]:
        """
        Get all of the books stored into the collection BookList.
        """
        booklist = self.bookclasses_nt.find({}, {"_id": 0})
        return await booklist.to_list(length=100)

    async def get_book_classes_ot(self) -> Dict[str, List[str]]:
        """
        Get all of the books stored into the collection BookList.
        """
        booklist = self.bookclasses_ot.find({}, {"_id": 0})
        return await booklist.to_list(length=100)

    async def get_book_classes(self) -> Dict[str, List[str]]:
        """
        Get all of the books stored into the collection BookList.
        """
        ot_classes = await self.bookclasses_ot.find({}, {"_id": 0}).to_list(length=100)
        nt_classes = await self.bookclasses_nt.find({}, {"_id": 0}).to_list(length=100)
        all_classes = ot_classes + nt_classes
        return all_classes

    async def get_book_class(self, book_list: List[str]) -> List[str]:
        """
        For a given list of books, get their corresponding class.
        """
        all_bookclasses = await self.get_book_classes()
        bookclasses = []
        for book in book_list:
            for bookgroup in all_bookclasses:
                if book in bookgroup["books"]:
                    bookclasses.append(bookgroup["group"])
        return bookclasses

    async def get_texts(self, 
                        language: str = "greek",
                        text_list=Optional[List[str]]) -> List[Dict[str, str]]:
        """
        Get the texts specified in text_list. If the argument text_list
        is set to None, return all the texts in the database.

        Args:
            language (str): The language to retrieve the data for.
            text_list (list): The list of texts to fetch from the database.

        Returns:
            dict: A dictionnary containing the different available texts.
        """
        if not text_list:
            collection = self.texts.find({"language": language}, {"_id": 0})
        else:
            collection = self.texts.find(
                {"book": {"$in": text_list}, "language": language}, {"_id": 0})
        book_data = await collection.to_list(length=1000)
        return book_data

    async def get_chapters(self,
                           language: str = "greek",
                           text_list=Optional[List[str]]) -> List[Dict[str, str]]:
        """
        Get the texts specified in text_list. If the argument text_list
        is set to None, return all the texts in the database.

        Args:
            text_list (list): The list of texts to fetch from the database.

        Returns:
            dict: A dictionnary containing the different available texts.
        """
        if not text_list:
            collection = self.chapters.find({"language": language}, {"_id": 0})
        else:
            collection = self.chapters.find(
                {"book": {"$in": text_list}, "language": language}, {"_id": 0})
        return await collection.to_list(length=1000)

    async def get_verses(self,
                         language: str = "greek",
                         text_list=Optional[List[str]]) -> List[Dict[str, str]]:
        """
        Get the texts specified in text_list. If the argument text_list
        is set to None, return all the texts in the database.

        Args:
            text_list (list): The list of texts to fetch from the database.

        Returns:
            dict: A dictionnary containing the different available texts.
        """
        if not text_list:
            collection = self.verses.find({}, {"_id": 0})
        else:
            collection = self.verses.find(
                {"book": {"$in": text_list}, "language": language}, {"_id": 0})
        return await collection.to_list(length=1000)

    def write_book_lists(self, book_names: Dict[str, str]) -> None:
        """
        Overwrite the collection BookList to write down the list
        of the books.
        """
        # Drop existing data
        self.booklists.drop()
        self.booklists.insert_many(book_names)

    def write_text(self, book_data: List[Dict[str, str]]) -> None:
        """
        Overwrite the collection GNTText to write down the textual
        data available for each book.
        """
        # Drop existing data
        self.texts.drop()
        # Add new data
        self.texts.insert_many(book_data)

    def write_chapters(self, book_data: List[Dict[str, Any]]) -> None:
        """
        Overwrite the collection GNTText to write down the textual
        data available for each book.
        """
        # Drop existing data
        self.chapters.drop()
        # Add new data
        self.chapters.insert_many(book_data)

    def write_verses(self, book_data: List[Dict[str, Any]]) -> None:
        """
        Overwrite the collection Verses to write down the textual
        data available for each book.
        """
        # Drop existing data
        self.verses.drop()
        # Add new data
        self.verses.insert_many(book_data)

    def write_book_classes(self, book_classes_nt: List[Dict[str, List[str]]], 
                                 book_classes_ot: List[Dict[str, List[str]]]) -> None:
        """
        Overwrite the collection BookClass to write down the textual data 
        and the corresponding values.
        """
        # Drop existing data
        self.bookclasses_nt.drop()
        self.bookclasses_ot.drop()
        # Add new data
        self.bookclasses_nt.insert_many(book_classes_nt)
        self.bookclasses_ot.insert_many(book_classes_ot)
