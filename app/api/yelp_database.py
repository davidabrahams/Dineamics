"""Pickling the Menu data from locu query"""

from os.path import exists
import sys
import pickle


class YelpDatabase(object):
    """
    A class that contains yelp information for specific queries. Contains a data member self.data, which is a dictionary mapping from (term, location) to a response
    """


    def __init__(self):
        self.data = {}

    def save(self, file_name):
        """Pickles the YelpDatabase object to a file.

        Args:
            file_name (str): The filename to save the database to.
        """
        if not exists(file_name):
            f = open(file_name, 'w')
        else:
            f = open(file_name, 'r+')
        f.seek(0, 0)
        pickle.dump(self, f)
        f.close()


def load(file_name):
    """Loads a pickled YelpDatabase object from a file and returns it.
    Args:
        file_name (str): The filename to load the database from.
    Returns:
        obj (MenuDatabase): The YelpDatabase object pickled to the file
    """
    if not exists(file_name):
        return YelpDatabase()
    else:
        f = open(file_name, 'r+')
        f.seek(0, 0)
        obj = pickle.load(f)
        f.close()
        return obj