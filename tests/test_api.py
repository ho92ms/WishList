from __future__ import annotations

import os
import sys
import tempfile

import pytest
import httpx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}"

from backend.main import app  # noqa: E402


def make_client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.parametrize("tag", ["food", "culture", "nature"])
@pytest.mark.asyncio
async def test_create_wishlist_item_ok(tag: str):
    async with make_client() as ac:
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
    async with make_client() as ac:
        r = await ac.get("/wishlist")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_delete_nonexistent_returns_404():
    async with make_client() as ac:
        r = await ac.delete("/wishlist/999999")
        assert r.status_code == 404
