# Powerline Adapter Setup Guide

**Use existing electrical wiring to connect your PVS6 to your monitoring system**

This guide shows you how to use TP-Link Powerline adapters (like AV1000) to connect your SunPower PVS6 gateway without running new Ethernet cables.

## Why Use Powerline Adapters?

✅ **No new cables** - Uses existing electrical wiring  
✅ **Easy installation** - Just plug into wall outlets  
✅ **No drilling** - No holes in walls needed  
✅ **Flexible placement** - Any outlet near your equipment  
✅ **Fast speeds** - 1000Mbps+ with modern adapters  
✅ **Secure** - Encrypted communication over power lines  

## How Powerline Works

### **Basic Concept**
```
PVS6 → Ethernet → Powerline Adapter 1 → Electrical Wiring → Powerline Adapter 2 → Monitoring System
```

### **What Happens**
1. **Ethernet signal** from PVS6 goes into Powerline Adapter 1
2. **Signal converted** to electrical signal on power lines
3. **Signal travels** through your home's electrical wiring
4. **Signal received** by Powerline Adapter 2
5. **Signal converted** back to Ethernet for your monitoring system

## TP-Link AV1000 Setup

### **What You Have**
- **TP-Link AV1000** - 1000Mbps Powerline adapters
- **Gigabit Ethernet** - Fast enough for any solar data
- **Plug-and-play** - Easy setup and pairing

### **Specifications**
- **Speed**: Up to 1000Mbps
- **Range**: Up to 300 meters over electrical wiring
- **Ethernet**: Gigabit Ethernet ports
- **Security**: 128-bit AES encryption

## Setup Options

### **Option 1: Pi + Powerline (Recommended)**

#### Hardware Needed
- **TP-Link AV1000 adapters** - You already have these
- **Raspberry Pi 4** - $65
- **MicroSD card** - $10
- **Power supply** - $10
- **Case** - $10
- **Total: ~$95** (plus your existing Powerline adapters)

#### Setup Architecture
```
PVS6 (172.27.153.1) → Ethernet → AV1000 Adapter 1 → Electrical Wiring → AV1000 Adapter 2 → Pi → WiFi → Home Network
```

#### Advantages
- ✅ **Uses existing wiring** - No new cables needed
- ✅ **Fast connection** - 1000Mbps is more than enough
- ✅ **Network isolation** - Pi maintains security
- ✅ **Feature-rich** - Full monitoring capabilities
- ✅ **Reliable** - Direct Ethernet to Pi

#### Setup Steps
1. **Install Pi** near router (where AV1000 Adapter 2 is)
2. **Connect Pi** to AV1000 Adapter 2 via Ethernet
3. **Connect PVS6** to AV1000 Adapter 1 via Ethernet
4. **Configure Pi** as network bridge
5. **Access via WiFi** from home network

### **Option 2: Direct Router Connection**

#### Setup Architecture
```
PVS6 (172.27.153.1) → Ethernet → AV1000 Adapter 1 → Electrical Wiring → AV1000 Adapter 2 → Router → Home Network
```

#### Advantages
- ✅ **Simple setup** - Just connect and configure
- ✅ **Uses existing wiring** - No new cables
- ✅ **Fast connection** - 1000Mbps speed

#### Disadvantages
- ❌ **Network complexity** - Need to configure routing
- ❌ **Security concerns** - PVS6 exposed to home network
- ❌ **DHCP conflicts** - May cause network issues

## Physical Setup

### **Step 1: Locate Your PVS6**
1. **Find PVS6** - Usually near main electrical panel
2. **Identify BLUE Ethernet port** - Look for "LAN" or "Installer" port (BLUE color)
3. **Avoid WHITE port** - This is for internet/cloud connection only
4. **Note location** - For Powerline adapter placement

### **Step 2: Choose Powerline Locations**
1. **Near PVS6** - Plug AV1000 Adapter 1 into outlet
2. **Near monitoring system** - Plug AV1000 Adapter 2 into outlet
3. **Consider electrical circuits** - Same circuit = better performance

