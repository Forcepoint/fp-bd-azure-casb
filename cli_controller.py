#
# Author:  Dlo Bagari
# created Date: 03-12-2019

from src.cli.cli_args import CliArgs
from sys import exit

if __name__ == "__main__":
    cli_args = CliArgs("azure_casb.sh")
    try:
        parser = cli_args.get_parser()
        args = parser.parse_args()
        args.function(args)
    except KeyboardInterrupt:
        print()
        exit()
