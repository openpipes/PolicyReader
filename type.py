#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: types
@author: mario
"""

class Other(object):
    def __init__(self,name,tag,sentence):
        self.name = name
        self.tag = tag
        self.sentence = sentence
    
    def __str__(self):
        return "[Other] name:{},tag:{}".format(self.name,self.tag)


class Noun(object):
    def __init__(self,name,sentence):
        self.name = name
        self.sentence = sentence
        
    def __str__(self):
        return "[Noun] {}".format(self.name)

    
class Rhetoric(object):
    def __init__(self,src,tar,srcType,sentence):
        self.src = src
        self.tar = tar
        self.srcType = srcType
        self.sentence = sentence
        
    def __str__(self):
        return "[Rhetoric] source:{}({}),target:{}".format(self.src,self.srcType,self.tar)
    

class Verb(object):
    def __init__(self,name,tag,sentence):
        self.name = name
        self.tag = tag
        self.sentence = sentence
        
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
        self.sentence = sentence
        # BIO annotation:
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
    def __init__(self,name,sentence,raw,**kw):
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
    
    
class University(object):
    """ University class
    :param name: the name of university
    :param location: the location of university
    """
    def __init__(self,name,sentence,location="unknown"):
        self.name = name
        self.location = location
        self.sentence = sentence
    
    def __str__(self):
        return "[University] name:{}".format(self.name)


class Location(object):
    """ Location class
    :param name: the name of location
    :param province: administrative region of province
    """
    def __init__(self,name,sentence,province="unknown"):
        self.name = name
        self.province = province
        self.sentence = sentence
        self.long = "" # can be updated
        self.lat = ""
        
    def __str__(self):
        return "[Location] name:{}".format(self.name)
    

class Department(object):
    """ Department class
    :param name: the name of department
    :param tier: the level of department
    """
    def __init__(self,name,sentence,tier="unknown"):
        self.name = name
        self.tier = tier
        self.sentence = sentence
    
    def __str__(self):
        return "[Department] name:{} tier:{}".format(self.name,self.tier)


class Enterprise(object):
    """ Enterprise class
    :param name: the name of enterprise
    :param location: the location of enterprise
    """
    def __init__(self,name,sentence,location="unknown"):
        self.name = name
        self.location = location
        self.sentence = sentence
        
    def __str__(self):
        return "[Enterprise] name:{} location:{}".format(self.name,self.location)

    