"""A script to grab itunes items for sale for market and data research."""
# coding: utf-8
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Last Update: 05-May-2024
# Requirements: minimal. check requirements.txt

# imports section

import json
import argparse
from pprint import pprint
from statistics import mean, median

import pandas as pd
import requests

# globals
__version__ = "1.0.6"
logo = """
┌────────────────────────┐
│            ┌───▶       │
│        ┌───┘   │       │
│        │   ┌───▶       │
│        │───┘   │       │
│        │       │       │
│        │      .▼       │
│       .│     (█)       │
│      (█)      '        │
│       '                │
│      ┌───────────┐     │
│      │ itunizer  │     │
└──────┴───────────┴─────┘
"""
ITUNES_URL_ENDPOINT = "https://itunes.apple.com/search?term={}&country={}&entity={}"

# arguments
parser = argparse.ArgumentParser(
    description='collects and processes itunes data including ibook, application, '
                'and other store items with metadata, example: itunizer -c ibook -s "corn" -t',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-s",
    "--search",
    dest="search_term",
    help="search term to search itunes store for",
    default="nginx",
    required=False,
)
parser.add_argument(
    "-c",
    "--category",
    dest="category_location",
    help="category in store to search for; what is available is movie, podcast, music, musicVideo, audiobook, shortFilm, tvShow, software, ebook, all",
    default="software",
    required=False,
)
parser.add_argument(
    "-p",
    "--print",
    dest="print_me",
    help="print to screen results, helpful for testing",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-n",
    "--no-logo",
    dest="logo_off",
    help="disables printing logo",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-t",
    "--table",
    dest="output_table",
    help="prints out table as format for data",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--country",
    dest="store_country",
    default="us",
    help="the store country you want to use for search results",
)
parser.add_argument(
    "--version",
    "-v",
    dest="app_version",
    help="prints the version",
    action="store_true",
    default=False,
)
args = vars(parser.parse_args())


# functions section


def get_content():
    """Get data from requests object from itunes endpoint."""
    r = requests.get(
        ITUNES_URL_ENDPOINT.format(
            args["search_term"], args["store_country"],
            args["category_location"]
        ),
        timeout=10  # Timeout after 10 seconds
    )
    return r


def get_mean(jsondata):
    """Get average of list of items using numpy."""
    if len(jsondata["results"]) > 1:
        # key name from itunes
        return mean(
            [
                float(price.get("price"))
                for price in jsondata["results"]
                if "price" in price
            ]
        )
    return float(jsondata["results"][0]["price"])


def get_max(jsondata):
    """Get max of list of items using max built in."""
    if len(jsondata["results"]) > 1:
        # key name from itunes
        return max(
            [
                float(price.get("price"))
                for price in jsondata["results"]
                if "price" in price
            ]
        )
    return float(jsondata["results"][0]["price"])


def get_min(jsondata):
    """Get max of list of items using max built in."""
    if len(jsondata["results"]) > 1:
        # key name from itunes
        return min(
            [
                float(price.get("price"))
                for price in jsondata["results"]
                if "price" in price
            ]
        )
    return float(jsondata["results"][0]["price"])


def get_median(jsondata):
    """Get median of list of items using statistics.median built in."""
    if len(jsondata["results"]) > 1:
        # key name from itunes
        return median(
            [
                float(price.get("price"))
                for price in jsondata["results"]
                if "price" in price
            ]
        )
    return float(jsondata["results"][0]["price"])


# main section


def main():
    """Main function that runs everything."""
    if not args["logo_off"]:  # print or not print logo
        print(logo)
    if args["app_version"]:
        print(f"Current version: {__version__}")
        exit(0)
    request_response = get_content()
    jsondata = request_response.json()
    # [trend['name'] for trend in the_data[0]['trends']]
    print()
    if args["print_me"]:  # if we are running a test or not
        print("json data:")
        pprint(jsondata)
        print("fields available:")
        for k, _ in jsondata["results"][0].items():
            print(k)
        exit("thanks for trying")
    average_price = get_mean(jsondata)
    max_price = get_max(jsondata)
    min_price = get_min(jsondata)
    median_price = get_median(jsondata)
    print("Results of the query")
    print("*****" * 5)
    print(
        f"The average price of the \033[94m{jsondata['resultCount']}\033[0m items matching search term\033[92m {args['search_term']}\033[0m: ${average_price:.2f}, the median is \033[94m{median_price:.2f}\033[0m, the min is \033[94m{min_price:.2f}\033[0m, and the max is \033[94m{max_price:.2f}\033[0m"
    )
    print("")
    if args["output_table"]:  # if we want to output a table instead of json
        print(
            pd.DataFrame(
                jsondata["results"], columns=["price", "artistName", "trackName"]
            )
        )
    else:
        with open(f"{args['search_term']}.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(request_response.json()))
        exit(f"file saved as {args['search_term']}.json")


if __name__ == "__main__":
    main()
