import time
from envirophat import light, weather, motion, analog, leds
from log import Log
from config import Config

class Enviro(object):
	logger = None
	cfg = None
	keep_fds = None
	precision = None

	def __init__(self):
		# BME680
		self.cfg = Config().get()
		self.logger = Log(self.cfg["enviro"]["log_file"]).get()
		self.precision = self.cfg["enviro"]["precision"]

	# EnviroPHAT
	def lightsOn(self):
		leds.on()

	def lightsOff(self):
		leds.off()

	def temp(self):
		try:
			return round(weather.temperature(), self.precision)
		except:
			self.logger.debug('Could not get temperature')

	def pressure(self):
		try:
			return round(weather.pressure(), self.precision)
		except:
			self.logger.debug('Could not get pressure')

	def light(self):
		try:
			return light.light()
		except:
			self.logger.debug('Could not get data from light sensor')

	def RGB(self):
		try:
			return light.rgb()
		except:
			self.logger.debug('Could not get data from light rgb sensor')

	def magnet(self):
		try:
			magnet = motion.magnetometer()
			return {
				"x": magnet[0],
				"y": magnet[1],
				"z": magnet[2]
			}
		except:
			self.logger.debug('Could not get data from magnetometer')

	def accel(self):
		try:
			accel = motion.accelerometer()
			return {
				"x": accel[0],
				"y": accel[1],
				"z": accel[2]
			}
		except:
			self.logger.debug('Could not get data from accelerometer')

	def motion(self):
		try:
			return {
				"magnet": self.magnet(),
				"accelerometer": self.accel(),
				"heading": motion.heading()
			}
		except:
			self.logger.debug('Could not get data from motion sensors')

	def analog(self):
		try:
			return analog.read_all()
		except:
			self.logger.debug('Could not get analog data')