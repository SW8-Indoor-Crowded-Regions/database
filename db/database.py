import os
from dotenv import load_dotenv
from mongoengine import connect


class Database:
	_connected = False

	def __init__(self, uri=None):
		if not Database._connected:
			load_dotenv(override=True)
			self.uri = uri if uri else os.getenv('MONGO_URL')

			if not self.uri:
				raise ValueError('MONGO_URL is not set!')

			connect(host=self.uri)
			Database._connected = True
			print('✔️ Connected to MongoDB')
