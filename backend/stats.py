from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models import WeeklyReport, WishlistItem


def top_tags(db: Session) -> List[Dict]:
    rows = db.query(WishlistItem.tag, func.count(WishlistItem.id)).group_by(WishlistItem.tag).all()
    return [{"tag": tag, "count": cnt} for tag, cnt in rows]


def top_cities(db: Session) -> List[Dict]:
    rows = db.query(WishlistItem.city, func.count(WishlistItem.id)).group_by(WishlistItem.city).all()
    return [{"city": city, "count": cnt} for city, cnt in rows]


def compute_weekly_top(db: Session, days: int = 7, limit: int = 10) -> List[Dict]:
    since = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.query(WishlistItem.poi_id, WishlistItem.name, func.count(WishlistItem.id).label("cnt"))
        .filter(WishlistItem.created_at >= since)
        .group_by(WishlistItem.poi_id, WishlistItem.name)
        .order_by(func.count(WishlistItem.id).desc())
        .limit(limit)
        .all()
    )
    return [{"poi_id": poi_id, "name": name, "count": cnt} for poi_id, name, cnt in rows]


def save_weekly_report(db: Session, payload: List[Dict]) -> WeeklyReport:
    report = WeeklyReport(payload_json=json.dumps(payload, ensure_ascii=False))
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def latest_weekly_report(db: Session) -> Dict:
    r = db.query(WeeklyReport).order_by(WeeklyReport.generated_at.desc()).first()
    if not r:
        return {"generated_at": None, "items": []}
    return {"generated_at": str(r.generated_at), "items": json.loads(r.payload_json)}
