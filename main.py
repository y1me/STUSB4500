# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
import EasyMCP2221
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
