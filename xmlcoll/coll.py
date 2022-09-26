from lxml import etree

max_tags = 5   # Maximum number of tags.

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

    def update_properties(self, properties):
        """Method to update the properties.

        Args:
            ``properties`` (:obj:`dict`):  A dictionary of properties.
            New properties are added.  Old properties are updated.  The
            keys for the dictionary entries are `name` and up to five
            optional tags labeled `tag1`, `tag2`, ..., `tag5`.

        Returns:
            On successful return, the properties have been updated.

        """

        for prop in properties:
            if isinstance(prop, tuple):
                assert(len(prop) <= max_tags + 1)

        self.properties = {**self.properties, **properties}


class Item(Properties):
    """A class for storing and retrieving data about a data item.

    Args:
        ``properties`` (:obj:`dict`, optional): A dictionary of properties.

    """

    def __init__(self, name, properties=None):
        self.properties = {}
        self.name = name
        if properties:
            self.update_properties(properties)

    def get_name(self):
        """Method to retrieve name of item.

        Return:
            :obj:`str`: The name of the same.

        """

        return self.name


class Collection(Properties):
    """A class for storing and retrieving data about data items.

    Args:
        ``items`` (:obj:`list`, optional): A list of individual
        :obj:`sdxml.sd.Item` objects.

    """

    def __init__(self, items=None):
        self.properties = {}
        self.collection = {}
        if items:
            for s in items:
                self.collection[s.get_name()] = s

    def add_item(self, item):
        """Method to add a item to a collection.

        Args:
            ``item`` (:obj:`sdxml.sd.Item`) The item to be added.

        Return:
            On successful return, the item has been added.

        """

        self.collection[item.get_name()] = item

    def remove_item(self, item):
        """Method to remove a item from a item collection.

        Args:
            ``item`` (:obj:`sdxml.sd.Item`) The item to be removed.

        Return:
            On successful return, the item has been removed.

        """

        self.collection.pop(item.get_name())

    def get(self):
        """Method to retrieve the item collection as a dictionary.

        Returns:
            :obj:`dict`: A dictionary of the items.

        """

        return self.collection

    def write_to_xml(self, file, pretty_print=True):
        """Method to write the collection to XML.

        Args:
            ``file`` (:obj:`str`) The output file name.

            ``pretty_print`` (:obj:`bool`, optional): If set to True,
            routine outputs the xml in nice indented format.

        Return:
            On successful return, the item collection data have been
            written to the XML output file.

        """

        root = etree.Element("collection")
        xml = etree.ElementTree(root)

        self._add_properties(root, self)

        my_coll = self.get()

        items = etree.SubElement(root, "items")

        for s in my_coll:

            my_item = etree.SubElement(items, "item")

            my_name = etree.SubElement(my_item, "name")

            my_name.text = my_coll[s].get_name()

            self._add_properties(my_item, my_coll[s])

        xml.write(file, pretty_print=pretty_print)

    def _add_properties(self, my_element, my_object):
        my_props = my_object.get_properties()

        if len(my_props):
            props = etree.SubElement(my_element, "properties")
            for prop in my_props:
                if isinstance(prop, str):
                    my_prop = etree.SubElement(props, "property", name=prop)
                elif isinstance(prop, tuple):
                    my_prop = etree.SubElement(props, "property", name=prop[0])
                    for i in range(1, len(prop)):
                        my_tag = "tag" + str(i)
                        my_prop.attrib[my_tag] = prop[i]

                my_prop.text = str(my_props[prop])

    def update_from_xml(self, file, xpath=""):
        """Method to update a item collection from an XML file.

        Args:
            ``file`` (:obj:`str`) The name of the XML file from which to update.

            ``xpath`` (:obj:`str`, optional): XPath expression to select
            items.  Defaults to all items.

        Returns:
            On successful return, the item collection has been updated.

        """

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.parse(file, parser)
        xml.xinclude()

        coll = xml.getroot()

        self._update_properties(coll, self)

        el_item = coll.xpath("//item" + xpath)

        for s in el_item:
            name = s.xpath(".//name")
            my_item = Item(name[0].text)
            self._update_properties(s, my_item)

            self.add_item(my_item)

    def _update_properties(self, my_element, my_object):
        el_props = my_element.xpath("properties")

        if len(el_props) > 0:
            props = el_props[0].xpath("property")

            my_props = {}
            for prop in props:
                attributes = prop.attrib
                my_keys = attributes.keys()
                if len(my_keys) == 1:
                    my_props[attributes[my_keys[0]]] = prop.text
                else:
                    tup = ()
                    for i in range(len(my_keys)):
                        tup += (attributes[my_keys[i]],)
                    my_props[tup] = prop.text

            my_object.update_properties(my_props)
