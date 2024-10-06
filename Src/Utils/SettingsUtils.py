import os
import json


def getSettings():
    current_directory = os.path.abspath(os.getcwd())
    with open(current_directory + '\\env.json') as config:
        env = json.load(config)
        return env
