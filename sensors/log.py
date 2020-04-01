import logging, os

class Log(object):
	
	def __init__(self, file):
		dir_path = os.path.dirname(os.path.realpath(__file__)) +"/"
		self.logger_setup(dir_path + file)
		self.logger = logging.getLogger(__name__)

	def logger_setup(self, file):
		if self.fh != None or self.keep_fds != None:
			return
			
		self.logger.setLevel(logging.DEBUG)
		self.logger.propagate = False
		self.fh = logging.FileHandler(file, "w")
		self.fh.setLevel(logging.DEBUG)
		self.logger.addHandler(self.fh)
		self.keep_fds = [self.fh.stream.fileno()]
	
	def get(self):
		return self.logger