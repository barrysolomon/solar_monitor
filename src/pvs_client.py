"""
PVS Gateway API client for reading solar data
"""
import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import config

class PVSClient:
    def __init__(self):
        self.base_url = config.PVS_BASE_URL
        self.session = requests.Session()
        self.session.timeout = 10
    
    def get_device_list(self) -> Optional[List[Dict]]:
        """
        Get the list of devices from the PVS gateway
        This is the main endpoint that returns all solar system data
        """
        try:
            url = f"{self.base_url}{config.DEVICE_LIST_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
            
            # The response is typically a JSON array of device objects
            data = response.json()
            return data if isinstance(data, list) else [data]
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching device list: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None
    
    def get_meter_data(self, device_id: str) -> Optional[Dict]:
        """
        Get detailed meter data for a specific device
        """
        try:
            url = f"{self.base_url}{config.METER_DATA_ENDPOINT}&DeviceID={device_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching meter data for device {device_id}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing meter data JSON: {e}")
            return None
    
    def parse_device_data(self, device: Dict) -> Dict:
        """
        Parse raw device data into standardized format
        """
        parsed = {
            'device_id': device.get('DeviceID', 'unknown'),
            'device_type': device.get('DeviceType', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'raw_data': device
        }
        
        # Extract power data (common fields across different device types)
        if 'p_3phsum_kw' in device:
            parsed['power_kw'] = float(device['p_3phsum_kw'])
        elif 'Power_kW' in device:
            parsed['power_kw'] = float(device['Power_kW'])
        elif 'kW' in device:
            parsed['power_kw'] = float(device['kW'])
        
        # Extract energy data
        if 'Energy_kWh' in device:
            parsed['energy_kwh'] = float(device['Energy_kWh'])
        elif 'kWh' in device:
            parsed['energy_kwh'] = float(device['kWh'])
        
        # Extract voltage data
        if 'Voltage_V' in device:
            parsed['voltage'] = float(device['Voltage_V'])
        elif 'Voltage' in device:
            parsed['voltage'] = float(device['Voltage'])
        
        # Extract current data
        if 'Current_A' in device:
            parsed['current'] = float(device['Current_A'])
        elif 'Current' in device:
            parsed['current'] = float(device['Current'])
        
        # Extract frequency data
        if 'Frequency_Hz' in device:
            parsed['frequency'] = float(device['Frequency_Hz'])
        elif 'Frequency' in device:
            parsed['frequency'] = float(device['Frequency'])
        
        return parsed
    
    def get_system_summary(self) -> Dict:
        """
        Get a summary of the entire solar system
        """
        devices = self.get_device_list()
        if not devices:
            return {
                'total_production_kw': 0,
                'total_consumption_kw': 0,
                'net_export_kw': 0,
                'system_online': False,
                'pvs_online': False,
                'device_count': 0,
                'timestamp': datetime.now().isoformat()
            }
        
        total_production = 0
        total_consumption = 0
        device_count = len(devices)
        
        for device in devices:
            device_type = device.get('DeviceType', '').lower()
            power = 0
            
            # Extract power value
            if 'p_3phsum_kw' in device:
                power = float(device['p_3phsum_kw'])
            elif 'Power_kW' in device:
                power = float(device['Power_kW'])
            elif 'kW' in device:
                power = float(device['kW'])
            
            # Categorize by device type
            if 'production' in device_type or 'pv' in device_type or 'inverter' in device_type:
                total_production += power
            elif 'consumption' in device_type or 'load' in device_type:
                total_consumption += power
        
        net_export = total_production - total_consumption
        
        return {
            'total_production_kw': total_production,
            'total_consumption_kw': total_consumption,
            'net_export_kw': net_export,
            'system_online': device_count > 0,
            'pvs_online': True,
            'device_count': device_count,
            'timestamp': datetime.now().isoformat()
        }
    
    def test_connection(self) -> bool:
        """
        Test if the PVS gateway is reachable
        """
        try:
            devices = self.get_device_list()
            return devices is not None and len(devices) > 0
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
