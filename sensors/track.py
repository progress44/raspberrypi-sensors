import logging, json
from requests import post
from log import Log
from config import Config

class Track(object):
    cfg = None
    logger = None

    def __init__(self):
        Track.cfg = Config().get()
        Track.logger = Log(Track.cfg["tracker"]["log_file"]).get()
        self.endpoint = Track.cfg["tracker"]["endpoint"]

    async def event(self, data):
        try:
            # make server request
            Track.logger.debug(json.dumps(data))

            r = post(self.endpoint, headers = {
                    "Content-Type": "application/json; charset=utf-8",
                }, data = json.dumps(data))
            
            Track.logger.debug(r)
            return r
        except:
            Track.logger.debug('Could not make the request to track sensors event')
        return None

