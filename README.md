# STUSB4500 EasyMCP2221 Integration

This project implements a Python interface to communicate with the **STMicroelectronics STUSB4500 USB Power Delivery controller** using the **EasyMCP2221 library** for I2C communication.

## Features

- I2C-based communication using the **MCP2221 USB-to-I2C bridge**.
- **Read/Write operations** to the Non-Volatile Memory (NVM) of the STUSB4500.
- Perform **full or sector-level reads and writes** to the NVM of the controller.
- Tools to **erase, unlock, and program** the STUSB4500 device.
- **Soft reset support** for consistent operation.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
    - [Basic Example](#basic-example)
    - [Key Functions](#key-functions)
- [Running the Script](#running-the-script)
- [Output Example](#output-example)
- [References](#references)

## Requirements

1. **Python Version**: 3.12 or higher
2. **Libraries**:
   - **EasyMCP2221**: This library provides an interface for communication over I2C using Microchip MCP2221.
   - Install the library with:
     ```bash
     pip install EasyMCP2221
     ```

3. **Hardware**:
   - **Microchip MCP2221** USB-to-I2C bridge.
   - **STUSB4500**, connected to the MCP2221 via I2C (default address: `0x28`).

## Installation

1. Clone this repository or download the provided `STUSB4500` implementation.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Hardware Setup

1. Connect the **MCP2221** USB-I2C bridge to your system.
2. Wire the MCP2221 to the **STUSB4500** controller:
    - Ensure proper I2C connections (SCL, SDA) and power supply connections to the STUSB4500.
3. Confirm that the MCP2221 device driver is installed and recognized by the OS.

## Usage

To use this interface, the `STUSB4500` class is the central component. Below is an explanation of its intended use.

### Key Functions

The `STUSB4500` class includes the following main methods:

#### NVM Operations:
- `read_full_nvm()`: Reads the entire NVM space.
- `write_full_nvm(data)`: Writes a full configuration array to the NVM.
- `read_nvm_sector(sector)`: Reads a specific NVM sector.
- `write_nvm_sector(sector, sector_data)`: Writes data to a specific NVM sector.
- `cust_full_erase_sector()`: Erases the STUSB4500's NVM memory.

#### Register Map:
- `read_full_regmap()`: Reads and prints the entire register map.

#### Device Commands:
- `soft_reset()`: Issues a soft reset to the STUSB4500.

## Running the Script

To run the example provided in the repository:

```bash
python main.py
```

Ensure that the MCP2221, STUSB4500, and I2C connections are properly set up.


## References

- [STUSB4500 Datasheet and Documentation](https://www.st.com)
- [EasyMCP2221 Library](https://pypi.org/project/EasyMCP2221/)
- [Microchip MCP2221](https://www.microchip.com)

## Notes

1. If no device is found, a `NotAckError` from the `EasyMCP2221` library will be raised.
2. Ensure the MCP2221 is recognized by your OS, and the required drivers are installed.