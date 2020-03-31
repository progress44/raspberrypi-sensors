#!/usr/bin/env python

import sys, signal, asyncio, time, getopt
from mapping import Mapping
from track import Track
from log import Log
from config import Config

cfg = None
logger = None
pid = None
loop = asyncio.get_event_loop()

def signal_handler(signal, frame):
    loop.stop()
    sys.exit(0)

async def runner():
    time.sleep(cfg["main"]["interval"])

    await Mapping().trackFast()
    await Mapping().trackSlow()

    asyncio.ensure_future(runner())

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    cfg = Config().get()
    logger = Log(cfg["main"]["log_file"]).get()

    # opts = getopt.getopt(argv, ["hfs"])

    # print(opts)
    
    asyncio.ensure_future(runner())
    loop.run_forever()

if __name__ == "__main__":
    main()