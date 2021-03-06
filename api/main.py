import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import users, applications, ratings, admin, documentation, meta, dashboard

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

origins = [os.getenv("FRONTEND_URL")]
if not origins[0]:
    origins = [config.CONFIG.frontend, "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ,["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="api/static"), name="static")

app.include_router(admin.router)
app.include_router(ratings.router)
app.include_router(applications.router)
app.include_router(users.router)
app.include_router(documentation.router)
app.include_router(meta.router)
app.include_router(dashboard.router)


@app.get("/")
async def docs_info():
    return {"docs": "api documentation at /docs or /redoc"}


if __name__ == "__main__":
    setup.admin()
    setup.migrate()
    uvicorn.run(
        "main:app",
        host=config.CONFIG.host,
        port=int(config.CONFIG.port),
        reload=bool(config.CONFIG.reload),
    )
