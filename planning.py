"""
@theme: Planning
"""
import sys
sys.path.append("/Users/mario/Documents/OneDrive/GitHub/")

from PolicyReader import Parser

class Planning(Document):
    def __init__(self,string):
        """ Planning contains possible subclasses:
            
            :Document: objective, planning document itself
            :Rhetoric: objective, rehtoric structure and elements
            :Verb: objective, verbal element
            :Entity: objective, entities embodedd in Document
            :Time: objective, time element extracted
        """
        self.__rawString__ = string
        
        self.Document = ""
        self.Rhetoric = ""
        self.Verb = ""
        self.Entity = ""
        self.Department = ""
        
        return 
    
    