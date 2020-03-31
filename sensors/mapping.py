import time, bme680
from yaml import load
from enviro import Enviro
from bosch import Bosch

class Mapping(object):
	cfg = None
	bosch = None
	
	def __init__(self):
		# BME680
		self.config()
		self.bosch = Bosch()

		
	def config(self):
		try:
			from yaml import CLoader as Loader
		except ImportError:
			from yaml import Loader

		with open("config.yml", "r") as ymlfile:
			self.cfg = load(ymlfile, Loader=Loader)


	async def fastSensors(self):
		Enviro.lightsOn()
		time.sleep(0.1)
		Enviro.lightsOff()

		temp 		= {"enviro": Enviro.temp(), "bosch": self.bosch.temp()}
		pressure 	= {"enviro": Enviro.pressure(), "bosch": self.bosch.pressure()}
		humidity 	= {"bosch": self.bosch.humidity()}
		motion 		= {"enviro": Enviro.motion()}
		light 		= {"enviro": { "lumen": Enviro.light(), "colors": Enviro.RGB()}}
		analog 		= {"enviro": Enviro.analog()}

		final 		= {
			"time": "%.20f" % time.time(),
			"temp": temp,
			"pressure": pressure,
			"humidity": humidity,
			"motion": motion,
			"light": light,
			"analog": analog
		}

		return final

	async def slowSensors(self):
		Enviro.lightsOn()
		time.sleep(0.1)
		Enviro.lightsOff()

		aq = await self.bosch.airQuality()

		final = {
			"time": "%.20f" % time.time(),
			"air_quality": {"bosch": aq}
		}
		
		return final