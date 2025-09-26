"""
Database management for solar monitoring data
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import config

class SolarDatabase:
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection with proper timeout and settings"""
        conn = sqlite3.connect(
            self.db_path, 
            timeout=10.0,  # 10 second timeout
            check_same_thread=False  # Allow use from multiple threads
        )
        # Enable WAL mode for better concurrency
        conn.execute('PRAGMA journal_mode=WAL')
        # Set busy timeout
        conn.execute('PRAGMA busy_timeout=5000')  # 5 seconds
        return conn
    
    def init_database(self):
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create solar_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solar_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    device_id TEXT,
                    device_type TEXT,
                    power_kw REAL,
                    energy_kwh REAL,
                    voltage REAL,
                    current REAL,
                    frequency REAL,
                    raw_data TEXT
                )
            ''')
            
            # Create system_status table for overall system health
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_production_kw REAL,
                    total_consumption_kw REAL,
                    net_export_kw REAL,
                    system_online BOOLEAN,
                    pvs_online BOOLEAN
                )
            ''')
            
            # Create indexes for better query performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON solar_data(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_device_id ON solar_data(device_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_status_timestamp ON system_status(timestamp)')
            
            conn.commit()
    
    def insert_solar_data(self, device_data: Dict):
        """Insert solar device data into the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO solar_data 
                (device_id, device_type, power_kw, energy_kwh, voltage, current, frequency, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                device_data.get('device_id'),
                device_data.get('device_type'),
                device_data.get('power_kw'),
                device_data.get('energy_kwh'),
                device_data.get('voltage'),
                device_data.get('current'),
                device_data.get('frequency'),
                json.dumps(device_data.get('raw_data', {}))
            ))
            
            conn.commit()
    
    def insert_system_status(self, status_data: Dict):
        """Insert system status data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_status 
                (total_production_kw, total_consumption_kw, net_export_kw, system_online, pvs_online)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                status_data.get('total_production_kw'),
                status_data.get('total_consumption_kw'),
                status_data.get('net_export_kw'),
                status_data.get('system_online'),
                status_data.get('pvs_online')
            ))
            
            conn.commit()
    
    def get_latest_data(self, hours: int = 24) -> List[Dict]:
        """Get the latest solar data for the specified number of hours"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM solar_data 
                WHERE timestamp >= datetime('now', '-{} hours')
                ORDER BY timestamp DESC
            '''.format(hours))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_system_status(self, hours: int = 24) -> List[Dict]:
        """Get system status data for the specified number of hours"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM system_status 
                WHERE timestamp >= datetime('now', '-{} hours')
                ORDER BY timestamp DESC
            '''.format(hours))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_daily_summary(self, days: int = 7) -> List[Dict]:
        """Get daily energy production summary"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    DATE(timestamp) as date,
                    SUM(energy_kwh) as daily_energy_kwh,
                    AVG(power_kw) as avg_power_kw,
                    MAX(power_kw) as peak_power_kw
                FROM solar_data 
                WHERE timestamp >= datetime('now', '-{} days')
                AND device_type = 'production_meter'
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            '''.format(days))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def cleanup_old_data(self):
        """Remove old data to prevent database from growing too large"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Keep only the most recent data points
            cursor.execute('''
                DELETE FROM solar_data 
                WHERE id NOT IN (
                    SELECT id FROM solar_data 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                )
            ''', (config.MAX_DATA_POINTS,))
            
            cursor.execute('''
                DELETE FROM system_status 
                WHERE id NOT IN (
                    SELECT id FROM system_status 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                )
            ''', (config.MAX_DATA_POINTS // 10,))  # Keep fewer status records
            
            conn.commit()