### **Step 3: Connect Devices**
1. **Connect PVS6 BLUE port** to AV1000 Adapter 1 via Ethernet
2. **Connect monitoring system** to AV1000 Adapter 2 via Ethernet
3. **Power on adapters** - Wait for LED indicators
4. **Important**: Use BLUE port, not WHITE port on PVS6

### **Step 4: Pair Adapters**
1. **Press pair button** on one adapter (usually for 2 seconds)
2. **Press pair button** on other adapter within 2 minutes
3. **Wait for pairing** - LEDs should show successful connection

## LED Status Guide

### **TP-Link AV1000 LEDs**
- **Power LED**: Solid = powered, Blinking = pairing
- **Ethernet LED**: Solid = connected, Off = no connection
- **Powerline LED**: Solid = paired, Blinking = searching
- **Status LED**: Green = good, Red = issues

### **Troubleshooting LEDs**
- **Red status LED**: Check electrical wiring, try different outlets
- **Blinking Powerline LED**: Adapters not paired, press pair buttons
- **No Ethernet LED**: Check Ethernet cable connections
- **No Power LED**: Check power outlet, adapter not plugged in

## Network Configuration

### **Option 1: Pi Bridge Configuration**

#### Pi Network Settings
```bash
# WiFi interface (connects to home network)
wlan0: 192.168.1.100 (assigned by router)

# Ethernet interface (connects to PVS6 via Powerline)
eth0: 172.27.153.3 (static IP in PVS6 network)
```

#### HAProxy Configuration
```bash
# Listen on all interfaces (WiFi)
frontend http-in
    bind *:80
    default_backend backend_servers

# Forward to PVS6 (via Powerline)
backend backend_servers
    server sv1 172.27.153.1:80
```

### **Option 2: Router Configuration**

#### Static Route Setup
```bash
# Add route to PVS6 network
sudo ip route add 172.27.153.0/24 via 192.168.1.1

# Or configure in router web interface
# Destination: 172.27.153.0/24
# Gateway: 192.168.1.1 (router IP)
```

#### Router Configuration Steps
1. **Access router** web interface (usually 192.168.1.1)
2. **Go to routing** or static routes section
3. **Add route** to 172.27.153.0/24 network
4. **Set gateway** to router's IP address
5. **Save configuration** and restart router

## Performance Optimization

### **Electrical Circuit Considerations**
- **Same circuit**: Best performance on same electrical circuit
- **Different circuits**: May work but slower speeds
- **Older wiring**: May affect performance
- **Power strips**: Avoid using power strips, plug directly into wall

### **Speed Expectations**
- **Theoretical**: Up to 1000Mbps
- **Real-world**: Usually 200-800Mbps depending on wiring
- **Solar data**: ~1-10KB per request (very small)
- **More than enough**: Solar monitoring uses <1% of capacity

### **Performance Tips**
- **Use same circuit** - Best performance on same electrical circuit
- **Avoid power strips** - Plug directly into wall outlets
- **Check wiring** - Older wiring may affect performance
- **Update firmware** - Keep adapters updated
- **Test different outlets** - Some outlets may work better

## Troubleshooting

### **Common Issues**

#### **Adapters Not Pairing**
- **Solution**: Press pair button on both adapters
- **Wait**: Allow 2 minutes for pairing process
- **Reset**: Unplug adapters for 30 seconds, then retry

#### **Slow Speeds**
- **Check wiring**: Older electrical wiring may affect performance
- **Try different outlets**: Some outlets may work better
- **Same circuit**: Best performance on same electrical circuit
- **Avoid interference**: Keep away from other electrical devices

#### **Connection Drops**
- **Check outlets**: Try different wall outlets
- **Electrical issues**: May indicate electrical wiring problems
- **Firmware**: Update adapter firmware if available
- **Reset**: Unplug adapters and retry pairing

#### **No Ethernet Connection**
- **Check port color**: Make sure you're using BLUE port on PVS6
- **Check cables**: Verify Ethernet cables are connected
- **LED indicators**: Check Ethernet LED status
- **Device power**: Ensure PVS6 and monitoring system are powered
- **Network settings**: Verify IP configuration (should be 172.27.153.x)

