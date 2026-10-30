"""A command line tool to search and compare prices of apps and music on the Apple Store."""

from __future__ import annotations

import argparse
import json
from pprint import pprint
from statistics import mean, median

import requests

__version__ = "1.0.3"

logo = """
+-------------------------------------+
|                         --\\         |
|                        /   -\\       |
|                       /      -\\     |
|                      /         -    |
|    \\                /               |
|     \\              /                |
|      \\           -/                 |
|       -\\        /                   |
|         \\      /                    |
|          \\    /       AppIntel      |
|           \\  /                      |
|            -/                       |
+-------------------------------------+
"""

ITUNES_URL_ENDPOINT = "https://itunes.apple.com/search?term={}&country={}&entity={}"


def get_content(
    search_term: str, store_country: str = "us", category: str = "software"
) -> requests.Response:
    """Fetch data from the iTunes search endpoint."""
    return requests.get(
        ITUNES_URL_ENDPOINT.format(search_term, store_country, category),
        timeout=10,
    )


def _prices(jsondata: dict) -> list[float]:
    return [float(item.get("price")) for item in jsondata.get("results", []) if "price" in item]


def get_mean(jsondata: dict) -> float:
    prices = _prices(jsondata)
    if not prices:
        return 0.0
    if len(prices) > 1:
        return mean(prices)
    return prices[0]


def get_max(jsondata: dict) -> float:
    prices = _prices(jsondata)
    if not prices:
        return 0.0
    if len(prices) > 1:
        return max(prices)
    return prices[0]


def get_min(jsondata: dict) -> float:
    prices = _prices(jsondata)
    if not prices:
        return 0.0
    if len(prices) > 1:
        return min(prices)
    return prices[0]


def get_median(jsondata: dict) -> float:
    prices = _prices(jsondata)
    if not prices:
        return 0.0
    if len(prices) > 1:
        return median(prices)
    return prices[0]


def format_table(results: list[dict]) -> str:
    if not results:
        return "(no results)"
    values = [
        (str(item.get("price")), str(item.get("artistName")), str(item.get("trackName")))
        for item in results
    ]
    header = ("price", "artistName", "trackName")
    rows = [header, *values]
    widths = [max(len(row[index]) for row in rows) for index in range(3)]
    lines = [" | ".join(field.ljust(widths[index]) for index, field in enumerate(header))]
    lines.append("-+-".join("-" * widths[index] for index in range(3)))
    lines.extend(
        " | ".join(field.ljust(widths[index]) for index, field in enumerate(row)) for row in values
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect and summarize data from the Apple iTunes Store",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s",
        "--search",
        dest="search_term",
        default="nginx",
        help="search term for the iTunes store",
    )
    parser.add_argument(
        "-c",
        "--category",
        dest="category_location",
        default="software",
        help="store category to search",
    )
    parser.add_argument(
        "-p",
        "--print",
        dest="print_me",
        action="store_true",
        default=False,
        help="print raw search results",
    )
    parser.add_argument(
        "-n",
        "--no-logo",
        dest="logo_off",
        action="store_true",
        default=False,
        help="disable the AppIntel logo",
    )
    parser.add_argument(
        "-t",
        "--table",
        dest="output_table",
        action="store_true",
        default=False,
        help="print a compact table instead of JSON",
    )
    parser.add_argument(
        "--country",
        dest="store_country",
        default="us",
        help="store country to search",
    )
    parser.add_argument(
        "--version",
        "-v",
        dest="app_version",
        action="store_true",
        default=False,
        help="print the AppIntel version",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.logo_off:
        print(logo)
    if args.app_version:
        print(f"Current version: {__version__}")
        return 0

    response = get_content(args.search_term, args.store_country, args.category_location)
    jsondata = response.json()

    if args.print_me:
        pprint(jsondata)
        for key in jsondata.get("results", [{}])[0]:
            print(f"{key}:")
        return 0

    average_price = get_mean(jsondata)
    max_price = get_max(jsondata)
    min_price = get_min(jsondata)
    median_price = get_median(jsondata)

    print("Results of the query")
    print("*****" * 5)
    print(
        f"The average price of the \033[94m{jsondata.get('resultCount', 0)}\033[0m items matching search term "
        f"\033[92m{args.search_term}\033[0m: ${average_price:.2f}, the median is \033[94m{median_price:.2f}\033[0m, "
        f"the min is \033[94m{min_price:.2f}\033[0m, and the max is \033[94m{max_price:.2f}\033[0m"
    )
    print("")

    if args.output_table:
        print(format_table(jsondata.get("results", [])))
    else:
        filename = f"{args.search_term}.json"
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(response.json(), file, indent=2)
        print(f"file saved as {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
