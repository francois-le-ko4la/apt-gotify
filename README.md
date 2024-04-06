# rasp-gotify

## Why ?

Are you looking to streamline your Raspberry Pi projects with efficient and customizable notification capabilities? Look no further! Our collection of notification scripts, seamlessly integrated with the Gotify platform, offers a robust solution for all your notification needs.

**What is Gotify?**

Gotify is a self-hosted notification server that allows you to send and receive messages in real-time through a simple REST API. With Gotify, you have full control over your notifications, ensuring privacy and security in your projects.

**Why Choose Gotify for Raspberry Pi?**
- Ease of Use: Our scripts are designed to be user-friendly, allowing even beginners to set up notifications on their Raspberry Pi quickly.
- Customizability: Tailor notifications to your specific requirements with customizable parameters such as message content, priority levels, and recipients.
- Flexibility: Whether you're monitoring system metrics, receiving alerts from sensors, or tracking events in your projects, our Gotify-enabled scripts offer versatile notification solutions.

**Features of Our Notification Scripts:**
- SSH notification
- APT notification
- reboot notification
- certbot notificaiotn
  
**How to Get Started:**

- Installation: Simply download and configure our notification scripts on your Raspberry Pi. Detailed installation instructions are provided below.
- Configuration: Customize the scripts to suit your needs by configuring parameters such as Gotify server URL, API token, and notification settings.
- Integration: Seamlessly integrate the scripts into your projects to start receiving notifications instantly.

**Empower Your Raspberry Pi Projects with Gotify-Enabled Notifications!**

With our notification scripts, harness the power of Gotify to enhance the functionality and efficiency of your Raspberry Pi projects. Whether you're a hobbyist, maker, or professional developer, our solution provides a reliable and scalable notification infrastructure tailored to your requirements.

## Global pre requisite (VENV)

To be able to launch our scripts we need a python venv:

```
python3 -m venv /opt/scripts/venv
source /opt/scripts/venv/bin/activate
pip install requests
deactivate
```

# apt-gotify
## Goal
Get apt notification after apt update/upgrade and get a notification when you need to reboot the server.

## Setup
- Copy files:
```
git clone https://github.com/francois-le-ko4la/rasp-gotify.git
cd rasp-gotify/
sudo mkdir -p /opt/scripts
sudo cp apt_gotify.py /opt/scripts
sudo cp 99update-notifier-gotify /etc/apt/apt.conf.d/
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
