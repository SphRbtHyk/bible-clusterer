"""
Python module containing the different endpoints of the application related to the
available texts.
"""
from typing import List, Optional
from fastapi import APIRouter, Query
from lxx_api.instances import database_instance, lxx_clusterer
from lxx_api.models import BookList, ClusteringResults, TextList, BookClasses

router = APIRouter()


@router.get("/booklists", response_model=List[BookList])
async def get_book_list():
    return await database_instance.get_book_lists()


@router.get("/bookclasses", response_model=List[BookClasses])
async def get_book_list():
    return await database_instance.get_book_classes()


@router.get("/texts", response_model=List[TextList])
async def get_book_text(q: Optional[List[str]] = Query([])):
    test = await database_instance.get_texts(q)
    return test


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
    # Get the corresponding ground truth group
    ground_truth = await database_instance.get_book_class(text_names)
    return lxx_clusterer.pipeline(text_corpus=text_corpus,
                                  names=text_names,
                                  n_clusters=10,
                                  ground_truth=ground_truth)
