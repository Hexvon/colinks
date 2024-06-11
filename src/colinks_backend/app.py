import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from colinks_backend.api.redirector import router as redirect_router
from colinks_backend.api.routers import router as links_router
from colinks_backend.config import CONFIG
from colinks_backend.db.engine import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=CONFIG.project_name)
api_app = FastAPI(title="colinks_api", docs_url="/docs")
app.mount("/api", api_app)

cur_dir = os.path.dirname(os.path.abspath(__file__))
front_dir = os.path.join(cur_dir, "frontend")
app.mount("/", StaticFiles(directory=front_dir, html=True))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {}


# Routers
api_app.include_router(links_router)
api_app.include_router(redirect_router)
