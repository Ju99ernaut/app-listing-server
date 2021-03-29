import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, applications, ratings

import data
import config

from constants import *

config.parse_args()
app = FastAPI(
    title="App Listing",
    description="Public API Rally community applications listing",
    version="1.0.0",
    openapi_tags=API_TAGS_METADATA,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(applications.router)
app.include_router(ratings.router)


@app.get("/")
async def root():
    return {"docs": "api documentation at /docs or /redoc"}


if __name__ == "__main__":
    data.setup()
    uvicorn.run("main:app", host=config.CONFIG.host, port=int(config.CONFIG.port))
