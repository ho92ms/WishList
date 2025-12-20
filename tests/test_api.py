from __future__ import annotations

import os
import tempfile

import pytest
from httpx import AsyncClient

# Set a dedicated test DB before importing the app/settings
_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}"

from backend.main import app  # noqa: E402


@pytest.mark.parametrize("tag", ["food", "culture", "nature"])
@pytest.mark.asyncio
async def test_create_wishlist_item_ok(tag: str):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "city": "Budapest",
            "poi_id": f"poi_{tag}",
            "name": "Test POI",
            "address": "Test Address",
            "tag": tag,
        }
        r = await ac.post("/wishlist", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["tag"] == tag
        assert data["city"] == "Budapest"


@pytest.mark.asyncio
async def test_list_wishlist_items_returns_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/wishlist")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_delete_nonexistent_returns_404():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.delete("/wishlist/999999")
        assert r.status_code == 404
