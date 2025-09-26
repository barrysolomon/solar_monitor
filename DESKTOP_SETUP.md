# Desktop Computer Setup Guide

**Running SunPower monitoring directly on your desktop/laptop computer**

This guide shows how to run the solar monitoring system directly on your computer using an old WiFi router as a network bridge, eliminating the need for a Raspberry Pi entirely.

## Overview

### **Why Run on Desktop?**
- ✅ **No additional hardware** - Use your existing computer
- ✅ **More powerful** - Better performance than Raspberry Pi
- ✅ **Easier development** - Familiar environment
- ✅ **Better debugging** - Full development tools available
- ✅ **Cost effective** - Only need old router + Ethernet cable (~$8)
- ✅ **Flexible** - Can run on Windows, macOS, or Linux

### **What We're Building**
```
PVS6 BLUE Port → Ethernet → Old Router → WiFi → Home Network → Your Computer (via normal WiFi)
```

**Important**: Your computer connects to your **normal home WiFi**, not the old router's WiFi. The old router bridges the PVS6 network to your home network.

## Hardware Requirements

### **Required Hardware**
- **Old WiFi router** - $0 (you already own it)
- **Ethernet cable** (10-25 feet) - ~$8
- **Your computer** - $0 (you already own it)

### **Total Cost: ~$8** (vs $100+ for Pi setup)

## Network Architecture

### **How It Works**
1. **PVS6 BLUE port** connects to router WAN port via Ethernet
2. **Router connects to home network** via WiFi
3. **Your computer** connects to home network via WiFi/Ethernet
4. **Router acts as bridge** between PVS6 network and home network
5. **Monitoring software** runs on your computer

### **Network Flow**
```
PVS6 (172.27.153.1) → Ethernet → Router → WiFi → Home Network → Your Computer
```

## Setup Steps

### **Step 1: Configure Router Bridge**

#### **Connect Hardware**
1. **Connect Ethernet cable** from PVS6 BLUE port to router WAN port
2. **Power on router** and wait for boot
3. **Connect to router WiFi** (default SSID)

#### **Configure Router**
1. **Access router web interface** (usually 192.168.1.1)
2. **Login** with default credentials (admin/admin)
3. **Change default password** for security
4. **Configure WiFi** to connect to your home network
5. **Save configuration** and restart router

#### **Test Router Bridge**
```bash
# Test PVS6 access through router
ping 172.27.153.1

# Test API access
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"
```

### **Step 2: Install Software on Computer**

#### **Install Python**
- **Windows**: Download from python.org
- **macOS**: `brew install python3` or download from python.org
- **Linux**: `sudo apt install python3 python3-pip`

#### **Install Dependencies**
```bash
# Navigate to project directory
cd /path/to/solar_monitor

# Install requirements
pip install -r requirements.txt
```

#### **Verify Installation**
```bash
# Test Python installation
python3 --version

# Test dependencies
python3 -c "import flask, requests, schedule"
```

### **Step 3: Configure Monitoring Software**

#### **Update Configuration**
```python
# config.py - No changes needed!
PVS_GATEWAY_IP = "172.27.153.1"  # PVS6 IP (unchanged)
PVS_GATEWAY_PORT = 80
PVS_GATEWAY_URL = f"http://{PVS_GATEWAY_IP}:{PVS_GATEWAY_PORT}"

# Router acts as transparent bridge
# PVS6 is accessible at same IP as before
```

#### **Test Connection**
```bash
# Test PVS6 connection
python3 solar_monitor.py --test-connection

# Should show successful connection to PVS6
```

### **Step 4: Run Monitoring System**

#### **Start Data Collection**
```bash
# Start data collection service
python3 solar_monitor.py --mode collector

# Or start web dashboard
python3 solar_monitor.py --mode dashboard
```

#### **Access Web Dashboard**
1. **Open web browser** to `http://localhost:5000`
2. **View real-time solar data** and charts
3. **Monitor system performance** and logs

## Platform-Specific Setup

### **Windows Setup**

#### **Install Python**
1. **Download Python** from python.org
2. **Run installer** with "Add to PATH" checked
3. **Verify installation** in Command Prompt:
   ```cmd
   python --version
   pip --version
   ```

#### **Install Dependencies**
```cmd
# Navigate to project directory
cd C:\path\to\solar_monitor

# Install requirements
pip install -r requirements.txt
```

#### **Run Monitoring**
```cmd
# Start data collection
python solar_monitor.py --mode collector

# Start web dashboard
python solar_monitor.py --mode dashboard
```

### **macOS Setup**

#### **Install Python**
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```

#### **Install Dependencies**
```bash
# Navigate to project directory
cd /path/to/solar_monitor

# Install requirements
pip3 install -r requirements.txt
```

#### **Run Monitoring**
```bash
# Start data collection
python3 solar_monitor.py --mode collector

# Start web dashboard
python3 solar_monitor.py --mode dashboard
```

### **Linux Setup**

#### **Install Python**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

#### **Install Dependencies**
```bash
# Navigate to project directory
cd /path/to/solar_monitor

# Install requirements
pip3 install -r requirements.txt
```

#### **Run Monitoring**
```bash
# Start data collection
python3 solar_monitor.py --mode collector

