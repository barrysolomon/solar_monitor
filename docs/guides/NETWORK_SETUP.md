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

### Option C: PVS6 Wi-Fi Hotspot Connection (RECOMMENDED)
1. **PVS6 broadcasts temporary Wi-Fi hotspot**
   - **SSID Format**: "SunPower" + last 5 digits of serial number
   - **Password Format**: First 3 digits + last 4 digits of serial number
   - **Example**: Serial `ZT123456789012345` → SSID: `SunPower12345`, Password: `12345`
   - **Network**: 172.27.152.x subnet (different from BLUE port!)
   - **Gateway IP**: 172.27.152.1

2. **Connect to PVS6 Wi-Fi**
   ```bash
   # Scan for PVS6 WiFi hotspot
   sudo iwlist wlan0 scan | grep -i sunpower
   
   # Connect using NetworkManager
   sudo nmcli device wifi connect "SunPower12345" password "22371297"
   
   # Verify connection
   iwconfig
   ip addr show wlan0
   # Should show: inet 172.27.152.X/24
   ```

3. **Access PVS6 API**
   ```bash
   # Test connectivity
   ping 172.27.152.1
   
   # Access solar data API
   curl "http://172.27.152.1/cgi-bin/dl_cgi?Command=DeviceList"
   ```

4. **Important Notes**
   - **Different IP range**: WiFi uses 172.27.152.x, not 172.27.153.x
   - **Temporary hotspot**: May disappear after 10-15 minutes of inactivity
   - **Reboot to restore**: Unplug PVS6 for 30 seconds to restore hotspot
   - **More reliable**: Often works when BLUE port has issues

### Option D: USB-to-Ethernet Adapter (Alternative Solution)
1. **When BLUE Ethernet port doesn't work**
   - **Hardware needed**: USB-to-Ethernet adapter (~$7)
   - **PVS6 requirement**: Must have USB-A ports (most PVS6 units have 3)
   - **Compatibility**: Not all adapters work - check community recommendations

2. **Setup Process**
   - **Connect adapter** to PVS6 USB port
   - **Connect Pi/computer** to adapter via Ethernet cable
   - **Configure network** as normal (172.27.153.x subnet)
   - **Test API access**: Same endpoints as BLUE port

3. **Benefits**
   - **Bypasses faulty BLUE port** hardware issues
   - **Same API access** as direct BLUE port connection
   - **Reliable connection** - USB ports typically more stable
   - **Cost effective** - Much cheaper than professional repair

## Step 3: Test PVS API Access

### Basic API Test
```bash
# Test the main API endpoint (IP varies by connection method)
curl "http://172.27.152.1/cgi-bin/dl_cgi?Command=DeviceList"  # WiFi hotspot
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"  # BLUE port

# Should return JSON data with your solar system information
```

### Common API Endpoints
**WiFi Hotspot (172.27.152.1):**
- `http://172.27.152.1/cgi-bin/dl_cgi?Command=DeviceList` - Main device data
- `http://172.27.152.1/cgi-bin/dl_cgi?Command=MeterData` - Detailed meter data
- `http://172.27.152.1/cgi-bin/dl_cgi?Command=SystemInfo` - System information

**BLUE Port (172.27.153.1):**
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

#### 4. BLUE Port "Link Detected: No" Issues
- **Check physical connections**: Ensure cable is firmly connected to BLUE port
- **Verify PVS6 power**: Look for power LED and status indicators
- **Reboot PVS6**: Unplug power for 30 seconds, wait 2-3 minutes after restart
- **Try different cable**: Test with known-good Ethernet cable
- **Check for multiple BLUE ports**: Some PVS6 units have multiple blue ports
- **Test cable/Pi Ethernet**: Connect Pi to home router to verify hardware works

#### 5. Wi-Fi Connection Issues (PVS6)
- **Hotspot disappears**: PVS6 WiFi is temporary, may need PVS6 reboot to restore
- **403 Forbidden errors**: Try different API endpoints or authentication methods
- **Connection hangs**: May cause Pi to lock up, require reboot
- **Signal strength**: PVS6 WiFi may have limited range
- **Alternative**: Use USB-to-Ethernet adapter in PVS6 USB ports (~$7 solution)

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
