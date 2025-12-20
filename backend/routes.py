from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models import WishlistItem
from backend.places_provider import PlacesProvider, PlacesProviderError
from backend.schemas import WishlistCreate, WishlistOut
from backend import stats as stats_service

router = APIRouter()
log = logging.getLogger("api")
provider = PlacesProvider()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/places/search")
def places_search(city: str, query: str = ""):
    try:
        return {"results": provider.search(city=city, query=query)}
    except PlacesProviderError as e:
        log.exception("Places provider failed")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        # ez fogja meg pl. a requests timeoutot, ha mégis átszivárogna
        log.exception("Unexpected error in places_search")
        raise HTTPException(status_code=502, detail=f"Upstream timeout/error: {e}")



@router.post("/wishlist", response_model=WishlistOut)
def wishlist_add(payload: WishlistCreate, db: Session = Depends(get_db)):
    item = WishlistItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/wishlist", response_model=list[WishlistOut])
def wishlist_list(tag: str | None = None, db: Session = Depends(get_db)):
    q = db.query(WishlistItem)
    if tag:
        q = q.filter(WishlistItem.tag == tag)
    return q.order_by(WishlistItem.created_at.desc()).all()


@router.delete("/wishlist/{item_id}")
def wishlist_delete(item_id: int, db: Session = Depends(get_db)):
    item = db.query(WishlistItem).filter(WishlistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"deleted": item_id}


@router.get("/stats/top-tags")
def stats_top_tags(db: Session = Depends(get_db)):
    return {"top_tags": stats_service.top_tags(db)}


@router.get("/stats/top-cities")
def stats_top_cities(db: Session = Depends(get_db)):
    return {"top_cities": stats_service.top_cities(db)}


@router.get("/stats/weekly-top")
def stats_weekly_top(db: Session = Depends(get_db)):
    return stats_service.latest_weekly_report(db)
