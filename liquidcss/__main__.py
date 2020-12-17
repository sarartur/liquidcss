import sys
import os

import liquidcss.cli as cli


def main():
    cli.dispatch(sys.argv[1:])
    
main()