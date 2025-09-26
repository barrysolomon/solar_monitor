# PVS6 Connection Troubleshooting Guide

This guide covers all known issues and solutions for connecting to SunPower PVS6 gateways.

## Connection Methods Overview

### Method 1: PVS6 WiFi Hotspot (RECOMMENDED)
- **IP Range**: 172.27.152.x
- **Gateway IP**: 172.27.152.1
- **Pros**: Works reliably, no physical cables
- **Cons**: Temporary hotspot, may disappear periodically

### Method 2: PVS6 Ethernet BLUE Port
- **IP Range**: 172.27.153.x  
- **Gateway IP**: 172.27.153.1
- **Pros**: Permanent wired connection
- **Cons**: Often disabled by default, requires configuration

### Method 3: USB-to-Ethernet Adapter
- **Use Case**: When BLUE port is problematic
- **Hardware**: USB 3.0 to Gigabit Ethernet adapter
- **Pros**: Bypasses BLUE port issues
- **Cons**: Requires additional hardware

## PVS6 WiFi Hotspot Connection

### Finding the WiFi Network

The PVS6 broadcasts a temporary WiFi hotspot with credentials derived from its serial number.

#### SSID and Password Formula
For serial number format: `ZT123456789012345`

**SSID**: `SunPower` + last 5 digits = `SunPower12345`  
**Password**: First 3 digits + last 4 digits = `22371297`

#### Connection Commands
```bash
# Scan for PVS6 WiFi hotspot
sudo iwlist wlan0 scan | grep -i sunpower

# Connect using NetworkManager
sudo nmcli device wifi connect "SunPower12345" password "22371297"

# Verify connection
iwconfig
ip addr show wlan0
# Should show: inet 172.27.152.X/24

# Test PVS6 access
ping 172.27.152.1
curl "http://172.27.152.1/cgi-bin/dl_cgi?Command=DeviceList"
```

### Common WiFi Issues

#### Issue: WiFi Hotspot Disappears
**Symptoms**: SSID not found in scan results
**Cause**: PVS6 disables hotspot after period of inactivity
**Solution**:
```bash
# Reboot PVS6 to restore hotspot
# 1. Unplug PVS6 power for 30 seconds
# 2. Plug back in and wait 2-3 minutes
# 3. Scan again for WiFi network
sudo iwlist wlan0 scan | grep -i sunpower
```

#### Issue: 403 Forbidden Errors
**Symptoms**: HTTP 403 when accessing PVS6 API
**Cause**: PVS6 internal state issue
**Solution**:
```bash
# Full PVS6 reboot required
# 1. Unplug PVS6 power for 30 seconds
# 2. Wait 3-5 minutes for complete startup
# 3. Test API access again
curl "http://172.27.152.1/cgi-bin/dl_cgi?Command=DeviceList"
```

#### Issue: Connection Hangs During Setup
**Symptoms**: `nmcli` or `dhclient` commands freeze
**Cause**: WiFi driver conflicts or interface issues
**Solution**:
```bash
# Reset WiFi interface
sudo ip link set wlan0 down
sudo ip link set wlan0 up

# Clean up WiFi processes
sudo pkill -f wpa_supplicant
sudo rm -rf /var/run/wpa_supplicant/

# Restart connection
sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -D nl80211,wext
sudo dhclient wlan0
```

#### Issue: Weak Signal Strength
**Symptoms**: Frequent disconnections, slow responses
**Cause**: Distance from PVS6 or interference
**Solution**:
- Move Raspberry Pi closer to PVS6
- Use WiFi antenna extension if available
- Check for 5GHz interference from other devices

## PVS6 Ethernet BLUE Port Issues

### Issue: "Link Detected: No"
**Symptoms**: `ethtool eth0` shows "Link detected: no"
**Cause**: BLUE port disabled in PVS6 configuration
**Diagnosis**:
```bash
sudo ethtool eth0
# Look for: "Link detected: no"
```

**Solutions**:
1. **Try different cables**: Test with known-good Ethernet cable
2. **Check PVS6 ports**: Ensure using BLUE port, not WHITE port
3. **Power cycle PVS6**: Unplug for 30 seconds, wait 2-3 minutes
4. **Check PVS6 configuration**: May require installer access to enable BLUE port

### Issue: WHITE Port Powers Down PVS6
**Symptoms**: Green light on PVS6 goes out when cable connected to WHITE port
**Cause**: WHITE port is WAN/Internet, not for local connections
**Solution**: Always use BLUE port for local connections

