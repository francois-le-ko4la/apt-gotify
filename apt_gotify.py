#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allow apt notifications to a gotify server.
"""
from __future__ import annotations

import argparse
import os
import platform
from pathlib import Path
import re
from enum import Enum, unique

from gotify import Gotify


URL = "https://xxxxxx:443"
TOKEN = "XXXX"
__VERSION__ = "0.1.0"


@unique
class Const(Enum):
    """Define constants."""

    APT_UPDT_AVAIL: str = "/var/lib/update-notifier/updates-available"
    APT_HISTORY: str = "/var/log/apt/history.log"
    APT_REBOOT: str = "/var/run/reboot-required"
    STAMP: str = "/tmp/apt_gotify.stamp"
    STAMP_UPDT: str = "/tmp/apt_gotify_update.stamp"
    STAMP_REBOOT: str = "/tmp/apt_gotify_reboot.stamp"
    SRCH_NO_UPDATE: str = "^0 updates can be applied immediately.$"
    MSG_CHK_UPD: str = "Check update done"
    MSG_UPDT_AVAIL: str = "update available"
    MSG_NO_UPDT_AVAIL: str = "up to date"
    MSG_UPDT_DONE: str = "Update done!"
    MSG_REBOOT_TITLE: str = "reboot required"
    MSG_REBOOT: str = "*** System reboot required ***\n\n"


def get_argparser() -> argparse.ArgumentParser:
    """Define the argument parser and return it.

    Returns:
        ArgumentParser

    """
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        '--notify-check-update-done',
        help="Notify check update",
        action = 'store_const', dest = 'cmd', const = 'notify_check_update_done')
    action.add_argument(
        '--notify-update',
        help='Notify update in progress',
        action = 'store_const', dest = 'cmd', const = 'notify_update')
    action.add_argument(
        "--notify-update-done",
        help='Notify update is done',
        action = 'store_const', dest = 'cmd', const = 'notify_update_done')
    action.add_argument(
        '--notify-reboot',
        help='Notify reboot is necessary',
        action = 'store_const', dest = 'cmd', const = 'notify_reboot')
    return parser


class MyNotification:
    """Prepare and send notification to Gotify."""

    def __init__(self, cmd: str) -> None:
        """Initialize and setup values."""
        self.__message = ""
        self.__title = ""
        self.__gotify = Gotify(base_url=URL, app_token=TOKEN)
        self.__valid = False
        func = getattr(self, f"_MyNotification__{cmd}", None)
        if func:
            func()
        else:
            print("yop")

    def send(self) -> None:
        """Send notification."""
        if self.__valid:
            self.__gotify.create_message(self.__message,
                                         title=self.__title,
                                         priority=0)

    @staticmethod
    def __build_title(title: str) -> str:
        return f"{platform.node()}: {title} " \
               f"({os.getenv('SUDO_USER', default='AUTO')})"

    def __notify_check_update_done(self) -> None:
        self.__valid = True
        self.__message = Const.MSG_CHK_UPD.value
        self.__title = self.__build_title(self.__message)

    def __notify_update(self) -> None:
        updates_available = Path(Const.APT_UPDT_AVAIL.value)
        stamp = Path(Const.STAMP.value)

        # no file no update
        if not updates_available.exists():
            return

        # stamp exists and created after the last update available
        if (stamp.exists()
            and updates_available.stat().st_mtime < stamp.stat().st_mtime):
            return

        # update the stamp file
        stamp.write_text("")

        self.__message = updates_available.read_text()
        update = not re.search(
                Const.SRCH_NO_UPDATE.value, self.__message, re.MULTILINE)
        msg = Const.MSG_UPDT_AVAIL.value \
                if update else Const.MSG_NO_UPDT_AVAIL.value
        self.__title = self.__build_title(msg)
        self.__valid = True

    def __notify_update_done(self) -> None:
        stamp = Path(Const.STAMP.value)
        stamp_update_done = Path(Const.STAMP_UPDT.value)

        if (stamp_update_done.exists()
            and stamp.stat().st_mtime < stamp_update_done.stat().st_mtime):
            return

        stamp_update_done.write_text("")
        self.__message = Const.MSG_UPDT_DONE.value
        self.__title = self.__build_title(self.__message)
        self.__valid = True

    def __notify_reboot(self) -> None:
        history = Path(Const.APT_HISTORY.value)
        stamp = Path(Const.STAMP_REBOOT.value)

        # Multiple apt tasks
        if stamp.exists() or not os.path.exists(Const.APT_REBOOT.value):
            return

        stamp.write_text("")
        self.__title = self.__build_title(Const.MSG_REBOOT_TITLE.value)
        self.__message = Const.MSG_REBOOT.value
        self.__valid = os.path.exists(Const.APT_REBOOT.value)


if __name__ == "__main__":
    args = get_argparser().parse_args()
    notif = MyNotification(args.cmd)
    notif.send()
