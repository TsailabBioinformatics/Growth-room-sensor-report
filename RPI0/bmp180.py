import Adafruit_BMP.BMP085 as BMP085


def bmp180Data():
    sensor = BMP085.BMP085()
    temperature = '{0:0.2f}'.format(sensor.read_temperature())
    pressure = '{0:0.2f}'.format(sensor.read_pressure())
    return temperature,pressure


#print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
#print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
#print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
#print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

print(bmp180Data())
