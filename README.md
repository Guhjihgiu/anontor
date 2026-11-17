# 🕶️ Anontor Framework
> A 250+ tool Red Team multi-tool for Termux and Linux.

Anontor is a lightweight, interactive CLI framework that aggregates the most critical offensive security tools into a single, navigable interface. It is designed for rapid reconnaissance, exploitation, and post-exploitation workflows.

## 🚀 Features
- **250+ Curated Tools**: Organized into 15 categories including Recon, Deep Recon, Exploit, Post, C2, Web, Network, Forensics, OSINT, Dorks, SSH, Rooted, Unrooted, and Native modules.
- **Dynamic Target Injection**: Uses `{TARGET}` placeholders to construct real-time commands against your specific target IP or domain.
- **Paginated UI**: Automatically organizes hundreds of tools into a clean, 15-per-page menu.
- **C++ & Python Memory Binding**: Ultra-fast 60k port scanning via `ctypes` C++ integration.
- **Anonymity Mesh**: Built-in Tor and Proxy chaining to route your traffic.
- **Honeypot Listener**: Deploy a local trap on your device to catch incoming scanners.
- **Command History**: Tracks your last 5 executed commands.
- **Binary Detection**: Warns you if a required tool (e.g., `nmap`, `sqlmap`) is missing.

## Installation

### Termux (Android)
```bash
git clone https://github.com/0xGhost/anontor.git
cd anontor
bash install.sh
main.py
```

### Linux (Debian/Ubuntu)
```bash
git clone https://github.com/0xGhost/anontor.git
cd anontor
bash install.sh
main.py
```
