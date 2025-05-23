from setuptools import setup, find_packages

setup(
	name='indoor_crowded_region_detection_database',
	version='1.1.1',
	packages=find_packages(),
	install_requires=['pymongo', 'python-dotenv', 'mongoengine', 'pyproj'],
	include_package_data=True,
	package_data={
		'': ['stubs/*.pyi'],
	},
	description='Database models for indoor region detection',
	author='Group 1 - SW8',
	url='https://github.com/SW8-Indoor-Crowded-Regions/database',
)
