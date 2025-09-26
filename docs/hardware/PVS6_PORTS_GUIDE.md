# PVS6 Ethernet Ports Guide

**Understanding the difference between BLUE and WHITE Ethernet ports**

This guide explains the critical difference between the two Ethernet ports on your SunPower PVS6 gateway and why you must use the correct one for local monitoring.

## PVS6 Has Two Ethernet Ports

### **🔵 BLUE Ethernet Port (LAN/Installer) - USE THIS ONE!**

#### **Purpose**
- **Installer/Technician access** - This is what we use for local monitoring
- **Local API access** - Full access to solar system data
- **Troubleshooting** - Designed for system diagnostics
- **Data collection** - Complete access to all solar metrics

#### **Network Details**
- **Network**: Isolated installer network (172.27.153.x)
- **Default IP**: 172.27.153.1
- **Subnet**: 172.27.153.0/24
- **DHCP**: PVS6 runs its own DHCP server
- **Security**: Designed for authorized installer access

#### **API Access**
- **Full API access** - All endpoints available
- **DeviceList**: `/cgi-bin/dl_cgi?Command=DeviceList`
- **MeterData**: `/cgi-bin/dl_cgi?Command=MeterData`
- **SystemInfo**: `/cgi-bin/dl_cgi?Command=SystemInfo`
- **Real-time data** - Live solar production data

#### **Use Cases**
- ✅ **Local monitoring** - Our solar monitoring system
- ✅ **Troubleshooting** - System diagnostics and repair
- ✅ **Data collection** - Historical data analysis
- ✅ **Per-panel monitoring** - Individual panel status

### **⚪ WHITE Ethernet Port (WAN/Internet) - DON'T USE THIS**

#### **Purpose**
- **Internet connection** for SunPower cloud services
- **Cloud communication** - Connects to SunPower servers
- **Firmware updates** - System software updates
- **Remote monitoring** - SunPower's cloud dashboard

#### **Network Details**
- **Network**: Connects to your home network (192.168.1.x)
- **Internet access** - Routes to SunPower cloud servers
- **Limited local access** - Minimal API functionality
- **Security**: Designed for cloud communication only

#### **API Access**
- **Limited API access** - May not provide solar data
- **Cloud-focused** - Designed for SunPower's servers
- **Restricted endpoints** - Many local APIs unavailable
- **No local data** - Cannot access real-time solar data

#### **Use Cases**
- ❌ **NOT for local monitoring** - Limited or no API access
- ❌ **NOT for data collection** - Cannot access solar data
- ❌ **NOT for troubleshooting** - Limited diagnostic access
- ✅ **Cloud services only** - SunPower's official monitoring

## Why We Must Use the BLUE Port

### **API Access Requirements**
```bash
# This works on BLUE port
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"

# This may NOT work on WHITE port
curl "http://192.168.1.100/cgi-bin/dl_cgi?Command=DeviceList"
```

### **Network Isolation**
- **BLUE port**: Maintains proper network isolation
- **WHITE port**: Exposes PVS6 to home network (security risk)
- **DHCP conflicts**: WHITE port can cause network issues
- **Reliability**: BLUE port designed for local access

### **Data Availability**
- **BLUE port**: Complete access to all solar data
- **WHITE port**: Limited or no access to solar data
- **Real-time data**: Only available through BLUE port
- **Historical data**: Only accessible via BLUE port

## Physical Identification

### **Visual Identification**
- **BLUE port**: Usually labeled "LAN" or "Installer"
- **WHITE port**: Usually labeled "WAN" or "Internet"
- **Color coding**: Blue = local, White = internet
- **Location**: Usually side by side on PVS6

### **Port Labels**
- **BLUE port**: "LAN", "Installer", "Local", "Tech"
- **WHITE port**: "WAN", "Internet", "Cloud", "Remote"
- **Documentation**: Check PVS6 manual for exact labels

## Setup Instructions

### **Correct Setup (BLUE Port)**
```
PVS6 BLUE Port → Ethernet Cable → Powerline Adapter → Pi → WiFi → Home Network
```

**Steps:**
1. **Find BLUE Ethernet port** on PVS6
2. **Connect Ethernet cable** to BLUE port
3. **Connect other end** to Powerline adapter or Pi
4. **Test connection**: `ping 172.27.153.1`
5. **Test API**: `curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"`

