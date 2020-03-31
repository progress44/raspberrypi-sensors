#!/usr/bin/env python

import sys, signal, asyncio, time, getopt
from mapping import Mapping
from track import Track
from log import Log
from config import Config

cfg = Config().get()
logger = Log(cfg["main"]["log_file"]).get()
loop = asyncio.get_event_loop()
process = 0

def signal_handler(signal, frame):
    loop.stop()
    sys.exit(0)

async def runner():
    global process
    
    time.sleep(cfg["main"]["interval"])
    
    if (process <= 1):
        await Mapping().trackFast()
    
    if (process == 0 or process == 2):
        await Mapping().trackSlow()

    asyncio.ensure_future(runner())

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfs", ["help", "fast", "slow"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    global process

    for o, a in opts:
        if o == "-f":
            process = 1
        elif o in ("-s"):
            process = 2
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    signal.signal(signal.SIGINT, signal_handler)
    asyncio.ensure_future(runner())
    loop.run_forever()

if __name__ == "__main__":
    main()