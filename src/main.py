"""
Main Application Entry Point

- Loads configuration
- Starts Modbus data collection loop
- (Optional) Integrates with IoT Hub
"""

import json
import time
from pathlib import Path

from src.modbus.collector import ModbusDataCollector
from src.core.logger import setup_logger


def load_config():
    """
    Load configuration from JSON file.
    """
    # Define the path to the configuration file
    config_path = Path("config/config.json")
    # Open and parse the JSON configuration
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    """
    Main execution loop.
    """
    # Load application configuration
    config = load_config()

    # Setup logging based on config level
    logger = setup_logger(level=config["app"]["log_level"])

    # Extract Modbus configuration section
    modbus_config = config["modbus"]

    # Initialize the Modbus data collector with device parameters
    collector = ModbusDataCollector(
        host=modbus_config["host"],
        port=modbus_config["port"],
        unit_id=modbus_config["unit_id"]
    )

    # Get polling interval, default to 5 seconds if not specified
    poll_interval = modbus_config.get("poll_interval", 5)

    # Log startup message
    logger.info("Starting Modbus Data Collector...")

    # Main data collection loop
    while True:
        # Collect data from the Modbus device
        data = collector.collect_data()

        # Log the collected data if successful
        if data:
            logger.info(f"Processed Data: {data}")
        
        # Wait before next polling cycle
    main()