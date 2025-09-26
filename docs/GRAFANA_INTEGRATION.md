# Grafana Integration Guide

**Professional-grade solar monitoring with Grafana**

This guide shows you how to set up Grafana for advanced solar data visualization, alerting, and professional monitoring of your SunPower system.

## Why Use Grafana?

✅ **Professional Dashboards** - Industry-standard monitoring interface  
✅ **Advanced Charts** - Complex visualizations and analytics  
✅ **Real-time Alerts** - Get notified of issues immediately  
✅ **Historical Analysis** - Deep dive into your solar data  
✅ **Mobile Access** - Mobile-optimized dashboards  
✅ **Export Capabilities** - Share reports and data  
✅ **Scalable** - Handles years of data efficiently  

## Architecture Overview

```
SunPower PVS6 → Raspberry Pi → Prometheus → Grafana
```

- **PVS6**: Your solar system gateway
- **Raspberry Pi**: Runs solar monitor + Prometheus + Grafana
- **Prometheus**: Time-series database for metrics
- **Grafana**: Visualization and dashboard platform

## Prerequisites

- Raspberry Pi running your solar monitoring system
- Basic familiarity with Docker (optional)
- 2-4 hours for setup
- Additional 2GB RAM recommended for Pi

## Setup Methods

### Method 1: Docker Compose (Recommended)

#### Step 1: Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker pi

# Reboot to apply changes
sudo reboot
```

#### Step 2: Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false

  solar-exporter:
    image: python:3.9-slim
    container_name: solar-exporter
    volumes:
      - ./solar_exporter.py:/app/solar_exporter.py
      - ./requirements.txt:/app/requirements.txt
    working_dir: /app
    command: >
      sh -c "pip install -r requirements.txt && 
             python solar_exporter.py"
    ports:
      - "8000:8000"
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:
```

#### Step 3: Create Prometheus Configuration

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 30s
  evaluation_interval: 30s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'solar-exporter'
    static_configs:
      - targets: ['solar-exporter:8000']
    scrape_interval: 30s
    metrics_path: /metrics
```

#### Step 4: Create Solar Exporter

Create `solar_exporter.py`:

```python
#!/usr/bin/env python3
"""
Prometheus exporter for SunPower solar data
"""
import time
import requests
import json
from prometheus_client import start_http_server, Gauge, Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
solar_power = Gauge('solar_power_kw', 'Current solar power production in kW')
solar_energy_today = Gauge('solar_energy_today_kwh', 'Today\'s solar energy production in kWh')
solar_voltage = Gauge('solar_voltage_v', 'Solar system voltage in V')
solar_current = Gauge('solar_current_a', 'Solar system current in A')
solar_frequency = Gauge('solar_frequency_hz', 'Solar system frequency in Hz')
system_online = Gauge('system_online', 'Solar system online status (1=online, 0=offline)')

# Counters for tracking
data_collection_errors = Counter('data_collection_errors_total', 'Total data collection errors')

