import time, logging
from yaml import load
from envirophat import light, weather, motion, analog, leds

class Enviro(object):
	logger = ""
	cfg = ""
	keep_fds = ""
	precision = ""

	def __init__(self):
		# BME680
		self.confg()
		self.logger()
		self.precision = cfg["enviro"]["precision"]

	def config(self):
		try:
			from yaml import CLoader as Loader
		except ImportError:
			from yaml import Loader

		with open("config.yml", "r") as ymlfile:
			self.cfg = load(ymlfile, Loader=Loader)

	def logger(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.DEBUG)
		self.logger.propagate = False
		fh = logging.FileHandler(self.cfg["enviro"]["log_file"], "w")
		fh.setLevel(logging.DEBUG)
		self.logger.addHandler(fh)
		self.keep_fds = [fh.stream.fileno()]

	# EnviroPHAT
	def lightsOn():
		leds.on()

	def lightsOff():
		leds.off()

	def temp():
		try:
			return round(weather.temperature(), self.precision)
		except:
			self.logger.debug('Could not get temperature')

	def pressure():
		try:
			return round(weather.pressure(), self.precision)
		except:
			self.logger.debug('Could not get pressure')

	def light():
		try:
			return light.light()
		except:
			self.logger.debug('Could not get data from light sensor')

	def RGB():
		try:
			return light.rgb()
		except:
			self.logger.debug('Could not get data from light rgb sensor')

	def magnet():
		try:
			magnet = motion.magnetometer()
			return {
				"x": magnet[0],
				"y": magnet[1],
				"z": magnet[2]
			}
		except:
			self.logger.debug('Could not get data from magnetometer')

	def accel():
		try:
			accel = motion.accelerometer()
			return {
				"x": accel[0],
				"y": accel[1],
				"z": accel[2]
			}
		except:
			self.logger.debug('Could not get data from accelerometer')

	def motion():
		try:
			return {
				"magnet": self.magnet(),
				"accelerometer": self.accel(),
				"heading": motion.heading()
			}
		except:
			self.logger.debug('Could not get data from motion sensors')

	def analog():
		try:
			return analog.read_all()
		except:
			self.logger.debug('Could not get analog data')