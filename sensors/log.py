import logging, os

class Log(object):
	loadedFiles = {}

	def __init__(self, file):
		dir_path = os.path.dirname(os.path.realpath(__file__)) +"/"
		self.logger_setup(dir_path + file)

	def logger_setup(self, file):
		for loaded in Log.loadedFiles.keys():
			if loaded == file:
				self.logger = Log.loadedFiles[file]
				return None

		self.logger = logging.getLogger(file)
		self.logger.setLevel(logging.DEBUG)
		self.logger.propagate = False
		fh = logging.FileHandler(file, "w")
		fh.setLevel(logging.DEBUG)
		self.logger.addHandler(fh)
		self.keep_fds = [fh.stream.fileno()]
		Log.loadedFiles[file] = self.logger
	
	def get(self):
		return self.logger