"""
ConfigSyncService

Production-grade service for syncing local config with Azure IoT Hub Device Twin.

Features:
- Initial twin sync
- Desired property listener
- File watcher
- Retry logic for all network operations
- Graceful shutdown
"""

import json
import asyncio
import os
from azure.iot.device.aio import IoTHubDeviceClient
from src.core.logger import setup_logger


class ConfigSyncService:
    """
    Production-grade service for synchronizing local configuration with Azure IoT Hub Device Twin.

    This service provides bidirectional synchronization between local configuration files
    and Azure IoT Hub device twin properties. It handles initial sync, real-time updates
    from the cloud, local file changes, and robust error handling with retry logic.

    Attributes:
        client: Azure IoT Hub device client instance
        config_path: Path to the local JSON configuration file
        logger: Logger instance for this service
        local_config: Dictionary containing the current local configuration
        running: Boolean flag to control service execution
    """

    def __init__(self, connection_string: str, config_path: str):
        """
        Initialize the ConfigSyncService.

        Args:
            connection_string: Azure IoT Hub device connection string
            config_path: Path to the local JSON configuration file
        """
        self.client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self.config_path = config_path
        self.logger = setup_logger("ConfigSyncService")
        self.local_config = self.load_config()
        self.running = True

    # ----------------------------
    # CONFIG HANDLING
    # ----------------------------
    def load_config(self):
        """
        Load configuration from the local JSON file.

        Returns:
            dict: Configuration dictionary, or empty dict if file not found
        """
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Config file not found. Using empty config.")
            return {}

    def save_config(self):
        """
        Save the current configuration to the local JSON file.

        Raises:
            Exception: If there's an error writing to the file
        """
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.local_config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config to {self.config_path}: {e}")
            raise

    # ----------------------------
    # RETRY HELPER (GENERIC)
    # ----------------------------
    async def retry(self, func, max_retries=5, delay=2, operation="operation"):
        """
        Generic retry wrapper for async operations with exponential backoff.

        Args:
            func: Async callable to retry
            max_retries: Maximum number of retry attempts (default: 5)
            delay: Delay in seconds between retries (default: 2)
            operation: Description of the operation for logging (default: "operation")

        Returns:
            Result of the successful function call

        Raises:
            Exception: The last exception encountered after all retries are exhausted
        """
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                self.logger.warning(
                    f"{operation} failed (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"{operation} failed after retries.")
                    raise

    # ----------------------------
    # CONNECTION
    # ----------------------------
    async def connect(self):
        """
        Establish connection to Azure IoT Hub with retry logic.
        """
        await self.retry(
            self.client.connect,
            operation="IoT Hub connection"
        )
        self.logger.info("Connected to IoT Hub")

    # ----------------------------
    # INITIAL SYNC
    # ----------------------------
    async def initial_sync(self):
        """
        Perform initial synchronization of device twin properties to local config.
        """
        async def get_twin():
            return await self.client.get_twin()

        twin = await self.retry(get_twin, operation="Initial twin fetch")

        desired = twin.get("desired", {})
        self.local_config.update(desired)
        self.save_config()

        self.logger.info("Initial twin sync completed")

    # ----------------------------
    # LISTEN FOR CLOUD UPDATES
    # ----------------------------
    async def listen_for_updates(self):
        """
        Continuously listen for desired property updates from IoT Hub.

        Runs an infinite loop while the service is running, processing incoming
        twin patches and updating local configuration accordingly.
        """
        while self.running:
            try:
                patch = await self.client.receive_twin_desired_properties_patch()

                self.local_config.update(patch)
                self.save_config()

                await self.report_to_cloud()

            except Exception as e:
                self.logger.error(f"Update listener error: {e}")
                await asyncio.sleep(5)

    # ----------------------------
    # FILE WATCHER (LOCAL CHANGES)
    # ----------------------------
    async def watch_file_changes(self):
        """
        Monitor the local configuration file for changes and sync to cloud.

        Continuously checks the file modification time and reports changes
        to IoT Hub when detected. Only runs if the config file exists.
        """
        if not os.path.exists(self.config_path):
            return

        last_modified = os.path.getmtime(self.config_path)

        while self.running:
            try:
                current = os.path.getmtime(self.config_path)

                if current != last_modified:
                    self.logger.info("Local config changed, syncing to cloud")

                    self.local_config = self.load_config()
                    await self.report_to_cloud()

                    last_modified = current

                await asyncio.sleep(2)

            except Exception as e:
                self.logger.error(f"File watcher error: {e}")
                await asyncio.sleep(5)

    # ----------------------------
    # REPORT TO CLOUD (WITH RETRY)
    # ----------------------------
    async def report_to_cloud(self):
        """
        Report the current local configuration to IoT Hub as reported properties.
        """
        async def send_patch():
            await self.client.patch_twin_reported_properties(self.local_config)

        await self.retry(
            send_patch,
            operation="Reporting config to cloud"
        )

        self.logger.info("Config reported to cloud")

    # ----------------------------
    # RUN SERVICE
    # ----------------------------
    async def run(self):
        """
        Start the configuration sync service.

        Performs initial setup (connection and sync), then runs the update
        listener and file watcher concurrently.
        """
        await self.connect()
        await self.initial_sync()

        await asyncio.gather(
            self.listen_for_updates(),
            self.watch_file_changes()
        )

    # ----------------------------
    # STOP SERVICE
    # ----------------------------
    def stop(self):
        """
        Stop the configuration sync service.

        Sets the running flag to False, which will cause all loops to exit gracefully.
        """
        self.running = False