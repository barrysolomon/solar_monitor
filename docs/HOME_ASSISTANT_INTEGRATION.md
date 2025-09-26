# Home Assistant Integration Guide

**Monitor your SunPower solar system in Home Assistant**

This guide shows you how to integrate your SunPower solar monitoring system with Home Assistant for advanced home automation and monitoring.

## Why Integrate with Home Assistant?

✅ **Unified Dashboard** - See solar data alongside other home devices  
✅ **Automation Possibilities** - Create automations based on solar production  
✅ **Mobile App** - Access solar data through Home Assistant mobile app  
✅ **Voice Control** - Ask Alexa/Google about your solar production  
✅ **Advanced Visualization** - Charts and graphs  
✅ **Alerts & Notifications** - Get notified of issues or achievements  

## Prerequisites

- Home Assistant installed and running
- SunPower monitoring system set up (this repository)
- Raspberry Pi running your solar monitor
- Both systems on the same network

## Integration Methods

### Method 1: REST API Integration (Recommended)

This method uses Home Assistant's REST sensor to read data from your solar monitoring system.

#### Step 1: Configure Home Assistant

Add this to your `configuration.yaml`:

```yaml
# SunPower Solar Monitoring Integration
sensor:
  - platform: rest
    name: "Solar Total Power"
    resource: "http://YOUR_PI_IP:5000/api/current_status"
    value_template: "{{ value_json.total_production_kw }}"
    unit_of_measurement: "kW"
    scan_interval: 30
    
  - platform: rest
    name: "Solar Today Energy"
    resource: "http://YOUR_PI_IP:5000/api/current_status"
    value_template: "{{ value_json.today_energy_kwh }}"
    unit_of_measurement: "kWh"
    scan_interval: 30
    
  - platform: rest
    name: "Solar System Status"
    resource: "http://YOUR_PI_IP:5000/api/current_status"
    value_template: "{{ value_json.system_online }}"
    scan_interval: 30

# Energy Dashboard Integration
energy:
  solar_production:
    - entity: sensor.solar_total_power
```

#### Step 2: Create Lovelace Dashboard

Create a new dashboard card:

```yaml
type: vertical-stack
cards:
  - type: gauge
    entity: sensor.solar_total_power
    name: Current Solar Production
    min: 0
    max: 10
    severity:
      green: 2
      yellow: 1
      red: 0
      
  - type: history-graph
    entities:
      - sensor.solar_total_power
    hours: 24
    title: Solar Production (24h)
    
  - type: entities
    entities:
      - sensor.solar_total_power
      - sensor.solar_today_energy
      - sensor.solar_system_status
    title: Solar System Status
```

### Method 2: MQTT Integration (Advanced)

For more advanced integration, you can publish solar data to MQTT.

#### Step 1: Install MQTT Broker

Add to your `configuration.yaml`:

```yaml
mqtt:
  broker: localhost
  port: 1883
  username: !secret mqtt_username
  password: !secret mqtt_password

# MQTT Sensors
sensor:
  - platform: mqtt
    name: "Solar Power MQTT"
    state_topic: "solar/power"
    unit_of_measurement: "kW"
    value_template: "{{ value_json.power }}"
    
  - platform: mqtt
    name: "Solar Energy MQTT"
    state_topic: "solar/energy"
    unit_of_measurement: "kWh"
    value_template: "{{ value_json.energy }}"
```

#### Step 2: Modify Solar Monitor

Add MQTT publishing to your solar monitor:

```python
# Add to requirements.txt
paho-mqtt==1.6.1

# Add to solar_monitor.py
import paho.mqtt.client as mqtt
import json

class MQTTPublisher:
    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker, port, 60)
        
    def publish_solar_data(self, data):
        # Publish power data
        power_data = {
            "power": data.get('total_production_kw', 0),
            "timestamp": data.get('timestamp')
        }
        self.client.publish("solar/power", json.dumps(power_data))
        
        # Publish energy data
        energy_data = {
            "energy": data.get('today_energy_kwh', 0),
            "timestamp": data.get('timestamp')
        }
        self.client.publish("solar/energy", json.dumps(energy_data))
```

### Method 3: Custom Component (Expert)

For the most advanced integration, create a custom Home Assistant component.

#### Step 1: Create Custom Component

Create directory structure:
```
custom_components/sunpower_local/
├── __init__.py
├── manifest.json
├── sensor.py
└── config_flow.py
```

