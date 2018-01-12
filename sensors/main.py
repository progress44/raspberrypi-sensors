#!/usr/bin/env python

import sys, signal, asyncio, time, bme680,logging, json
from daemonize import Daemonize
from daemon import Daemon
from envirophat import light, weather, motion, analog, leds
from requests import post, get


loop = asyncio.get_event_loop()
pid = "sensors.pid"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/var/log/sensors.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]
burn_time = 30

endpoint = "http://sensors.progress44.com/v1/environment"

# BME680
boschSensors = bme680.BME680()

def boschSetup():
	boschSensors.set_humidity_oversample(bme680.OS_2X)
	boschSensors.set_pressure_oversample(bme680.OS_4X)
	boschSensors.set_temperature_oversample(bme680.OS_8X)
	boschSensors.set_filter(bme680.FILTER_SIZE_3)
	boschSensors.set_gas_status(bme680.DISABLE_GAS_MEAS)

def boschTemp():

	if boschSensors.get_sensor_data():
		return boschSensors.data.temperature
	else:
		return None

def boschPressure():

	if boschSensors.get_sensor_data():
		return boschSensors.data.pressure
	else:
		return None

def boschHumidity():

	if boschSensors.get_sensor_data():
		return boschSensors.data.humidity
	else:
		return None

async def boschAirQuality():
	boschSensors.set_gas_status(bme680.ENABLE_GAS_MEAS)

	start_time = time.time()
	curr_time = time.time()
	burn_in_time = burn_time
	burn_in_data = []

	boschSensors.set_gas_heater_temperature(320)
	boschSensors.set_gas_heater_duration(150)
	boschSensors.select_gas_heater_profile(0)

	while curr_time - start_time < burn_in_time:
		curr_time = time.time()
		if boschSensors.get_sensor_data() and boschSensors.data.heat_stable:
			gas = boschSensors.data.gas_resistance
			logger.debug("Gas resistance: " + str(gas))
			burn_in_data.append(gas)
			time.sleep(1)

	gas_baseline = sum(burn_in_data[-50:]) / 50.0
	hum_baseline = 40.0
	hum_weighting = 0.25

	if boschSensors.get_sensor_data() and boschSensors.data.heat_stable:
		hum_offset = boschSensors.data.humidity - hum_baseline
		gas_offset = gas_baseline - boschSensors.data.gas_resistance

		if hum_offset > 0:
			hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)
		else:
			hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

		if gas_offset > 0:
			gas_score = (boschSensors.data.gas_resistance / gas_baseline) * (100 - (hum_weighting * 100))
		else:
			gas_score = 100 - (hum_weighting * 100)

		air_quality_score = hum_score + gas_score
		logger.debug(air_quality_score)

	boschSensors.set_gas_status(bme680.DISABLE_GAS_MEAS)
	return air_quality_score


# EnviroPHAT
def enviroLightsOn():
	leds.on()

def enviroLightsOff():
	leds.off()

def enviroTemp():
	return round(weather.temperature(),4)

def enviroPressure():
	return round(weather.pressure(),4)

def enviroLight():
	return light.light()

def enviroRGB():
	return light.rgb()

def enviroMotion():
	magnet = motion.magnetometer() 
	accel = motion.accelerometer()
	return {
		"magnet": {
			"x": magnet[0], 
			"y": magnet[1], 
			"z": magnet[2]
		}, 
		"accelerometer": {
			"x": accel[0], 
			"y": accel[1], 
			"z": accel[2]
		}, 
		"heading": motion.heading()
	}

def enviroAnalog():
	return analog.read_all()


# Group data
async def fastSensors():
	time.sleep(burn_time)
	boschSetup()

	enviroLightsOn()
	time.sleep(1)

	temp 		= {"enviro": enviroTemp(), "bosch": boschTemp()}
	pressure 	= {"enviro": enviroPressure(), "bosch": boschPressure()}
	humidity 	= {"bosch": boschHumidity()}
	motion 		= {"enviro": enviroMotion()}
	light 		= {"enviro": { "lumen": enviroLight(), "colors": enviroRGB()}}
	analog 		= {"enviro": enviroAnalog()}

	final 		= {
		"time": "%.20f" % time.time(),
		"temp": temp,
		"pressure": pressure,
		"humidity": humidity,
		"motion": motion,
		"light": light,
		"analog": analog
	}

	logger.debug(json.dumps(final))

	# make server request
	r = post(endpoint, headers = {
        	"Content-Type": "application/json; charset=utf-8",
        }, data = json.dumps(final))
	logger.debug(r)

	enviroLightsOff()
	return None

async def slowSensors():
	enviroLightsOn()
	time.sleep(1)
	enviroLightsOff()
	aq = await boschAirQuality()
	final = {
		"time": "%.20f" % time.time(),
		"air_quality": {"bosch": aq}
	}
	logger.debug(json.dumps(final))

	# make server request
	r = post(endpoint, headers = {
                "Content-Type": "application/json; charset=utf-8",
        }, data = json.dumps(final))
	logger.debug(r)

	return aq

def signal_handler(signal, frame):
    loop.stop()
    sys.exit(0)

async def runner():
	await fastSensors()
	await slowSensors()
	asyncio.ensure_future(runner())

	return None

def main():
	signal.signal(signal.SIGINT, signal_handler)
	asyncio.ensure_future(runner())
	loop.run_forever()

class DD(Daemon):
	def run(self):
		main()

if __name__ == "__main__":
	daemon = DD(pid)
	daemon.start()

#main()
