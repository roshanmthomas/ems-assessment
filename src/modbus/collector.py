"""
ModbusDataCollector (Production-Level)

Reads process data from UR20-3EM-230V-AC module.

IMPORTANT:
- Uses process data mapping (offset-based)
- No fixed register addresses
- Each measurement = 32-bit float (2 registers)
"""

from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import logging
from datetime import datetime


class ModbusDataCollector:
    """
    A class for collecting electrical measurement data from a UR20-3EM-230V-AC Modbus device.

    This collector connects to the device via Modbus TCP, reads input registers containing
    process data, and decodes the measurements into usable float values. The data includes
    voltage, current, power, and frequency readings.

    Attributes:
        client (ModbusTcpClient): The Modbus TCP client for communication.
        unit_id (int): The Modbus slave unit identifier.
        logger (logging.Logger): Logger instance for recording operations and errors.
    """

    def __init__(self, host: str, port: int = 502, unit_id: int = 1):
        """
        Initialize the Modbus Data Collector.

        Args:
            host (str): The IP address or hostname of the Modbus device.
            port (int, optional): The Modbus TCP port number. Defaults to 502.
            unit_id (int, optional): The Modbus slave unit ID. Defaults to 1.

        Raises:
            None: Initialization doesn't raise exceptions, but connection will be tested later.
        """
        self.client = ModbusTcpClient(host, port=port)
        self.unit_id = unit_id

        # Configure logging for the collector
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )
        self.logger = logging.getLogger("ModbusCollector")

    def connect(self):
        """
        Establish connection to the Modbus device.

        Attempts to connect to the configured Modbus device. This method should be called
        before performing any read operations.

        Raises:
            ConnectionError: If the connection to the device fails.
        """
        if not self.client.connect():
            raise ConnectionError("Failed to connect to Modbus device")

    def read_input_registers(self, start: int, count: int):
        """
        Read input registers from the Modbus device.

        Input registers contain process data that cannot be modified. This method reads
        the specified number of registers starting from the given address.

        Args:
            start (int): The starting register address (0-based).
            count (int): The number of registers to read.

        Returns:
            list: A list of register values.

        Raises:
            Exception: If there's an error reading the registers.
        """
        response = self.client.read_input_registers(
            address=start,
            count=count,
            unit=self.unit_id
        )

        if response.isError():
            raise Exception(f"Error reading registers at {start}")

        return response.registers

    def decode_float(self, registers):
        """
        Decode a 32-bit floating point value from two Modbus registers.

        The UR20-3EM-230V-AC module stores measurements as 32-bit floats spanning
        two consecutive 16-bit registers. This method decodes them using little-endian
        byte and word order as specified in the device manual.

        Args:
            registers (list): A list of two register values containing the float data.

        Returns:
            float: The decoded floating point value.

        Note:
            Based on the device manual: Intel format (Little Endian) is used.
        """
        decoder = BinaryPayloadDecoder.fromRegisters(
            registers,
            byteorder=Endian.LITTLE,
            wordorder=Endian.LITTLE
        )
        return decoder.decode_32bit_float()

    def collect_data(self) -> dict:
        """
        Collect all measurement data from the UR20-3EM-230V-AC module.

        This method reads the process data registers and extracts the electrical measurements.
        The register mapping is based on the device's process data layout where each
        measurement occupies two consecutive registers (32-bit float).

        Register Mapping (process data):
        - Voltage: registers 0-1 (V)
        - Current: registers 2-3 (A)
        - Power: registers 4-5 (W)
        - Frequency: registers 6-7 (Hz)

        Returns:
            dict or None: A dictionary containing timestamped measurement data with keys:
                - device: Device identifier (e.g., "UR20-3EM-230V-AC")
                - timestamp: ISO format timestamp
                - voltage_v: Voltage in volts (rounded to 2 decimal places)
                - current_a: Current in amperes (rounded to 2 decimal places)
                - power_w: Power in watts (rounded to 2 decimal places)
                - frequency_hz: Frequency in hertz (rounded to 2 decimal places)
            Returns None if an error occurs during data collection.

        Raises:
            None: Exceptions are caught and logged internally.
        """
        try:
            # Establish connection to the device
            self.connect()

            # Read the first 8 registers to get all 4 measurements (4 floats * 2 registers each)
            registers = self.read_input_registers(0, 8)

            # Decode each measurement from its register pair
            voltage = self.decode_float(registers[0:2])
            current = self.decode_float(registers[2:4])
            power = self.decode_float(registers[4:6])
            frequency = self.decode_float(registers[6:8])

            # Package the data with timestamp and rounded values
            data = {
                "device": "UR20-3EM-230V-AC",
                "timestamp": datetime.utcnow().isoformat(),
                "voltage_v": round(voltage, 2),
                "current_a": round(current, 2),
                "power_w": round(power, 2),
                "frequency_hz": round(frequency, 2)
            }

            # Log successful data collection
            self.logger.info(f"Collected Data: {data}")
            return data

        except Exception as e:
            # Log any errors that occur during collection
            self.logger.error(f"Error: {e}")
            return None

        finally:
            # Always close the connection, even if an error occurred
            self.client.close()