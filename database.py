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
    def segment(self):
        """
        Method responsible for transform the raw database files in something usable be the framework.
        """
        pass
