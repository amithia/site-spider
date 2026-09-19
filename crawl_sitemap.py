#!/usr/bin/env python3
"""Backward-compatible entry point for running from a repo checkout.

The actual implementation now lives in the `sitespider` package
(see sitespider/cli.py) so it can be installed via pip/pipx. This
shim keeps `python3 crawl_sitemap.py <url>` working for anyone running
straight from a git clone.
"""

import sys

from sitespider.cli import main

if __name__ == "__main__":
    sys.exit(main())
