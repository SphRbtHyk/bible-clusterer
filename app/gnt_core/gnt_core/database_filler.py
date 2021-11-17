"""
Python module to fill up the database with the data available in the data/ folder.
"""
from pathlib import Path
from loguru import logger
import os
from gnt_core.database import MongoConnector
import asyncio
import json


class DataBaseFiller:
    """
    Class to fill up the database by parsing the data available in the folder
    data/sbgnlt.
    Should only be run once upon install of the application on the system.
    """

    def __init__(self, mongo_database: str = "gnt", mongo_host: str = "localhost", mongo_port: int = 27017) -> None:
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
        self.texts_chapter = list()
        self.texts_verses = list()

    async def connect(self):
        """
        Connect to the database.
        """
        await self.database_instance.connect()

    def load_sblgnt(self, input_folder: str = "../data/sblgnt/") -> None:
        """
        Load the SBLGNT JSON files into a list of Python dictionary using encoding
        adapted to the gnt. The only loaded text is the lemmed and stemmed
        words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        # Load the greek text
        for file in Path(Path(__file__).resolve().parent / input_folder).glob("*.txt"):
            logger.info(f"--- Writting down text found in files: {file} ---")
            book = file.name.split("-")[1]
            split_text = file.read_text(encoding="utf8").split("\n")
            text = ""
            for line in split_text:
                if line:
                    word = line.split(" ")[-1]
                    text += word + " "
            self.texts.append({"book": book, "text": text})
    
    def load_sbglnt_chapters(self, input_folder: str = "../data/sblgnt/") -> None:
        """
        Load the SBLGNT JSON files into a list of Python dictionary on
        a per chapter basis using encoding
        adapted to the gnt. The only loaded text is the lemmed and stemmed
        words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        for file in Path(Path(__file__).resolve().parent / input_folder).glob("*.txt"):
            book = file.name.split("-")[1]
            split_text = file.read_text(encoding="utf8").split("\n")
            texts = {}
            for text in split_text:
                parsed_text = text.split(" ")
                if parsed_text[0]:
                    chapter_ix = str(int(parsed_text[0][2:4]))
                    try:
                        texts[chapter_ix] += parsed_text[-1] + " "
                    except KeyError:
                        texts[chapter_ix] = parsed_text[-1]
            self.texts_chapter.append({"book": book, "chapters": texts})

    def load_sbglnt_verses(self, input_folder: str = "../data/sblgnt/") -> None:
        """
        Load the SBLGNT JSON files into a list of Python dictionary on
        a per verse basis using encoding
        adapted to the gnt. The only loaded text is the lemmed and stemmed
        words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        for file in Path(Path(__file__).resolve().parent / input_folder).glob("*.txt"):   
            book = file.name.split("-")[1]
            split_text = file.read_text(encoding="utf8").split("\n")
            text = {}
            for texts in split_text:
                parsed_text = texts.split(" ")
                if parsed_text[0]:
                    chapter_ix = str(int(parsed_text[0][2:4]))
                    verse_ix = str(int(parsed_text[0][4:6]))
                    # Check if chapter already exists
                    try:
                        text[chapter_ix]
                    # If it doesn't, fill it with an empty dictionary
                    except KeyError:
                        text[chapter_ix] = {}
                    # Else, fill it with content
                    try:
                        text[chapter_ix][verse_ix] += parsed_text[-1] + " "
                    except KeyError:
                        text[chapter_ix][verse_ix] = parsed_text[-1]  
            self.texts_verses.append({"book": book, "verses": text})
    
    def load_lxx(self, input_folder: str = "../data/lxx/") -> None:
        """
        Load the LXX JSON files into a list of Python dictionary using encoding
        adapted to the text. The only loaded text is the lemmed and stemmed
        words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        # Load the greek text
        for file in Path(Path(__file__).resolve().parent / input_folder).glob("*.js"):
            logger.info(f"--- Writting down text found in files: {file} ---")
            book = file.name.split(".")[0]
            opened_file = json.loads(file.read_text("utf-8"))
            text = ""
            for _, verses in opened_file.items():
                for words in verses:
                    text += words["lemma"] + " "
            self.texts.append({"book": book, "text": text})

    def load_lxx_chapters(self, input_folder: str = "../data/lxx/") -> None:
        """
        Load the LXX JSON files into a list of Python dictionary using encoding
        adapted to the text. The only loaded text is the lemmed and stemmed
        words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        for file in Path(Path(__file__).resolve().parent / input_folder).glob("*.js"):
            book = file.name.split(".")[0]
            opened_file = json.loads(file.read_text("utf-8"))
            text = {}
            for verses_nbr, verses in opened_file.items():
                chapter_ix = verses_nbr.split(".")[1]
                for verse_content in verses:
                    try:
                        text[chapter_ix] += verse_content["lemma"] + " "
                    except KeyError:
                        text[chapter_ix] = verse_content["lemma"]
            self.texts_chapter.append({"book": book, "chapters": text})

    def load_lxx_verses(self, input_folder: str = "../data/lxx/") -> None:
        """
        Load the LXX JSON files into a list of Python dictionary on a per verse basis,
        using encoding adapted to the text. The only loaded text is the
        lemmed and stemmed words, as only these will be considered whenever performing the
        clustering.

        Args:
            input_folder (str): Folder to find the data in
        """
        for file in Path(Path(__file__).resolve().parent / input_folder).glob("*.js"):
            book = file.name.split(".")[0]
            opened_file = json.loads(file.read_text("utf-8"))
            text = {}
            for verses_nbr, verses in opened_file.items():
                chapter_ix = verses_nbr.split(".")[1]
                for verse_content in verses:
                    verse_ix = verses_nbr.split(".")[2]
                    # Check if chapter already exists
                    try:
                        text[chapter_ix]
                    # If it doesn't, fill it with an empty dictionary
                    except KeyError:
                        text[chapter_ix] = {}
                    # Else, fill it with content
                    try:
                        text[chapter_ix][verse_ix] += verse_content["lemma"] + " "
                    except KeyError:
                        text[chapter_ix][verse_ix] = verse_content["lemma"]  
            self.texts_verses.append({"book": book, "verses": text})

    def load_json(self):
        """
        Load OT and NT texts.
        """
        self.load_sblgnt()
        self.load_lxx()
        self.load_lxx_chapters()
        self.load_sbglnt_chapters()
        self.load_lxx_verses()
        self.load_sbglnt_verses()

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
        book_classes_nt = [
            {"group": "Pauline", "books":  [
                "Ga", "Php", "1Th", "Phm", "Ro", "2Co", "1Co"]},
            {"group": "Deutero-Pauline", "books": ["Eph", "Col", "2Th"]},
            {"group": "Pastoral", "books": ["1Ti", "2Ti", "Tit"]},
            {"group": "Gospels", "books": ["Jn", "Mk", "Lk", "Mt"]},
            {"group": "Other epistles", "books": [
                "Ac", "Re", "1Pe", "2Pe", "Jas", "Jud", "Heb"]},
            {"group": "Johannine", "books": ["1Jn", "2Jn", "3Jn"]}]
        book_classes_ot = [
            {"group": "Law", "books": ["Gen", "Exod", "Lev", "Num", "Deut"]},
            {"group": "History", "books": ["JoshA", "JoshB", "JudgA", 
            "JudgB", "1Kgs", "2Kgs", "1Sam", "2Sam", "1Chr", "2Chr", "1Esd",
            "TobBA","TobS", "Esth", "1Macc", "2Macc", "3Macc"]},
            {"group": "Wisdom", "books": ["Ps", "PsSol", "Job", "Prov", "Eccl",
            "Wis", "Sir", "Song"]},
            {"group": "Prophets", "books": ["Hos", "Amos", "Mic",
            "Joel", "Obad", "Jonah", "Nah", "Hab",
            "Zeph", "Zec", "Mal", "Isa", "Jer", "Bar", "Lam", "Ezek", "DanOG", "DanTh"]}
        ]
        self.database_instance.write_book_classes(
            book_classes_nt=book_classes_nt,
            book_classes_ot=book_classes_ot
        )
        logger.info("Successfully wrote book classes")

    def write_texts(self) -> None:
        """
        Overwrite the collection GNTText to write down the textual
        data available for each book.
        """
        self.database_instance.write_text(self.texts)
        logger.info("Successfully wrote text content.")

    def write_chapters(self) -> None:
        """
        Overwrite the collection Chapters to write down the textual
        data available for each book.
        """
        self.database_instance.write_chapters(self.texts_chapter)
        logger.info("Successfully wrote text content separated as a chapter.")

    def write_verses(self) -> None:
        """
        Overwrite the collection Verses to write down the textual
        data available for each book.
        """
        self.database_instance.write_verses(self.texts_verses)
        logger.info("Successfully wrote text content separated in verses.")

    async def main(self) -> None:
        """
        Fill up the database for the Web App.
        """
        await self.connect()
        self.load_json()
        self.write_booklist()
        self.write_book_classes()
        self.write_texts()
        self.write_chapters()
        self.write_verses()


def fill():
    """
    Main function to fill database
    """
    MONGO_HOST = os.environ["GNT_MONGODB_HOST"] if "GNT_MONGODB_HOST" in os.environ else "localhost"
    MONGO_PORT = os.environ["GNT_MONGODB_PORT"] if "GNT_MONGODB_PORT" in os.environ else 27017
    MONGO_DATABASE = os.environ["GNT_MONGODB_DATABASE"] if "GNT_MONGODB_DATABASE" in os.environ else "gnt"
    # Create the database filler object
    filler = DataBaseFiller(mongo_database=MONGO_DATABASE, mongo_host=MONGO_HOST, mongo_port=MONGO_PORT)
    # Fill up database
    loop = asyncio.get_event_loop()
    loop.run_until_complete(filler.main())


if __name__ == '__main__':
    fill()