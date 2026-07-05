"""Nova AI — External API Integrations

Central hub for third-party API services:
- News API
- Currency/Unit conversion
- Dictionary/Thesaurus
- Translation
- Flight/Train status
- Stock/Crypto prices
- Web scraping
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import httpx

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("api_services.integrations")


@dataclass
class NewsArticle:
    title: str
    description: str
    url: str
    source: str
    published_at: str


@dataclass
class ConversionResult:
    value: float
    unit_from: str
    unit_to: str
    result: float


class APIServiceHub:
    """
    Centralized API integrations for Nova AI.
    Manages all third-party API calls.
    """

    def __init__(self) -> None:
        self._news_api_key = settings.NEWS_API_KEY
        self._google_api_key = settings.GOOGLE_API_KEY
        logger.info("APIServiceHub initialized")

    # ── News ───────────────────────────────────────────────────────────────

    async def get_news(self, query: str = "technology", page_size: int = 5) -> list[NewsArticle]:
        """Fetch news articles from NewsAPI."""
        if not self._news_api_key:
            logger.warning("News API key not set")
            return []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://newsapi.org/v2/everything",
                    params={"q": query, "pageSize": page_size, "sortBy": "publishedAt", "apiKey": self._news_api_key},
                )
                resp.raise_for_status()
                data = resp.json()
                return [
                    NewsArticle(
                        title=a["title"],
                        description=a.get("description", ""),
                        url=a["url"],
                        source=a["source"]["name"],
                        published_at=a["publishedAt"],
                    )
                    for a in data.get("articles", [])
                ]
        except Exception as exc:
            logger.warning("News fetch failed", error=str(exc))
            return []

    # ── Currency Conversion ────────────────────────────────────────────────

    async def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> Optional[ConversionResult]:
        """Convert between currencies using open exchange rates."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"https://api.exchangerate-api.com/v4/latest/{from_curr.upper()}",
                )
                resp.raise_for_status()
                data = resp.json()
                rate = data["rates"].get(to_curr.upper())
                if rate:
                    return ConversionResult(
                        value=amount,
                        unit_from=from_curr.upper(),
                        unit_to=to_curr.upper(),
                        result=round(amount * rate, 2),
                    )
                return None
        except Exception as exc:
            logger.warning("Currency conversion failed", error=str(exc))
            return None

    # ── Dictionary ─────────────────────────────────────────────────────────

    async def lookup_word(self, word: str) -> Optional[dict]:
        """Look up a word definition using Free Dictionary API."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
                resp.raise_for_status()
                data = resp.json()[0]
                meanings = []
                for m in data.get("meanings", []):
                    for d in m.get("definitions", [])[:2]:
                        meanings.append({
                            "part_of_speech": m["partOfSpeech"],
                            "definition": d["definition"],
                            "example": d.get("example", ""),
                        })
                return {"word": word, "meanings": meanings, "phonetic": data.get("phonetic", "")}
        except Exception as exc:
            logger.warning("Dictionary lookup failed", error=str(exc))
            return None

    # ── Translation ─────────────────────────────────────────────────────────

    async def translate(self, text: str, target_language: str = "hi") -> Optional[str]:
        """Translate text using LibreTranslate or Google Translate."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    "https://libretranslate.de/translate",
                    json={"q": text, "source": "auto", "target": target_language},
                )
                resp.raise_for_status()
                return resp.json().get("translatedText")
        except Exception:
            pass

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"https://translate.googleapis.com/translate_a/single",
                    params={
                        "client": "gtx",
                        "sl": "auto",
                        "tl": target_language,
                        "dt": "t",
                        "q": text,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                return "".join([part[0] for part in data[0] if part[0]])
        except Exception as exc:
            logger.warning("Translation failed", error=str(exc))
            return None

    # ── Stock / Crypto ─────────────────────────────────────────────────────

    async def get_stock_price(self, symbol: str) -> Optional[dict]:
        """Get stock price using Alpha Vantage or Yahoo Finance."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                    params={"range": "1d", "interval": "1d"},
                )
                resp.raise_for_status()
                data = resp.json()
                meta = data["chart"]["result"][0]["meta"]
                return {
                    "symbol": symbol.upper(),
                    "price": meta["regularMarketPrice"],
                    "previous_close": meta["previousClose"],
                    "change": round(meta["regularMarketPrice"] - meta["previousClose"], 2),
                    "currency": meta.get("currency", "USD"),
                }
        except Exception as exc:
            logger.warning("Stock price fetch failed", error=str(exc))
            return None

    async def get_crypto_price(self, symbol: str = "bitcoin") -> Optional[dict]:
        """Get cryptocurrency price from CoinGecko."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"https://api.coingecko.com/api/v3/simple/price",
                    params={"ids": symbol.lower(), "vs_currencies": "usd,inr", "include_24hr_change": "true"},
                )
                resp.raise_for_status()
                data = resp.json()
                coin = data.get(symbol.lower(), {})
                return {
                    "symbol": symbol,
                    "price_usd": coin.get("usd"),
                    "price_inr": coin.get("inr"),
                    "change_24h": coin.get("usd_24h_change"),
                }
        except Exception as exc:
            logger.warning("Crypto price fetch failed", error=str(exc))
            return None
