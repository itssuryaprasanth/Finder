import pdb
from abc import ABC
from abc import abstractmethod


class LocatorFactory(ABC):

    @abstractmethod
    def build_locator(self):
        pass


class ID(LocatorFactory):

    def __init__(self, attributes):
        self.attr = attributes

    def build_locator(self):
        try:
            attributes = self.attr['attributes']
            if isinstance(attributes['name'], str):
                return {"id": attributes['name']}
            else:
                raise Exception("Error Code: 1004")
        except KeyError:
            return {}


class className(LocatorFactory):
    def __init__(self, attributes):
        self.attr = attributes

    def build_locator(self) -> dict:
        #pdb.set_trace()
        data = {'tag': 'button',
                'attributes': {'id': 'truste-consent-required', 'type': 'button', 'class': ['truste-button3']}}
        try:
            attributes = self.attr['attributes']
            if isinstance(attributes['class'], list) or isinstance(attributes['class'], str):
                return {"className": attributes['class']}
            else:
                raise Exception("Error Code: 1003")
        except KeyError:
            return {}


class Name(LocatorFactory):

    def __init__(self, attributes):
        self.attr = attributes

    def build_locator(self) -> dict | None:
        data = {'tag': 'button',
                'attributes': {'id': 'truste-consent-required', 'type': 'button', 'class': ['truste-button3']}}
        try:
            attributes = self.attr['attributes']
            if isinstance(attributes['name'], list) or isinstance(attributes['name'], str):
                return {"Name": attributes['name']}
            else:
                raise Exception("Error Code: 1004")
        except KeyError:
            return {}
            raise Exception("Error Code: 1004")


class Xpath(LocatorFactory):

    def __init__(self, attributes):
        self.attr = attributes

    def build_locator(self):
        """Syntax: //tagName[@attributeName='Value']"""
        try:
            attributes = self.attr['attributes']
            pass
        except:
            pass


class CssSelector(LocatorFactory):

    def build_locator(self):
        pass


class CreateLocator:
    locators: list = []
    final_set: set = {}

    def __init__(self, attributes):
        self.extract_attributes = attributes

    def mapper(self):
        for iteration, attributes in enumerate(self.extract_attributes, start=1):
            CreateLocator.locators.append(className(attributes).build_locator())
            CreateLocator.locators.append(Name(attributes).build_locator())
            CreateLocator.locators.append(ID(attributes).build_locator())
            print("{} iteration data stored in global list".format(iteration))
            if CreateLocator.locators:
                print("Updated global list {}".format(CreateLocator.locators))
            else:
                print("New global list {}".format(CreateLocator.locators))
        print("****************************************************")
        print("Final global list after removing duplicates in main entry")
        print(CreateLocator.locators)
        return CreateLocator.locators


# if __name__ == '__main__':
#     CreateLocator()