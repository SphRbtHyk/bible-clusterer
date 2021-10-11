# Copyright 2020 BULL SAS All rights reserved

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lxx_api.instances import database_instance
from lxx_api.routers import router


app = FastAPI(
    title="LXX clusterer API",
    version="1.0.0",
    description="A REST API to interact with the lxx data",
)


@app.on_event("startup")
async def startup():
    await database_instance.connect()
    print("Connected mongo database")


@app.on_event("shutdown")
async def startup():
    await database_instance.close()


app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origin_regex="http?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
