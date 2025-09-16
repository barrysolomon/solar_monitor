"""
Configuration settings for the Solar Monitor application
"""
import os

# PVS Gateway Configuration
PVS_IP = os.getenv('PVS_IP', '172.27.153.1')
PVS_PORT = os.getenv('PVS_PORT', '80')
PVS_BASE_URL = f"http://{PVS_IP}:{PVS_PORT}"

# API Endpoints
DEVICE_LIST_ENDPOINT = "/cgi-bin/dl_cgi?Command=DeviceList"
METER_DATA_ENDPOINT = "/cgi-bin/dl_cgi?Command=MeterData"

# Database Configuration
DATABASE_PATH = "solar_data.db"

# Polling Configuration
POLL_INTERVAL_SECONDS = 30  # How often to poll the PVS gateway
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

# Web Dashboard Configuration
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
DEBUG = True

# Data Retention
MAX_DATA_POINTS = 10000  # Maximum number of data points to keep in database
