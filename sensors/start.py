#!/usr/bin/env python

import logging
import sys, time
from daemonize import Daemonize
from main import Sensors

pid = "/tmp/test.pid"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("error.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

def main():
    Sensors()

daemon = Daemonize(app="sensors", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()