#### Step 2: Component Files

**manifest.json**:
```json
{
  "domain": "sunpower_local",
  "name": "SunPower Local",
  "documentation": "https://github.com/your-repo/solar_monitor",
  "requirements": ["requests"],
  "dependencies": [],
  "codeowners": ["@your-username"]
}
```

**sensor.py**:
```python
import logging
import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class SunPowerLocalSensor(SensorEntity):
    def __init__(self, coordinator, name, key, unit):
        self.coordinator = coordinator
        self._name = name
        self._key = key
        self._unit = unit
        
    @property
    def name(self):
        return self._name
        
    @property
    def native_value(self):
        return self.coordinator.data.get(self._key, 0)
        
    @property
    def native_unit_of_measurement(self):
        return self._unit
```

## Automation Examples

### Example 1: Solar Production Alerts

```yaml
# automation.yaml
- alias: "Solar Production Alert"
  trigger:
    platform: numeric_state
    entity_id: sensor.solar_total_power
    above: 8
  action:
    - service: notify.mobile_app_your_phone
      data:
        title: "High Solar Production!"
        message: "Solar system producing {{ states('sensor.solar_total_power') }}kW"
```

### Example 2: Energy Usage Optimization

```yaml
- alias: "Optimize Energy Usage"
  trigger:
    platform: numeric_state
    entity_id: sensor.solar_total_power
    above: 5
  action:
    - service: switch.turn_on
      entity_id: switch.water_heater
    - service: switch.turn_on
      entity_id: switch.electric_vehicle_charger
```

### Example 3: System Health Monitoring

```yaml
- alias: "Solar System Offline Alert"
  trigger:
    platform: state
    entity_id: sensor.solar_system_status
    to: "off"
  action:
    - service: notify.mobile_app_your_phone
      data:
        title: "Solar System Offline!"
        message: "Check your solar monitoring system"
```

## Energy Dashboard Integration

### Configure Energy Dashboard

Add to your `configuration.yaml`:

```yaml
energy:
  solar_production:
    - entity: sensor.solar_total_power
      name: "Solar Production"
      
  grid_consumption:
    - entity: sensor.solar_total_power
      name: "Grid Consumption"
```

### Energy Dashboard Card

```yaml
type: energy-solar-graph
entities:
  - sensor.solar_total_power
```

## Advanced Features

### Historical Data

```yaml
# Add to configuration.yaml
recorder:
  include:
    entities:
      - sensor.solar_total_power
      - sensor.solar_today_energy
      - sensor.solar_system_status
```

### Custom Dashboard

Create a dedicated solar dashboard:

```yaml
# solar_dashboard.yaml
title: Solar Monitoring
path: solar
icon: mdi:solar-power
cards:
  - type: gauge
    entity: sensor.solar_total_power
    name: Current Production
    min: 0
    max: 10
    
  - type: history-graph
    entities:
      - sensor.solar_total_power
    hours: 24
    
  - type: statistics-graph
    entities:
      - sensor.solar_today_energy
    period: day
```

## Troubleshooting

### Common Issues

#### "Cannot connect to solar monitor"
- Check Pi IP address in configuration
- Verify solar monitor is running
- Test API endpoint: `http://YOUR_PI_IP:5000/api/current_status`

#### "No data showing"
- Check sensor configuration
- Verify API response format
- Check Home Assistant logs

#### "MQTT not working"
- Verify MQTT broker is running
- Check credentials in secrets.yaml
- Test MQTT connection

### Debug Steps

1. **Test API endpoint**:
   ```bash
   curl http://YOUR_PI_IP:5000/api/current_status
   ```

2. **Check Home Assistant logs**:
   ```bash
   tail -f /config/home-assistant.log
   ```

3. **Verify sensor states**:
   Go to Developer Tools > States and look for your sensors

## Benefits of Integration

### Unified Experience
- **Single dashboard** for all home devices
- **Consistent interface** across all platforms
- **Mobile app access** to solar data

### Automation Possibilities
- **Smart energy management** based on solar production
- **Automated alerts** for system issues
- **Voice control** through Alexa/Google

### Advanced Monitoring
- **Historical data** and trends
- **Energy dashboard** integration
- **Custom visualizations**

---

**Next Steps**: Choose your integration method and follow the step-by-step guide. Start with Method 1 (REST API) for the easiest setup!
