#!/usr/bin/env python

import sys, signal, asyncio, time,logging, json
from daemonize import Daemonize
from daemon import Daemon
from requests import post, get
from bosch import Bosch
from enviro import Enviro
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("config.yml", "r") as ymlfile:
    cfg = load(ymlfile, Loader=Loader)

loop = asyncio.get_event_loop()
pid = cfg["main"]["pid"]
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(cfg["main"]["log_file"], "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]
endpoint = cfg["main"]["endpoint"]
bosch = Bosch()

# Group data
async def fastSensors():
	Enviro.lightsOn()
	time.sleep(0.1)
	Enviro.lightsOff()

	temp 		= {"enviro": Enviro.temp(), "bosch": bosch.temp()}
	pressure 	= {"enviro": Enviro.pressure(), "bosch": bosch.pressure()}
	humidity 	= {"bosch": bosch.humidity()}
	motion 		= {"enviro": Enviro.motion()}
	light 		= {"enviro": { "lumen": Enviro.light(), "colors": Enviro.rGB()}}
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

	logger.debug(json.dumps(final))

	# make server request
	r = post(endpoint, headers = {
        	"Content-Type": "application/json; charset=utf-8",
        }, data = json.dumps(final))
	logger.debug(r)

	return None

async def slowSensors():
	Enviro.lightsOn()
	time.sleep(0.1)
	Enviro.lightsOff()

	aq = await bosch.airQuality()

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
	time.sleep(cfg["main"]["interval"])
	await fastSensors()
	#await slowSensors()
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
