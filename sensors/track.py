import logging, json
from requests import post
from log import Log
from config import Config

class Track(object):
    cfg = None
    logger = None
    endpoint = None
    
    def __init__(self):
        self.cfg = Config().get()
        self.logger = Log(self.cfg["tracker"]["log_file"]).get()
        self.endpoint = self.cfg["tracker"]["endpoint"]

    async def event(self, data):
        try:
            # make server request
            self.logger.debug(json.dumps(data))

            r = post(self.endpoint, headers = {
                    "Content-Type": "application/json; charset=utf-8",
                }, data = json.dumps(data))
            
            self.logger.debug(r)
            return r
        except:
            self.logger.debug('Could not make the request to track sensors event')
        return None

