from os.path import exists
import pickle


class MenuDatabase(object):
    """
    A class that contains menu information for restaurants. Contains a data member self.data, which is a dictionary mapping from (unencoded_restaurant_name, locality) to menu.
    """
    def __init__(self):
        self.data = {}

    def save(self, file_name):
        """Pickles the MenuDatabase object to a file.

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

    def __str__(self):
        return str(self.data)


def load(file_name):
    """Loads a pickled MenuDatabase object from a file and returns it.
    Args:
        file_name (str): The filename to load the database from.
    Returns:
        obj (MenuDatabase): The MenuDatabase object pickled to the file
    """

    if not exists(file_name):
        return MenuDatabase()
    else:
        f = open(file_name, 'r+')
        f.seek(0, 0)
        obj = pickle.load(f)
        f.close()
        return obj