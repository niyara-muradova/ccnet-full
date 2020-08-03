import serial
import os
import configparser


class Device:

    serial = None

    def __init__(self):
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.timeout = 20
        self.serial.writeTimeout = 20

        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE

    def close_port(self):
        if self.serial:
            self.serial.close()
            
def createConfig(configName):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'port': '/dev/ttyUSB0',
                         'baudrate': 9600, 'timeout': 10, 'writeTimeout': 10}
    with open(configName, 'w') as configfile:
        config.write(configfile)

configName = 'default.conf'

if not os.path.exists(configName):
    createConfig(configName)
            
