
# SSRF lab from scratch

### **DISCLAIMER**
<img src="screenshots/DISCLAIMER.png" width="200">

---

### **INTRO**
This lab will help to understand how everything works under the hood when it comes to SSRF vulnerabilities.  
It is important to build hands-on lab from scratch.  
**❗️I will periodically update this repository to add new levels.**

---
### **TOOLS**

![Kali Linux](https://img.shields.io/badge/Kali_Linux-black?style=for-the-badge&logo=kalilinux&logoColor=white)
![Firefox](https://img.shields.io/badge/Firefox-2B1B3D?style=for-the-badge&logo=firefox&logoColor=FF7139)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)

---
### **STRUCTURE (Spoilers)**
<img src="screenshots/STRUCTURE.png" width="200">

Backend at `http://127.0.0.1:5050`  
Internal server at `http://127.0.0.1:5051`

---

### **HOW TO USE**

1. In Firefox `about:config` change `network.proxy.allow_hijacking_localhost` from **false** to **true** so that Burp can intercept localhost requests.  
2. Download the lab.  

3. Navigate to the `SSRF-homie-lab/` directory.
4. To start a level, replace `N` with the level number in the command below:
```
bash start_level.sh -N
```

5. Open `http://127.0.0.1:5050/levelN` and try to find SSRF. 

*The levels are not arranged by difficulty. I don't follow a specific progression when creating them; the numbers are only used for ordering.

---

### **CONTACTS**
If you have any suggestions or would like to discuss something, feel free to reach out to me through the contacts in my profile.
