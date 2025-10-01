#!/usr/bin/env python3
"""
Solar Monitor Configuration Loader
Loads settings from .env file with fallbacks to defaults

Author: Barry Solomon
Email: barry@testingalchemy.com
Copyright (c) 2025 Barry Solomon
Licensed under the MIT License - see LICENSE file for details
"""

import os
from pathlib import Path

class Config:
    def __init__(self):
        self.load_env_file()
        
    def load_env_file(self):
        """Load environment variables from .env file"""
        env_file = Path('/opt/solar_monitor/.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    @property
    def pvs6_serial(self):
        return os.getenv('PVS6_SERIAL_NUMBER', 'YOUR_PVS6_SERIAL')
    
    @property
    def pvs6_wifi_ssid(self):
        return os.getenv('PVS6_WIFI_SSID', 'SunPower12345')
    
    @property
    def pvs6_wifi_password(self):
        return os.getenv('PVS6_WIFI_PASSWORD', 'YOUR_WIFI_PASSWORD')
    
    @property
    def pvs6_ip(self):
        return os.getenv('PVS6_IP_ADDRESS', '172.27.152.1')
    
    @property
    def database_path(self):
        return os.getenv('DATABASE_PATH', '/opt/solar_monitor/solar_data.db')
    
    @property
    def collector_interval(self):
        return int(os.getenv('COLLECTOR_INTERVAL', '60'))
    
    @property
    def system_timezone(self):
        return os.getenv('SYSTEM_TIMEZONE', 'America/Denver')
    
    @property
    def backup_path(self):
        return os.getenv('BACKUP_PATH', '/opt/solar_monitor/backups')
    
    @property
    def weather_api_key(self):
        return os.getenv('WEATHER_API_KEY', '')
    
    @property
    def weather_latitude(self):
        return os.getenv('WEATHER_LATITUDE', '39.7392')  # Default to Denver, CO
    
    @property
    def weather_longitude(self):
        return os.getenv('WEATHER_LONGITUDE', '-104.9903')  # Default to Denver, CO
    
    @property
    def weather_enabled(self):
        return os.getenv('WEATHER_ENABLED', 'true').lower() == 'true'

# Global config instance
config = Config()
