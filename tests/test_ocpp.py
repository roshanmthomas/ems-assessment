"""
Test cases for OCPP components
"""

import pytest
from src.ocpp.client import ChargePointClient


@pytest.mark.asyncio
async def test_boot_notification():
    """Test that boot notification is sent correctly."""
    cp = ChargePointClient("CP_1", None)

    cp.call = pytest.AsyncMock(return_value={"status": "Accepted"})

    await cp.send_boot()

    cp.call.assert_called_once()