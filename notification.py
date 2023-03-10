#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allow apt notifications to a gotify server.
"""

import argparse
import platform

from gotify import Gotify


URL = "https://www.url.fr:443"
TOKEN = "XXX"
__VERSION__ = "0.1.0"


def get_argparser() -> argparse.ArgumentParser:
    """Define the argument parser and return it.

    Returns:
        ArgumentParser

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--title',
        help="title", required=True)
    parser.add_argument(
        '--message',
        help='message', required=True)
    parser.add_argument(
        '--prio',
        help='priority', type=int, required=True)
    return parser


if __name__ == "__main__":
    args = get_argparser().parse_args()
    notification = Gotify(base_url=URL, app_token=TOKEN)
    
    notification.create_message(args.message,
                                title=f"{platform.node()}: {args.title}",
                                priority=args.prio)
