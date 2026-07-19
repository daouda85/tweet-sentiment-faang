import json

import pytest

from src.api import main


@pytest.mark.asyncio
async def test_tweets_endpoint_uses_configured_export(tmp_path, monkeypatch):
    export = tmp_path / "tweets.json"
    export.write_text(json.dumps([{"id": "42", "text": "Netflix earnings update"}]))
    monkeypatch.setattr(main.twitter_config, "XQUIK_EXPORT_PATH", str(export))

    response = await main.get_tweets(limit=1)

    assert response["source"] == "xquik_export"
    assert response["count"] == 1
    assert response["tweets"][0]["id"] == "42"
    assert response["tweets"][0]["text"] == "Netflix earnings update"
