"""A script to grab itunes items for sale for market research and data research purposes."""
# coding: utf-8
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt

# imports section

import requests
import argparse
from pprint import pprint
from statistics import mean
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# globals
__version__ = "0.5.4"
logo = """
┌────────────────────────┐
│                        │
│                        │
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
itunes_url_endpoint = 'https://itunes.apple.com/search?term={}&country=us&entity={}'

# arguments
parser = argparse.ArgumentParser(description='collects and processes itunes data including ibook, application, and other store items with metadata, run "python3 test_itunize.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--search', dest='search_term', help='search term to search itunes store for', default='nginx', required=False)
parser.add_argument('-c', '--category', dest='category_location', help='category in store to search for', default='software', required=False)
parser.add_argument('-p', '--print', dest='print_me', help='print to screen results, helpful for testing', action='store_true', default=False)
parser.add_argument('-n', '--no-logo', dest='logo_off', help='disables printing logo', action='store_true', default=False)
parser.add_argument('-t', '--table', dest='output_table', help='prints out table as format for data', action='store_true', default=False)
args = vars(parser.parse_args())


# functions section


def get_content():
    """Get data from requests object from itunes endpoint."""
    r = requests.get(itunes_url_endpoint.format(args['search_term'], args['category_location']))
    return r


def get_mean(jsondata):
    """Get average of list of items using numpy."""
    return mean([float(price['formattedPrice'][1:]) for price in jsondata['results']])  # key name from itunes


# main section


def main():
    """Main function that runs everything."""
    if not args['logo_off']:  # print or not print logo
        print(logo)
    request_response = get_content()
    jsondata = request_response.json()
    # [trend['name'] for trend in the_data[0]['trends']]
    average_price = get_mean(jsondata)
    print("The average price of the \033[94m{0}\033[0m items matching search term\033[92m {1}\033[0m: ${2:.2f}".format(jsondata['resultCount'], args['search_term'], average_price))
    print()
    if args['print_me']:  # if we are running a test or not
        print('json data:')
        pprint(jsondata)
        print('fields available:')
        for key in jsondata['results'].keys():
            print(key)
        exit('thanks for trying')
    if args['output_table']:  # if we want to output a table instead of json
        val2 = request_response.json()
        # print(val2['results'][0])
        print(pd.DataFrame(val2['results'], columns=["formattedPrice", "artistName", "trackName"]))
    else:
        with open('{}.json'.format(args['search_term']), 'w') as f:
            f.write(''.join(str(x) for x in [request_response.json()]))
        exit('file saved as {}.json'.format(args['search_term']))

if __name__ == "__main__":
    main()