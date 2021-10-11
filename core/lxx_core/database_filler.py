"""
Python module to fill up the database with the data available in the data/ folder.
"""
from pathlib import Path
from loguru import logger
from lxx_core.database import MongoConnector
import asyncio


class DataBaseFiller:
    """
    Class to fill up the database by parsing the data available in the folder
    data/sbgnlt.
    Should only be run once upon install of the application on the system.
    """

    def __init__(self, mongo_database: str = "lxx", mongo_host: str = "localhost", mongo_port: int = 27017) -> None:
        """
        Initializes an object of class DataBaseFiller, using the information of the
        mongo database.

        Args:
            mongo_database (str): Name of the mongo database to connect to.
            mongo_host (str): Host of the database
            mongo_port (int): Port exposed by the database
        """
        self.database_instance = MongoConnector(
            mongo_database, mongo_host, mongo_port)
        self.texts = list()

    async def connect(self):
        """
        Connect to the database.
        """
        await self.database_instance.connect()

    def load_json(self, input_folder: str = "data/sblgnt/") -> None:
        """
        Load the JSON files into a list of Python dictionary using encoding
        adapted to the LXX. The only loaded text is the lemmed and stemmed
        words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        # Load the greek text
        for file in Path(input_folder).glob("*.txt"):
            book = file.name.split("-")[1]
            split_text = file.read_text(encoding="utf8").split("\n")
            text = ""
            for line in split_text:
                if line:
                    word = line.split(" ")[-1]
                    text += word + " "
            self.texts.append({"book": book, "text": text})

    def write_booklist(self) -> None:
        """
        Overwrite the booklist in the mongo collection.
        """
        self.database_instance.write_book_lists(
            [text['book'] for text in self.texts])
        logger.info("Successfully wrote list of books")

    def write_book_classes(self) -> None:
        """
        Write the bookclasses in the mongo collection.
        """
        book_classes = [
            {"group": "Pauline", "books":  [
                "Ga", "Php", "1Th", "Phm", "Ro", "2Co", "1Co"]},
            {"group": "Deutero-Pauline", "books": ["Eph", "Col", "2Th"]},
            {"group": "Pastoral", "books": ["1Ti", "2Ti", "Tit"]},
            {"group": "Gospels", "books": ["Jn", "Mk", "Lk", "Mt"]},
            {"group": "Other", "books": [
                "Ac", "Re", "1Pe", "2Pe", "Jas", "Jud", "Heb"]}
        ]
        self.database_instance.write_book_classes(
            book_classes
        )
        logger.info("Successfully wrote book classes")

    def write_texts(self) -> None:
        """
        Overwrite the collection LXXText to write down the textual
        data available for each book.
        """
        self.database_instance.write_text(self.texts)
        logger.info("Successfully wrote text content.")

    async def main(self) -> None:
        """
        Fill up the database for the Web App.
        """
        await self.connect()
        self.load_json()
        self.write_booklist()
        self.write_book_classes()
        self.write_texts()


if __name__ == "__main__":
    # TODO: parse variable from environment
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    # Create the database filler object
    filler = DataBaseFiller(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT)
    # Fill up database
    loop = asyncio.get_event_loop()
    loop.run_until_complete(filler.main())
