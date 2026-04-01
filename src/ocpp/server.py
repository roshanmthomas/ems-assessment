"""
OCPP Server

Handles:
- BootNotification
- MeterValues
- Sends ChargingProfile
"""

from ocpp.routing import on
from ocpp.v16.enums import Action
from ocpp.v16 import ChargePoint as cp


class ChargePointServer(cp):
    """
    OCPP Charge Point Server implementation.

    This class extends the OCPP ChargePoint to provide server functionality
    for handling OCPP messages from clients. It processes boot notifications,
    meter values, and charging profile requests.
    """

    @on(Action.BootNotification)
    async def on_boot(self, **kwargs):
        """Handle BootNotification."""
        # Accept the boot notification from the charge point
        return {"status": "Accepted"}

    @on(Action.MeterValues)
    async def on_meter(self, **kwargs):
        """Handle MeterValues."""
        # Log receipt of meter values (could be stored or processed further)
        print("Meter values received")

    @on(Action.SetChargingProfile)
    async def on_set_profile(self, **kwargs):
        """Handle ChargingProfile."""
        # Log receipt of charging profile and accept it
        print("Charging profile received")
        return {"status": "Accepted"}