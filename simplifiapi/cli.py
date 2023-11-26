import json
import logging
import sys

import configargparse

from simplifiapi.client import Client

logger = logging.getLogger("simplifiapi")


def parse_arguments(args):
    parser = configargparse.ArgumentParser()

    # Credential
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

    # Datasets
    parser.add_argument('--transactions',
                        action="store_true",
                        default=False,
                        help="Retrieve transactions")

    # Export
    parser.add_argument('--filename',
                        default="output",
                        help="Write results to file this prefix")

    return parser.parse_args(args)


def write_data(options, data, name):
    filename = "{}_{}.json".format(options.filename, name)
    with open(filename, "w+") as f:
        json.dump(data, f, indent=2)


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

    # Retrieve first dataset
    # TODO: Support multiple datasets
    datasets = client.get_datasets()
    datasetId = datasets[0]["id"]

    if (options.transactions):
        transactions = client.get_transactions(datasetId)
        write_data(options, transactions, "transactions")
