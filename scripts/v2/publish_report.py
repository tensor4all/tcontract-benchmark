#!/usr/bin/env python3
"""Timing-v2 shim over `campaign_toolkit.publish_report`. See `scripts/v2/_shim.py`."""
import sys

from _shim import run

if __name__ == "__main__":
    sys.exit(run("publish_report"))
