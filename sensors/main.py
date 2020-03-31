#!/usr/bin/env python

import sys, signal, asyncio, time,logging, json, yaml
from daemonize import Daemonize
from daemon import Daemon
from requests import post, get
from bosch import Bosch
from enviro import Enviro

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

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
	enviro.lightsOn()
	time.sleep(1)
	enviro.lightsOff()

	temp 		= {"enviro": enviro.temp(), "bosch": bosch.temp()}
	pressure 	= {"enviro": enviro.pressure(), "bosch": bosch.pressure()}
	humidity 	= {"bosch": bosch.humidity()}
	motion 		= {"enviro": enviro.motion()}
	light 		= {"enviro": { "lumen": enviro.light(), "colors": enviro.rGB()}}
	analog 		= {"enviro": enviro.analog()}

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
	enviro.lightsOn()
	time.sleep(1)
	enviro.lightsOff()

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
	time.sleep(1)
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
