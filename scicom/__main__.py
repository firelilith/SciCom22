import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("--help", help="show this text and exit. for help on subcommands run scicom.py subcommand --help.",
                    action="store_true")
parser.add_subparsers(title="newton")

