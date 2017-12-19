#!/usr/bin/env python

import sys, signal, asyncio, time, bme680
from envirophat import light, weather, motion, analog, leds

class Sensors:

	loop = asyncio.get_event_loop()

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
		burn_in_time = 60
		burn_in_data = []

		boschSensors.set_gas_heater_temperature(320)
		boschSensors.set_gas_heater_duration(150)
		boschSensors.select_gas_heater_profile(0)

		while curr_time - start_time < burn_in_time:
			curr_time = time.time()
			if boschSensors.get_sensor_data() and boschSensors.data.heat_stable:
				gas = boschSensors.data.gas_resistance
				print(gas)
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
			print(air_quality_score)

		boschSensors.set_gas_status(bme680.DISABLE_GAS_MEAS)
		return air_quality_score


	# EnviroPHAT
	def enviroLightsOn():
		leds.on()

	def enviroLightsOff():
		leds.off()

	def enviroTemp():
		return round(weather.temperature(),2)

	def enviroPressure():
		return round(weather.pressure(),2)

	def enviroLight():
		return light.light()

	def enviroRGB():
		return light.rgb()

	def enviroMotion():
		magnet = motion.magnetometer() 
		accel = motion.accelerometer()
		return [[magnet[0], magnet[1], magnet[2]], [accel[0], accel[1], accel[2]], motion.heading()]

	def enviroAnalog():
		return analog.read_all()


	# Group data
	async def fastSensors():
		time.sleep(30)
		boschSetup()

		enviroLightsOn()
		time.sleep(1)

		temp 		= [enviroTemp(), boschTemp()]
		pressure 	= [enviroPressure(), boschPressure()]
		humidity 	= [boschHumidity()]
		motion 		= enviroMotion()
		light 		= [enviroLight(), enviroRGB()]
		analog 		= [enviroAnalog()]

		print(temp, pressure, humidity, motion, light, analog)

		# make server request

		enviroLightsOff()
		asyncio.ensure_future(fastSensors())
		return None

	async def slowSensors():
		enviroLightsOn()
		time.sleep(1)
		enviroLightsOff()
		aq = await boschAirQuality()
		print([aq])

		# make server request

		asyncio.ensure_future(slowSensors())
		return aq

	def signal_handler(signal, frame):  
	    loop.stop()
	    sys.exit(0)


	def __init__:

		signal.signal(signal.SIGINT, signal_handler)
		asyncio.ensure_future(fastSensors())
		asyncio.ensure_future(slowSensors())
		loop.run_forever()
