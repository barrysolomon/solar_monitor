# Bluetooth Integration Setup Guide

## 🔵 Overview

This guide covers setting up Bluetooth Low Energy (BLE) features for your SunPower solar monitoring system. Bluetooth enables direct mobile app connections, wireless sensor integration, and smart home automation.

## 🎯 Bluetooth Features

### **Core Capabilities**
- **Direct Mobile Connection**: Connect to Pi via Bluetooth without WiFi
- **Offline Data Sync**: Collect data when internet is down
- **Wireless Sensors**: Integrate Bluetooth temperature and weather sensors
- **Smart Home Automation**: Control devices based on solar production
- **Push Notifications**: Real-time alerts sent directly to your phone
- **Data Backup**: Wireless backup of monitoring data
- **Peer-to-Peer Sharing**: Share data between multiple Pi units

### **Use Cases**
- **Mobile App**: Direct connection to Pi without WiFi dependency
- **Weather Integration**: Bluetooth weather stations for accurate forecasting
- **Panel Monitoring**: Temperature sensors for panel health
- **Smart Home**: Automate devices based on solar production
- **Backup Systems**: Wireless data backup and synchronization

## 🛠️ Hardware Requirements

### **Required**
- **Raspberry Pi 4** (any RAM size) - Built-in Bluetooth
- **Bluetooth-enabled mobile device** (phone/tablet)
- **MicroSD card** (32GB+ recommended)

### **Optional Sensors**
- **Bluetooth Temperature Sensors** - Panel temperature monitoring
- **Weather Stations** - Accurate production forecasting
- **Humidity Sensors** - Environmental monitoring
- **Power Quality Meters** - Advanced electrical monitoring

## 📱 Software Setup

### **Step 1: Enable Bluetooth on Pi**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Bluetooth packages
sudo apt install -y bluez bluez-tools bluetooth

# Enable Bluetooth service
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Check Bluetooth status
sudo systemctl status bluetooth
```

### **Step 2: Install Python Bluetooth Libraries**

```bash
# Install Python Bluetooth libraries
sudo apt install -y python3-bluez python3-dbus python3-gi

# Install additional Python packages
pip3 install pybluez dbus-python
```

### **Step 3: Configure Bluetooth**

```bash
# Edit Bluetooth configuration
sudo nano /etc/bluetooth/main.conf

# Add these lines:
[General]
DiscoverableTimeout = 0
PairableTimeout = 0
```

### **Step 4: Set Up Bluetooth Services**

```bash
# Create Bluetooth service directory
sudo mkdir -p /etc/bluetooth/services

# Create solar monitoring service
sudo nano /etc/bluetooth/services/solar_monitor.service
```

**Service Configuration:**
```ini
[Service]
Name=Solar Monitor
UUID=12345678-1234-1234-1234-123456789abc
Type=primary
```

### **Step 5: Install Bluetooth Monitor**

```bash
# Copy Bluetooth monitor script
sudo cp bluetooth_monitor.py /opt/solar_monitor/
sudo chmod +x /opt/solar_monitor/bluetooth_monitor.py

# Create systemd service
sudo nano /etc/systemd/system/bluetooth-monitor.service
```

**Systemd Service:**
```ini
[Unit]
Description=Bluetooth Solar Monitor
After=bluetooth.service
Requires=bluetooth.service

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/solar_monitor
ExecStart=/usr/bin/python3 /opt/solar_monitor/bluetooth_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **Step 6: Enable and Start Service**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable Bluetooth monitor service
sudo systemctl enable bluetooth-monitor

# Start the service
sudo systemctl start bluetooth-monitor

# Check status
sudo systemctl status bluetooth-monitor
```

## 📱 Mobile App Integration

### **Android App Setup**

1. **Enable Bluetooth** on your Android device
2. **Install BLE Scanner** app from Play Store
3. **Scan for devices** - Look for "Solar Monitor"
4. **Connect** to the Pi's Bluetooth service
5. **Configure** data collection settings

### **iOS App Setup**

1. **Enable Bluetooth** on your iPhone/iPad
2. **Install LightBlue Explorer** from App Store
3. **Scan for devices** - Look for "Solar Monitor"
4. **Connect** to the Pi's Bluetooth service
5. **Configure** data collection settings

### **Custom Mobile App**

For a custom mobile app, you'll need to implement BLE client functionality:

```python
# Example BLE client code for mobile app
import asyncio
from bleak import BleakClient

async def connect_to_solar_monitor():
    # Scan for solar monitor device
    devices = await BleakScanner.discover()
    solar_device = None
    
    for device in devices:
        if "Solar Monitor" in device.name:
            solar_device = device
            break
    
    if solar_device:
        # Connect to device
        async with BleakClient(solar_device.address) as client:
            # Subscribe to solar data characteristic
            await client.start_notify(
                "12345678-1234-1234-1234-123456789ac1",
                notification_handler
            )
            
            # Keep connection alive
            while True:
                await asyncio.sleep(1)

def notification_handler(sender, data):
    # Process solar data from Pi
    print(f"Received solar data: {data}")
```

## 🌡️ Sensor Integration

### **Temperature Sensors**

**Recommended Sensors:**
- **Bluetooth Thermometers** - $15-25
- **Weather Stations** - $30-50
- **Industrial Sensors** - $50-100

**Setup:**
1. **Pair sensor** with Pi via Bluetooth
2. **Configure data collection** in bluetooth_monitor.py
3. **Set up automation** based on temperature data

### **Weather Stations**

**Features:**
- **Temperature monitoring** for panel efficiency
- **Humidity tracking** for environmental conditions
- **Pressure monitoring** for weather forecasting
- **Wind speed** for safety monitoring

**Integration:**
```python
# Example weather sensor integration
def process_weather_data(sensor_data):
    temp = sensor_data.get("temperature", 0)
    humidity = sensor_data.get("humidity", 0)
    pressure = sensor_data.get("pressure", 0)
    
    # Adjust solar production forecast
    forecast = calculate_production_forecast(temp, humidity, pressure)
    
    # Store in database
    store_weather_data(sensor_data, forecast)
