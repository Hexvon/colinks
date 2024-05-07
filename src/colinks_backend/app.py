from contextlib import asynccontextmanager

from fastapi import FastAPI

from colinks_backend.api.colinks import router as links_router
from colinks_backend.config import CONFIG
from colinks_backend.db.engine import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=CONFIG.project_name, docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {}


# Routers
app.include_router(links_router)