### **Advanced Troubleshooting**

#### **Test Powerline Connection**
```bash
# Test connection between adapters
ping 172.27.153.1

# Should work if Powerline adapters are paired correctly
```

#### **Check Network Routes**
```bash
# Check routing table
ip route show

# Should show route to 172.27.153.0/24 network
```

#### **Monitor Performance**
```bash
# Test speed between adapters
iperf3 -s  # On one side
iperf3 -c 172.27.153.1  # On other side
```

## Alternative Powerline Models

### **TP-Link Models**
- **TL-PA4010** - Basic 100Mbps
- **TL-PA7010** - 1000Mbps with passthrough
- **TL-PA8010** - 1000Mbps with WiFi
- **TL-PA9020** - 2000Mbps with passthrough

### **Other Brands**
- **Netgear Powerline** - Similar functionality
- **D-Link Powerline** - Alternative option
- **Linksys Powerline** - Another choice

### **Choosing Adapters**
- **Speed**: 1000Mbps+ recommended for future-proofing
- **Passthrough**: Don't lose power outlets
- **WiFi**: Some models include WiFi access point
- **Security**: Look for AES encryption

## Cost Comparison

### **Powerline vs. Ethernet Cable**
- **Powerline adapters**: $50-100 (one-time cost)
- **Ethernet cable**: $15-25 (one-time cost)
- **Installation**: Powerline = easy, Ethernet = may require drilling
- **Flexibility**: Powerline = any outlet, Ethernet = fixed location

### **Powerline vs. Raspberry Pi**
- **Powerline only**: $50-100
- **Pi + Powerline**: $145-195
- **Features**: Pi adds monitoring, storage, web dashboard
- **Complexity**: Pi adds setup complexity but more features

## Best Practices

### **Installation**
- **Plan placement** - Choose optimal outlet locations
- **Test performance** - Try different outlets before final placement
- **Document setup** - Note which outlets work best
- **Label connections** - Mark which adapter goes where

### **Maintenance**
- **Keep firmware updated** - Check for updates regularly
- **Monitor performance** - Watch for speed degradation
- **Clean connections** - Keep Ethernet ports clean
- **Check LEDs** - Monitor connection status

### **Security**
- **Use encryption** - Ensure adapters use AES encryption
- **Change passwords** - Set strong passwords if available
- **Monitor access** - Watch for unauthorized connections
- **Update regularly** - Keep firmware and software updated

## Integration with Other Systems

### **Home Assistant**
```yaml
# Use Powerline connection for HA integration
sensor:
  - platform: rest
    name: "Solar Power"
    resource: "http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList"
    value_template: "{{ value_json.p_3phsum_kw }}"
```

### **Grafana**
```yaml
# Prometheus configuration for Powerline setup
scrape_configs:
  - job_name: 'solar-powerline'
    static_configs:
      - targets: ['172.27.153.1:80']
    scrape_interval: 30s
```

### **MQTT**
```python
# MQTT publisher using Powerline connection
import paho.mqtt.client as mqtt
import requests

def publish_solar_data():
    # Get data from PVS6 via Powerline
    response = requests.get('http://172.27.153.1/cgi-bin/dl_cgi?Command=DeviceList')
    data = response.json()
    
    # Publish to MQTT
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.publish("solar/data", json.dumps(data))
    client.disconnect()
```

## Success Criteria

### **Connection Test**
- **Ping PVS6**: `ping 172.27.153.1` should work
- **LED status**: All LEDs should show green/good status
- **Speed test**: Should get 200Mbps+ in real-world conditions
- **Stability**: Connection should remain stable for hours

### **Performance Test**
- **Solar data access**: Should get data within 1-2 seconds
- **Dashboard loading**: Web dashboard should load quickly
- **Data collection**: Should collect data every 30 seconds reliably
- **No timeouts**: Should not experience connection timeouts

---

**Ready to set up Powerline adapters?** Choose your setup option and follow the step-by-step guide. Start with Option 1 (Pi + Powerline) for the best features and reliability!
