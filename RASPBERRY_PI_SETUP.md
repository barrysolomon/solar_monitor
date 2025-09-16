# Solar Monitor Setup Guide - Step by Step

## Phase 1: Hardware Setup

### Step 1: Prepare Raspberry Pi
1. Download **Raspberry Pi Imager** from [rpi.org](https://www.raspberrypi.org/downloads/)
2. Insert microSD card into your computer
3. Open Raspberry Pi Imager
4. Select **Raspberry Pi OS Lite (64-bit)** (no desktop needed)
5. Click gear icon → Enable SSH → Set username/password
6. Write image to SD card

### Step 2: Initial Boot
1. Insert SD card into Raspberry Pi
2. Connect Ethernet cable to Pi
3. Connect power supply
4. Wait 2-3 minutes for first boot

### Step 3: Find Pi on Network
```bash
# On your computer, scan for the Pi
nmap -sn 192.168.1.0/24  # Adjust for your network
# Look for "Raspberry Pi Foundation" device
```

### Step 4: SSH into Pi
```bash
ssh pi@192.168.1.XXX  # Replace with Pi's IP
# Default password: raspberry (or what you set)
```

## Phase 2: Network Configuration

### Step 5: Configure Pi Network
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y haproxy python3-pip git

# Configure static IP for PVS connection
sudo nano /etc/dhcpcd.conf
```

Add these lines to `/etc/dhcpcd.conf`:
```
interface eth0
static ip_address=172.27.153.3/24
nogateway
```

### Step 6: Configure HAProxy Bridge
```bash
sudo nano /etc/haproxy/haproxy.cfg
```

Add this configuration:
```
frontend http-in
    bind *:80
    default_backend backend_servers

backend backend_servers
    server sv1 172.27.153.1:80

listen stats
    bind *:8080
    stats enable
    stats uri /
    stats refresh 10s
    stats admin if LOCALHOST
```

### Step 7: Enable Services
```bash
sudo systemctl enable haproxy
sudo systemctl start haproxy
sudo reboot
```

## Phase 3: Software Installation

### Step 8: Install Python Dependencies
```bash
# After reboot, SSH back in
ssh pi@192.168.1.XXX

# Install Python packages
pip3 install flask requests schedule python-dateutil plotly pandas numpy
```

### Step 9: Download Solar Monitor Code
```bash
# Create project directory
mkdir -p ~/solar_monitor
cd ~/solar_monitor

# Transfer code files from your computer
scp -r /Users/barrysolomon/Projects/solar_monitor/* pi@192.168.1.XXX:~/solar_monitor/
```

### Step 10: Configure the Application
```bash
cd ~/solar_monitor
nano config.py
```

Update the configuration:
```python
# PVS Gateway Configuration
PVS_IP = '172.27.153.1'  # PVS6 IP
PVS_PORT = '80'
PVS_BASE_URL = f'http://{PVS_IP}:{PVS_PORT}'

# Polling Configuration  
POLL_INTERVAL_SECONDS = 30

# Web Dashboard Configuration
WEB_HOST = "0.0.0.0"  # Allow access from other devices
WEB_PORT = 5000
```

## Phase 4: Physical Connections

### Step 11: Connect to PVS6
1. **Locate your PVS6 unit** (usually near electrical panel)
2. **Find the "LAN" or "Installer" Ethernet port**
3. **Connect Ethernet cable** from Pi to PVS6 LAN port
4. **Power on both devices**

### Step 12: Test Connection
```bash
python3 solar_monitor.py --test-connection
```

You should see:
```
✓ PVS gateway connection successful!
✓ Found X devices
```

### Step 13: Start Full System
```bash
# Start the monitoring system
python3 solar_monitor.py

# Should show:
# Starting web dashboard on http://0.0.0.0:5000
# Data collection started
```

### Step 14: Access Dashboard
- Open web browser on any device on your network
- Go to `http://192.168.1.XXX:5000` (Pi's IP address)
- You should see your solar monitoring dashboard

## Phase 5: Make it Permanent

### Step 15: Auto-start Service
```bash
# Create systemd service
sudo nano /etc/systemd/system/solar-monitor.service
```

Add this content:
```ini
[Unit]
Description=Solar Monitor Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/solar_monitor
ExecStart=/usr/bin/python3 solar_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 16: Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable solar-monitor.service
sudo systemctl start solar-monitor.service

# Check status
sudo systemctl status solar-monitor.service
```

## Troubleshooting

### Issue 1: Can't reach PVS6 (172.27.153.1)
```bash
# Check if Pi can ping PVS6
ping 172.27.153.1

# If no response:
# 1. Check Ethernet cable connection
# 2. Try different Ethernet port on PVS6
# 3. Reboot PVS6 (unplug for 30 seconds)
```

### Issue 2: PVS6 returns 403/500 errors
```bash
# This usually means PVS6 needs reboot
# Unplug PVS6 power for 30 seconds
# Wait 2-3 minutes for full startup
# Test again
```

### Issue 3: Pi loses WiFi connection
```bash
# Check Pi's network status
ip addr show

# Restart networking
sudo systemctl restart networking
```

### Issue 4: Dashboard not accessible
```bash
# Check if service is running
ps aux | grep python

# Check firewall (if enabled)
sudo ufw status

# Test locally on Pi
curl http://localhost:5000
```

## Hardware Shopping List
- Raspberry Pi 4 (4GB RAM) - ~$65
- 32GB MicroSD card - ~$10
- Power supply (5V, 3A) - ~$10
- Ethernet cable (10-25 feet) - ~$8
- Case (optional) - ~$10
- **Total Cost: ~$100**

## Time Estimate
- Hardware setup: 30 minutes
- Software installation: 45 minutes
- Configuration: 30 minutes
- Testing: 30 minutes
- **Total: 2-3 hours**

## Success Criteria
- Pi can ping PVS6 (172.27.153.1)
- `python3 solar_monitor.py --test-connection` succeeds
- Web dashboard accessible from home network
- Data collection running automatically
- Service starts on boot
