# appintel

## What

Gather market data into a machine readable form from iTunes store data.

## Install

The easiest way is pip: `pip3 install appintel`.

## Usage

Use the `-h` for options:

```bash
$ itunizer -h
usage: appintel [-h] [-s SEARCH_TERM] [-c CATEGORY_LOCATION] [-p] [-n] [-t]
                [--country STORE_COUNTRY] [--version]

collects and processes app store data including ibook, application, and other
store items with metadata, example: itunizer -c ibook -s "corn" -t

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH_TERM, --search SEARCH_TERM
                        search term to search itunes store for (default:
                        nginx)
  -c CATEGORY_LOCATION, --category CATEGORY_LOCATION
                        category in store to search for (default: software)
  -p, --print           print to screen results, helpful for testing (default:
                        False)
  -n, --no-logo         disables printing logo (default: False)
  -t, --table           prints out table as format for data (default: False)
  --country STORE_COUNTRY
                        the store country you want to use for search results
                        (default: us)
  --version, -v         prints the version (default: False)
  ```

## Why?

It is difficult to get nice structured data from Apple. This helps with that.

## Example search

!['example'](https://user-images.githubusercontent.com/616585/35492868-5dcf0e90-047d-11e8-974f-0dd7a0f33311.png)
