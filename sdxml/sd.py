import numpy as np
from lxml import etree

class Properties:
    """A class for storing and retrieving properties."""

    def __init__(self):
        self.properties = {}

    def get_properties(self):
        """Method to retrieve the properties.

        Returns:
            :obj:`dict`: The dictionary of current properties.

        """

        return self.properties

    def get_property(self, key):
        """Method to retrieve a property.

        Args:
            ``keys`` (:obj:`str` or :obj:`tuple`):  A string or tuple
            of strings giving the key for the property.
        Returns:
            :obj:`str`: The property as a string.

        """

        return str(self.properties[key])

    def update_properties(self, properties):
        """Method to update the properties.

        Args:
            ``properties`` (:obj:`dict`):  A dictionary of properties.
            New properties are added.  Old properties are updated.

        Returns:
            On successful return, the properties have been updated.

        """

        self.properties = {**self.properties, **properties}

class Sample(Properties):
    """A class for storing and retrieving data about a data sample.

    Args:
        ``properties`` (:obj:`dict`, optional): A dictionary of properties.

    """

    def __init__(self, name, properties=None):
        self.properties = {}
        self.name = name
        if properties:
            self.update_properties(properties)

    def get_name(self):
        """Method to retrieve name of sample.

        Return:
            :obj:`str`: The name of the same.

        """

        return self.name

class Collection(Properties):
    """A class for storing and retrieving data about data samples.

    Args:
        ``samples`` (:obj:`list`, optional): A list of individual
        :obj:`sdxml.sd.Sample` objects.

    """

    def __init__(self, samples=None):
        self.properties = {}
        self.collection = {}
        if samples:
            for s in samples:
                self.collection[s.get_name()] = s

    def add_sample(self, sample):
        """Method to add a sample to a collection.

        Args:
            ``sample`` (:obj:`sdxml.sd.Sample`) The sample to be added.

        Return:
            On successful return, the sample has been added.

        """

        self.collection[sample.get_name()] = sample

    def remove_sample(self, sample):
        """Method to remove a sample from a sample collection.

        Args:
            ``sample`` (:obj:`sdxml.sd.Sample`) The sample to be removed.

        Return:
            On successful return, the sample has been removed.

        """

        self.collection.pop(sample.get_name())

    def get(self):
        """Method to retrieve the sample collection as a dictionary.

        Returns:
            :obj:`dict`: A dictionary of the samples.

        """

        return self.collection

