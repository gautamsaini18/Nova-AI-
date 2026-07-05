"""Nova AI — Navigation & Maps Service

Provides directions, places search, traffic info,
and GPS integration via Google Maps / OpenStreetMap.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import httpx

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("navigation.service")


@dataclass
class Place:
    name: str
    address: str
    rating: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    distance: Optional[str] = None


@dataclass
class Direction:
    distance: str
    duration: str
    polyline: Optional[str] = None
    steps: list[str] = None


class NavigationService:
    """
    Maps, directions, and places search.
    Uses Google Maps API when available, falls back to OpenStreetMap.
    """

    def __init__(self) -> None:
        self._api_key = settings.GOOGLE_API_KEY
        logger.info("NavigationService initialized")

    async def search_places(self, query: str, location: Optional[str] = None) -> list[Place]:
        """Search for places (restaurants, hospitals, etc.)."""
        if self._api_key:
            return await self._search_google(query, location)
        return await self._search_osm(query, location)

    async def _search_google(self, query: str, location: Optional[str]) -> list[Place]:
        """Search places via Google Places API."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                params = {"query": query, "key": self._api_key}
                if location:
                    params["location"] = location
                resp = await client.post(
                    "https://places.googleapis.com/v1/places:searchText",
                    json={"textQuery": query},
                    headers={"X-Goog-Api-Key": self._api_key, "Content-Type": "application/json"},
                    params={"fields": "places.displayName,places.formattedAddress,places.rating,places.location,places.nationalPhoneNumber,places.websiteUri"},
                )
                resp.raise_for_status()
                data = resp.json()
                places = []
                for p in data.get("places", []):
                    places.append(Place(
                        name=p.get("displayName", {}).get("text", ""),
                        address=p.get("formattedAddress", ""),
                        rating=p.get("rating"),
                        latitude=p.get("location", {}).get("latitude"),
                        longitude=p.get("location", {}).get("longitude"),
                        phone=p.get("nationalPhoneNumber"),
                        website=p.get("websiteUri"),
                    ))
                return places
        except Exception as exc:
            logger.warning("Google Places search failed", error=str(exc))
            return []

    async def _search_osm(self, query: str, location: Optional[str]) -> list[Place]:
        """Search places via OpenStreetMap Nominatim."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                params = {"q": query, "format": "json", "limit": 5}
                if location:
                    params["city"] = location
                resp = await client.get("https://nominatim.openstreetmap.org/search", params=params)
                resp.raise_for_status()
                data = resp.json()
                return [
                    Place(
                        name=p.get("display_name", "").split(",")[0],
                        address=p.get("display_name", ""),
                        latitude=float(p["lat"]) if p.get("lat") else None,
                        longitude=float(p["lon"]) if p.get("lon") else None,
                    )
                    for p in data
                ]
        except Exception as exc:
            logger.warning("OSM search failed", error=str(exc))
            return []

    async def get_directions(self, origin: str, destination: str) -> Optional[Direction]:
        """Get driving directions between two points."""
        if not self._api_key:
            logger.warning("Google API key required for directions")
            return None
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://maps.googleapis.com/maps/api/directions/json",
                    params={"origin": origin, "destination": destination, "key": self._api_key, "mode": "driving"},
                )
                resp.raise_for_status()
                data = resp.json()
                if not data.get("routes"):
                    return None
                route = data["routes"][0]
                leg = route["legs"][0]
                return Direction(
                    distance=leg["distance"]["text"],
                    duration=leg["duration"]["text"],
                    polyline=route.get("overview_polyline", {}).get("points"),
                    steps=[s["html_instructions"] for s in leg["steps"]],
                )
        except Exception as exc:
            logger.warning("Directions fetch failed", error=str(exc))
            return None

    def format_directions_response(self, origin: str, destination: str, direction: Direction) -> str:
        """Format directions into a natural language response."""
        return (
            f"From {origin} to {destination} is {direction.distance} and will take "
            f"approximately {direction.duration}. I'll send the route to your phone."
        )
