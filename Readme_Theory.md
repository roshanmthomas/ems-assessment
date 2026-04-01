# Theoretical Answers – Energy Management System

## 1. Azure IoT Edge Startup File

The crucial file is:

**config.yaml**

**Location:**

* Linux: /etc/iotedge/config.yaml
* Windows: C:\ProgramData\iotedge\config.yaml

This file contains:

* Device provisioning details
* Connection string
* Certificates and security configuration

It is required for the IoT Edge runtime to connect to Azure IoT Hub and start modules.

---

## 2. Python Service Architecture

I structured the application using a modular layered architecture:

* Hardware Layer → Modbus, sensors
* Protocol Layer → IoT Hub, MQTT
* Service Layer → Business logic
* Core Layer → Logging, configuration

Key principles:

* Separation of concerns
* Async-first design
* Dependency injection
* Testability

---

## 3. Testing Async Code with pytest

I used pytest with pytest-asyncio:

Example:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_func()
    assert result == expected
```

Best practices:

* Use AsyncMock
* Avoid real network calls
* Use fixtures
* Isolate logic

---

## 4. Installing InfluxDB & Grafana

I used Docker for local setup:

```bash
docker run -d -p 8086:8086 influxdb
docker run -d -p 3000:3000 grafana/grafana
```

Alternative:

* Deploy as Azure IoT Edge modules

Data flow:
Device → Python Service → InfluxDB → Grafana

---

## Assumptions

* IoT Edge runtime is installed
* Modbus register mapping is available
* Device Twin is enabled
