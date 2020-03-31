#!/usr/bin/env python

import sys, signal, asyncio, time,logging, json
from envirophat import light, weather, motion, analog, leds
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("config.yml", "r") as ymlfile:
    cfg = load(ymlfile, Loader=Loader)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(cfg["enviro"]["log_file"], "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]
precision = cfg["enviro"]["precision"]

class Enviro(object):

    # EnviroPHAT
    def lightsOn():
        leds.on()

    def lightsOff():
        leds.off()

    def temp():
        try:
            return round(weather.temperature(), precision)
        except:
            logger.debug('Could not get temperature')

    def pressure():
        try:
            return round(weather.pressure(), precision)
        except:
            logger.debug('Could not get pressure')

    def light():
        try:
            return light.light()
        except:
            logger.debug('Could not get data from light sensor')

    def rGB():
        try:
            return light.rgb()
        except:
            logger.debug('Could not get data from light rgb sensor')

    def magnet():
        try:
            magnet = motion.magnetometer()
            return {
                "x": magnet[0], 
                "y": magnet[1], 
                "z": magnet[2]
            }
        except:
            logger.debug('Could not get data from magnetometer')

    def envirpAccel():
        try:
            accel = motion.accelerometer()
            return {
                "x": accel[0], 
                "y": accel[1], 
                "z": accel[2]
            }
        except:
            logger.debug('Could not get data from accelerometer')

    def motion():
        try:
            return {
                "magnet": enviroMagnet(), 
                "accelerometer": enviroAccel(), 
                "heading": motion.heading()
            }
        except:
            logger.debug('Could not get data from motion sensors')

    def analog():
        try:
            return analog.read_all()
        except:
            logger.debug('Could not get analog data')