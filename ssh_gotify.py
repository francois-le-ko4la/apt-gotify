#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allow ssh login notifications to a gotify server.
Add this line at the end of /etc/pam.d/sshd:
    session optional pam_exec.so /opt/scripts/ssh_gotify.py
"""

import os
import platform

from gotify import Gotify


URL = "https://url:8143"
TOKEN = "XXXX"
__VERSION__ = "0.1.0"


if __name__ == "__main__":
    if os.environ.get('PAM_TYPE') == "open_session":
        notification = Gotify(base_url=URL, app_token=TOKEN)
        user = os.environ.get('PAM_USER')
        rhost = os.environ.get('PAM_RHOST')
        message = f"SSH login: {user} from {rhost}"
        notification.create_message(message,
                                    title=f"{platform.node()}: SSH login",
                                    priority=5)