class SolarExporter:
    def __init__(self, solar_api_url="http://localhost:5000/api/current_status"):
        self.solar_api_url = solar_api_url
        
    def collect_data(self):
        """Collect data from solar monitoring system"""
        try:
            response = requests.get(self.solar_api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Update Prometheus metrics
            solar_power.set(data.get('total_production_kw', 0))
            solar_energy_today.set(data.get('today_energy_kwh', 0))
            solar_voltage.set(data.get('voltage', 0))
            solar_current.set(data.get('current', 0))
            solar_frequency.set(data.get('frequency', 0))
            system_online.set(1 if data.get('system_online', False) else 0)
            
            logger.info(f"Data collected: {data.get('total_production_kw', 0)}kW")
            
        except Exception as e:
            logger.error(f"Error collecting data: {e}")
            data_collection_errors.inc()
            
    def run(self):
        """Run the exporter"""
        logger.info("Starting Solar Prometheus Exporter")
        
        # Start Prometheus metrics server
        start_http_server(8000)
        
        # Collect data every 30 seconds
        while True:
            self.collect_data()
            time.sleep(30)

if __name__ == "__main__":
    exporter = SolarExporter()
    exporter.run()
```

#### Step 5: Create Requirements File

Create `requirements.txt`:

```
requests==2.31.0
prometheus_client==0.17.1
```

#### Step 6: Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Method 2: Manual Installation

#### Step 1: Install Prometheus

```bash
# Download Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-arm64.tar.gz
tar xvfz prometheus-2.45.0.linux-arm64.tar.gz
cd prometheus-2.45.0.linux-arm64

# Create systemd service
sudo nano /etc/systemd/system/prometheus.service
```

Add this content:

```ini
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=pi
ExecStart=/home/pi/prometheus-2.45.0.linux-arm64/prometheus --config.file=/home/pi/prometheus.yml --storage.tsdb.path=/home/pi/prometheus-data
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Step 2: Install Grafana

```bash
# Add Grafana repository
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Install Grafana
sudo apt update
sudo apt install grafana

# Enable and start Grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

## Grafana Dashboard Setup

### Step 1: Access Grafana

1. Open web browser
2. Go to `http://YOUR_PI_IP:3000`
3. Login with username: `admin`, password: `admin123`

### Step 2: Add Prometheus Data Source

1. Go to **Configuration** → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Set URL: `http://localhost:9090`
5. Click **Save & Test**

### Step 3: Create Solar Dashboard

#### Basic Dashboard

```json
{
  "dashboard": {
    "title": "Solar Monitoring Dashboard",
    "panels": [
      {
        "title": "Current Solar Power",
        "type": "gauge",
        "targets": [
          {
            "expr": "solar_power_kw",
            "legendFormat": "Power (kW)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "min": 0,
            "max": 10,
            "unit": "kW"
          }
        }
      },
      {
        "title": "Solar Production (24h)",
        "type": "graph",
        "targets": [
          {
            "expr": "solar_power_kw",
            "legendFormat": "Power (kW)"
          }
        ],
        "xAxis": {
          "mode": "time"
        },
        "yAxes": [
          {
            "label": "Power (kW)",
            "min": 0
          }
        ]
      }
    ]
  }
}
```

#### Advanced Dashboard

```json
{
  "dashboard": {
    "title": "Advanced Solar Monitoring",
    "panels": [
      {
        "title": "Power Production",
        "type": "stat",
        "targets": [
          {
            "expr": "solar_power_kw",
            "legendFormat": "Current Power"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "kW",
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 2},
                {"color": "green", "value": 5}
              ]
            }
          }
        }
      },
      {
        "title": "Daily Energy Production",
        "type": "bargauge",
        "targets": [
          {
            "expr": "solar_energy_today_kwh",
            "legendFormat": "Today's Energy"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "kWh"
          }
        }
      },
      {
        "title": "System Status",
        "type": "stat",
        "targets": [
          {
            "expr": "system_online",
            "legendFormat": "System Status"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "mappings": [
              {"type": "value", "value": "0", "text": "Offline"},
              {"type": "value", "value": "1", "text": "Online"}
            ],
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "green", "value": 1}
              ]
            }
          }
        }
      }
    ]
  }
}
```

## Alerting Setup

### Step 1: Create Alert Rules

Create `alert_rules.yml`:

```yaml
groups:
  - name: solar_alerts
    rules:
      - alert: SolarSystemOffline
        expr: system_online == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Solar system is offline"
          description: "Solar system has been offline for more than 5 minutes"
          
      - alert: LowSolarProduction
        expr: solar_power_kw < 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low solar production"
          description: "Solar production is below 1kW for more than 10 minutes"
          
      - alert: HighSolarProduction
        expr: solar_power_kw > 8
        for: 1m
        labels:
          severity: info
        annotations:
          summary: "High solar production"
          description: "Solar production is above 8kW"
```

### Step 2: Configure Alert Channels

1. Go to **Alerting** → **Notification channels**
2. Add email channel:
   - **Name**: Email Alerts
   - **Type**: Email
   - **Email addresses**: your-email@example.com
   - **Subject**: Solar Alert: {{ .GroupLabels.alertname }}

### Step 3: Test Alerts

```bash
# Test alert by stopping solar monitor
sudo systemctl stop solar-monitor

# Check Grafana alerts
# Go to Alerting → Alert Rules
```

## Mobile Access

### Step 1: Enable Mobile Access

1. Go to **Configuration** → **Preferences**
2. Enable **Mobile** access
3. Set **Mobile theme** to dark or light

### Step 2: Install Grafana Mobile App

- **iOS**: Download Grafana app from App Store
- **Android**: Download Grafana app from Google Play
- **Login** with your Grafana credentials
- **Access** your solar dashboard on mobile

## Advanced Features

### Data Export

```bash
# Export dashboard as JSON
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:3000/api/dashboards/db/solar-monitoring > solar_dashboard.json

# Export data as CSV
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "http://localhost:3000/api/datasources/proxy/1/api/v1/query_range?query=solar_power_kw&start=2023-01-01T00:00:00Z&end=2023-01-02T00:00:00Z&step=1h" > solar_data.csv
```

### Custom Queries

```promql
# Average power over last hour
avg_over_time(solar_power_kw[1h])

# Total energy today
sum(increase(solar_energy_today_kwh[1d]))

# System uptime percentage
avg_over_time(system_online[1d]) * 100
```

### Backup and Restore

```bash
# Backup Grafana data
sudo cp -r /var/lib/grafana /backup/grafana-$(date +%Y%m%d)

# Restore Grafana data
sudo cp -r /backup/grafana-20230101/* /var/lib/grafana/
sudo systemctl restart grafana-server
```

## Troubleshooting

### Common Issues

#### "Cannot connect to Prometheus"
- Check Prometheus is running: `docker-compose ps`
- Verify port 9090 is accessible
- Check Prometheus logs: `docker-compose logs prometheus`

#### "No data in Grafana"
- Verify data source connection
- Check Prometheus targets: `http://localhost:9090/targets`
- Verify solar exporter is running

#### "High memory usage"
- Reduce data retention: `--storage.tsdb.retention.time=7d`
- Increase Pi RAM or use swap file
- Consider data aggregation

### Performance Optimization

```yaml
# prometheus.yml optimization
global:
  scrape_interval: 60s  # Reduce frequency
  evaluation_interval: 60s

# Reduce retention
command:
  - '--storage.tsdb.retention.time=30d'  # 30 days instead of 200h
```

## Benefits of Grafana Integration

### Professional Monitoring
- **Industry-standard** monitoring interface
- **Advanced visualizations** and analytics
- **Real-time alerts** and notifications
- **Historical analysis** and trending

### Mobile Access
- **Mobile-optimized** dashboards
- **Push notifications** for alerts
- **Offline access** to cached data
- **Touch-optimized** interface

### Data Management
- **Efficient storage** with Prometheus
- **Data retention** policies
- **Export capabilities** for analysis
- **Backup and restore** functionality

---

**Next Steps**: Choose your setup method and follow the step-by-step guide. Start with Docker Compose for the easiest setup!
