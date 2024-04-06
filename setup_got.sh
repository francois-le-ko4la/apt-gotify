#!/bin/sh
#
# DESCRIPTION:
# This script sets up gotify notification
#
# REQUIREMENTS:
# - Linux platform: Ubuntu 20/04+
# - python 3.6+
#

SCRIPT_PATH="/opt/scripts"
URL="https://raw.githubusercontent.com/francois-le-ko4la/rasp-gotify/main"
PKG="python3-full"
LIB="requests python-dotenv"

# Logging function
log() {
    echo "$(date --iso-8601=seconds) - GOT - $1"
}

# Check if the platform is Linux
if [ "$(uname)" != "Linux" ]; then
    echo "This script only works on Linux systems."
    exit 1
fi

# Check if the platform is Ubuntu 20.04 or newer
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "$ID" = "ubuntu" ] && [ "${VERSION_ID%.*}" -ge 20 ]; then
        log "Ubuntu 20.04 or newer detected."
    else
        echo "Unsupported Ubuntu version. Exiting..."
        exit 1
    fi
else
    echo "Unable to detect the operating system."
    exit 1
fi

log "Install python3-full..."
apt-get -yq install $PKG > /dev/null 2>&1

log "Create scripts repository..."
mkdir -p $SCRIPT_PATH
log "Create python venv..."
python3 -m venv $SCRIPT_PATH/venv > /dev/null 2>&1
log "Install lib..."
$SCRIPT_PATH/venv/bin/python -m pip install --upgrade pip > /dev/null 2>&1
$SCRIPT_PATH/venv/bin/python -m pip install $LIB > /dev/null 2>&1
log "Download GOT files..."
for file in apt_gotify.py notification.py ssh_gotify.py
do
        wget -q -O $SCRIPT_PATH/$file $URL/$file > /dev/null 2>&1
        chmod +x $SCRIPT_PATH/$file
        if [ -f "/etc/update-motd.d/$file" ]; then
                log "File $file exists. Delete $file."
                rm /etc/update-motd.d/$file
        fi
done

#.env file
if [ -f "$SCRIPT_PATH/.env" ]; then
	log "File $SCRIPT_PATH/.env exists. Edit your parameters!"
else
	log "File $SCRIPT_PATH/.env does not exist. Create a file. Edit your parameters!"
	wget -q -O $SCRIPT_PATH/.env $URL/env_example > /dev/null 2>&1
fi

#setup apt notification
log "Add apt notification..."
wget -q -O /etc/apt/apt.conf.d/99update-notifier-gotify $URL/99update-notifier-gotify > /dev/null 2>&1

#set up SSH notification
if grep -q "/opt/scripts/ssh_gotify.py" /etc/pam.d/sshd; then
    log "SSH Notification already set up in /etc/pam.d/sshd."
else
    echo "# Notify SSH" | sudo tee -a /etc/pam.d/sshd > /dev/null
    echo "session optional pam_exec.so /opt/scripts/ssh_gotify.py" | sudo tee -a /etc/pam.d/sshd > /dev/null 2>&1
    log "SSH notification has been added to /etc/pam.d/sshd."
fi

#reboot_gotify.service
log "Add reboot notification..."
wget -q -O /etc/systemd/system/reboot_gotify.service $URL/reboot_gotify.service> /dev/null 2>&1
sudo systemctl enable reboot_gotify.service
sudo systemctl start reboot_gotify.service

log "Operation completed successfully."
