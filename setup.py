from setuptools import setup, find_packages

setup(
    name="indoor_crowded_region_detection_database",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pymongo",
        "python-dotenv"
        "mongoegine"
    ],
    description="Database models for indoor region detection",
    author="Group 1 - SW8",
    url="https://github.com/SW8-Indoor-Crowded-Regions/database",
)
