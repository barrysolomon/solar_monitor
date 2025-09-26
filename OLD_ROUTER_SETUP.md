# Old WiFi Router Setup Guide

**Using an old WiFi router as a network bridge for SunPower PVS6 monitoring**

This guide shows how to repurpose an old WiFi router as a cost-effective alternative to a Raspberry Pi for bridging between your home network and the PVS6 gateway.

## Overview

### **Why Use an Old Router?**
- ✅ **Cost-effective** - Use existing hardware you already own
- ✅ **Dedicated device** - Doesn't interfere with other network devices
- ✅ **Built-in networking** - Already has Ethernet ports and WiFi
- ✅ **Low power consumption** - Typically 5-15W vs Pi's 3-5W
- ✅ **Reliable** - Designed for 24/7 operation
- ✅ **Easy setup** - Familiar router configuration interface

### **What We're Building**
```
PVS6 BLUE Port → Ethernet → Old Router → WiFi → Home Network → Monitoring Device
```

## Hardware Requirements

### **Router Requirements**
- **Ethernet ports** - At least 2 (WAN + LAN)
- **WiFi capability** - 802.11n or better
- **OpenWrt/DD-WRT support** - For advanced configuration (optional)
- **Power supply** - Original or compatible
- **Age** - Any router from 2010+ should work

### **Additional Hardware**
- **Ethernet cable** - 10-25 feet (same as Pi setup)
- **Power outlet** - Near PVS6 location
- **Optional**: Ethernet switch if you need more ports

### **Cost Comparison**
- **Old Router**: $0 (you already own it)
- **Ethernet cable**: ~$8
- **Total Cost**: ~$8 vs ~$100 for Pi setup

## Router Selection Guide

### **Ideal Router Features**
- **Dual-band WiFi** (2.4GHz + 5GHz)
- **Gigabit Ethernet** ports
- **USB ports** (for future storage)
- **OpenWrt support** (for advanced features)
- **Good WiFi range** (for reliable connection)

### **Minimum Requirements**
- **100Mbps Ethernet** ports
- **802.11n WiFi** (or better)
- **WAN + LAN ports**
- **Web configuration interface**

### **Router Brands That Work Well**
- **Linksys** - Good OpenWrt support
- **Netgear** - Reliable, good range
- **TP-Link** - Cost-effective, decent performance
- **ASUS** - Advanced features, good WiFi
- **D-Link** - Basic but functional

## Setup Options

### **Option 1: Basic Router Bridge (Easiest)**

#### **How It Works**
1. **Router connects to PVS6** via Ethernet (BLUE port)
2. **Router connects to home network** via WiFi
3. **Router acts as bridge** between networks
4. **Monitoring device** connects to router's WiFi

#### **Network Architecture**
```
PVS6 (172.27.153.1) → Ethernet → Router → WiFi → Home Network → Your Device
```

#### **Configuration Steps**
1. **Connect Ethernet cable** from PVS6 BLUE port to router WAN port
2. **Power on router** and wait for boot
3. **Connect to router WiFi** (default SSID/password)
4. **Access router web interface** (usually 192.168.1.1)
5. **Configure WiFi** to connect to your home network
6. **Test connection** to PVS6

### **Option 2: Advanced Router Bridge (OpenWrt)**

#### **How It Works**
1. **Flash OpenWrt firmware** to router
2. **Configure network bridging** between interfaces
3. **Set up routing rules** for PVS6 network
4. **Enable advanced features** like VPN, monitoring

#### **Advantages**
- **More control** over network configuration
- **Advanced features** like VPN, QoS, monitoring
- **Better security** with custom firewall rules
- **Extensibility** with additional packages

#### **Requirements**
- **Router with OpenWrt support**
- **Technical knowledge** for firmware flashing
- **Risk tolerance** (flashing can brick router)

## Step-by-Step Setup

### **Step 1: Prepare Router**

#### **Reset to Factory Defaults**
1. **Power on router** with reset button held
2. **Hold reset** for 30 seconds
3. **Release reset** and wait for reboot
4. **Router will boot** with default settings

#### **Access Router Interface**
1. **Connect to router WiFi** (default SSID)
2. **Open web browser** to 192.168.1.1
3. **Login** with default credentials (admin/admin)
4. **Change default password** for security

### **Step 2: Configure Network**

#### **WiFi Configuration**
1. **Go to WiFi settings**
2. **Scan for your home network**
3. **Connect to home network** with password
4. **Save configuration**

#### **Ethernet Configuration**
1. **Go to WAN settings**
2. **Set WAN port** to connect to PVS6
3. **Configure static IP** if needed
4. **Enable DHCP** for PVS6 network

### **Step 3: Test Connection**

#### **Test PVS6 Access**
```bash
# From router's web interface or connected device
ping 172.27.153.1

# Test API access
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"
```

#### **Test Home Network Access**
```bash
# Test internet connectivity
ping 8.8.8.8

# Test home network access
ping 192.168.1.1
```

## Advanced Configuration

### **OpenWrt Setup (Advanced Users)**

#### **Flash OpenWrt Firmware**
1. **Download OpenWrt firmware** for your router model
2. **Access router web interface**
3. **Upload firmware** via firmware update
4. **Wait for flash** to complete
5. **Router will reboot** with OpenWrt

#### **Configure Network Bridging**
```bash
# Configure network interfaces
uci set network.lan.proto='static'
uci set network.lan.ipaddr='192.168.1.100'
uci set network.lan.netmask='255.255.255.0'

# Configure WiFi
uci set wireless.@wifi-iface[0].network='lan'
uci set wireless.@wifi-iface[0].ssid='SolarBridge'

# Configure routing
uci add network route
uci set network.@route[-1].target='172.27.153.0/24'
uci set network.@route[-1].gateway='192.168.1.1'

# Apply configuration
uci commit network
/etc/init.d/network restart
```

