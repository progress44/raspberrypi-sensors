import logging, json
from requests import post
from yaml import load
from log import Log

class Track(object):
    cfg = None
    logger = None
    endpoint = None
    keep_fds = None

    def config(self):
        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader

        with open("config.yml", "r") as ymlfile:
            self.cfg = load(ymlfile, Loader=Loader)

    def __init__(self):
        self.config()
        self.logger = Log(self.cfg["enviro"]["log_file"]).get()
        self.endpoint = self.cfg["tracker"]["endpoint"]

    async def event(self, data):
        try:
            # make server request
            r = post(self.endpoint, headers = {
                    "Content-Type": "application/json; charset=utf-8",
                }, data = json.dumps(data))
            self.logger.debug(r)
            return r
        except:
            self.logger.debug('Could not make the request to track sensors event')
        return None

