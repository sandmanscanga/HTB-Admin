
# HTB-Admin

A tool used for manipulating HackTheBox machine instances from the command line.

---

## OS & Python Version Info

```bash
lsb_release -a
# Distributor ID: Kali
# Description:    Kali GNU/Linux Rolling
# Release:        2022.2
# Codename:       kali-rolling
```

*Tested using Python 3.10.4*

---

**Installation**

```bash

git clone https://github.com/sandmanscanga/HTB-Admin.git
cd HTB-Admin

# To run on a portable basis
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

####  OR  ####

# To run installed on the system
sudo bash install.sh

```

---

## Example Usage

```bash

# Portable Install
python htb-admin.py -q backdoor         # search for a machine called 'backdoor'
python htb-admin.py -s backdoor         # start a machine called 'backdoor'
python htb-admin.py -r                  # reset the current active machine
python htb-admin.py -k                  # kill the current active machine
python htb-admin.py -f flag:difficulty  # submit a flag to current active machine
python htb-admin.py -t                  # return just the IP of the current active machine
python htb-admin.py -l                  # return the local tun0 ip address for HTB VPN

#### OR ####

# Full Install
htb-admin -q backdoor         # search for a machine called 'backdoor'
htb-admin -s backdoor         # start a machine called 'backdoor'
htb-admin -r                  # reset the current active machine
htb-admin -k                  # kill the current active machine
htb-admin -f flag:difficulty  # submit a flag to current active machine
htb-admin -t                  # return just the IP of the current active machine
htb-admin -l                  # return the local tun0 ip address for HTB VPN

```

**This application was designed for educational purposes ONLY. I am not responsible for any misuse of the application or legal issues that arise due to you're own decisions.**
