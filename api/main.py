import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, applications, ratings, admin, documentation

from data import setup
import config

from constants import API_TAGS_METADATA

config.parse_args()
app = FastAPI(
    title="App Listing",
    description="Public API Rally community applications listing",
    version="1.0.1",
    openapi_tags=API_TAGS_METADATA,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(ratings.router)
app.include_router(applications.router)
app.include_router(users.router)
app.include_router(documentation.router)


@app.get("/")
async def docs_info():
    return {"docs": "api documentation at /docs or /redoc"}


if __name__ == "__main__":
    setup.admin()
    uvicorn.run("main:app", host=config.CONFIG.host, port=int(config.CONFIG.port))
