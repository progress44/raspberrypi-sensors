import logging, json
from requests import post
from yaml import load

class Track(object):
    cfg = ""
    logger = ""
    endpoint = ""
    keep_fds = ""

    def config():
        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader

        with open("config.yml", "r") as ymlfile:
            self.cfg = load(ymlfile, Loader=Loader)
        
    def logger():
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        fh = logging.FileHandler(cfg["tracker"]["log_file"], "w")
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.keep_fds = [fh.stream.fileno()]

    def __init__:
        self.confg()
        self.logger()
        self.endpoint = cfg["tracker"]["endpoint"]

    async def event(data):
        # Group data
        config()
        logger()

        try:
            # make server request
            r = post(endpoint, headers = {
                    "Content-Type": "application/json; charset=utf-8",
                }, data = json.dumps(data))
            self.logger.debug(r)
            return r
        except:
            self.logger.debug('Could not make the request to track sensors event')
        return None

