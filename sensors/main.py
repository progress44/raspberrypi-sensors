#!/usr/bin/env python

import sys
import time
import bme680

from envirophat import light, weather, motion, analog, leds


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

def boschAirQuality():
	boschSensors.set_gas_status(bme680.ENABLE_GAS_MEAS)

	boschSensors.set_gas_heater_temperature(200)
	boschSensors.set_gas_heater_duration(150)
	boschSensors.select_gas_heater_profile(0)

	sleep(150)

	if sensor.data.heat_stable:
		return sensor.data.gas_resistance
	else:
		return None



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
	return [motion.magnetometer(), motion.accelerometer(), motion.heading()]

def enviroAnalog():
	return analog.read_all()


# Group data
def __init__:
	boschSetup()

	while True:
		enviroLightsOn()
		sleep(1)

		temp 		= [enviroTemp(), boschTemp()]
		pressure 	= [enviroPressure(), boschPressure()]
		humidity 	= [boschHumidity()]
		motion 		= enviroMotion()
		light 		= [enviroLight(), enviroRGB()]
		analog 		= [enviroAnalog()]

		airQuality = [boschAirQuality()]

		enviroLightsOff()
		sleep(5)




