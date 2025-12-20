from __future__ import annotations

import re
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

from backend.config import settings


class PlacesProviderError(RuntimeError):
    pass


class PlacesProvider:
    def __init__(self) -> None:
        self._city_cache: Dict[str, Tuple[float, float]] = {}

    def search(self, city: str, query: str = "") -> List[Dict[str, Any]]:
        if settings.places_provider.lower() != "osm":
            raise PlacesProviderError(f"Unsupported provider: {settings.places_provider}")

        city = city.strip()
        query = query.strip()

        lat, lon = self._geocode_city(city)
        time.sleep(0.2)  # etiquette / rate limit friendliness
        return self._overpass_search(lat=lat, lon=lon, query=query)

    def _headers(self) -> Dict[str, str]:
        return {"User-Agent": settings.osm_user_agent}

    def _geocode_city(self, city: str) -> Tuple[float, float]:
        if not city:
            raise PlacesProviderError("City is empty")

        key = city.lower()
        if key in self._city_cache:
            return self._city_cache[key]

        url = f"{settings.nominatim_base_url}/search"
        params = {"q": city, "format": "json", "limit": 1}
        r = requests.get(url, params=params, headers=self._headers(), timeout=settings.places_http_timeout_s)
        if r.status_code != 200:
            raise PlacesProviderError(f"Nominatim error: HTTP {r.status_code}")

        data = r.json()
        if not data:
            raise PlacesProviderError(f"City not found: {city}")

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        self._city_cache[key] = (lat, lon)
        return lat, lon

    def _filters(self, query: str) -> List[str]:
        if not query:
            return [
                'node(around:R, LAT, LON)["tourism"];',
                'node(around:R, LAT, LON)["amenity"];',
                'node(around:R, LAT, LON)["leisure"];',
            ]

        safe = re.escape(query)
        return [
            f'node(around:R, LAT, LON)["name"~"{safe}",i];',
            f'node(around:R, LAT, LON)["amenity"]["name"~"{safe}",i];',
            f'node(around:R, LAT, LON)["tourism"]["name"~"{safe}",i];',
        ]

    def _overpass_search(self, lat: float, lon: float, query: str) -> List[Dict[str, Any]]:
        radius = int(settings.places_radius_m)
        limit = int(settings.places_limit)

        blocks = [b.replace("R", str(radius)).replace("LAT", str(lat)).replace("LON", str(lon)) for b in self._filters(query)]

        overpass_ql = f"""
[out:json][timeout:25];
(
  {' '.join(blocks)}
);
out center;
"""

        r = requests.post(
            settings.overpass_base_url,
            data={"data": overpass_ql},
            headers=self._headers(),
            timeout=settings.places_http_timeout_s,
        )
        if r.status_code != 200:
            raise PlacesProviderError(f"Overpass error: HTTP {r.status_code}")

        payload = r.json()
        elements = payload.get("elements", [])

        def to_result(el: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            tags = el.get("tags", {})
            name = tags.get("name")
            if not name:
                return None

            poi_id = f"osm:{el.get('type')}:{el.get('id')}"
            return {
                "poi_id": poi_id,
                "name": name,
                "address": self._format_address(tags),
                "lat": el.get("lat"),
                "lon": el.get("lon"),
            }

        results = [x for x in (to_result(e) for e in elements) if x is not None]
        results.sort(key=lambda x: x["name"].lower())
        return results[:limit]

    def _format_address(self, tags: Dict[str, Any]) -> Optional[str]:
        parts = []
        if tags.get("addr:street"):
            parts.append(tags.get("addr:street"))
        if tags.get("addr:housenumber"):
            parts.append(tags.get("addr:housenumber"))
        if tags.get("addr:city"):
            parts.append(tags.get("addr:city"))
        if tags.get("addr:postcode"):
            parts.append(tags.get("addr:postcode"))
        return " ".join([p for p in parts if p]) if parts else None
