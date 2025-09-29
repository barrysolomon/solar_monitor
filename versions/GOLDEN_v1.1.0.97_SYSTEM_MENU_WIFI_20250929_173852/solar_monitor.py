#!/usr/bin/env python3
"""
Solar Monitor - Main Application Launcher
Replaces SunPower cloud service with local monitoring
"""
import sys
import argparse
import threading
import time
from datetime import datetime
import config
from data_collector import SolarDataCollector
from web_dashboard import app

def run_data_collector():
    """Run the data collection service in a separate thread"""
    collector = SolarDataCollector()
    collector.run_continuous()

def run_web_dashboard():
    """Run the web dashboard"""
    print(f"Starting web dashboard on http://{config.WEB_HOST}:{config.WEB_PORT}")
    app.run(host=config.WEB_HOST, port=config.WEB_PORT, debug=False, use_reloader=False)

def main():
    parser = argparse.ArgumentParser(description='Solar Monitor - Local SunPower Monitoring')
    parser.add_argument('--mode', choices=['collector', 'dashboard', 'both'], default='both',
                       help='Run mode: collector only, dashboard only, or both')
    parser.add_argument('--test-connection', action='store_true',
                       help='Test PVS gateway connection and exit')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Solar Monitor - SunPower Local Monitoring System")
    print("=" * 60)
    print(f"PVS Gateway: {config.PVS_BASE_URL}")
    print(f"Database: {config.DATABASE_PATH}")
    print(f"Poll Interval: {config.POLL_INTERVAL_SECONDS} seconds")
    print("=" * 60)
    
    # Test connection if requested
    if args.test_connection:
        print("Testing PVS gateway connection...")
        from pvs_client import PVSClient
        client = PVSClient()
        if client.test_connection():
            print("✓ PVS gateway connection successful!")
            devices = client.get_device_list()
            if devices:
                print(f"✓ Found {len(devices)} devices")
                for device in devices[:3]:  # Show first 3 devices
                    print(f"  - {device.get('DeviceType', 'Unknown')}: {device.get('DeviceID', 'Unknown')}")
            else:
                print("⚠ No devices found")
        else:
            print("✗ PVS gateway connection failed!")
            print("Please check your network setup (see NETWORK_SETUP.md)")
            sys.exit(1)
        return
    
    # Run selected mode
    if args.mode == 'collector':
        print("Starting data collector only...")
        run_data_collector()
    elif args.mode == 'dashboard':
        print("Starting web dashboard only...")
        run_web_dashboard()
    else:  # both
        print("Starting both data collector and web dashboard...")
        
        # Start data collector in background thread
        collector_thread = threading.Thread(target=run_data_collector, daemon=True)
        collector_thread.start()
        
        # Give collector time to start
        time.sleep(2)
        
        # Start web dashboard (main thread)
        run_web_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down Solar Monitor...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
