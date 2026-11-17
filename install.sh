#!/bin/bash
echo "=========================================="
echo "    ANONTOR FRAMEWORK INSTALLER"
echo "=========================================="

echo "[*] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing core dependencies (Nmap, SQLMap, Hydra, Clang, Tor, etc)..."
pkg install -y python git curl wget clang make nmap whois dnsutils tor proxychains-ng tcpdump openssh hydra sqlmap aircrack-ng

echo "[*] Installing Python dependencies..."
pip install requests

echo "[*] Setting up 'main.py' command..."
INSTALL_DIR="$PREFIX/share/anontor"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$INSTALL_DIR"
cp -r "$SRC_DIR"/* "$INSTALL_DIR/"
chmod 755 "$INSTALL_DIR/main.py"

cat > "$PREFIX/bin/main.py" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd "$PREFIX/share/anontor" || exit 1
exec ./main.py "$@"
EOF
chmod 755 "$PREFIX/bin/main.py"

echo "=========================================="
echo " INSTALLATION COMPLETE!"
echo " Run the framework with: main.py"
echo "=========================================="