```

## 🏠 Smart Home Automation

### **Home Assistant Integration**

**Configuration:**
```yaml
# configuration.yaml
bluetooth:
  - mac_address: "AA:BB:CC:DD:EE:FF"  # Pi's Bluetooth MAC
    name: "Solar Monitor Pi"

automation:
  - alias: "High Solar Production"
    trigger:
      platform: bluetooth
      mac_address: "AA:BB:CC:DD:EE:FF"
      characteristic: "12345678-1234-1234-1234-123456789ac1"
    condition:
      condition: template
      value_template: "{{ trigger.payload.production > 5000 }}"
    action:
      - service: climate.set_temperature
        entity_id: climate.living_room
        data:
          temperature: 72
```

### **OpenHAB Integration**

**Items:**
```java
// solar_monitor.items
Group SolarMonitor
Number SolarProduction "Solar Production [%.1f W]" <sun> (SolarMonitor)
Number SolarConsumption "Solar Consumption [%.1f W]" <power> (SolarMonitor)
Number SolarNet "Net Power [%.1f W]" <power> (SolarMonitor)
```

**Rules:**
```java
// solar_monitor.rules
rule "High Solar Production"
when
    Item SolarProduction changed
then
    if (SolarProduction.state > 5000) {
        // Turn on AC
        sendCommand(AC_Power, ON)
        logInfo("Solar", "High production - AC turned on")
    }
end
```

## 🔧 Troubleshooting

### **Common Issues**

#### **Bluetooth Not Working**
```bash
# Check Bluetooth status
sudo systemctl status bluetooth

# Restart Bluetooth service
sudo systemctl restart bluetooth

# Check Bluetooth adapter
hciconfig
```

#### **Device Not Discoverable**
```bash
# Make Pi discoverable
sudo hciconfig hci0 piscan

# Check discoverable status
hciconfig hci0
```

#### **Connection Issues**
```bash
# Check paired devices
bluetoothctl
> paired-devices

# Remove and re-pair device
> remove AA:BB:CC:DD:EE:FF
> pair AA:BB:CC:DD:EE:FF
```

#### **Service Not Starting**
```bash
# Check service logs
sudo journalctl -u bluetooth-monitor -f

# Check Python dependencies
pip3 list | grep -E "(bluetooth|dbus|gi)"
```

### **Performance Optimization**

#### **Bluetooth Range**
- **Indoor range**: 10-30 meters
- **Outdoor range**: 30-100 meters
- **Obstacles**: Walls reduce range significantly
- **Interference**: WiFi, microwaves can affect performance

#### **Battery Life**
- **BLE sensors**: 6-12 months on coin cell
- **Pi power**: Minimal impact on Pi power consumption
- **Mobile devices**: BLE uses less battery than WiFi

## 📊 Monitoring and Logs

### **Service Monitoring**
```bash
# Check service status
sudo systemctl status bluetooth-monitor

# View logs
sudo journalctl -u bluetooth-monitor -f

# Check Bluetooth connections
bluetoothctl
> info AA:BB:CC:DD:EE:FF
```

### **Database Queries**
```sql
-- View Bluetooth sensor data
SELECT * FROM bluetooth_sensors 
ORDER BY timestamp DESC 
LIMIT 10;

-- View automation triggers
SELECT * FROM automation_logs 
WHERE trigger_type = 'bluetooth'
ORDER BY timestamp DESC;
```

## 🚀 Advanced Features

### **Multi-Pi Network**
- **Mesh networking** between multiple Pi units
- **Data synchronization** across locations
- **Load balancing** for large installations
- **Redundancy** for critical monitoring

### **Professional Integration**
- **Modbus over Bluetooth** for industrial sensors
- **MQTT over Bluetooth** for IoT integration
- **REST API** over Bluetooth for custom applications
- **WebSocket** over Bluetooth for real-time data

### **Security Considerations**
- **Encryption** for sensitive data transmission
- **Authentication** for device connections
- **Access control** for different user levels
- **Audit logging** for security monitoring

## 📚 Additional Resources

### **Documentation**
- [BlueZ Bluetooth Stack](http://www.bluez.org/)
- [Python Bluetooth Programming](https://pybluez.readthedocs.io/)
- [BLE Development Guide](https://developer.bluetooth.org/)

### **Community Projects**
- [Home Assistant Bluetooth](https://www.home-assistant.io/integrations/bluetooth/)
- [OpenHAB Bluetooth Binding](https://www.openhab.org/addons/bindings/bluetooth/)
- [ESP32 Bluetooth Projects](https://github.com/espressif/esp-idf)

### **Hardware Recommendations**
- **Bluetooth Sensors**: [Adafruit](https://www.adafruit.com/), [SparkFun](https://www.sparkfun.com/)
- **Weather Stations**: [Ambient Weather](https://ambientweather.com/), [AcuRite](https://www.acurite.com/)
- **Industrial Sensors**: [Honeywell](https://sensing.honeywell.com/), [Sensirion](https://sensirion.com/)

---

**Note**: Bluetooth integration requires a Raspberry Pi 4 or newer. Older Pi models don't have built-in Bluetooth support.
