# Energy Management System – Assessment

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 Overview

This project implements a comprehensive Energy Management System (EMS) assessment platform that integrates multiple industrial protocols and cloud services. The system is designed for monitoring and managing electrical infrastructure in real-time.

### Key Technologies

* **Azure IoT Hub & IoT Edge** - Cloud connectivity and edge computing
* **Python (async architecture)** - High-performance asynchronous processing
* **Modbus TCP (pymodbus)** - Industrial protocol for device communication
* **OCPP 1.6** - Open Charge Point Protocol for EV charging infrastructure
* **Optional: InfluxDB & Grafana** - Time-series data storage and visualization

---

## 🧩 Architecture & Features

### 1. ConfigSyncService

A production-grade service for bidirectional configuration synchronization:

* **Device Twin Sync**: Automatic synchronization between local config and Azure IoT Hub Device Twin
* **Desired Properties**: Real-time handling of cloud-initiated configuration changes
* **Reported Properties**: Local configuration changes reported back to the cloud
* **File Watcher**: Monitors local configuration files for changes
* **Retry Logic**: Robust error handling with exponential backoff
* **Graceful Shutdown**: Clean service termination

### 2. ModbusDataCollector

Industrial data acquisition from electrical measurement devices:

* **UR20-3EM-230V-AC Support**: Specialized support for Weidmüller UR20 modules
* **Process Data Mapping**: Offset-based register reading for accurate measurements
* **Float Decoding**: Proper 32-bit float decoding from Modbus registers
* **Structured Logging**: Comprehensive logging with timestamps and device metadata
* **Error Handling**: Graceful handling of connection and read failures

**Measurements Collected:**
- Voltage (V)
- Current (A)
- Power (W)
- Frequency (Hz)

### 3. OCPP Client & Server

Electric vehicle charging infrastructure communication:

* **BootNotification**: Automatic registration with central system on startup
* **MeterValues**: Periodic transmission of charging session data (15-second intervals)
* **ChargingProfile**: Handling of dynamic charging profiles from the central system
* **Async Processing**: Non-blocking message handling for high throughput

---

## 📋 Prerequisites

- Python 3.8 or higher
- Azure IoT Hub account (for cloud features)
- Modbus-compatible electrical measurement device
- OCPP-compliant charging station (optional)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/username/ems-assessment.git
cd ems-assessment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install with pip
pip install -r requirements.txt

```

### 4. Configure the System

Edit `config/config.json`:

```json
{
  "app": {
    "log_level": "INFO"
  },
  "modbus": {
    "host": "192.168.1.100",
    "port": 502,
    "unit_id": 1,
    "poll_interval": 5
  },
  "iot_hub": {
    "connection_string": "your-azure-iot-hub-connection-string"
  }
}
```

### 5. Run the Application

```bash
# Direct execution
python src/main.py

```

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test Categories

```bash
pytest tests/test_modbus.py
pytest tests/test_ocpp.py
pytest tests/test_config.py
```

---

### Docker

```bash
# Build Docker image
make docker-build

# Run in container
make docker-run
```

---

## 📁 Project Structure

```
ems-assessment/
├── src/
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   └── logger.py          # Centralized logging configuration
│   ├── modbus/
│   │   └── collector.py       # Modbus data collection
│   ├── ocpp/
│   │   ├── client.py          # OCPP client implementation
│   │   └── server.py          # OCPP server implementation
│   └── config_sync/
│       └── service.py         # Azure IoT Hub config sync
├── tests/
│   ├── test_modbus.py         # Modbus collector tests
│   ├── test_ocpp.py           # OCPP component tests
│   └── test_config.py         # Config sync tests
├── config/
│   └── config.json            # Application configuration
├── Dockerfile                 # Docker container definition
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Modern Python packaging
├── setup.py                  # Traditional packaging
├── tox.ini                   # Testing configuration
├── Makefile                  # Development tasks
├── .pre-commit-config.yaml   # Pre-commit hooks
├── MANIFEST.in              # Package manifest
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md                # This file
└── Readme_Theory.md         # Theoretical documentation
```

---

## 🔧 Configuration

### Modbus Configuration

```json
{
  "modbus": {
    "host": "192.168.1.100",
    "port": 502,
    "unit_id": 1,
    "poll_interval": 5
  }
}
```

### Azure IoT Hub Configuration

```json
{
  "iot_hub": {
    "connection_string": "HostName=your-hub.azure-devices.net;DeviceId=your-device;SharedAccessKey=your-key"
  }
}
```

### Logging Configuration

```json
{
  "app": {
    "log_level": "INFO"
  }
}
```

---

## 📊 Monitoring & Observability

- **Structured Logging**: All components use consistent logging format
- **Azure IoT Hub Integration**: Real-time telemetry and command handling
- **Error Handling**: Comprehensive error reporting and recovery
- **Performance Metrics**: Built-in timing and throughput measurements

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write comprehensive docstrings
- Add unit tests for new functionality
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Weidmüller for UR20-3EM-230V-AC module documentation
- Open Charge Alliance for OCPP specifications
- Microsoft Azure IoT team for IoT Hub services

---

## 📞 Support

For questions, issues, or contributions, please:

- Open an issue on GitHub
- Check the theoretical documentation in [Readme_Theory.md](Readme_Theory.md)
- Review the code documentation and docstrings

---

## 📊 Architecture

Modbus → Python → IoT Hub → InfluxDB → Grafana

---

## 📌 Notes

* Register addresses should be taken from device manual
* Endianness handled (Little Endian for Modbus TCP)

---

## 📚 Reference

Weidmüller UR20 Manual (provided)
