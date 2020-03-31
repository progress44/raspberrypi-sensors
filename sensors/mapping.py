import time, bme680
from yaml import load
from envirophat import light, weather, motion, analog, leds

class Mapping(object):
	cfg = ""
    
    def __init__(self):
		# BME680
		self.confg()
		
    def config(self):
		try:
			from yaml import CLoader as Loader
		except ImportError:
			from yaml import Loader

		with open("config.yml", "r") as ymlfile:
			self.cfg = load(ymlfile, Loader=Loader)


    async def fastSensors():
        Enviro.lightsOn()
        time.sleep(0.1)
        Enviro.lightsOff()

        temp 		= {"enviro": Enviro.temp(), "bosch": bosch.temp()}
        pressure 	= {"enviro": Enviro.pressure(), "bosch": bosch.pressure()}
        humidity 	= {"bosch": bosch.humidity()}
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

    async def slowSensors():
        Enviro.lightsOn()
        time.sleep(0.1)
        Enviro.lightsOff()

        aq = await bosch.airQuality()

        final = {
            "time": "%.20f" % time.time(),
            "air_quality": {"bosch": aq}
        }
        
        return final