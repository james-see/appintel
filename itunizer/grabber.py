# What: A script to grab itunes items for sale for market research and data research purposes
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-Jan-2018
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt

import requests
import argparse
from pprint import pprint

# globals
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
args = vars(parser.parse_args())
# functions

def getContent():
    # global search_term, category_location
    r = requests.get(itunes_url_endpoint.format(args['search_term'], args['category_location']))
    return r



def main():
    if args['logo_off'] == False:
        print(logo)
    request_response = getContent()
    if args['print_me']:
        pprint(request_response.json())
        exit('thanks for trying')
    else:
        with open('{}.json'.format(args['search_term']), 'w') as f:
            f.write(''.join(str(x) for x in [request_response.json()]))
        exit('file saved as {}.json'.format(args['search_term']))

if __name__ == "__main__":
    main()