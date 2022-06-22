import os
from pathlib import Path
from typing import Callable, Optional

from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.types import Scope

if os.environ.get("DEV"):
    # I work with the following layout during development:
    # \__ build
    #     \__ index.html
    # \__ backend
    #     \__ quara
    #         \__agent
    #             \__ server.py
    # So:
    #   parent => ~/backend/quara/agent
    #   parent.parent => ~/backend/quara
    #   parent.parent.parent => ~/backend
    #   parent.parent.parent.parent / "build" => ~/build
    STATIC_ROOT = os.environ.get(
        "STATIC_ROOT", Path(__file__).parent.parent.parent.parent / "build"
    )
else:
    # In production we expect HTML build directory to be found in ~/backend/quara/agent/html
    # But it's always possible to use STATIC_ROOT environment variable to configure location of HTML build directory.
    STATIC_ROOT = os.environ.get("STATIC_ROOT", Path(__file__).parent / "html")


class SPAStaticFiles(StaticFiles):
    """Serve a single page application"""

    async def get_response(self, path: str, scope: Scope):

        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response(".", scope)
        return response


def create_server(
    api: FastAPI, html_root: Optional[str] = None
) -> Starlette:

    # Check if web directory was provided
    if html_root is None:
        html_root = STATIC_ROOT

    # First create an instance of StaticFiles to serve the HTML directory
    website = SPAStaticFiles(directory=html_root, html=True)

    # Create a Starlette instance
    server = Starlette(
        on_startup=api.on_startup,
        on_shutdown=api.on_shutdown,
        routes=[
            Mount("/api", api, name="api"),
            Mount("/", website, name="web"),
        ]
    )

    # Return the Starlette instance
    return server


def factory() -> None:
    """A factory used by uvicorn to start the application.

    Uvicorn factories are called without argument.
    They should return an ASGI application such as a Starlette application or FastAPI application.

    In our case, we return a Starlette application which is has two routes:
        - A mounted FastAPI application on "/api": The API
        - A mounted StaticFile application on "/": The frontend

    To start a new server simply run:
        $ uvicorn --factory quara.agent.server

    Configuration should be provided either through environment variables or through files.
    """
    # Let's say we've got a function which returns a FastAPI application in a module
    #       No argument   A FastAPI instance
    #             |         |
    #             V         V
    # create_app: ()  ->  FastAPI
    from gnt_api.main import app

    # Use create_server to return a server as Starlette instance
    return create_server(app)
