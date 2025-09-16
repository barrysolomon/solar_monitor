"""
Data collection service for solar monitoring
Polls the PVS gateway and stores data in the database
"""
import time
import schedule
import logging
from datetime import datetime
from typing import Optional
import config
from pvs_client import PVSClient
from database import SolarDatabase

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('solar_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SolarDataCollector:
    def __init__(self):
        self.pvs_client = PVSClient()
        self.database = SolarDatabase()
        self.last_successful_poll = None
        self.consecutive_failures = 0
        
    def collect_data(self):
        """
        Main data collection function
        Polls PVS gateway and stores data in database
        """
        try:
            logger.info("Starting data collection cycle")
            
            # Test connection first
            if not self.pvs_client.test_connection():
                logger.warning("PVS gateway not reachable, skipping this cycle")
                self.consecutive_failures += 1
                return False
            
            # Get device list from PVS
            devices = self.pvs_client.get_device_list()
            if not devices:
                logger.warning("No device data received from PVS")
                self.consecutive_failures += 1
                return False
            
            logger.info(f"Received data for {len(devices)} devices")
            
            # Process each device
            devices_stored = 0
            for device in devices:
                try:
                    parsed_data = self.pvs_client.parse_device_data(device)
                    self.database.insert_solar_data(parsed_data)
                    devices_stored += 1
                except Exception as e:
                    logger.error(f"Error processing device {device.get('DeviceID', 'unknown')}: {e}")
            
            # Get and store system summary
            system_summary = self.pvs_client.get_system_summary()
            self.database.insert_system_status(system_summary)
            
            # Update success tracking
            self.last_successful_poll = datetime.now()
            self.consecutive_failures = 0
            
            logger.info(f"Successfully stored data for {devices_stored} devices")
            logger.info(f"System summary: {system_summary['total_production_kw']:.2f}kW production, "
                       f"{system_summary['net_export_kw']:.2f}kW net export")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in data collection: {e}")
            self.consecutive_failures += 1
            return False
    
    def cleanup_old_data(self):
        """Clean up old data to prevent database from growing too large"""
        try:
            self.database.cleanup_old_data()
            logger.info("Cleaned up old data from database")
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def get_status(self) -> dict:
        """Get current status of the data collector"""
        return {
            'last_successful_poll': self.last_successful_poll.isoformat() if self.last_successful_poll else None,
            'consecutive_failures': self.consecutive_failures,
            'pvs_online': self.pvs_client.test_connection(),
            'database_path': config.DATABASE_PATH,
            'poll_interval': config.POLL_INTERVAL_SECONDS
        }
    
    def run_continuous(self):
        """Run data collection continuously with error handling"""
        logger.info("Starting continuous data collection")
        logger.info(f"Polling PVS gateway at {config.PVS_IP} every {config.POLL_INTERVAL_SECONDS} seconds")
        
        # Schedule regular data collection
        schedule.every(config.POLL_INTERVAL_SECONDS).seconds.do(self.collect_data)
        
        # Schedule daily cleanup
        schedule.every().day.at("02:00").do(self.cleanup_old_data)
        
        # Initial data collection
        self.collect_data()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                
                # If we have too many consecutive failures, try to recover
                if self.consecutive_failures >= 5:
                    logger.warning("Multiple consecutive failures detected, attempting recovery")
                    time.sleep(30)  # Wait before retrying
                    self.consecutive_failures = 0
                    
        except KeyboardInterrupt:
            logger.info("Data collection stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error in continuous collection: {e}")

def main():
    """Main entry point for the data collector"""
    collector = SolarDataCollector()
    
    # Test initial connection
    if not collector.pvs_client.test_connection():
        logger.error("Cannot connect to PVS gateway. Please check network setup.")
        logger.error("See NETWORK_SETUP.md for troubleshooting steps.")
        return
    
    logger.info("PVS gateway connection successful, starting data collection")
    collector.run_continuous()

if __name__ == "__main__":
    main()
