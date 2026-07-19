"""Helpers for loading Xquik or TweetClaw tweet exports."""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TEXT_FIELDS = ("text", "content", "tweet_text", "full_text", "body")
ID_FIELDS = ("id", "tweet_id", "tweetId", "url")
AUTHOR_FIELDS = ("author", "username", "screen_name", "user", "handle")
CREATED_FIELDS = ("created_at", "createdAt", "timestamp", "date")


def load_xquik_export(path: str, limit: int) -> list[dict[str, Any]]:
    """Load an Xquik or TweetClaw export into the dashboard tweet shape."""
    if limit <= 0:
        return []

    source_path = Path(path).expanduser()
    rows = _read_rows(source_path)

    tweets: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        text = _first_text(row, TEXT_FIELDS)
        if not text:
            continue

        author = _author_name(row) or "xquik_export"
        created_at = (
            _first_text(row, CREATED_FIELDS) or datetime.now(timezone.utc).isoformat()
        )
        tweet_id = _first_text(row, ID_FIELDS) or f"xquik-{index}"

        tweets.append(
            {
                "id": str(tweet_id),
                "text": text,
                "created_at": created_at,
                "user": {
                    "name": author.lstrip("@"),
                    "screen_name": author.lstrip("@"),
                    "followers_count": _as_int(_metric_value(row, "followers_count")),
                },
                "retweet_count": _as_int(
                    _metric_value(row, "retweet_count", "retweets")
                ),
                "favorite_count": _as_int(
                    _metric_value(row, "favorite_count", "like_count", "likes")
                ),
                "hashtags": _extract_hashtags(row, text),
                "sentiment": _normalise_sentiment(row.get("sentiment")),
                "confidence": _as_float(row.get("confidence"), default=0.75),
                "source": "xquik_export",
            }
        )

        if len(tweets) == limit:
            break

    return tweets


def _read_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return [dict(row) for row in csv.DictReader(handle)]

    raw = path.read_text(encoding="utf-8-sig").strip()
    if not raw:
        return []

    if suffix in {".jsonl", ".ndjson"}:
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
        return [row for row in rows if isinstance(row, dict)]

    payload = json.loads(raw)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("tweets", "data", "items", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
        return [payload]
    return []


def _first_text(row: dict[str, Any], fields: tuple[str, ...]) -> str:
    for field in fields:
        value = row.get(field)
        if isinstance(value, float) and not math.isfinite(value):
            continue
        if isinstance(value, (str, int, float)) and str(value).strip():
            return str(value).strip()
    return ""


def _author_name(row: dict[str, Any]) -> str:
    author = _first_text(row, AUTHOR_FIELDS)
    if author:
        return author

    for field in ("author", "user"):
        value = row.get(field)
        if isinstance(value, dict):
            author = _first_text(value, ("username", "screen_name", "name"))
            if author:
                return author
    return ""


def _metric_value(row: dict[str, Any], *fields: str) -> Any:
    containers = [row]
    for field in ("public_metrics", "metrics", "author", "user"):
        value = row.get(field)
        if isinstance(value, dict):
            containers.append(value)
            nested_metrics = value.get("public_metrics")
            if isinstance(nested_metrics, dict):
                containers.append(nested_metrics)

    for container in containers:
        for field in fields:
            value = container.get(field)
            if value is not None:
                return value
    return None


def _extract_hashtags(row: dict[str, Any], text: str) -> list[str]:
    value = row.get("hashtags")
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [tag.strip() for tag in value.replace(",", " ").split()]
    return [word for word in text.split() if word.startswith("#")]


def _normalise_sentiment(value: Any) -> str:
    sentiment = str(value or "neutral").strip().casefold()
    if sentiment in {"positive", "negative", "neutral"}:
        return sentiment
    return "neutral"


def _as_int(value: Any) -> int:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0
    if not math.isfinite(number):
        return 0
    return max(0, int(number))


def _as_float(value: Any, *, default: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    if 1 < number <= 100:
        number /= 100
    return min(1.0, max(0.0, number))
