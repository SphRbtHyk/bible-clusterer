"""
Python module containing the data models of the data exchanged by the application.
"""
from typing import Dict, List
from pydantic import BaseModel


class BookList(BaseModel):
    """
    Model class representing the data associated with the list of books.
    """
    books: List[str]


class BookClasses(BaseModel):
    """
    Model class representing the data associated with the
    description of each book class.
    """
    group: str
    books: List[str]


class TextList(BaseModel):
    """
    Model class representing the data associated with a list of text.
    """
    book: str
    text: str


class TextChapter(BaseModel):
    """
    Model class representing the data displayed on a per chapter basis.
    """
    book: str
    chapters: Dict[str, str]


class TextVerses(BaseModel):
    """
    Model class representing the data displayed on a per chapter basis.
    """
    book: str
    verses: Dict[str, Dict[str, str]]


class ClusteringResults(BaseModel):
    """
    Model class representing results associated with a clustering processing.
    """
    projection: Dict[str, List[float]]
    labels: List[str]
    clusters: List[str]
    ground_truth: List[str]
