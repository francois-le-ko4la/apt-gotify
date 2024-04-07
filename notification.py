#!/opt/scripts/venv/bin/python3
# -*- coding: utf-8 -*-
"""
This script allow apt notifications to a gotify server.
"""

import os
import argparse
import platform
import requests
from dotenv import load_dotenv


load_dotenv()
URL = os.getenv('GOTIFY_URL')
TOKEN = os.getenv('GOTIFY_TOKEN')
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
            "message": args.message,
            "priority": args.prio,
            "title": f"{platform.node()}: {args.title}"
        }, timeout=1)
        resp.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException, Exception) as err:
        print ("Error:", err)
