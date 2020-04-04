import time, bme680
from enviro import Enviro
from bosch import Bosch
from track import Track

class Mapping(object):
	
	def __init__(self):
		# BME680
		self.enviro = Enviro()
		self.track = Track()

	async def fastSensors(self):
		self.enviro.lightsOn()
		time.sleep(0.1)
		self.enviro.lightsOff()
		self.bosch = Bosch(false)

		temp 		= {"enviro": self.enviro.temp(), "bosch": self.bosch.temp()}
		pressure 	= {"enviro": self.enviro.pressure(), "bosch": self.bosch.pressure()}
		humidity 	= {"bosch": self.bosch.humidity()}
		motion 		= {"enviro": self.enviro.motion()}
		light 		= {"enviro": { "lumen": self.enviro.light(), "colors": self.enviro.RGB()}}
		analog 		= {"enviro": self.enviro.analog()}

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
		self.enviro.lightsOn()
		time.sleep(0.1)
		self.enviro.lightsOff()
		self.bosch = Bosch(true)

		aq = await self.bosch.airQuality()

		final = {
			"time": "%.20f" % time.time(),
			"air_quality": {"bosch": aq}
		}
		
		return final

	async def trackFast(self):
		final = await self.fastSensors()
		# make server request
		await self.track.event(final)

	async def trackSlow(self):
		final = await self.slowSensors()
		# make server request
		await self.track.event(final)

