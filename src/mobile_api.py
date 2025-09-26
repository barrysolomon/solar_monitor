#!/usr/bin/env python3
"""
Mobile API Extensions for Solar Monitoring System

This module provides REST API endpoints specifically designed for mobile app integration,
including real-time data, historical charts, and Bluetooth Low Energy services.

Features:
- REST API endpoints for mobile app
- Bluetooth Low Energy service
- Real-time data streaming
- Historical data queries
- Push notification support
- Device management

Author: Solar Monitor Project
License: MIT
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import sqlite3
import threading
import queue

# Import existing modules
from pvs_client import PVSClient
from database import SolarDatabase
from version import get_version_string, get_full_version_info

class MobileAPI:
    """
    Mobile API service for solar monitoring system.
    
    Provides REST endpoints and Bluetooth Low Energy services
    specifically designed for mobile app integration.
    """
    
    def __init__(self, database_path: str = "solar_data.db"):
        self.database_path = database_path
        self.logger = logging.getLogger(__name__)
        self.pvs_client = PVSClient()
        self.db = SolarDatabase(database_path)
        
        # Mobile app configuration
        self.mobile_config = {
            'refresh_interval': 30,  # seconds
            'max_history_days': 365,
            'enable_bluetooth': True,
            'enable_notifications': True
        }
        
        # Data cache for mobile app
        self.data_cache = {
            'dashboard': {},
            'last_update': None,
            'cache_ttl': 30  # seconds
        }
        
        # Notification queue for mobile apps
        self.notification_queue = queue.Queue()
        
        # Bluetooth service (if available)
        self.ble_service = None
        self._setup_bluetooth()
    
    def _setup_bluetooth(self):
        """Initialize Bluetooth Low Energy service for mobile app."""
        try:
            from bluetooth_monitor import BluetoothMonitor
            self.ble_service = BluetoothMonitor(self.database_path)
            self.logger.info("Bluetooth service initialized for mobile app")
        except ImportError:
            self.logger.warning("Bluetooth libraries not available")
            self.ble_service = None
    
    def start_service(self):
        """Start the mobile API service."""
        self.logger.info("Starting mobile API service...")
        
        # Start Bluetooth service if available
        if self.ble_service:
            self.ble_service.start_service()
        
        # Start data refresh thread
        self._start_data_refresh()
        
        self.logger.info("Mobile API service started successfully")
    
    def stop_service(self):
        """Stop the mobile API service."""
        self.logger.info("Stopping mobile API service...")
        
        if self.ble_service:
            self.ble_service.stop_service()
        
        self.logger.info("Mobile API service stopped")
    
    def _start_data_refresh(self):
        """Start background thread for data refresh."""
        def refresh_data():
            while True:
                try:
                    self._refresh_dashboard_data()
                    time.sleep(self.mobile_config['refresh_interval'])
                except Exception as e:
                    self.logger.error(f"Data refresh error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=refresh_data, daemon=True)
        thread.start()
    
    def _refresh_dashboard_data(self):
        """Refresh dashboard data cache."""
        try:
            # Get current solar data
            current_data = self._get_current_solar_data()
            
            # Update cache
            self.data_cache['dashboard'] = current_data
            self.data_cache['last_update'] = datetime.now().isoformat()
            
            # Send to Bluetooth if connected
            if self.ble_service:
                self.ble_service.send_notification(
                    f"Solar Update: {current_data.get('production', 0):.1f}kW"
                )
            
        except Exception as e:
            self.logger.error(f"Dashboard data refresh error: {e}")
    
    def _get_current_solar_data(self) -> Dict:
        """Get current solar production data."""
        try:
            # Get latest data from database
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT production_kw, consumption_kw, net_power_kw, timestamp
                FROM solar_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                production, consumption, net_power, timestamp = row
                return {
                    'production': production or 0,
                    'consumption': consumption or 0,
                    'net_power': net_power or 0,
                    'timestamp': timestamp,
                    'status': 'online'
                }
            else:
                return {
                    'production': 0,
                    'consumption': 0,
                    'net_power': 0,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'no_data'
                }
                
        except Exception as e:
            self.logger.error(f"Error getting current solar data: {e}")
            return {
                'production': 0,
                'consumption': 0,
                'net_power': 0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
    
    def get_dashboard_data(self) -> Dict:
        """Get dashboard data for mobile app."""
        try:
            # Check cache first
            if (self.data_cache['last_update'] and 
                (datetime.now() - datetime.fromisoformat(self.data_cache['last_update'])).seconds < self.data_cache['cache_ttl']):
                return self.data_cache['dashboard']
            
            # Refresh data if cache is stale
            self._refresh_dashboard_data()
            return self.data_cache['dashboard']
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {
                'production': 0,
                'consumption': 0,
                'net_power': 0,
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
    
    def get_historical_data(self, start_date: str, end_date: str, interval: str = 'hour') -> List[Dict]:
        """Get historical data for charts."""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Build query based on interval
            if interval == 'hour':
                cursor.execute("""
                    SELECT 
                        strftime('%Y-%m-%d %H:00:00', timestamp) as time_bucket,
                        AVG(production_kw) as avg_production,
                        AVG(consumption_kw) as avg_consumption,
                        AVG(net_power_kw) as avg_net_power,
                        SUM(production_kw * 0.25) as total_production_kwh
                    FROM solar_data 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY time_bucket
                    ORDER BY time_bucket
                """, (start_date, end_date))
            elif interval == 'day':
                cursor.execute("""
                    SELECT 
                        strftime('%Y-%m-%d', timestamp) as time_bucket,
                        AVG(production_kw) as avg_production,
                        AVG(consumption_kw) as avg_consumption,
                        AVG(net_power_kw) as avg_net_power,
                        SUM(production_kw * 0.25) as total_production_kwh
                    FROM solar_data 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY time_bucket
                    ORDER BY time_bucket
                """, (start_date, end_date))
            else:  # minute
                cursor.execute("""
                    SELECT 
                        timestamp,
                        production_kw,
                        consumption_kw,
                        net_power_kw
                    FROM solar_data 
                    WHERE timestamp BETWEEN ? AND ?
                    ORDER BY timestamp
                """, (start_date, end_date))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Format data for mobile app
            data = []
            for row in rows:
                if interval in ['hour', 'day']:
                    data.append({
                        'timestamp': row[0],
                        'production': row[1] or 0,
                        'consumption': row[2] or 0,
                        'net_power': row[3] or 0,
                        'total_production': row[4] or 0
                    })
                else:
                    data.append({
                        'timestamp': row[0],
                        'production': row[1] or 0,
                        'consumption': row[2] or 0,
                        'net_power': row[3] or 0
                    })
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error getting historical data: {e}")
            return []
    
    def get_device_list(self) -> List[Dict]:
        """Get list of all devices for mobile app."""
        try:
            # Get device list from PVS6
            devices = self.pvs_client.get_device_list()
            
            # Format for mobile app
            device_list = []
            for device in devices:
                device_list.append({
                    'id': device.get('device_id'),
                    'name': device.get('device_name'),
                    'type': device.get('device_type'),
                    'status': device.get('status'),
                    'production': device.get('production_kw', 0),
                    'last_seen': device.get('last_seen')
                })
            
            return device_list
            
        except Exception as e:
            self.logger.error(f"Error getting device list: {e}")
            return []
    
    def get_system_alerts(self) -> List[Dict]:
        """Get system alerts and warnings for mobile app."""
        try:
            alerts = []
            
            # Check for system issues
            current_data = self.get_dashboard_data()
            
            # Low production alert
            if current_data.get('production', 0) < 0.1:
                alerts.append({
                    'type': 'warning',
                    'message': 'Low solar production detected',
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'medium'
                })
            
            # High consumption alert
            if current_data.get('consumption', 0) > 10:
                alerts.append({
                    'type': 'info',
                    'message': 'High energy consumption detected',
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'low'
                })
            
            # System offline alert
            if current_data.get('status') == 'offline':
                alerts.append({
                    'type': 'error',
                    'message': 'Solar monitoring system offline',
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'high'
                })
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error getting system alerts: {e}")
            return []
    
    def send_notification(self, message: str, device_id: Optional[str] = None):
        """Send notification to mobile app."""
        try:
            notification = {
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'device_id': device_id
            }
            
            # Add to notification queue
            self.notification_queue.put(notification)
            
            # Send via Bluetooth if available
            if self.ble_service:
                self.ble_service.send_notification(message, device_id)
            
            self.logger.info(f"Notification sent: {message}")
            
        except Exception as e:
            self.logger.error(f"Error sending notification: {e}")
    
    def get_notifications(self) -> List[Dict]:
        """Get pending notifications for mobile app."""
        notifications = []
        
        try:
            while not self.notification_queue.empty():
                notification = self.notification_queue.get_nowait()
                notifications.append(notification)
        except queue.Empty:
            pass
        
        return notifications


# Flask app for mobile API
app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Initialize mobile API
mobile_api = MobileAPI()

@app.route('/api/mobile/dashboard', methods=['GET'])
def get_mobile_dashboard():
    """Get dashboard data for mobile app."""
    try:
        data = mobile_api.get_dashboard_data()
        return jsonify({
            'success': True,
            'data': data,
            'version': get_version_string(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/historical', methods=['GET'])
def get_historical_data():
    """Get historical data for charts."""
    try:
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        interval = request.args.get('interval', 'hour')
        
        if not start_date or not end_date:
            return jsonify({
                'success': False,
                'error': 'Start and end dates are required'
            }), 400
        
        data = mobile_api.get_historical_data(start_date, end_date, interval)
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/devices', methods=['GET'])
def get_device_list():
    """Get list of all devices."""
    try:
        devices = mobile_api.get_device_list()
        return jsonify({
            'success': True,
            'devices': devices,
            'count': len(devices),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/alerts', methods=['GET'])
def get_alerts():
    """Get system alerts and warnings."""
    try:
        alerts = mobile_api.get_system_alerts()
        return jsonify({
            'success': True,
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/notifications', methods=['GET'])
def get_notifications():
    """Get pending notifications."""
    try:
        notifications = mobile_api.get_notifications()
        return jsonify({
            'success': True,
            'notifications': notifications,
            'count': len(notifications),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/config', methods=['GET'])
def get_config():
    """Get mobile app configuration."""
    try:
        return jsonify({
            'success': True,
            'config': mobile_api.mobile_config,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/version', methods=['GET'])
def get_mobile_version():
    """Get version information for mobile app."""
    try:
        return jsonify({
            'success': True,
            'version': get_version_string(),
            'full_info': get_full_version_info(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/mobile/status', methods=['GET'])
def get_status():
    """Get mobile API status."""
    try:
        return jsonify({
            'success': True,
            'status': {
                'api_running': True,
                'bluetooth_available': mobile_api.ble_service is not None,
                'last_update': mobile_api.data_cache.get('last_update'),
                'cache_size': len(mobile_api.data_cache.get('dashboard', {})),
                'notification_queue_size': mobile_api.notification_queue.qsize()
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Start mobile API service
    mobile_api.start_service()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)
