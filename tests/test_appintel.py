"""Smoke tests for appintel."""

import argparse

from appintel.appintel import (
    __version__,
    build_parser,
    format_table,
    get_max,
    get_mean,
    get_median,
    get_min,
)


def test_version() -> None:
    assert __version__ == "1.0.4"


def test_build_parser_defaults() -> None:
    parser: argparse.ArgumentParser = build_parser()
    args = parser.parse_args([])
    assert args.search_term == "nginx"
    assert args.store_country == "us"
    assert args.category_location == "software"


def test_statistics() -> None:
    data = {"results": [{"price": 1.0}, {"price": 3.0}, {"price": 5.0}]}
    assert get_mean(data) == 3.0
    assert get_median(data) == 3.0
    assert get_min(data) == 1.0
    assert get_max(data) == 5.0


def test_format_table() -> None:
    results = [
        {"price": 1.0, "artistName": "Artist A", "trackName": "Song A"},
        {"price": 2.0, "artistName": "Artist B", "trackName": "Song B"},
    ]
    output = format_table(results)
    assert "price" in output
    assert "Artist A" in output
