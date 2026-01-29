#!/bin/bash

# macOS TCP tuning for high-concurrency benchmarking
# Run with: sudo ./experiment/tune_macos.sh

echo "=== Current Settings ==="
sysctl kern.ipc.somaxconn
sysctl kern.maxfiles
sysctl kern.maxfilesperproc
sysctl net.inet.tcp.msl
sysctl net.inet.ip.portrange.first
sysctl net.inet.ip.portrange.last

echo ""
echo "=== Applying Tuning ==="

# Increase TCP connection backlog (default 2048)
sudo sysctl -w kern.ipc.somaxconn=8192

# Increase max files
sudo sysctl -w kern.maxfiles=524288
sudo sysctl -w kern.maxfilesperproc=262144

# Reduce TIME_WAIT timeout (default 15000ms = 15s)
sudo sysctl -w net.inet.tcp.msl=1000

# Increase ephemeral port range
sudo sysctl -w net.inet.ip.portrange.first=1024
sudo sysctl -w net.inet.ip.portrange.last=65535

echo ""
echo "=== New Settings ==="
sysctl kern.ipc.somaxconn
sysctl kern.maxfiles
sysctl kern.maxfilesperproc
sysctl net.inet.tcp.msl
sysctl net.inet.ip.portrange.first
sysctl net.inet.ip.portrange.last

echo ""
echo "=== File Descriptor Limit ==="
ulimit -n
echo "To increase: ulimit -n 65536"

echo ""
echo "Note: These settings reset on reboot."
echo "For permanent changes, add to /etc/sysctl.conf"
