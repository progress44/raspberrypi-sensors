#!/usr/bin/env python

import sys, signal, asyncio, time, logging, json, track
from yaml import load
from bosch import Bosch
from enviro import Enviro
from mapping import Mapping
from track import Track

cfg = ""
logger = ""
pid = ""
bosch = ""
loop = asyncio.get_event_loop()

def config():
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    with open("config.yml", "r") as ymlfile:
        cfg = load(ymlfile, Loader=Loader)

    pid = cfg["main"]["pid"]

def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler(cfg["main"]["log_file"], "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]

async def trackFast():
	final = Mapping.fastSensors()
	logger.debug(json.dumps(final))

	# make server request
	r = Track.event(final)



def signal_handler(signal, frame):
    loop.stop()
    sys.exit(0)

async def runner():
	time.sleep(cfg["main"]["interval"])

	await fastSensors()
	asyncio.ensure_future(runner())

	return None

def main():
	signal.signal(signal.SIGINT, signal_handler)
    
    bosch = Bosch()
    
	asyncio.ensure_future(runner())
	loop.run_forever()

if __name__ == "__main__":
	main()