# Start web dashboard
python3 solar_monitor.py --mode dashboard
```

## Running as Service

### **Windows Service**

#### **Using NSSM (Non-Sucking Service Manager)**
1. **Download NSSM** from nssm.cc
2. **Install service**:
   ```cmd
   nssm install SolarMonitor "C:\Python\python.exe" "C:\path\to\solar_monitor\solar_monitor.py --mode collector"
   ```
3. **Start service**:
   ```cmd
   nssm start SolarMonitor
   ```

### **macOS Service**

#### **Using launchd**
1. **Create plist file**:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.solar.monitor</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/path/to/solar_monitor/solar_monitor.py</string>
           <string>--mode</string>
           <string>collector</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
   </dict>
   </plist>
   ```
2. **Install service**:
   ```bash
   sudo cp com.solar.monitor.plist /Library/LaunchDaemons/
   sudo launchctl load /Library/LaunchDaemons/com.solar.monitor.plist
   ```

### **Linux Service**

#### **Using systemd**
1. **Create service file**:
   ```ini
   [Unit]
   Description=Solar Monitor
   After=network.target

   [Service]
   Type=simple
   User=yourusername
   WorkingDirectory=/path/to/solar_monitor
   ExecStart=/usr/bin/python3 solar_monitor.py --mode collector
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
2. **Install service**:
   ```bash
   sudo cp solar-monitor.service /etc/systemd/system/
   sudo systemctl enable solar-monitor
   sudo systemctl start solar-monitor
   ```

## Advantages of Desktop Setup

### **Performance Benefits**
- ✅ **More CPU power** - Better performance than Raspberry Pi
- ✅ **More RAM** - Handle larger datasets and more concurrent connections
- ✅ **Faster storage** - SSD vs SD card performance
- ✅ **Better multitasking** - Run other applications simultaneously

### **Development Benefits**
- ✅ **Familiar environment** - Use your preferred IDE and tools
- ✅ **Better debugging** - Full development tools available
- ✅ **Easier testing** - Quick iteration and testing
- ✅ **Version control** - Easy Git integration

### **Cost Benefits**
- ✅ **No additional hardware** - Use existing computer
- ✅ **Only $8 total cost** - Just Ethernet cable
- ✅ **92% savings** vs Raspberry Pi setup
- ✅ **No ongoing costs** - No additional power consumption

### **Flexibility Benefits**
- ✅ **Multiple platforms** - Windows, macOS, Linux
- ✅ **Easy updates** - Simple software updates
- ✅ **Customization** - Easy to modify and extend
- ✅ **Integration** - Easy to integrate with other software

## Troubleshooting

### **Common Issues**

#### **Can't Access PVS6**
- **Problem**: Router not bridging properly
- **Solution**: Check router configuration, verify WiFi connection

#### **Python Import Errors**
- **Problem**: Dependencies not installed
- **Solution**: Run `pip install -r requirements.txt`

#### **Port Already in Use**
- **Problem**: Another service using port 5000
- **Solution**: Change port in config.py or stop conflicting service

#### **Permission Errors**
- **Problem**: Insufficient permissions
- **Solution**: Run with appropriate user permissions

### **Testing Commands**
```bash
# Test PVS6 connectivity
ping 172.27.153.1

# Test API access
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"

# Test Python installation
python3 --version

# Test dependencies
python3 -c "import flask, requests, schedule"

# Test monitoring software
python3 solar_monitor.py --test-connection
```

## Integration Options

### **Home Assistant Integration**
```yaml
# Use desktop computer as bridge for HA
sensor:
  - platform: rest
    name: "Solar Power"
    resource: "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"
    value_template: "{{ value_json.p_3phsum_kw }}"
```

### **Grafana Integration**
```yaml
# Prometheus configuration
scrape_configs:
  - job_name: 'sunpower'
    static_configs:
      - targets: ['172.27.153.1:80']
```

### **Custom Integrations**
- **MQTT publishing** - Send data to MQTT broker
- **Database integration** - Store in PostgreSQL, MySQL
- **API endpoints** - Create REST API for other applications
- **Webhooks** - Send data to external services

## Best Practices

### **Security**
- **Change router password** immediately
- **Use firewall** to restrict access
- **Regular updates** - Keep Python and dependencies updated
- **Backup data** - Regular database backups

### **Performance**
- **Monitor resources** - Check CPU, memory, disk usage
- **Optimize database** - Regular cleanup and optimization
- **Log management** - Rotate logs to prevent disk full
- **Error handling** - Robust error handling and recovery

### **Reliability**
- **Service management** - Use proper service management
- **Health checks** - Monitor service health
- **Automatic restart** - Configure automatic restart on failure
- **Monitoring** - Monitor the monitoring system

## Summary

### **When to Use Desktop Setup**
- ✅ **You have a computer** that can run 24/7
- ✅ **Cost is primary concern** (saving $95+)
- ✅ **Want familiar environment** for development
- ✅ **Need better performance** than Raspberry Pi
- ✅ **Want easy customization** and integration

### **Quick Start**
1. **Set up router bridge** (connect PVS6 to router)
2. **Install Python** and dependencies on your computer
3. **Test PVS6 connection** through router
4. **Run monitoring software** on your computer
5. **Access web dashboard** at localhost:5000

### **Total Cost**
- **Hardware**: ~$8 (Ethernet cable only)
- **Software**: Free (Python + open source)
- **Savings**: $95+ vs Raspberry Pi setup

The desktop setup is **perfect** for your situation because it:
- **Uses your existing computer** (no new hardware needed)
- **Saves $95+** compared to Pi setup
- **Provides better performance** than Raspberry Pi
- **Offers familiar development environment**
- **Makes the project accessible** to anyone with a computer

This approach makes SunPower local monitoring **truly accessible** to everyone! 🎉
