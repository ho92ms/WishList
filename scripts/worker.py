from __future__ import annotations

import os
import sys
import time
import schedule

# Ensure project root is on sys.path when running directly
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config import settings  # noqa: E402
from backend.db import SessionLocal, init_db  # noqa: E402
from backend.stats import compute_weekly_top, save_weekly_report  # noqa: E402


def job() -> None:
    db = SessionLocal()
    try:
        payload = compute_weekly_top(db=db, days=settings.weekly_report_days, limit=settings.weekly_report_top_n)
        save_weekly_report(db=db, payload=payload)
        print("Weekly report generated:", payload)
    finally:
        db.close()


def main() -> None:
    init_db()

    schedule.every(7).days.do(job)
    job()  # run once at start for easy demo

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
