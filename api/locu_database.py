"""Pickling the Menu data from locu query"""

from os.path import exists
import sys
import pickle


class MenuDatabase(object):
    def __init__(self):
        self.data = {}

    def save(self, file_name):
        if not exists(file_name):
            f = open(file_name, 'w')
        else:
            f = open(file_name, 'r+')
        f.seek(0, 0)
        pickle.dump(self, f)
        f.close()


def load(file_name):
    if not exists(file_name):
        return MenuDatabase()
    else:
        f = open(file_name, 'r+')
        f.seek(0, 0)
        obj = pickle.load(f)
        f.close()
        return obj