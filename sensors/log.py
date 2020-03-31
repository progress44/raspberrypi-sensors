import logging

class Log(object):

	def __init__(self, file):
		self.logger_setup(file)

	def logger_setup(self, file):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.DEBUG)
		self.logger.propagate = False
		fh = logging.FileHandler(file, "w")
		fh.setLevel(logging.DEBUG)
		self.logger.addHandler(fh)
		self.keep_fds = [fh.stream.fileno()]
	
	def get(self):
		return self.logger