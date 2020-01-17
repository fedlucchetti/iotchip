#from __future__ import division
#import logging
#import time
#import math


# Registers/etc:
PCA9546_ADDRESS     = 0xEE
CHANNEL_0           = 0x01
CHANNEL_1           = 0x02
CHANNEL_2           = 0x04
CHANNEL_3           = 0x08
DISABLE_ALL         = 0x00


def software_reset(i2c=None, **kwargs):
    """Sends a software reset (SWRST) command to all servo drivers on the bus."""
    # Setup I2C interface for device 0x00 to talk to all of them.
    if i2c is None:
        import Adafruit_GPIO.I2C as I2C
        i2c = I2C
    self._device = i2c.get_i2c_device(0x00, **kwargs)
    self._device.writeRaw8(0x06)  # SWRST


class PCA9546(object):
    

    
    def __init__(self, address=PCA9546_ADDRESS, i2c=None, **kwargs):
        """Initialize the PCA9685."""
        # Setup I2C interface for the device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        address_array = [0] * 4
	while not i2c.try_lock():
		pass
	external_addresses = i2c.scan()

    def scan(self):
        self.address_array = [0] * 4
        i = 0
        while i<4:
		while not i2c.try_lock():
			pass

        	if i == 0:
			i2c.writeto(PCA9546_ADDRESS,CHANNEL_0, stop = True)
		elif i == 1:
			i2c.writeto(PCA9546_ADDRESS, CHANNEL_1, stop = True)
		elif i == 2:
			i2c.writeto(PCA9546_ADDRESS, CHANNEL_2, stop = True)
		elif i == 3:
            i2c.writeto(PCA9546_ADDRESS, CHANNEL_3, stop = True)

		temp = i2c.scan()
		for address in self.external_addresses:
			temp.remove(address)
		if len(temp) == 1: 
			self.address_array[i] = temp[0]
		else:
			print('sqdfd')
		i += 1

	i2c.writeto(PCA9546_ADDRESS, DISABLE_ALL, stop = True)

    def select_channel(self, addr):
	self.scan()
	if addr in self.address_array:
		i = self.address_array.index(addr)
		if i == 0:
			i2c.writeto(PCA9546_ADDRESS, CHANNEL_0, stop = True)
 			return true
		elif i == 1:
			i2c.writeto(PCA9546_ADDRESS, CHANNEL_1, stop = True)
                        return true
                elif i == 2:
                        i2c.writeto(PCA9546_ADDRESS, CHANNEL_2, stop = True)
                        return true
                elif i == 3:
                        i2c.writeto(PCA9546_ADDRESS, CHANNEL_3, stop = True)
                        return true
	else:
		return false




