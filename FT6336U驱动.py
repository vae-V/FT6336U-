from Maix import GPIO
from fpioa_manager import fm
import utime
from micropython import const
from machine import I2C

I2C_SDA_PIN = 23
I2C_SCL_PIN = 24

i2c = I2C(I2C.I2C0, mode=I2C.MODE_MASTER,scl=I2C_SCL_PIN, sda=I2C_SDA_PIN)#iic初始化

print('ID：'+str(i2c.scan()))#搜索地址
utime.sleep_ms(300)

I2C_ADDRESS = const(0x38)  #FT6336U寄存器地址

REG_MODE_SWITCH = const(0x00)
REG_TD_STATUS = const(0x02)
REG_P1_XH = const(0x03)
REG_P1_XL = const(0x04)
REG_P1_YH = const(0x05)
REG_P1_YL = const(0x06)
REG_P1_WEIGHT = const(0x07)
REG_P1_MISC = const(0x08)
REG_P2_XH = const(0x09)
REG_P2_XL = const(0x0A)
REG_P2_YH = const(0x0B)
REG_P2_YL = const(0x0C)
REG_P2_WEIGHT = const(0x0D)
REG_P2_MISC = const(0x0E)
REG_ID_G_THGROUP = const(0x80)
REG_ID_G_THDIFF = const(0x85)
REG_ID_G_CTRL = const(0x86)
REG_ID_G_TIMEENTERMONITOR = const(0x87)
REG_ID_G_PERIODACTIVE = const(0x88)
REG_ID_G_PERIODMONITOR = const(0x89)
REG_ID_G_FREQ_HOPPING_EN = const(0x8B)
REG_ID_G_TEST_MODE_FILTER = const(0x96)
REG_ID_G_CIPHER_MID = const(0x9F)
REG_ID_G_CIPHER_LOW = const(0xA0)
REG_ID_G_LIB_VERSION_H = const(0xA1)
REG_ID_G_LIB_VERSION_L = const(0xA2)
REG_ID_G_CIPHER_HIGH = const(0xA3)
REG_ID_G_MODE = const(0xA4)
REG_ID_G_PMODE = const(0xA5)
REG_ID_G_FIRMID = const(0xA6)
REG_ID_G_FOCALTECH_ID = const(0xA8)
REG_ID_G_VIRTUAL_KEY_THRES = const(0xA9)
REG_ID_G_IS_CALLING = const(0xAD)
REG_ID_G_FACTORY_MODE = const(0xAE)
REG_ID_G_RELEASE_CODE_ID = const(0xAF)
REG_ID_G_FACE_DEC_MODE = const(0xB0)
REG_ID_G_STATE = const(0xBC)

DEVICE_MODE_WORKING = const(0x00)
DEVICE_MODE_FACTORY = const(0x40)

CHIP_CODE_FT6336U = const(0x02)

class FT6336U():
    read_buffer = bytearray(2)
    write_buffer = bytearray(1)

    def __init__(self, i2c, rst=None):
        if I2C_ADDRESS not in i2c.scan():
            print("Chip not detected")
        self.i2c = i2c
        self.rst = rst
        if self._readfrom_mem(REG_ID_G_CIPHER_LOW) != CHIP_CODE_FT6336U:
            print("Unsupported chip")
        self.set_mode_working()

    def _readfrom_mem(self, register, num_bytes=1):
        self.i2c.readfrom_mem_into(I2C_ADDRESS, register, self.read_buffer)
        if num_bytes == 1:
            return int.from_bytes(self.read_buffer, "large") >> 8
        if num_bytes == 2:
            return int.from_bytes(self.read_buffer, "large")
        raise ValueError("Unsupported buffer size")

    def _writeto_mem(self, register, *data):
        self.write_buffer[0] = data[0]
        self.i2c.writeto_mem(I2C_ADDRESS, register, self.write_buffer)

    def set_mode_working(self):
        self._writeto_mem(REG_MODE_SWITCH, DEVICE_MODE_WORKING)

    def set_mode_factory(self):
        self._writeto_mem(REG_MODE_SWITCH, DEVICE_MODE_FACTORY)

    def get_points(self):
        return self._readfrom_mem(REG_TD_STATUS)

    def get_p1_x(self):
        return self._readfrom_mem(REG_P1_XH, num_bytes=2) & 0x0FFF

    def get_p1_y(self):
        return self._readfrom_mem(REG_P1_YH, num_bytes=2) & 0x0FFF

    def get_p2_x(self):
        return self._readfrom_mem(REG_P2_XH, num_bytes=2) & 0x0FFF

    def get_p2_y(self):
        return self._readfrom_mem(REG_P2_YH, num_bytes=2) & 0x0FFF

    def get_positions(self):
        positions = []
        num_points = self.get_points()
        if num_points > 0:
            positions.append((self.get_p1_x(),self.get_p1_y()))
        if num_points > 1:
            positions.append((self.get_p2_x(),self.get_p2_y()))
        return positions


touch =FT6336U(i2c)
while True:
  utime.sleep_ms(1000)#检测周期
  print(touch.get_positions())#调用get_positions()获取坐标，支持两点
