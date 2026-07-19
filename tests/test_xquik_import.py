import json

import pytest

from src.data.xquik_import import load_xquik_export


def test_skips_blank_rows_before_applying_limit(tmp_path):
    export = tmp_path / "tweets.json"
    export.write_text(
        json.dumps(
            [
                {"text": ""},
                {"text": float("nan")},
                {"text": "first valid tweet"},
                {"text": "second valid tweet"},
            ]
        )
    )

    tweets = load_xquik_export(str(export), limit=2)

    assert [tweet["text"] for tweet in tweets] == [
        "first valid tweet",
        "second valid tweet",
    ]


def test_maps_nested_author_and_public_metrics(tmp_path):
    export = tmp_path / "tweets.json"
    export.write_text(
        json.dumps(
            {
                "data": [
                    {
                        "id": "123",
                        "text": "Apple launch reactions #AAPL",
                        "author": {
                            "username": "analyst",
                            "public_metrics": {"followers_count": "1200"},
                        },
                        "public_metrics": {
                            "retweet_count": 7,
                            "like_count": 19,
                        },
                        "sentiment": " Positive ",
                        "confidence": 92,
                    }
                ]
            }
        )
    )

    tweet = load_xquik_export(str(export), limit=1)[0]

    assert tweet["user"] == {
        "name": "analyst",
        "screen_name": "analyst",
        "followers_count": 1200,
    }
    assert tweet["retweet_count"] == 7
    assert tweet["favorite_count"] == 19
    assert tweet["hashtags"] == ["#AAPL"]
    assert tweet["sentiment"] == "positive"
    assert tweet["confidence"] == pytest.approx(0.92)


def test_normalises_invalid_numeric_values(tmp_path):
    export = tmp_path / "tweets.jsonl"
    export.write_text(
        json.dumps(
            {
                "text": "Neutral update",
                "followers_count": -5,
                "retweet_count": "12.8",
                "favorite_count": "not-a-number",
                "confidence": "nan",
            }
        )
    )

    tweet = load_xquik_export(str(export), limit=1)[0]

    assert tweet["user"]["followers_count"] == 0
    assert tweet["retweet_count"] == 12
    assert tweet["favorite_count"] == 0
    assert tweet["confidence"] == pytest.approx(0.75)


def test_ignores_non_object_jsonl_records(tmp_path):
    export = tmp_path / "tweets.jsonl"
    export.write_text(
        "\n".join(
            [
                json.dumps("metadata"),
                json.dumps({"id": "42", "text": "valid tweet"}),
            ]
        )
    )

    tweets = load_xquik_export(str(export), limit=1)

    assert [tweet["id"] for tweet in tweets] == ["42"]


def test_non_positive_limit_returns_no_rows(tmp_path):
    export = tmp_path / "tweets.json"
    export.write_text(json.dumps([{"text": "unused"}]))

    assert load_xquik_export(str(export), limit=0) == []
