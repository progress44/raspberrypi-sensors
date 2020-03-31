from yaml import load
import os 

class Config(object):
	cfg = None

	def __init__(self, file = "config.yml"):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.config(dir_path + file)

	def config(self, file):
		try:
			from yaml import CLoader as Loader
		except ImportError:
			from yaml import Loader

		with open(file, "r") as ymlfile:
			self.cfg = load(ymlfile, Loader=Loader)
	
	def get(self):
		return self.cfg