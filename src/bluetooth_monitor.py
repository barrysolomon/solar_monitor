#!/usr/bin/env python3
"""
Bluetooth Integration for SunPower Solar Monitoring System

This module provides Bluetooth Low Energy (BLE) connectivity for the solar monitoring system,
enabling direct mobile app connections, wireless sensor integration, and smart home automation.

Features:
- Direct mobile app connection via Bluetooth
- Wireless sensor data collection
- Smart home automation triggers
- Offline data synchronization
- Push notifications to mobile devices

Requirements:
- Raspberry Pi 4 with Bluetooth
- BlueZ Bluetooth stack
- Python bluetooth libraries

Author: Solar Monitor Project
License: MIT
"""

import json
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional, Callable
import sqlite3

try:
    import bluetooth
    from bluetooth import BluetoothSocket, RFCOMM
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False
    logging.warning("Bluetooth libraries not available. Install pybluez: pip install pybluez")

try:
    import dbus
    import dbus.mainloop.glib
    from gi.repository import GLib
    DBUS_AVAILABLE = True
except ImportError:
    DBUS_AVAILABLE = False
    logging.warning("DBus libraries not available. Install python3-dbus and python3-gi")

class BluetoothMonitor:
    """
    Bluetooth Low Energy monitor for solar data and sensor integration.
    
    Provides BLE services for:
    - Solar data broadcasting
    - Mobile app connectivity
    - Wireless sensor collection
    - Smart home automation
    """
    
    def __init__(self, database_path: str = "solar_data.db"):
        self.database_path = database_path
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.connected_devices = set()
        self.sensor_data = {}
        self.automation_callbacks = []
        
        # Bluetooth service UUIDs
        self.SOLAR_SERVICE_UUID = "12345678-1234-1234-1234-123456789abc"
        self.SENSOR_SERVICE_UUID = "12345678-1234-1234-1234-123456789abd"
        self.NOTIFICATION_SERVICE_UUID = "12345678-1234-1234-1234-123456789abe"
        
        # Characteristic UUIDs
        self.SOLAR_DATA_CHAR_UUID = "12345678-1234-1234-1234-123456789ac1"
        self.SENSOR_DATA_CHAR_UUID = "12345678-1234-1234-1234-123456789ac2"
        self.NOTIFICATION_CHAR_UUID = "12345678-1234-1234-1234-123456789ac3"
        
        if not BLUETOOTH_AVAILABLE:
            self.logger.error("Bluetooth libraries not available. Cannot start Bluetooth monitor.")
            return
            
        self._setup_bluetooth()
    
    def _setup_bluetooth(self):
        """Initialize Bluetooth adapter and services."""
        try:
            # Check if Bluetooth is available
            self.socket = BluetoothSocket(RFCOMM)
            self.logger.info("Bluetooth adapter initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Bluetooth: {e}")
            raise
    
    def start_service(self):
        """Start the Bluetooth monitoring service."""
        if not BLUETOOTH_AVAILABLE:
            self.logger.error("Cannot start Bluetooth service - libraries not available")
            return False
            
        self.is_running = True
        self.logger.info("Starting Bluetooth monitoring service...")
        
        # Start BLE advertising
        self._start_ble_advertising()
        
        # Start sensor monitoring
        self._start_sensor_monitoring()
        
        # Start automation engine
        self._start_automation_engine()
        
        self.logger.info("Bluetooth monitoring service started successfully")
        return True
    
    def stop_service(self):
        """Stop the Bluetooth monitoring service."""
        self.is_running = False
        self.logger.info("Stopping Bluetooth monitoring service...")
        
        # Disconnect all devices
        for device in list(self.connected_devices):
            self._disconnect_device(device)
        
        # Close Bluetooth socket
        try:
            self.socket.close()
        except:
            pass
        
        self.logger.info("Bluetooth monitoring service stopped")
    
    def _start_ble_advertising(self):
        """Start BLE advertising for mobile app discovery."""
        def advertise():
            while self.is_running:
                try:
                    # Advertise solar monitoring service
                    self._advertise_service()
                    time.sleep(1)
                except Exception as e:
                    self.logger.error(f"BLE advertising error: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=advertise, daemon=True)
        thread.start()
    
    def _advertise_service(self):
        """Advertise the solar monitoring BLE service."""
        # This would use BlueZ D-Bus API to advertise services
        # Implementation depends on BlueZ version and system configuration
        pass
    
    def _start_sensor_monitoring(self):
        """Start monitoring Bluetooth sensors."""
        def monitor_sensors():
            while self.is_running:
                try:
                    # Scan for Bluetooth sensors
                    self._scan_bluetooth_sensors()
                    time.sleep(30)  # Scan every 30 seconds
                except Exception as e:
                    self.logger.error(f"Sensor monitoring error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=monitor_sensors, daemon=True)
        thread.start()
    
    def _scan_bluetooth_sensors(self):
        """Scan for and connect to Bluetooth sensors."""
        try:
            # Scan for nearby Bluetooth devices
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            
            for addr, name in nearby_devices:
                if self._is_sensor_device(name):
                    self._connect_sensor(addr, name)
                    
        except Exception as e:
            self.logger.error(f"Bluetooth sensor scan error: {e}")
    
    def _is_sensor_device(self, name: str) -> bool:
        """Check if a Bluetooth device is a sensor we want to monitor."""
        sensor_keywords = [
            "temperature", "weather", "humidity", "pressure",
            "sensor", "monitor", "meter", "gauge"
        ]
        
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in sensor_keywords)
    
    def _connect_sensor(self, address: str, name: str):
        """Connect to a Bluetooth sensor and start data collection."""
        try:
            # Connect to sensor
            sensor_socket = BluetoothSocket(RFCOMM)
            sensor_socket.connect((address, 1))
            
            # Start data collection thread
            def collect_data():
                while self.is_running:
                    try:
                        data = sensor_socket.recv(1024)
                        if data:
                            self._process_sensor_data(address, name, data)
                    except Exception as e:
                        self.logger.error(f"Sensor data collection error: {e}")
                        break
                
                sensor_socket.close()
            
            thread = threading.Thread(target=collect_data, daemon=True)
            thread.start()
            
            self.logger.info(f"Connected to sensor: {name} ({address})")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to sensor {name}: {e}")
    
    def _process_sensor_data(self, address: str, name: str, data: bytes):
        """Process data received from Bluetooth sensors."""
        try:
            # Parse sensor data (format depends on sensor type)
            sensor_data = self._parse_sensor_data(data)
            
            # Store in database
            self._store_sensor_data(address, name, sensor_data)
            
            # Update sensor data cache
            self.sensor_data[f"{address}_{name}"] = {
                "timestamp": datetime.now().isoformat(),
                "data": sensor_data
            }
            
            # Trigger automations
            self._trigger_automations("sensor_data", sensor_data)
            
        except Exception as e:
            self.logger.error(f"Sensor data processing error: {e}")
    
    def _parse_sensor_data(self, data: bytes) -> Dict:
        """Parse sensor data based on sensor type."""
        # This would parse different sensor data formats
        # For now, return a generic structure
        return {
            "raw_data": data.hex(),
            "timestamp": datetime.now().isoformat(),
            "parsed": True
        }
    
    def _store_sensor_data(self, address: str, name: str, data: Dict):
        """Store sensor data in the database."""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bluetooth_sensors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT,
                    name TEXT,
                    data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                INSERT INTO bluetooth_sensors (address, name, data)
                VALUES (?, ?, ?)
            """, (address, name, json.dumps(data)))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Database storage error: {e}")
    
    def _start_automation_engine(self):
        """Start the smart home automation engine."""
        def automation_loop():
            while self.is_running:
                try:
                    # Check for automation triggers
                    self._check_automation_triggers()
                    time.sleep(5)  # Check every 5 seconds
                except Exception as e:
                    self.logger.error(f"Automation engine error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=automation_loop, daemon=True)
        thread.start()
    
    def _check_automation_triggers(self):
        """Check for conditions that trigger smart home automations."""
        try:
            # Get latest solar data
            solar_data = self._get_latest_solar_data()
            
            if solar_data:
                # Check automation conditions
                self._trigger_automations("solar_data", solar_data)
                
        except Exception as e:
            self.logger.error(f"Automation trigger check error: {e}")
    
    def _get_latest_solar_data(self) -> Optional[Dict]:
        """Get the latest solar production data."""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM solar_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "timestamp": row[1],
                    "production": row[2],
                    "consumption": row[3],
                    "net": row[4]
                }
            
        except Exception as e:
            self.logger.error(f"Solar data retrieval error: {e}")
        
        return None
    
    def _trigger_automations(self, trigger_type: str, data: Dict):
        """Trigger smart home automations based on solar data or sensor data."""
        for callback in self.automation_callbacks:
            try:
                callback(trigger_type, data)
            except Exception as e:
                self.logger.error(f"Automation callback error: {e}")
    
    def add_automation_callback(self, callback: Callable):
        """Add a callback function for automation triggers."""
        self.automation_callbacks.append(callback)
    
    def send_notification(self, message: str, device_address: Optional[str] = None):
        """Send a push notification to connected mobile devices."""
        try:
            notification_data = {
                "type": "notification",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            if device_address:
                # Send to specific device
                self._send_to_device(device_address, notification_data)
            else:
                # Send to all connected devices
                for address in self.connected_devices:
                    self._send_to_device(address, notification_data)
                    
        except Exception as e:
            self.logger.error(f"Notification sending error: {e}")
    
    def _send_to_device(self, address: str, data: Dict):
        """Send data to a specific Bluetooth device."""
        try:
            # This would send data via BLE characteristic
            # Implementation depends on the mobile app's BLE service
            pass
        except Exception as e:
            self.logger.error(f"Device communication error: {e}")
    
    def get_sensor_data(self) -> Dict:
        """Get current sensor data."""
        return self.sensor_data.copy()
    
    def get_connected_devices(self) -> List[str]:
        """Get list of connected device addresses."""
        return list(self.connected_devices)
    
    def is_bluetooth_available(self) -> bool:
        """Check if Bluetooth is available on this system."""
        return BLUETOOTH_AVAILABLE


def create_bluetooth_automation_examples():
    """Create example automation functions for smart home integration."""
    
    def high_production_automation(trigger_type: str, data: Dict):
        """Example: Turn on AC when solar production is high."""
        if trigger_type == "solar_data" and data.get("production", 0) > 5000:  # 5kW+
            print("High solar production detected - turning on AC")
            # This would integrate with smart home systems
            # e.g., Home Assistant, OpenHAB, etc.
    
    def low_production_automation(trigger_type: str, data: Dict):
        """Example: Turn off non-essential devices when production is low."""
        if trigger_type == "solar_data" and data.get("production", 0) < 1000:  # <1kW
            print("Low solar production detected - turning off non-essential devices")
            # Smart home automation code here
    
    def temperature_automation(trigger_type: str, data: Dict):
        """Example: Adjust fan speed based on panel temperature."""
        if trigger_type == "sensor_data" and "temperature" in data.get("data", {}):
            temp = data["data"]["temperature"]
            if temp > 80:  # 80°F
                print("High panel temperature detected - increasing fan speed")
                # Fan control automation here
    
    return [
        high_production_automation,
        low_production_automation,
        temperature_automation
    ]


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create Bluetooth monitor
    bt_monitor = BluetoothMonitor()
    
    if bt_monitor.is_bluetooth_available():
        # Add automation examples
        for automation in create_bluetooth_automation_examples():
            bt_monitor.add_automation_callback(automation)
        
        # Start the service
        if bt_monitor.start_service():
            try:
                print("Bluetooth monitoring service running...")
                print("Press Ctrl+C to stop")
                
                while True:
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\nStopping Bluetooth service...")
                bt_monitor.stop_service()
        else:
            print("Failed to start Bluetooth service")
    else:
        print("Bluetooth not available on this system")
