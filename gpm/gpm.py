#!/usr/bin/env python
import sys
from gpm.cli import CLI

def main():
    args = sys.argv[1:]
    cli = CLI(args)
    cli.run()

if __name__ == "__main__":
    main()