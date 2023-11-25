import sys

import configargparse


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
    return parser.parse_args(args)


def main():
    options = parse_arguments(sys.argv[1:])
