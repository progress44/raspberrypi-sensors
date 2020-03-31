#!/usr/bin/env python

import sys, signal, asyncio, time, bme680,logging, json, yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(cfg["bosch"]["log_file"], "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]
burn_time = cfg["bosch"]["burn_time"]

class Bosch(object):
	sensors = ""

	def setup(self):
		self.sensors.set_humidity_oversample(bme680.OS_2X)
		self.sensors.set_pressure_oversample(bme680.OS_4X)
		self.sensors.set_temperature_oversample(bme680.OS_8X)
		self.sensors.set_filter(bme680.FILTER_SIZE_3)
		self.sensors.set_gas_status(bme680.ENABLE_GAS_MEAS)

		self.sensors.set_gas_heater_temperature(cfg["bosch"]["heater_temp"])
		self.sensors.set_gas_heater_duration(cfg["bosch"]["heater_duration"])
		self.sensors.select_gas_heater_profile(cfg["bosch"]["heater_profile"])

	def __init__(self):
		# BME680
		self.sensors = bme680.BME680()
		setup()

	def temp(self):
		if self.sensors.get_sensor_data():
			return self.sensors.data.temperature
		else:
			return None

	def pressure(self):
		if self.sensors.get_sensor_data():
			return self.sensors.data.pressure
		else:
			return None

	def humidity(self):
		if self.sensors.get_sensor_data():
			return self.sensors.data.humidity
		else:
			return None

	async def airQuality(self):
		self.sensors.set_gas_status(bme680.ENABLE_GAS_MEAS)

		start_time = time.time()
		curr_time = time.time()
		burn_in_time = burn_time
		burn_in_data = []

		self.sensors.set_gas_heater_temperature(320)
		self.sensors.set_gas_heater_duration(150)
		self.sensors.select_gas_heater_profile(0)

		while curr_time - start_time < burn_in_time:
			curr_time = time.time()
			if self.sensors.get_sensor_data() and self.sensors.data.heat_stable:
				gas = self.sensors.data.gas_resistance
				logger.debug("Gas resistance: " + str(gas))
				burn_in_data.append(gas)
				time.sleep(1)

		gas_baseline = sum(burn_in_data[-50:]) / 50.0
		hum_baseline = 40.0
		hum_weighting = 0.25

		if self.sensors.get_sensor_data() and self.sensors.data.heat_stable:
			hum_offset = self.sensors.data.humidity - hum_baseline
			gas_offset = gas_baseline - self.sensors.data.gas_resistance

			if hum_offset > 0:
				hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)
			else:
				hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

			if gas_offset > 0:
				gas_score = (self.sensors.data.gas_resistance / gas_baseline) * (100 - (hum_weighting * 100))
			else:
				gas_score = 100 - (hum_weighting * 100)

			air_quality_score = hum_score + gas_score
			logger.debug(air_quality_score)

		self.sensors.set_gas_status(bme680.DISABLE_GAS_MEAS)
		return air_quality_score
