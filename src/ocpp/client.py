"""
OCPP Client

Sends:
- BootNotification on startup
- MeterValues every 15 seconds
"""

import asyncio
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call


class ChargePointClient(cp):
    """
    OCPP Charge Point Client implementation.

    This class extends the OCPP ChargePoint to provide client functionality
    for communicating with an OCPP server. It handles boot notifications
    and periodic meter value reporting.
    """

    async def send_boot(self):
        """Send BootNotification to server."""
        # Create the boot notification payload with charge point details
        request = call.BootNotificationPayload(
            charge_point_model="ModelX",
            charge_point_vendor="VendorY"
        )
        # Send the request to the server
        await self.call(request)

    async def send_meter(self):
        """Send MeterValues periodically."""
        while True:
            # Create meter values payload with current readings
            request = call.MeterValuesPayload(
                connector_id=1,
                meter_value=[{"value": "100"}]
            )
            # Send the meter values to the server
            await self.call(request)
            # Wait 15 seconds before sending next update
            await asyncio.sleep(15)