




import EasyMCP2221
import time

class STUSB4500(EasyMCP2221.Device):
    # Default I2C address for STUSB4500
    STUSB4500_ADDR = 0x28

    # STUSB4500 NVM Register addresses
    NVM_FTP_KEY             = 0x95
    NVM_FTP_CTRL_0          = 0x96
    NVM_FTP_CTRL_1          = 0x97
    NVM_FTP_CUST_SER        = 0x97
    NVM_UNLOCK_CODE         = 0x47
    NVM_UNLOCK_RESET        = 0x00
    NVM_FTP_CUST_RST_N      = 0x40
    NVM_FTP_CUST_RST        = 0x00
    NVM_START_ADDR          = 0x53
    NVM_SIZE                = 0x10  # Assuming NVM size is 16 bytes for this example

    FTP_CUST_PASSWORD_REG   = 0x95
    FTP_CUST_PASSWORD	    = 0x47
    FTP_CTRL_0              = 0x96
    FTP_CUST_PWR            = 0x80
    FTP_CUST_RST_N          = 0x40
    FTP_CUST_REQ            = 0x10
    FTP_CUST_SECT           = 0x07
    FTP_CTRL_1              = 0x97
    FTP_CUST_FULL_ERASE     = 0xFA
    FTP_CUST_OPCODE_SPA     = 0x07
    FTP_CUST_OPCODE_EMA     = 0x05
    FTP_CUST_OPCODE_SDP     = 0x01
    FTP_CUST_OPCODE_EEPROM  = 0x06
    RW_BUFFER               = 0x53

    READ                    = 0x00
    WRITE_PL                = 0x01
    WRITE_SER               = 0x02
    READ_PL	                = 0x03
    READ_SER                = 0x04
    ERASE_SECTOR            = 0x05
    PROG_SECTOR             = 0x06
    SOFT_PROG_SECTOR        = 0x07

    SECTOR_0                = 0x00
    SECTOR_1                = 0x01
    SECTOR_2                = 0x02
    SECTOR_3                = 0x03
    SECTOR_4                = 0x04
    SECTOR_5                = 0x05
    SECTOR_SIZE             = 8
    SECTOR_COUNT            = 5





    def __init__(self):
        # Initialize the parent class (EasyMCP2221.Device)
        super().__init__()

    def unlock_nvm(self):
        # Write unlock code to the NVM unlock register
        self.stusb4500_write([self.NVM_FTP_KEY,self.NVM_UNLOCK_CODE])
        self.stusb4500_write([self.NVM_FTP_CTRL_0,self.NVM_FTP_CUST_RST_N])
        self.stusb4500_write([self.NVM_FTP_CTRL_0,self.NVM_FTP_CUST_RST])
        time.sleep(0.01)  # Small delay to ensure the command is processed
        self.stusb4500_write([self.NVM_FTP_CTRL_0,self.NVM_FTP_CUST_RST_N])
        #self.i2c.write_byte_data(self.STUSB4500_ADDR, self.NVM_UNLOCK_REG, self.NVM_UNLOCK_CODE)
        #time.sleep(0.01)  # Small delay to ensure the command is processed
    def stusb4500_write(self,payload):
        self.I2C_write(addr=self.STUSB4500_ADDR, data=bytes(payload))
    def stusb4500_read(self, start_address,size):
        self.I2C_write(self.STUSB4500_ADDR, [start_address], kind='nonstop')

        # Read max 100 bytes
        dataraw = self.I2C_read(addr=self.STUSB4500_ADDR, size=size, kind='restart', timeout_ms=200)
        return dataraw

    def read_nvm_sector(self,sector):
        self.stusb4500_write([self.FTP_CTRL_0, self.NVM_FTP_CUST_RST_N | self.FTP_CUST_REQ | sector])
        return self.stusb4500_read(self.NVM_START_ADDR,self.SECTOR_SIZE)

    def write_nvm_sector(self,sector,sector_data):
        self.stusb4500_write([self.RW_BUFFER] + sector_data)
        self.stusb4500_write([self.NVM_FTP_CTRL_1, self.FTP_CUST_OPCODE_SDP])
        self.stusb4500_write([self.NVM_FTP_CTRL_0, self.FTP_CUST_RST_N | self.FTP_CUST_REQ])
        time.sleep(0.01)  # Small delay to ensure the command is processed
        self.stusb4500_write([self.NVM_FTP_CTRL_1, self.FTP_CUST_OPCODE_EEPROM])
        self.stusb4500_write([self.NVM_FTP_CTRL_0, self.FTP_CUST_RST_N | self.FTP_CUST_REQ | sector])
        time.sleep(0.01)  # Small delay to ensure the command is processed

    def cust_full_erase_sector(self):
        self.stusb4500_write([self.NVM_FTP_CTRL_1, self.FTP_CUST_FULL_ERASE])
        self.stusb4500_write([self.NVM_FTP_CTRL_0, self.FTP_CUST_RST_N | self.FTP_CUST_REQ])
        time.sleep(0.01)  # Small delay to ensure the command is processed
        self.stusb4500_write([self.NVM_FTP_CTRL_1, self.FTP_CUST_OPCODE_SPA])
        self.stusb4500_write([self.NVM_FTP_CTRL_0, self.FTP_CUST_RST_N | self.FTP_CUST_REQ])
        time.sleep(0.01)  # Small delay to ensure the command is processed
        self.stusb4500_write([self.NVM_FTP_CTRL_1, self.FTP_CUST_OPCODE_EMA])
        self.stusb4500_write([self.NVM_FTP_CTRL_0, self.FTP_CUST_RST_N | self.FTP_CUST_REQ])
        time.sleep(0.01)  # Small delay to ensure the command is processed

    def unlock_nvm_exit(self):
        self.stusb4500_write([self.NVM_FTP_CTRL_0, self.NVM_FTP_CUST_RST_N, self.NVM_FTP_CUST_RST])
       # self.stusb4500_write([self.NVM_FTP_CTRL_1, self.NVM_FTP_CUST_RST])
        self.stusb4500_write([self.NVM_FTP_KEY,self.NVM_UNLOCK_RESET])

    def read_full_nvm(self):
        # Unlock NVM space
        self.unlock_nvm()

        self.stusb4500_write([self.NVM_FTP_CTRL_1,self.READ])

        sectorData = []
        for sector in range(self.SECTOR_COUNT):
            sectorData.append(self.read_nvm_sector(sector))

        self.unlock_nvm_exit()

        # Read NVM data from STUSB4500

        #nvm_data = []
        #for i in range(self.NVM_SIZE):
            # Read each byte from the NVM
         #   data = self.i2c.read_byte_data(self.STUSB4500_ADDR, self.NVM_START_ADDR + i)
         #   nvm_data.append(data)
          #  time.sleep(0.01)  # Small delay to ensure stable communication

        return sectorData

    def write_full_nvm(self,data):
        # Unlock NVM space
        self.unlock_nvm()

        self.cust_full_erase_sector()

        for sector in range(self.SECTOR_COUNT):
            self.write_nvm_sector(sector, data[sector])

    self.unlock_nvm_exit()

    def print_nvm_data(self):
        # Read the NVM data
        nvm_data = self.read_full_nvm()

        # Print the NVM data
        print("STUSB4500 NVM Data:")
        for i, data in enumerate(nvm_data):
            print("sector " + str(i) + " =")
            print(data)
            for b in data:
                print(hex(b), end='')
            print("\n")

def main():
    STUSB4500_Config = [
         [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],# Data_C0, Data_C1, Data_C2, Data_C3, Data_C4, Data_C5, Data_C6, Data_C7
         [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],# Data_C8, Data_C9, Data_CA, Data_CB, Data_CC, Data_CD, Data_CE, Data_CF
         [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],# Data_D0, Data_D1, Data_D2, Data_D3, Data_D4, Data_D5, Data_D6, Data_D7
         [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],# Data_D8, Data_D9, Data_DA, Data_DB, Data_DC, Data_DD, Data_DE, Data_DF
         [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # Data_E0, Data_E1, Data_E2, Data_E3, Data_E4, Data_E5, Data_E6, Data_E7
         # Data_C0, Data_C1, Data_C2, Data_C3, Data_C4, Data_C5, Data_C6, Data_C7
     ]
    # Create an instance of the STUSB4500 class
    stusb4500 = STUSB4500()


    print("NVM before writing")
    stusb4500.print_nvm_data()
    stusb4500.write_full_nvm(STUSB4500_Config)
    print("NVM after writing")
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