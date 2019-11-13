#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: extractor
@author: mario
"""
from pyhanlp import *
from datetime import datetime
import sys
sys.path.append("/Users/mario/Documents/OneDrive/GitHub/")
from PolicyReader.parser import Parser,DependencyParser
import pandas as pd
import os

# encoding
_encoding = "utf8"

class ExtractorException(Exception):
    pass

class RelationExtractor(DependencyParser):
    def embedding(self):
        # ./src/wv_model
        pass
    
    
    def verbalExtractor(self):
        pass
    
    
    def __init__(self,doc):
        """ RelationExtractor extracts relations from Document """
        # doc contains a really large corpus:
        if not doc.sentences:
            raise ExtractorException("Update Document before execute Extractor.")
            
        corpus = doc.sentences
        
        super(RelationExtractor, self).__init__()
    

       
        