import sys
import argparse
import logging
from app.twitter_harvester import TwitterHarvester as Twitter
from app.db import DB, Keyword, TwitterToken

# Gather our code in a main() function


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    group_name = args.group

    database = DB('', '', 'amost_twitter')
    database.connect()

    keyword = Keyword(database.con, database.meta)
    token = TwitterToken(database.con, database.meta)

    keyword_list = keyword.find_by_group(group_name)
    twitter_token = token.find_by_group(group_name)

    crawler = Twitter(twitter_token, keyword_list)
    crawler.execute()

    logging.debug("Your Argument: %s" % args.group)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A CLI app to harvest twitter data and store it in CouchDB",
        fromfile_prefix_chars='@')

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
