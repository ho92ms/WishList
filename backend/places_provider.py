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

        time.sleep(0.3)  # OSM etiquette
        return self._overpass_search(lat=lat, lon=lon, query=query)

    def _headers(self) -> Dict[str, str]:
        return {
            "User-Agent": settings.osm_user_agent,
            "Accept": "application/json",
        }

    # ---------- GEOCODING ----------

    def _geocode_city(self, city: str) -> Tuple[float, float]:
        if not city:
            raise PlacesProviderError("City is empty")

        key = city.lower()
        if key in self._city_cache:
            return self._city_cache[key]

        if settings.geocoder_provider.lower() == "open_meteo":
            lat, lon = self._geocode_city_open_meteo(city)
            self._city_cache[key] = (lat, lon)
            return lat, lon

        # fallback: Nominatim (lokál)
        url = f"{settings.nominatim_base_url}/search"
        params = {"q": city, "format": "json", "limit": 1}

        try:
            r = requests.get(
                url,
                params=params,
                headers=self._headers(),
                timeout=settings.places_http_timeout_s,
            )
        except requests.RequestException as e:
            raise PlacesProviderError(f"Nominatim request failed: {e}")

        if r.status_code != 200:
            raise PlacesProviderError(f"Nominatim HTTP {r.status_code}")

        data = _safe_json(r)
        if not data:
            raise PlacesProviderError(f"City not found: {city}")

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        self._city_cache[key] = (lat, lon)
        return lat, lon

    def _geocode_city_open_meteo(self, city: str) -> Tuple[float, float]:
        url = f"{settings.openmeteo_geocoding_base_url}/search"
        params = {"name": city, "count": 1, "format": "json"}

        try:
            r = requests.get(
                url,
                params=params,
                headers=self._headers(),
                timeout=settings.places_http_timeout_s,
            )
        except requests.RequestException as e:
            raise PlacesProviderError(f"Open-Meteo geocoding request failed: {e}")

        if r.status_code != 200:
            raise PlacesProviderError(f"Open-Meteo HTTP {r.status_code}")

        data = _safe_json(r)
        results = data.get("results") or []
        if not results:
            raise PlacesProviderError(f"City not found (Open-Meteo): {city}")

        return float(results[0]["latitude"]), float(results[0]["longitude"])



    def _filters(self, query: str) -> List[str]:
        if not query:
            return [
                'node(around:R, LAT, LON)["tourism"];',
                'node(around:R, LAT, LON)["amenity"];',
            ]

        safe = re.escape(query)
        return [
            f'node(around:R, LAT, LON)["name"~"{safe}",i];',
            f'node(around:R, LAT, LON)["amenity"]["name"~"{safe}",i];',
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
        except requests.RequestException as e:
            raise PlacesProviderError(f"Overpass request failed: {e}")

        if r.status_code != 200:
            raise PlacesProviderError(f"Overpass HTTP {r.status_code}")

        return _safe_json(r)

    def _overpass_search(self, lat: float, lon: float, query: str) -> List[Dict[str, Any]]:
        ql = self._overpass_query(lat, lon, query)
        urls = [settings.overpass_base_url]

        if settings.overpass_fallback_url:
            urls.append(settings.overpass_fallback_url)

        last_error = None

        for url in urls:
            try:
                payload = self._try_overpass(url, ql)
                elements = payload.get("elements", [])
                results = self._elements_to_results(elements)
                return results[: settings.places_limit]
            except PlacesProviderError as e:
                last_error = str(e)

        raise PlacesProviderError(last_error or "Overpass failed")

    def _elements_to_results(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []

        for el in elements:
            tags = el.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            results.append(
                {
                    "poi_id": f"osm:{el.get('type')}:{el.get('id')}",
                    "name": name,
                    "address": self._format_address(tags),
                    "lat": el.get("lat"),
                    "lon": el.get("lon"),
                }
            )

        return results

    def _format_address(self, tags: Dict[str, Any]) -> Optional[str]:
        parts = [tags.get(k) for k in ("addr:street", "addr:housenumber", "addr:city") if tags.get(k)]
        return " ".join(parts) if parts else None
