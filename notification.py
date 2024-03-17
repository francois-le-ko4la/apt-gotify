#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allow apt notifications to a gotify server.
"""

import argparse
import platform
import requests


URL = "https://www.url.fr:443"
TOKEN = "XXX"
APP = URL + '/message?token=' + TOKEN
__VERSION__ = "0.1.1"


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
    
    try:
        resp = requests.post(APP, json={
            "message": "Well hello there.",
            "priority": 2,
            "title": f"{platform.node()}: {args.title}"
        }, timeout=1)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
