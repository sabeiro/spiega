#!/usr/bin/env bash
# Set total swap to a fixed size (one swap file). Run on the Jetson with sudo.
# Usage: sudo ./configure_jetson.sh 4G   # 4 GiB total swap
# Usage: sudo ./configure_jetson.sh 6G   # 6 GiB total swap
set -e

TOTAL_SWAP="${1:?Usage: $0 <size>   e.g. $0 4G}"
SWAPFILE="/swapfile"

# Turn off all swap so we control the total
swapoff -a 2>/dev/null || true

# Remove old swap file if it exists so we can recreate with new size
rm -f "$SWAPFILE"

# Create one swap file with the desired total size
fallocate -l "$TOTAL_SWAP" "$SWAPFILE"
chmod 600 "$SWAPFILE"
mkswap "$SWAPFILE"
swapon "$SWAPFILE"

# Make it permanent. For exactly this total on reboot, remove or comment other swap lines in /etc/fstab (e.g. UUID=... swap).
if ! grep -q "^${SWAPFILE} " /etc/fstab; then
    echo "${SWAPFILE} none swap sw 0 0" >> /etc/fstab
fi

# Prefer swapping other processes so more physical RAM is free for Ollama (cudaMalloc uses RAM, not swap).
# 80 = swap out more aggressively; leaves more free RAM for the GPU model.
if [ -w /proc/sys/vm/swappiness ]; then
    echo 80 > /proc/sys/vm/swappiness
    echo "vm.swappiness set to 80 (persist in /etc/sysctl.conf if you want: vm.swappiness=80)"
fi

echo "Swap set to $TOTAL_SWAP total. Current:"
free -h

# Disable system nginx at startup (we use nginx in Docker)
if command -v systemctl >/dev/null 2>&1; then
    if systemctl is-enabled nginx 2>/dev/null | grep -q enabled; then
        systemctl stop nginx 2>/dev/null || true
        systemctl disable nginx
        echo "System nginx disabled and stopped (Docker nginx is used)."
    else
        echo "System nginx already disabled or not present."
    fi
else
    echo "systemctl not found; skip disabling system nginx."
fi
