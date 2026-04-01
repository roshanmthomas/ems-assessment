"""
Test cases for ConfigSyncService
"""

import pytest
from unittest.mock import AsyncMock
from src.config_sync.service import ConfigSyncService


@pytest.mark.asyncio
async def test_report_to_cloud():
    """Test that report_to_cloud sends local config to IoT Hub."""
    service = ConfigSyncService("fake_conn", "config/config.json")

    service.client = AsyncMock()
    service.local_config = {"test": 1}

    await service.report_to_cloud()

    service.client.patch_twin_reported_properties.assert_called_once()