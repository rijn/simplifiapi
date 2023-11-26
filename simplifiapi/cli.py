import sys
import logging

import configargparse

from simplifiapi.client import Client

logger = logging.getLogger("simplifiapi")


def parse_arguments(args):
    parser = configargparse.ArgumentParser()
    parser.add_argument('--email',
                        nargs="?",
                        default=None,
                        help="The e-mail address for your Quicken Simplifi account")
    parser.add_argument('--password',
                        nargs="?",
                        default=None,
                        help="The password for your Quicken Simplifi account")
    parser.add_argument('--token',
                        nargs="?",
                        default=None,
                        help="Use existing token to bypass MFA check")
    return parser.parse_args(args)


def main():
    options = parse_arguments(sys.argv[1:])

    client = Client()

    token = options.token
    if (not token):
        token = client.get_token(
            email=options.email, password=options.password)

    if (client.verify_token(token) == False):
        logger.error("Unable to log in simplifi.")
        return