### **Incorrect Setup (WHITE Port)**
```
PVS6 WHITE Port → Ethernet Cable → Router → Home Network
```

**Problems:**
- ❌ **Limited API access** - May not get solar data
- ❌ **Network conflicts** - DHCP conflicts with router
- ❌ **Security issues** - Exposes PVS6 to home network
- ❌ **Unreliable** - Not designed for local access

## Network Architecture

### **BLUE Port Network**
```
PVS6 BLUE Port (172.27.153.1)
    ↕
Isolated Installer Network (172.27.153.x)
    ↕
Raspberry Pi Bridge (172.27.153.3)
    ↕
Home WiFi Network (192.168.1.x)
```

### **WHITE Port Network**
```
PVS6 WHITE Port
    ↕
Home Network (192.168.1.x)
    ↕
Internet Router
    ↕
SunPower Cloud Servers
```

## Troubleshooting

### **Common Mistakes**

#### **Using Wrong Port**
- **Problem**: Connected to WHITE port instead of BLUE
- **Symptoms**: No API access, wrong IP address, limited data
- **Solution**: Switch to BLUE port

#### **Wrong IP Address**
- **Problem**: Expecting 192.168.1.x instead of 172.27.153.x
- **Symptoms**: Cannot ping PVS6, connection refused
- **Solution**: Use 172.27.153.1 for BLUE port

#### **Network Conflicts**
- **Problem**: WHITE port connected to home router
- **Symptoms**: DHCP conflicts, network instability
- **Solution**: Disconnect WHITE port, use BLUE port only

### **Testing Port Connection**

#### **Test BLUE Port**
```bash
# Should work on BLUE port
ping 172.27.153.1
curl "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"

# Should return solar data
```

#### **Test WHITE Port**
```bash
# May not work on WHITE port
ping 192.168.1.100
curl "http://192.168.1.100/cgi-bin/dl_cgi?Command=DeviceList"

# May return limited or no data
```

## Security Considerations

### **BLUE Port Security**
- **Isolated network** - Not accessible from internet
- **Local access only** - Requires physical connection
- **Authorized access** - Designed for installers/technicians
- **Secure by design** - Maintains network isolation

### **WHITE Port Security**
- **Internet accessible** - Can be reached from internet
- **Cloud communication** - Connects to external servers
- **Potential exposure** - May expose PVS6 to attacks
- **Less secure** - Designed for cloud, not local access

## Best Practices

### **Always Use BLUE Port**
- ✅ **Connect to BLUE port** for local monitoring
- ✅ **Use 172.27.153.x network** for PVS6 access
- ✅ **Maintain network isolation** for security
- ✅ **Test API access** before proceeding

### **Avoid WHITE Port**
- ❌ **Don't connect WHITE port** to home network
- ❌ **Don't expect API access** from WHITE port
- ❌ **Don't use WHITE port** for local monitoring
- ❌ **Don't expose WHITE port** to internet

## Integration Examples

### **Raspberry Pi Setup**
```bash
# Pi network configuration for BLUE port
# WiFi interface: 192.168.1.100 (home network)
# Ethernet interface: 172.27.153.3 (PVS6 network)

# HAProxy configuration
backend backend_servers
    server sv1 172.27.153.1:80  # BLUE port IP
```

### **Powerline Adapter Setup**
```
PVS6 BLUE Port → Ethernet → Powerline Adapter 1 → Electrical Wiring → Powerline Adapter 2 → Pi
```

### **Home Assistant Integration**
```yaml
# Use BLUE port IP for HA integration
sensor:
  - platform: rest
    name: "Solar Power"
    resource: "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"
    value_template: "{{ value_json.p_3phsum_kw }}"
```

## Summary

### **Key Points**
- **BLUE port**: Use for local monitoring (172.27.153.1)
- **WHITE port**: Don't use for local monitoring
- **API access**: Only available through BLUE port
- **Network isolation**: Maintained by BLUE port
- **Security**: BLUE port is more secure for local access

### **Quick Reference**
- **Connect to**: BLUE Ethernet port
- **IP address**: 172.27.153.1
- **Network**: 172.27.153.x
- **API endpoint**: `/cgi-bin/dl_cgi?Command=DeviceList`
- **Test command**: `ping 172.27.153.1`

---

**Remember**: Always use the BLUE Ethernet port for local solar monitoring! 🔵
