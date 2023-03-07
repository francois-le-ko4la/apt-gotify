# apt-gotify


## Setup
```
git clone https://github.com/francois-le-ko4la/apt-gotify.git
cd apt-gotify/
sudo pip3 install gotify
sudo mkdir -p /opt/scripts
sudo cp apt_gotify.py /opt/scripts
sudo chmod +x /opt/scripts/apt_gotify.py
```

`/etc/apt/apt.conf.d/50gotify`
```
APT::Update::Pre-Invoke {"/opt/scripts/apt_gotify.py --message 'Check update'"};
APT::Update::Post-Invoke {"/opt/scripts/apt_gotify.py --notify-update"};
DPkg::Post-Invoke {"/opt/scripts/apt_gotify.py --message 'Update done!'"};
DPkg::Post-Invoke {"/opt/scripts/apt_gotify.py --notify-reboot"};
```
