# Network Setup Guide for SunPower PVS Gateway

## Overview
This guide will help you connect to your SunPower PVS gateway to read solar data locally, replacing the now-defunct SunPower cloud service.

## Prerequisites
- SunPower PVS5 or PVS6 gateway
- Computer/Raspberry Pi with network access
- Basic networking knowledge

## Step 1: Locate Your PVS Gateway

### Finding the PVS Gateway
1. Look for a small box near your electrical panel (usually gray/white)
2. It should have Ethernet ports and/or Wi-Fi capability
3. The default IP address is typically `172.27.153.1`

### Check Current Network Configuration
```bash
# Scan for the PVS gateway on your network
nmap -sn 172.27.153.0/24

# Or try pinging the default IP
ping 172.27.153.1
```

## Step 2: Understanding PVS6 Ethernet Ports

### **PVS6 Has Two Ethernet Ports**

#### **Blue Ethernet Port (LAN/Installer) - USE THIS ONE!**
- **Purpose**: **Installer/Technician access** - This is what we use!
- **Network**: Isolated installer network (172.27.153.x)
- **Access**: Full API access to solar data
- **Security**: Designed for authorized installer access
- **Default IP**: 172.27.153.1
- **Use Case**: Local monitoring, troubleshooting, data collection

#### **White Ethernet Port (WAN/Internet) - DON'T USE THIS**
- **Purpose**: **Internet connection** for cloud services
- **Network**: Connects to your home network/internet
- **Access**: Limited - mainly for cloud communication
- **Security**: Designed for SunPower cloud services
- **Use Case**: SunPower cloud monitoring, firmware updates

### **Why We Use the Blue Port**
✅ **Full API access** - `/cgi-bin/dl_cgi?Command=DeviceList` works  
✅ **Network isolation** - Maintains proper security  
✅ **Reliable connection** - Designed for local access  
✅ **All solar data** - Complete access to system information  

### **Why Not the White Port**
❌ **Limited API access** - May not provide solar data  
❌ **Network conflicts** - DHCP conflicts with home router  
❌ **Security issues** - Exposes PVS6 to home network  
❌ **Unreliable** - Designed for cloud, not local access  

## Step 3: Network Connection Options

### Option A: Direct Ethernet Connection (Recommended)
1. **Connect directly to PVS BLUE port**
   - Use a laptop/computer with Ethernet port
   - Connect Ethernet cable to PVS **BLUE** "LAN" or "Installer" port
   - Set your computer's IP to `172.27.153.3` (or any IP in 172.27.153.x range)
   - Subnet mask: `255.255.255.0`

2. **Configure your computer's network settings:**
   ```bash
   # On macOS/Linux
   sudo ifconfig en0 172.27.153.3 netmask 255.255.255.0
   
   # Test connection
   ping 172.27.153.1
   ```

### Option B: Router Bridge Setup
1. **Use a dedicated router/access point**
   - Connect router WAN port to PVS **BLUE** LAN port
   - Configure router to bridge the networks
   - Access PVS through router's network

### Option C: Wi-Fi Connection (PVS6 only)
1. **Connect to PVS Wi-Fi network**
   - Look for network named "SunPower" or similar
   - Default password is often "sunpower" or "installer"
   - Once connected, access `http://172.27.153.1`
   - **Note**: Wi-Fi may have limited API access compared to BLUE Ethernet port

## Step 3: Test PVS API Access

### Basic API Test
```bash
# Test the main API endpoint
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"

# Should return JSON data with your solar system information
```

### Common API Endpoints
- `http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList` - Main device data
- `http://172.27.153.1/cgi-bin/dl_cgi?Command=MeterData` - Detailed meter data
- `http://172.27.153.1/cgi-bin/dl_cgi?Command=SystemInfo` - System information

## Step 4: Troubleshooting

### Common Issues

#### 1. Connection Refused (403/500 errors)
- **Solution**: Reboot the PVS gateway
- Unplug power for 30 seconds, then plug back in
- Wait 2-3 minutes for full startup

#### 2. Can't Reach 172.27.153.1
- **Check port color**: Make sure you're using the **BLUE** Ethernet port
- Check Ethernet cable connection
- Verify your computer's IP is in the same subnet (172.27.153.x)
- Try different Ethernet port on PVS

#### 3. Wrong Ethernet Port
- **Using WHITE port**: Limited or no API access
- **Solution**: Switch to BLUE port for full API access
- **Test**: `curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"`

#### 4. Wi-Fi Connection Issues (PVS6)
- Reset PVS Wi-Fi settings if needed
- Check for firmware updates
- Some newer PVS6 units may have different default settings
- **Note**: Wi-Fi may have limited API access compared to BLUE Ethernet port

#### 5. DHCP Conflicts
- PVS runs its own DHCP server on BLUE port
- Don't connect PVS WHITE port directly to your main home network
- Use isolated network or dedicated router

## Step 5: Production Setup

### For Permanent Installation
1. **Use a Raspberry Pi or dedicated computer**
2. **Set up static IP configuration**
3. **Configure automatic startup of monitoring service**
4. **Set up network routing to access from main network**

### Network Security
- Keep PVS on isolated network segment
- Use firewall rules to restrict access
- Consider VPN for remote access
- Don't expose PVS directly to internet

## Step 6: Verify Data Collection

Once connected, you should see JSON data like:
```json
[
  {
    "DeviceID": "PVS001",
    "DeviceType": "PV_Supervisor",
    "p_3phsum_kw": 5.2,
    "Energy_kWh": 1250.5,
    "Voltage_V": 240.1,
    "Current_A": 21.7
  },
  {
    "DeviceID": "METER001", 
    "DeviceType": "Production_Meter",
    "p_3phsum_kw": 4.8,
    "Energy_kWh": 1180.2
  }
]
```

## Next Steps
After successful network setup:
1. Run the solar monitoring application
2. Configure the PVS_IP in config.py if different from default
3. Start data collection and web dashboard
4. Set up automated monitoring and alerts

## Support
- Check SunPower community forums for firmware-specific issues
- Some PVS units may have different default IPs or API endpoints
- Consider contacting Enphase if your system uses their microinverters
