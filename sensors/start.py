#!/usr/bin/env python
 
import sys, time
from daemonize import Daemonize
from main import Sensors

pid = "/tmp/test.pid"

def main():
    Sensors()

daemon = Daemonize(app="sensors", pid=pid, action=main)
daemon.start()