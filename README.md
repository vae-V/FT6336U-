# FT6336U-
FT6336U电容式触摸屏控制器IC的MicroPython I2C驱动器。可以用于K210，openMV等。

驱动程序只需要一个MicroPythonI2C要实例化的对象。请参考您的开发板原理图，以建立正确的I2C引脚。

然后，可以使用I2C对象。对于最简单的操作，请使用touch.get_positions()方法返回注册点的X和Y坐标。这将返回最多两个点。如果找不到设备，请确保IC已通电(例如，如果它连接到单独的电源管理芯片)。

import uFT6336U
touch = uFT6336U.FT6336U(i2c_bus)

touch.get_positions()