### Issue: Static IP Configuration Conflicts
**Symptoms**: Network interface won't come up with static IP
**Solution**:
```bash
# Remove static IP configuration
sudo nano /etc/dhcpcd.conf
# Comment out or remove:
# interface eth0
# static ip_address=172.27.153.3/24
# nogateway

# Restart networking
sudo systemctl restart dhcpcd
```

## USB-to-Ethernet Adapter Solution

### When to Use
- BLUE port shows "Link detected: no"
- Ethernet connection unreliable
- Need dedicated PVS6 connection while maintaining WiFi

### Hardware Requirements
- USB 3.0 to Gigabit Ethernet adapter
- Compatible with Linux (most are)
- Examples: UGREEN, Cable Matters, Anker adapters

### Setup Process
```bash
# Connect USB adapter to Pi
# Adapter should appear as eth1 or similar

# Check new interface
ip addr show
# Look for new ethernet interface (eth1, enx*, etc.)

# Configure for PVS6 network
sudo ip addr add 172.27.153.3/24 dev eth1
sudo ip link set eth1 up

# Test connection
ping 172.27.153.1
```

### Benefits
- Bypasses problematic BLUE port
- Dedicated PVS6 connection
- Maintains WiFi for home network access
- More reliable than WiFi hotspot

## General PVS6 Behavior Notes

### Normal Behavior
- PVS6 WiFi hotspot appears for ~10-15 minutes after power-on
- API responses may be slow (2-5 seconds)
- Device list updates every 15-30 seconds
- Some 403 errors are normal during PVS6 startup

### IP Address Variations
- **WiFi hotspot**: Always 172.27.152.1
- **BLUE port**: Usually 172.27.153.1 (may vary)
- **Subnet**: /24 (255.255.255.0) for both networks

### Power and Connectivity
- PVS6 requires stable power connection
- Green LED should be solid (not blinking)
- WiFi hotspot only appears when PVS6 is fully operational
- BLUE port may be disabled by default in some configurations

## Testing and Verification

### Quick Connection Test
```bash
# Test basic connectivity
ping -c 3 172.27.152.1  # WiFi hotspot
ping -c 3 172.27.153.1  # BLUE port

# Test API access
curl -s "http://172.27.152.1/cgi-bin/dl_cgi?Command=DeviceList" | head -5
```

### Full System Test
```bash
# Comprehensive test script
#!/bin/bash
echo "=== PVS6 Connection Test ==="

# Test WiFi connection
if iwconfig wlan0 | grep -q "SunPower"; then
    echo "✓ Connected to PVS6 WiFi"
    PVS_IP="172.27.152.1"
else
    echo "✗ Not connected to PVS6 WiFi"
    PVS_IP="172.27.153.1"
fi

# Test ping
if ping -c 1 $PVS_IP > /dev/null 2>&1; then
    echo "✓ PVS6 ping successful ($PVS_IP)"
else
    echo "✗ PVS6 ping failed ($PVS_IP)"
    exit 1
fi

# Test API
if curl -s "http://$PVS_IP/cgi-bin/dl_cgi?Command=DeviceList" | grep -q "devices"; then
    echo "✓ PVS6 API accessible"
    DEVICE_COUNT=$(curl -s "http://$PVS_IP/cgi-bin/dl_cgi?Command=DeviceList" | grep -o '"SERIAL"' | wc -l)
    echo "✓ Found $DEVICE_COUNT devices"
else
    echo "✗ PVS6 API not accessible"
fi

echo "=== Test Complete ==="
```

## Emergency Recovery

### Complete Reset Procedure
If all connection methods fail:

1. **Power cycle everything**:
   - Unplug PVS6 for 60 seconds
   - Reboot Raspberry Pi
   - Wait 5 minutes for full startup

2. **Reset network configuration**:
   ```bash
   # Clear all network config
   sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
   sudo nano /etc/dhcpcd.conf  # Remove static IP config
   sudo reboot
   ```

3. **Start fresh**:
   - Reconfigure WiFi from scratch
   - Test each connection method individually
   - Document which method works for your setup

### Getting Help
- Check PVS6 serial number for correct WiFi credentials
- Verify PVS6 model (PVS5 vs PVS6 have different behaviors)
- Contact SunPower installer if BLUE port needs enabling
- Consider professional network troubleshooting if issues persist