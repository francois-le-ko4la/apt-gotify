# apt-gotify
## Goal
Get apt notification after apt update/upgrade and get a notification when you need to reboot the server.

## Setup
- Copy files:
```
sudo pip3 install gotify
git clone https://github.com/francois-le-ko4la/rasp-gotify.git
cd rasp-gotify/
sudo mkdir -p /opt/scripts
sudo cp apt_gotify.py /opt/scripts
sudo cp 50gotify /etc/apt/apt.conf.d/
sudo chmod +x /opt/scripts/apt_gotify.py
```

- Edit and customize `/opt/scripts/apt_gotify.py`:
```
URL = "https://url:443"
TOKEN = "XXXXX"
```

# reboot-gotify
## Goal
Get a notification when you restart your ubuntu environment.

## Setup
- Copy files:
```
sudo pip3 install gotify
git clone https://github.com/francois-le-ko4la/rasp-gotify.git
cd rasp-gotify/
sudo cp reboot_gotify.service /etc/systemd/system
sudo mkdir -p /opt/scripts
cp notification.py /opt/scripts
sudo chmod +x /opt/scripts/notification.py
```

- Edit and customize `/opt/scripts/notification.py`
```
URL = "https://url:443"
TOKEN = "XXXXX"
```

- Start the service:
```
sudo systemctl enable reboot_gotify.service
sudo systemctl start reboot_gotify.service
```


# docker-gotify
## Goal
Get a notification when you restart your docker environment.

## Setup
- Copy files:
```
sudo pip3 install gotify
git clone https://github.com/francois-le-ko4la/rasp-gotify.git
cd rasp-gotify/
sudo cp docker_gotify.service /etc/systemd/system
sudo mkdir -p /opt/scripts
cp notification.py /opt/scripts
sudo chmod +x /opt/scripts/notification.py
```

- Edit and customize `/opt/scripts/notification.py`
```
URL = "https://url:443"
TOKEN = "XXXXX"
```

- Start the service:
```
sudo systemctl enable docker_gotify.service
sudo systemctl start docker_gotify.service
```

# Certbot
## Goal
Regular certificate generation with Cerbot/Docker.

## Setup
- Copy files:
```
git clone https://github.com/francois-le-ko4la/rasp-gotify.git
cd rasp-gotify/
sudo cp letsencrypt.* /etc/systemd/system
sudo mkdir -p /opt/scripts
cp certbot_renew.sh /opt/scripts
sudo chmod +x /opt/scripts/certbot_renew.sh
```

- Edit and customize `/opt/scripts/certbot_renew.sh`:
```
URL="https://url:443"
TOKEN="XXXXX"
CERT="/etc/letsencrypt/live/<domain>/fullchain.pem"
```

- Start the service:
```
sudo systemctl enable letsencrypt.timer
sudo systemctl start letsencrypt.timer
```

# ssh-gotify
## Goal

Track SSH Login

## Setup
- Copy files:
```
git clone https://github.com/francois-le-ko4la/rasp-gotify.git
cd rasp-gotify/
sudo mkdir -p /opt/scripts
cp ssh_gotify.py /opt/scripts
sudo chmod +x /opt/scripts/ssh_gotify.py
```

- Edit and customize `/opt/scripts/ssh_gotify.py`:
```
URL = "https://url:443"
TOKEN = "XXXXX"
```

- Edit `/etc/pam.d/sshd` and add:
```
session optional pam_exec.so /opt/scripts/ssh_gotify.py
```
