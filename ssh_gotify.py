#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allow ssh login notifications to a gotify server.
Add this line at the end of /etc/pam.d/sshd:
    session optional pam_exec.so /opt/scripts/ssh_gotify.py
"""

import os
import platform
import requests


URL = "https://url:8143"
TOKEN = "XXXX"
APP = URL + '/message?token=' + TOKEN
__VERSION__ = "0.1.0"


if __name__ == "__main__":
    if os.environ.get('PAM_TYPE') == "open_session":
        user = os.environ.get('PAM_USER')
        rhost = os.environ.get('PAM_RHOST')
        message = f"SSH login: {user} from {rhost}"
        try:
            resp = requests.post(APP, json={
                "message": message,
                "priority": 5,
                "title": f"{platform.node()}: SSH login"
            }, timeout=1)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