### **Custom Firmware Options**

#### **DD-WRT**
- **Easier setup** than OpenWrt
- **Good GUI** for configuration
- **Limited customization** compared to OpenWrt

#### **Tomato**
- **User-friendly** interface
- **Good performance** monitoring
- **Limited router support**

## Performance Considerations

### **Router Performance**
- **CPU power** - Affects routing performance
- **RAM** - More RAM = better performance
- **WiFi speed** - 802.11n minimum, 802.11ac preferred
- **Ethernet speed** - 100Mbps minimum, Gigabit preferred

### **Network Performance**
- **WiFi range** - Router placement affects signal strength
- **Interference** - 2.4GHz band can be crowded
- **Bandwidth** - Solar data is low bandwidth, not critical

### **Reliability**
- **24/7 operation** - Routers designed for continuous use
- **Heat management** - Ensure good ventilation
- **Power supply** - Use original or compatible power supply

## Troubleshooting

### **Common Issues**

#### **Can't Access Router**
- **Problem**: Default IP not working
- **Solution**: Check router label for default IP, try 192.168.0.1

#### **WiFi Not Connecting**
- **Problem**: Can't connect to home network
- **Solution**: Check WiFi password, signal strength

#### **PVS6 Not Accessible**
- **Problem**: Can't reach 172.27.153.1
- **Solution**: Check Ethernet cable, verify BLUE port connection

#### **Slow Performance**
- **Problem**: Router struggling with traffic
- **Solution**: Check CPU usage, consider router upgrade

### **Testing Commands**
```bash
# Test router connectivity
ping 192.168.1.1

# Test PVS6 connectivity
ping 172.27.153.1

# Test API access
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"

# Test internet connectivity
ping 8.8.8.8
```

## Security Considerations

### **Router Security**
- **Change default password** immediately
- **Disable WPS** if not needed
- **Use WPA2/WPA3** encryption
- **Regular firmware updates**

### **Network Security**
- **Isolate PVS6 network** from internet
- **Use firewall rules** to restrict access
- **Monitor network traffic** for anomalies

### **Access Control**
- **Limit admin access** to specific devices
- **Use strong passwords** for all accounts
- **Enable logging** for security monitoring

## Integration with Monitoring System

### **Python Client Configuration**
```python
# Update config.py for router setup
PVS_GATEWAY_IP = "172.27.153.1"  # PVS6 IP (unchanged)
PVS_GATEWAY_PORT = 80
PVS_GATEWAY_URL = f"http://{PVS_GATEWAY_IP}:{PVS_GATEWAY_PORT}"

# Router acts as transparent bridge
# No changes needed to existing code
```

### **Home Assistant Integration**
```yaml
# Use router as bridge for HA
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

## Cost Analysis

### **Old Router Setup**
- **Router**: $0 (already owned)
- **Ethernet cable**: $8
- **Power consumption**: ~10W
- **Total cost**: $8

### **Raspberry Pi Setup**
- **Pi 4**: $65
- **SD card**: $10
- **Power supply**: $10
- **Ethernet cable**: $8
- **Case**: $10
- **Total cost**: $103

### **Savings**
- **Cost savings**: $95 (92% reduction)
- **Power savings**: Minimal difference
- **Setup complexity**: Similar

## Advantages and Disadvantages

### **Advantages**
- ✅ **Cost-effective** - Use existing hardware
- ✅ **Dedicated device** - Doesn't interfere with other devices
- ✅ **Built-in networking** - Ethernet + WiFi included
- ✅ **Reliable** - Designed for 24/7 operation
- ✅ **Easy setup** - Familiar router interface
- ✅ **Good performance** - Adequate for solar monitoring

### **Disadvantages**
- ❌ **Limited customization** - Compared to Pi
- ❌ **Older hardware** - May be slower/less reliable
- ❌ **Firmware limitations** - Stock firmware may be restrictive
- ❌ **No GPIO** - Can't add sensors or other hardware
- ❌ **Less flexible** - Harder to modify for specific needs

## Best Practices

### **Router Selection**
- **Choose router** with good OpenWrt support
- **Check specifications** - CPU, RAM, WiFi capabilities
- **Verify compatibility** - Ensure it works with your setup

### **Configuration**
- **Reset to defaults** before starting
- **Change default passwords** immediately
- **Test thoroughly** before deploying
- **Document settings** for future reference

### **Maintenance**
- **Regular updates** - Keep firmware current
- **Monitor performance** - Check CPU/memory usage
- **Backup configuration** - Save settings before changes
- **Plan for replacement** - Old hardware will eventually fail

## Summary

### **When to Use Old Router**
- ✅ **You have an old router** lying around
- ✅ **Cost is primary concern** (saving $95)
- ✅ **Basic monitoring** is sufficient
- ✅ **You're comfortable** with router configuration

### **When to Use Raspberry Pi**
- ✅ **Need customization** and flexibility
- ✅ **Want to add sensors** or other hardware
- ✅ **Need GPIO pins** for future projects
- ✅ **Prefer Linux** environment

### **Quick Start**
1. **Find old router** with Ethernet + WiFi
2. **Reset to factory defaults**
3. **Connect PVS6 BLUE port** to router WAN
4. **Configure WiFi** to connect to home network
5. **Test PVS6 access** via router
6. **Deploy monitoring system**

The old router approach is an excellent **cost-effective alternative** that can save you $95 while providing the same core functionality as a Raspberry Pi setup!
