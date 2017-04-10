from __future__ import print_function
import sys
import argparse
import logging
from app.search import TwitterSearch

# Gather our code in a main() function


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    group_name = args.group
    app_type = args.type

    if app_type == 'search':
        crawler = TwitterSearch(group_name)
        crawler.execute()
    else:
        # Run streaming api script here
        print('Streaming API')

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A CLI app to harvest twitter data and store it in CouchDB",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "type",
        help="Type of script Search API/Streaming API",
        metavar="TYPE"
    )

    parser.add_argument(
        "group",
        help="The group of keywords",
        metavar="GROUP")

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
