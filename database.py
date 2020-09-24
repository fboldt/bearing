from abc import ABC, abstractmethod

class Database(ABC): 
    """
    Base inteface to implement database wrapper classes.
    """
    @abstractmethod
    def download(self):
        """
        Method responsible for download the raw database files.
        """
        pass

    @abstractmethod
    def segmentate(self):
        """
        Method responsible for transform the raw database files in somthing usable be the framework.
        """
        pass

    @abstractmethod
    def description(self):
        """
        Method responsible for returning a description of the database classes and samples.
        """
        pass    
