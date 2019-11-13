#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: types
@author: mario
"""

class TypeException(Exception):
    pass

class Document(object):
    name = "" # equivalent to title
    vocab = ""
    content = ""
    title = ""
    verb = ""
    rhetoric = ""
    time = ""
    department = ""
    entity = ""
    doctype = ""
    sentences = []
    indexedSegments = []
    def query(self,word):
        """ Query functions as the extraction method of having a micro structure
        :word: the word is to be searched
        """
        
        pass
        
    
    def loader(self,path):
        f = open(path,"r",encoding="utf8")
        lines = f.read().splitlines()
        f.close()
        return "\n".join(lines)
    
        
    def __init__(self,string="",path=None,title=None):
        if path:
            self.__docpath__ = path
            self.content = self.loader(path)
        else:
            self.content = string
        
        if not self.content:
            raise TypeException("Bad document input.")            
        
        """ Title of document should be recognised """
        if title:
            self.title = title
        else:
            pass # run script
            
    
    def __str__(self):
        LIMIT = 50
        return "[Document] : {}...".format(self.content[:LIMIT])
    
    
    #def 
    
    
class Rhetoric(object):
    def __init__(self,name,tag):
        self.name = name
        self.tag = tag
    def __str__(self):
        return "[Rhetoric] name:{},tag:{}".format(self.name,self.tag)
    

class Verb(object):
    def __init__(self,name,tag):
        self.name = name
        self.tag = tag
        
    def __str__(self):
        return "[Verb] name:{},tag:{}".format(self.name,self.tag)
    
        
class Entity(object):
    """ Entity class: each indexed entity should be saved as Entity. """
    def updateTriple(self,ref:str,value):
        """ :ref: name of relationship between entity and value 
            :value: value which is connected to entity
        """
        if self.triples.get(ref):
            self.triples[ref] += [value]
        else:
            self.triples[ref] = [value]
            
    
    def __init__(self,name,tag,**kargs):
        """ *kargs follow in the form of ref=x,value=y """
        self.name = name
        self.tag = tag
        self.triples = {}
            

class Time(object):
    pass

class Department(object):
    pass