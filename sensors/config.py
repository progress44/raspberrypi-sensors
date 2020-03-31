from yaml import load

class Config(object):
	cfg = None

	def __init__(self, file = "config.yml"):
		self.config(file)

	def config(self, file):
		try:
			from yaml import CLoader as Loader
		except ImportError:
			from yaml import Loader

		with open(file, "r") as ymlfile:
			self.cfg = load(ymlfile, Loader=Loader)
	
	def get(self):
		return self.cfg