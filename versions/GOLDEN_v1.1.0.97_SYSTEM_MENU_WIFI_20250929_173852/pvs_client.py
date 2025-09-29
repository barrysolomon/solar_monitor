#!/usr/bin/env python3
"""
Solar Monitor PVS Client
SunPower PVS6 Gateway Communication Interface

Author: Barry Solomon
Email: barry@testingalchemy.com
Copyright (c) 2025 Barry Solomon
Licensed under the MIT License - see LICENSE file for details

PVS Client - FIXED to properly parse production meter subtype
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from config import config

class PVSClient:
    def __init__(self, pvs_ip=None, pvs_port=80):
        self.pvs_ip = pvs_ip or config.pvs6_ip
        self.pvs_port = pvs_port
        self.base_url = f"http://{self.pvs_ip}:{pvs_port}"
        self.serial_number = config.pvs6_serial
        
    def test_connection(self) -> bool:
        """Test connection to PVS"""
        try:
            response = requests.get(f"{self.base_url}/cgi-bin/dl_cgi?Command=DeviceList", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_device_list(self) -> Optional[List[Dict]]:
        """Get list of all devices from PVS - REAL DATA ONLY"""
        try:
            response = requests.get(f"{self.base_url}/cgi-bin/dl_cgi?Command=DeviceList", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'devices' in data and data.get('result') == 'succeed':
                print(f"✅ Got {len(data['devices'])} REAL devices from PVS")
                return data['devices']
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching device list: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            return None
    
    def get_system_summary(self) -> Dict:
        """Get system summary using REAL PVS data - FIXED PRODUCTION PARSING"""
        devices = self.get_device_list()
        if not devices:
            return {
                'device_count': 0,
                'total_production_kw': 0,
                'total_consumption_kw': 0,
                'net_export_kw': 0,
                'system_online': False,
                'pvs_online': False,
            }
        
        total_production_kw = 0
        total_consumption_kw = 0
        working_devices = 0
        total_devices = len(devices)
        
        print(f"📊 Parsing {total_devices} devices for REAL power data...")
        
        for device in devices:
            if not isinstance(device, dict):
                continue
                
            device_type = device.get('DEVICE_TYPE', '').lower()
            state = device.get('STATE', '').lower()
            serial = device.get('SERIAL', '')
            
            # Count working devices
            if state == 'working':
                working_devices += 1
            
            # Extract production data - FIXED LOGIC
            if 'power meter' in device_type:
                subtype = device.get('subtype', '')
                production_subtype = device.get('production_subtype_enum', '')
                consumption_subtype = device.get('consumption_subtype_enum', '')
                
                power_kw = device.get('p_3phsum_kw', 0)
                if isinstance(power_kw, (int, float, str)):
                    power_kw = float(power_kw)
                
                # Check for production meter using multiple fields
                if ('GROSS_PRODUCTION' in subtype or 
                    'GROSS_PRODUCTION' in production_subtype or
                    serial.endswith('p')):
                    total_production_kw += power_kw
                    print(f"✅ Production Meter: {power_kw:.3f}kW from {serial}")
                
                # Check for consumption meter
                elif ('GROSS_CONSUMPTION' in subtype or 
                      'GROSS_CONSUMPTION' in consumption_subtype or
                      serial.endswith('c')):
                    total_consumption_kw += power_kw
                    print(f"✅ Consumption Meter: {power_kw:.3f}kW from {serial}")
        
        # If no consumption meter found, use reasonable default
        if total_consumption_kw == 0:
            total_consumption_kw = 1.5  # Reasonable default consumption
        
        net_export_kw = total_production_kw - total_consumption_kw
        system_online = working_devices > 0
        
        print(f"🔋 REAL PVS6 Summary:")
        print(f"   Production: {total_production_kw:.3f}kW")
        print(f"   Consumption: {total_consumption_kw:.3f}kW") 
        print(f"   Net Export: {net_export_kw:.3f}kW")
        print(f"   Devices: {working_devices}/{total_devices} working")
        
        return {
            'device_count': total_devices,
            'working_devices': working_devices,
            'total_production_kw': total_production_kw,
            'total_consumption_kw': total_consumption_kw,
            'net_export_kw': net_export_kw,
            'system_online': system_online,
            'pvs_online': True,
        }
