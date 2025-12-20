from __future__ import annotations

import re
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests import Response

from backend.config import settings


class PlacesProviderError(RuntimeError):
    pass


def _safe_json(resp: Response) -> Any:
    try:
        return resp.json()
    except ValueError:
        text = (resp.text or "").strip()
        snippet = text[:300].replace("\n", " ")
        raise PlacesProviderError(f"Non-JSON response (HTTP {resp.status_code}): {snippet}")


class PlacesProvider:
    def __init__(self) -> None:
        self._city_cache: Dict[str, Tuple[float, float]] = {}

    def search(self, city: str, query: str = "") -> List[Dict[str, Any]]:
        if settings.places_provider.lower() != "osm":
            raise PlacesProviderError(f"Unsupported provider: {settings.places_provider}")

        city = city.strip()
        query = query.strip()

        lat, lon = self._geocode_city(city)

        # Udvariasság
        time.sleep(0.3)

        return self._overpass_search(lat=lat, lon=lon, query=query)

    def _headers(self) -> Dict[str, str]:
        return {"User-Agent": settings.osm_user_agent, "Accept": "application/json"}

    def _geocode_city(self, city: str) -> Tuple[float, float]:
        if not city:
            raise PlacesProviderError("City is empty")

        key = city.lower()
        if key in self._city_cache:
            return self._city_cache[key]

        url = f"{settings.nominatim_base_url}/search"
        params = {"q": city, "format": "json", "limit": 1}

        try:
            r = requests.get(url, params=params, headers=self._headers(), timeout=settings.places_http_timeout_s)
        except requests.RequestException as e:
            raise PlacesProviderError(f"Nominatim request failed: {e}")

        if r.status_code != 200:
            raise PlacesProviderError(f"Nominatim HTTP {r.status_code}: {(r.text or '')[:200]}")

        data = _safe_json(r)
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

    def _overpass_query(self, lat: float, lon: float, query: str) -> str:
        radius = int(settings.places_radius_m)
        blocks = [
            b.replace("R", str(radius)).replace("LAT", str(lat)).replace("LON", str(lon))
            for b in self._filters(query)
        ]
        return f"""
[out:json][timeout:25];
(
  {' '.join(blocks)}
);
out center;
"""

    def _try_overpass(self, url: str, ql: str) -> Dict[str, Any]:
        try:
            r = requests.post(
                url,
                data={"data": ql},
                headers=self._headers(),
                timeout=settings.places_http_timeout_s,
            )
        except requests.ReadTimeout:
            raise PlacesProviderError(f"Overpass timeout at {url}")
        except requests.RequestException as e:
            raise PlacesProviderError(f"Overpass request failed at {url}: {e}")

        if r.status_code != 200:
            raise PlacesProviderError(f"Overpass HTTP {r.status_code} at {url}: {(r.text or '')[:250]}")

        payload = _safe_json(r)
        return payload

    def _overpass_search(self, lat: float, lon: float, query: str) -> List[Dict[str, Any]]:
        limit = int(settings.places_limit)
        ql = self._overpass_query(lat, lon, query)

        urls = [settings.overpass_base_url]
        fallback = getattr(settings, "overpass_fallback_url", None)
        if fallback:
            urls.append(fallback)

        last_err: Optional[str] = None

        # próbáljuk mindkét endpointot 1-1 alkalommal, minimális backoffal
        for url in urls:
            for attempt in (1, 2):
                try:
                    if attempt > 1:
                        time.sleep(0.6)
                    payload = self._try_overpass(url, ql)
                    elements = payload.get("elements", [])
                    results = self._elements_to_results(elements)
                    results.sort(key=lambda x: x["name"].lower())
                    return results[:limit]
                except PlacesProviderError as e:
                    last_err = str(e)

        raise PlacesProviderError(last_err or "Overpass failed")

    def _elements_to_results(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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

        return [x for x in (to_result(e) for e in elements) if x is not None]

    def _format_address(self, tags: Dict[str, Any]) -> Optional[str]:
        parts = []
        for k in ("addr:street", "addr:housenumber", "addr:city", "addr:postcode"):
            if tags.get(k):
                parts.append(tags.get(k))
        return " ".join([p for p in parts if p]) if parts else None
