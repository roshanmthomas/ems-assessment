"""
Test cases for ModbusDataCollector
"""

from unittest.mock import MagicMock
from src.modbus.collector import ModbusDataCollector


def test_collect_data_success():
    """Test successful data collection from Modbus device."""
    collector = ModbusDataCollector("localhost")

    # Mock connection
    collector.connect = MagicMock()

    # Mock register response (float 50Hz approx)
    collector.read_input_registers = MagicMock(
        return_value=[0x4248, 0x0000, 0, 0, 0, 0, 0x4248, 0x0000]
    )

    data = collector.collect_data()

    assert data is not None
    assert "frequency_hz" in data