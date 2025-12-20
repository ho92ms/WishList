from __future__ import annotations

from fastapi import FastAPI

from backend.db import init_db
from backend.logging_conf import setup_logging
from backend.routes import router

setup_logging()
init_db()

app = FastAPI(title="Travel Wishlist API")
app.include_router(router)
