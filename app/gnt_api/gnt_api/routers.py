"""
Python module containing the different endpoints of the application related to the
available texts.
"""
from typing import List, Optional
from fastapi import APIRouter, Query
from gnt_api.instances import database_instance, gnt_clusterer
from gnt_api.models import BookList, ClusteringResults, TextList, BookClasses, TextChapter, TextVerses

router = APIRouter()


@router.get("/booklists", response_model=List[BookList])
async def get_book_list():
    return await database_instance.get_book_lists()


@router.get("/bookclasses", response_model=List[BookClasses])
async def get_book_list():
    return await database_instance.get_book_classes()

@router.get("/bookclasses/nt", response_model=List[BookClasses])
async def get_book_list():
    return await database_instance.get_book_classes_nt()

@router.get("/bookclasses/ot", response_model=List[BookClasses])
async def get_book_list():
    return await database_instance.get_book_classes_ot()

@router.get("/texts", response_model=List[TextList])
async def get_book_text(q: Optional[List[str]] = Query([])):
    return await database_instance.get_texts(q)

@router.get("/texts/verses", response_model=List[TextVerses])
async def get_book_text(q: Optional[List[str]] = Query([])):
    return await database_instance.get_verses(q)

@router.get("/texts/chapters", response_model=List[TextChapter])
async def get_book_text(q: Optional[List[str]] = Query([])):
    return await database_instance.get_chapters(q)

@router.post("/clusterize", response_model=List[ClusteringResults])
async def post_clusterize(book: Optional[List[str]] = Query([])):
    # Get the text associated with the query
    texts = await database_instance.get_texts(book)
    # Format the text according to the one required by the optimizer
    text_corpus = []
    text_names = []
    for book_data in texts:
        text_corpus.append(book_data["text"])
        text_names.append(book_data["book"])
    print(text_names)
    # Get the corresponding ground truth group
    ground_truth = await database_instance.get_book_class(text_names)
    return gnt_clusterer.pipeline(text_corpus=text_corpus,
                                  names=text_names,
                                  n_clusters=10,
                                  ground_truth=ground_truth)

@router.post("/clusterize/chapters", response_model=List[ClusteringResults])
async def post_clusterize(book: Optional[List[str]] = Query([])):
    """
    Perform clustering within chapters.
    """
    # Get the text associated with the query
    texts = await database_instance.get_chapters(book)
    # Format the text according to the one required by the optimizer
    text_corpus = []
    text_names = []
    book_chapter_label = []
    # For each book
    for book_data in texts:
        # Get the data on a per chapter basis
        for chapter_nbr, chapter_content in book_data["chapters"].items():
            text_corpus.append(chapter_content)
            text_names.append(book_data["book"])
            book_chapter_label.append(f"{chapter_nbr}{book_data['book']}")
    return gnt_clusterer.pipeline(text_corpus=text_corpus,
                                  names=book_chapter_label,
                                  n_clusters=10,
                                  ground_truth=text_names)

@router.post("/clusterize/verses", response_model=List[ClusteringResults])
async def post_clusterize(book: Optional[List[str]] = Query([])):
    """
    Perform clustering within verses.
    """
    # Get the text associated with the query
    texts = await database_instance.get_verses(book)
    # Format the text according to the one required by the optimizer
    text_corpus = []
    text_names = []
    book_chapter_verse_label = []
    # For each book
    for book_data in texts:
        # Get the data on a per chapter basis
        for chapter_nbr, chapter_content in book_data["verses"].items():
            for verse_nbr, verse_content in chapter_content.items():
                text_corpus.append(verse_content)
                text_names.append(book_data["book"])
                book_chapter_verse_label.append(f"{book_data['book']}{chapter_nbr},{verse_nbr}")
    clustering_results =  gnt_clusterer.pipeline(text_corpus=text_corpus,
                                  names=book_chapter_verse_label,
                                  n_clusters=10,
                                  ground_truth=text_names)
    return clustering_results
