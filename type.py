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
    
        
    def __init__(self,path=None,string="",title=None):
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
    def __init__(self,src,tar,decoration,sentence):
        """ Entity objective follows in a BIO format. """
        self.src = src
        self.tar = tar
        self.decoration = decoration
        self.triple = (src,decoration,tar)
        # BIO annotation:
        bio = ""
        src = ""
        tar = ""
        dec = ""
        for index,char in enumerate(self.src):
            if index == 0:
                src += char + "_B-Verb"
            else:
                src += char + "_I-Verb"
        for index,char in enumerate(self.tar):
            if index == 0:
                tar += char + "_B-Obj"
            else:
                tar += char + "_I-Obj"
        for index,char in enumerate(self.decoration):
            if index == 0:
                dec += char + "_B-Dec"
            else:
                dec += char + "_I-Dec"
        # replace the raw sentence:
        sentence = sentence.replace(self.src,src)
        sentence = sentence.replace(self.tar,tar)
        sentence = sentence.replace(self.decoration,dec)
        self.entityAnnotation = sentence
        
        
    def __str__(self):
        return "[Entity] v:{} d:{} o:{}".format(self.src,self.decoration,self.tar)
            

class Time(object):
    def __init__(self,name,raw):
        pass

class Department(object):
    pass