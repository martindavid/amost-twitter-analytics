#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import logging
from app.search import TwitterSearch
from app.streaming import TwitterStreamRunner


def main(args, loglevel):
    """ Main method"""
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    group_name = args.group
    app_type = args.type

    if app_type == 'search':
        crawler = TwitterSearch(group_name)
        crawler.execute()
    elif app_type == 'stream':
        crawler = TwitterStreamRunner(group_name)
        crawler.execute()

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="A CLI app to harvest twitter data and store it in CouchDB",
        fromfile_prefix_chars='@')

    PARSER.add_argument(
        "type",
        help="Type of script Search API/Streaming API",
        metavar="TYPE"
    )

    PARSER.add_argument(
        "group",
        help="The group of keywords",
        metavar="GROUP")

    PARSER.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")

    ARGS = PARSER.parse_args()

    # Setup logging
    if ARGS.verbose:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

    main(ARGS, LOG_LEVEL)
