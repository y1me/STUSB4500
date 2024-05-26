




import EasyMCP2221
import time

class STUSB4500(EasyMCP2221.Device):
    # Default I2C address for STUSB4500
    STUSB4500_ADDR = 0x28

    # STUSB4500 NVM Register addresses
    NVM_UNLOCK_REG = 0x95
    NVM_UNLOCK_CODE = 0x47
    NVM_START_ADDR = 0x53
    NVM_SIZE = 0x10  # Assuming NVM size is 16 bytes for this example

    def __init__(self):
        # Initialize the parent class (EasyMCP2221.Device)
        super().__init__()

    def unlock_nvm(self):
        # Write unlock code to the NVM unlock register

        self.I2C_write(
            addr=MEM_ADDR,
            data=b'\x26\x00'
        )
        self.i2c.write_byte_data(self.STUSB4500_ADDR, self.NVM_UNLOCK_REG, self.NVM_UNLOCK_CODE)
        time.sleep(0.01)  # Small delay to ensure the command is processed

    def read_nvm(self):
        # Unlock NVM space
        self.unlock_nvm()

        # Read NVM data from STUSB4500
        nvm_data = []
        for i in range(self.NVM_SIZE):
            # Read each byte from the NVM
            data = self.i2c.read_byte_data(self.STUSB4500_ADDR, self.NVM_START_ADDR + i)
            nvm_data.append(data)
            time.sleep(0.01)  # Small delay to ensure stable communication

        return nvm_data

    def print_nvm_data(self):
        # Read the NVM data
        nvm_data = self.read_nvm()

        # Print the NVM data
        print("STUSB4500 NVM Data:")
        for i, data in enumerate(nvm_data):
            print(f"Byte {i:02X}: {data:02X}")

def main():
    # Create an instance of the STUSB4500 class
    stusb4500 = STUSB4500()

    # Print the NVM data
    stusb4500.print_nvm_data()

if __name__ == "__main__":
    main()





"""


# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mcp = EasyMCP2221.Device()
    MEM_ADDR = 0x28
    MEM_POS = 6

    mcp.I2C_write(
        addr=MEM_ADDR,
        data=b'\x26\x00'
        )
    # Seek EEPROM to position

    mcp.I2C_write(
        addr=MEM_ADDR,
        data=MEM_POS.to_bytes(1, byteorder='little'),
        kind='nonstop')

    # Read max 100 bytes
    dataraw = mcp.I2C_read(
        addr=MEM_ADDR,
        size=143,
        kind='restart',
        timeout_ms=200)

    #data = data.split(b'\0')
    listo = dataraw.hex()
    n = 2
    datalist = [listo[i:i + n] for i in range(0, len(listo), n)]
    print(datalist)
    Offset = 6
    for val in datalist :
        print("Address " + hex(Offset) + " = 0x" + val)
        Offset +=1


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""