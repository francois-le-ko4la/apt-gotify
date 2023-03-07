#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allow apt notifications to a gotify server.
"""

import argparse
import os
import platform
from pathlib import Path

from gotify import Gotify


URL = "https://xxxxxx:443"
TOKEN = "XXXX"
__VERSION__ = "0.1.0"


def get_argparser() -> argparse.ArgumentParser:
    """Define the argument parser and return it.

    Returns:
        ArgumentParser

    """
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        '--message',
        dest='message', help="JSON Keyfile", default=None)
    action.add_argument(
        '--notify-update',
        help='Deactivate SSL Verification', default=False, action="store_true")
    action.add_argument(
        '--notify-reboot',
        help='Logging on', default=False, action="store_true")
    return parser


class MyNotification:
    """Prepare and send notification to Gotify."""

    def __init__(self, message, notify_update, notify_reboot):
        """Initialize and setup values."""
        self.__message = message
        self.__title = ""
        self.__gotify = Gotify(base_url=URL, app_token=TOKEN)
        self.__valid = False
        if message:
            self.__notify_message()
        if notify_update:
            self.__notify_updates()
        if notify_reboot:
            self.__notify_reboot()

    def send(self) -> None:
        """Send notification."""
        if self.__valid:
            self.__gotify.create_message(self.__message,
                                         title=self.__title,
                                         priority=0)

    def __notify_message(self) -> None:
        self.__valid = True
        self.__title = f"{platform.node()}: {self.__message}"

    def __notify_updates(self) -> None:
        update_file = Path("/var/lib/update-notifier/updates-available")
        if update_file.exists():
            srch = "0 updates can be applied immediately."
            self.__message = update_file.read_text()
            update = (self.__message.find(srch) == -1)
            msg = "up to date"
            if update:
                msg = "update available"
                stream = os.popen('apt list --upgradable 2>/dev/null')
                pkg = stream.read()
                self.__message = f"{msg}\n\n{pkg}"
            self.__title = f"{platform.node()}: {msg}"
            self.__valid = True

    def __notify_reboot(self) -> None:
        history = Path("/var/log/apt/history.log")
        self.__title = f"{platform.node()}: reboot required"
        pkg = history.read_text().split('\n\n')[-1]
        self.__message = f"*** System reboot required ***\n\n{pkg}"
        self.__valid = os.path.exists("/var/run/reboot-required")


if __name__ == "__main__":
    args = get_argparser().parse_args()
    notif = MyNotification(args.message,
                           args.notify_update,
                           args.notify_reboot)
    notif.send()
