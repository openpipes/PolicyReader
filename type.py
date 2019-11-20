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
    vocab = "" # can be further indexed for query in both dependencies or structures
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
        try:
            f = open(path,"r",encoding="utf8")
            lines = f.read().splitlines()
        except:
            f = open(path,"r",encoding="gbk")
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
class Noun(object):
    def __init__(self,name):
        self.name = name
    
    def __str__(self):
        return "[Noun] {}".format(self.name)

    
class Rhetoric(object):
    def __init__(self,src,tar,srcType):
        self.src = src
        self.tar = tar
        self.srcType = srcType
    def __str__(self):
        return "[Rhetoric] source:{}({}),target:{}".format(self.src,self.srcType,self.tar)
    

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
    year = ""
    month = ""
    day = ""
    hour = ""
    minute = ""
    second = ""
    def __init__(self,name,raw,**kw):
        """ Time class: recognize time element in corpus
        :name: normalised time format e.g. "2011-11-11 00:00:00"
        :raw: raw textual mention in the raw corpus
            ------
        **kw: a set of {year, month, day, hour, minute, second} attrs
        """
        self.name = name
        self.raw = raw
        if kw:
            for k,v in kw.items():
                if k in dir(self):
                    self.__setattr__(k,v)
    
    def __str__(self):
        return "[Time] time:{},raw:{}".format(self.name,self.raw)
    

class Department(object):
    pass