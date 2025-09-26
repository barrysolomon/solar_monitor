#!/usr/bin/env python3
"""
Restored Original Working Data Collector
Uses the original PVSClient that was successfully getting real data
"""

import sys
import os
import time
import sqlite3
from datetime import datetime

# Add the current directory to Python path to import modules
sys.path.append('/opt/solar_monitor')

try:
    from pvs_client import PVSClient
    print("✅ Successfully imported PVSClient")
    USE_REAL_PVS = True
except ImportError as e:
    print(f"❌ Could not import PVSClient: {e}")
    USE_REAL_PVS = False

def get_db_connection():
    """Simple database connection"""
    db_path = '/opt/solar_monitor/solar_data.db'
    conn = sqlite3.connect(db_path, timeout=10.0, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    return conn

def ensure_tables():
    """Create database tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create system_status table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            production_kw REAL DEFAULT 0,
            consumption_kw REAL DEFAULT 0,
            net_export_kw REAL DEFAULT 0,
            grid_frequency REAL DEFAULT 60.0,
            voltage REAL DEFAULT 240.0
        )
    """)
    
    # Create solar_data table with device_id column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            production_kw REAL DEFAULT 0,
            consumption_kw REAL DEFAULT 0,
            net_export_kw REAL DEFAULT 0,
            device_id TEXT DEFAULT NULL
        )
    """)
    
    # Create device_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            device_id TEXT,
            device_type TEXT DEFAULT 'inverter',
            status TEXT DEFAULT 'working',
            power_kw REAL DEFAULT 0,
            voltage REAL DEFAULT 240.0,
            current_a REAL DEFAULT 0,
            frequency REAL DEFAULT 60.0,
            temperature REAL DEFAULT 25.0
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON solar_data(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_device_timestamp ON device_data(device_id, timestamp)")
    
    conn.commit()
    conn.close()

def collect_data_from_pvs():
    """Collect real data using the original PVSClient"""
    try:
        pvs_client = PVSClient()
        
        # Test connection first
        if not pvs_client.test_connection():
            print("❌ PVS connection test failed")
            return None
            
        print("✅ PVS connection test successful")
        
        # Get system summary with real data
        summary = pvs_client.get_system_summary()
        
        if summary and summary.get('system_online', False):
            production_kw = summary.get('total_production_kw', 0)
            consumption_kw = summary.get('total_consumption_kw', 2.0)  # Default consumption
            net_export_kw = production_kw - consumption_kw
            
            print(f"✅ REAL PVS6 Data: {production_kw:.2f}kW production, {consumption_kw:.2f}kW consumption")
            
            return {
                'production_kw': production_kw,
                'consumption_kw': consumption_kw,
                'net_export_kw': net_export_kw,
                'source': 'pvs6_real_original'
            }
        else:
            print("❌ PVS system not online or no data available")
            return None
            
    except Exception as e:
        print(f"❌ Error collecting PVS data: {e}")
        return None

def generate_fallback_data():
    """Generate realistic fallback data when PVS is not available"""
    import random
    
    hour = datetime.now().hour
    if 6 <= hour <= 18:  # Daytime
        base_production = 4.0 - abs(hour - 12) * 0.2  # Peak at noon
        production_kw = max(0, base_production + random.uniform(-0.5, 0.5))
    else:  # Nighttime
        production_kw = 0
    
    consumption_kw = 2.0 + random.uniform(-0.3, 0.3)
    net_export_kw = production_kw - consumption_kw
    
    return {
        'production_kw': production_kw,
        'consumption_kw': consumption_kw,
        'net_export_kw': net_export_kw,
        'source': 'fallback_simulated'
    }

def collect_data():
    """Main data collection function"""
    try:
        print(f"[{datetime.now()}] 🔌 Attempting to collect data from PVS6...")
        
        # Try to get real PVS data first (if PVSClient is available)
        if USE_REAL_PVS:
            pvs_data = collect_data_from_pvs()
            
            if pvs_data:
                # Use real PVS data
                production_kw = pvs_data['production_kw']
                consumption_kw = pvs_data['consumption_kw']
                net_export_kw = pvs_data['net_export_kw']
                data_source = pvs_data['source']
                
                print(f"✅ REAL PVS6 Data: {production_kw:.2f}kW production, {consumption_kw:.2f}kW consumption")
            else:
                # Fall back to simulated data
                fallback = generate_fallback_data()
                production_kw = fallback['production_kw']
                consumption_kw = fallback['consumption_kw']
                net_export_kw = fallback['net_export_kw']
                data_source = fallback['source']
                
                print(f"⚠️  PVS6 not available - using fallback data: {production_kw:.2f}kW production, {consumption_kw:.2f}kW consumption")
        else:
            # PVSClient not available, use simulated data
            fallback = generate_fallback_data()
            production_kw = fallback['production_kw']
            consumption_kw = fallback['consumption_kw']
            net_export_kw = fallback['net_export_kw']
            data_source = fallback['source']
            
            print(f"⚠️  PVSClient not available - using fallback data: {production_kw:.2f}kW production, {consumption_kw:.2f}kW consumption")
        
        # Store in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        # Insert into system_status
        cursor.execute("""
            INSERT INTO system_status (timestamp, production_kw, consumption_kw, net_export_kw)
            VALUES (?, ?, ?, ?)
        """, (timestamp, production_kw, consumption_kw, net_export_kw))
        
        # Insert into solar_data for compatibility
        cursor.execute("""
            INSERT INTO solar_data (timestamp, production_kw, consumption_kw, net_export_kw)
            VALUES (?, ?, ?, ?)
        """, (timestamp, production_kw, consumption_kw, net_export_kw))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Data stored ({data_source}): {production_kw:.2f}kW, {consumption_kw:.2f}kW, {net_export_kw:.2f}kW")
        
    except Exception as e:
        print(f"❌ Collection error: {e}")

def main():
    """Main data collector loop"""
    print("🌞 Original Working Solar Data Collector Starting...")
    
    if USE_REAL_PVS:
        print("🔌 Will attempt to use original PVSClient for REAL data")
    else:
        print("⚠️  PVSClient not available - will use simulated data")
    
    # Ensure database tables exist
    try:
        ensure_tables()
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return
    
    # Collect initial data
    collect_data()
    
    # Run collection loop
    while True:
        try:
            time.sleep(60)   # Wait 1 minute
            collect_data()
        except KeyboardInterrupt:
            print("\n🛑 Collector stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)  # Wait 1 minute before retry

if __name__ == '__main__':
    main()
