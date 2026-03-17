"""NewsAPI news source."""

import logging

import requests

from ..config import settings
from ..core.exceptions import APIError
from ..core.models import Article
from . import NewsSource


class NewsAPI(NewsSource):
    """News source for NewsAPI."""

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = settings.newsapi_api_key

    def fetch_articles(self, query: str):
        """Fetch articles from NewsAPI."""
        logger = logging.getLogger(__name__)
        logger.debug(f"Fetching articles from NewsAPI for query: {query}")

        params = {
            "q" : query,
            "apiKey"  :  self.api_key,
            "pageSize": settings.max_articles,
            "language" : "es"
        }
        try:
            logger.debug("Making request to NewsAPI")
            response = requests.get(self.BASE_URL, params=params, timeout=settings.request_timeout)
            response.raise_for_status()
            data = response.json()
            articles = [
                Article(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    url=article.get("url", ""),
                )
            for article in data.get("articles", [])
            ]
            logger.info(f"Retrieved {len(articles)} articles from NewsAPI")
            return articles
        except requests.RequestException as e:
            logger.error(f"Failed to fetch articles from NewsAPI: {e}")
            msg = f"Error al obtener artículos de NewsAPI: {e}. Verifique su conexión a internet y la clave de API de NewsAPI."
            raise APIError(msg) from e