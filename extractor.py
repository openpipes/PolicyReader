#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: extractor
@author: mario
"""
from pyhanlp import *
from datetime import datetime
import sys
sys.path.append("C:\\Users\\HiWin10\\Documents\\GitHub\\")
from PolicyReader.parser import Parser,DependencyParser
import pandas as pd
import os

# encoding
_encoding = "utf8"

class ExtractorException(Exception):
    pass

class EntityExtractor(object):
    def extract(self):
        vob_entites = []
        for each in self.indexedDependency:
            vob_entites += [self.verbalExtractor(each)]
        # end. assign 
        self.doc.entity = vob_entites
        return self.doc
    
    def embedding(self):
        # ./src/wv_model
        pass
    
    
    def rhetoricExtractor(self,relObj):
        """ Rhetoric rule: 形容词和副词 """
        # _adjRef = ["a","ad","an","ag","al"]
        # _advRef = ["d"]
        pass
    
    
    
    def verbalExtractor(self,relObj):
        """ A number of rules: 动宾,并列, 主谓等 """
        # df = pd.DataFrame(dp.default_dependency),
        # `dependency.default_dependency` for query:
        # 动宾关系
        df = pd.DataFrame(relObj.default_dependency)
        df_vob = df[df["DEPREL"] == "动宾关系"]
        if df_vob.empty: # no 动宾关系 found
            return []
        vob = []
        duplicates = pd.DataFrame()
        for i in range(len(df_vob)):
            row = df_vob.iloc[i,]
            obj = row["LEMMA"]
            v = df[df["ID"] == row["HEAD"]]  # find the verbal trigger
            v = v["LEMMA"].values[0]            
            q = relObj.query_by_word(word=row["LEMMA"],depth=1,ID=row["ID"])[0]
            q = q.drop(index=(q[q["LEMMA"]==obj].index))
            dec = "".join(q["LEMMA"].tolist())
            # remove the duplicated entity (e.g. subset of the existed)
            if not duplicates.empty:
                if row["ID"] not in duplicates["ID"].values:
                    entity = Entity(src=v,tar=obj,decoration=dec,sentence=relObj._default_text)
                    vob += [entity]
            else:
                entity = Entity(src=v,tar=obj,decoration=dec,sentence=relObj._default_text)
                vob += [entity]
            duplicates = duplicates.append(q)
        # end 
        return vob
        
    
    def __init__(self,doc):
        """ EntityExtractor extracts entity from Document 
            Document class will be updated with entities
        """
        self.doc = doc
        # doc contains a really large corpus:
        if not doc.sentences:
            raise ExtractorException("Update Document before execute Extractor.")
        # sentences should be a list of corpus:
        corpus = doc.sentences        
        # call ._default_parser
        relObj = []
        for index,each in enumerate(corpus):
            relObj += [DependencyParser()._default_parser(each)]
            sys.stdout.write("\r[DependencyParser] process No.%s sentence ..."%(index+1))
            sys.stdout.flush()
        # here, the index follows the order in sentences:
        self.indexedDependency = relObj
       
        