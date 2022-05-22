import json


class Dict(dict):
	'''
		This class is used to create a dictionary that can be accessed using dot notation as well as bracket notation

		Example
		-------
			>>> config = Dict({"a": 1, "b": 2})
			>>> config.a
			>>> 1
			>>> config["b"]
			>>> 2
	'''
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__


class Configuration(object):
	'''
		This class is used to load the config file

		Parameters
		----------
			None

		Returns
		-------
			None

		Example
		-------
			>>> config = Configuration.load_json("./config.json")
			# This will load the config file
			Using the config file:
			>>> config.inputDirectory
			# This will return the input directory
			or you can use the following:
			>>> config['inputDirectory']
			# This also will return the input directory
	'''
	@staticmethod
	def __load__(data):
		'''
			This function loads the config file

			Parameters
			----------
				data: dict
					The data to load

			Returns
			-------
				dict
					The loaded data

			Example
			-------
				>>> Configuration.__load__(data)
				# This will load the data
		'''
		if type(data) is dict:
			return Configuration.load_dict(data)
		return data

	@staticmethod
	def load_dict(data: dict)-> Dict:
		'''
			This function loads data from a dictionary

			Parameters
			----------
				data: dict
					The data to load

			Returns
			-------
				Dict
					The loaded data

			Example
			-------
				>>> Configuration.load_dict(data)
				# This will load the data
		'''
		result = Dict()
		for key, value in data.items():
			result[key] = Configuration.__load__(value)
		return result

	@staticmethod
	def load_json(configPath: str):
		'''
			This function loads the json config file

			Parameters
			----------
				configPath: str
					The path of the config file

			Returns
			-------
				dict
					The loaded data

			Example
			-------
				>>> Configuration.load_json(configPath)
				# This will load the config file
		'''
		with open(configPath, 'r') as file:
			result = Configuration.__load__(json.loads(file.read()))
		return result
