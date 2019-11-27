#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: extractor
@author: mario
"""
from pyhanlp import *
from datetime import datetime
import sys
import pandas as pd
import os
import gensim
import numpy as np
from collections import Counter
#from .parser import Parser,DependencyParser
#from .type import *
#Entity,Rhetoric,Noun,Department,Enterprise,Location,University,Other

import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ExtractorException(Exception):
    pass


class EntityExtractor(object):
    def dependencyExtract(self):
        # sentences should be a list of corpus:
        corpus = self.doc.sentences        
        # call ._default_parser
        relObj = []
        vob_entites,rhe,noun = [],[],[]
        for index,each in enumerate(corpus):
            _rel = DependencyParser().default_parser(each)
            # pre-defined entities like: org, people, loc...
            self.entityExtractor(_rel)
            self.rhetoricExtractor(_rel)
            self.nounExtractor(_rel)
            self.predefinedExtractor(_rel)
            # temporarily storage:
            relObj += [_rel]
            sys.stdout.write("\r[DependencyParser] process No.{} sentences ...".format(index+1))
            sys.stdout.flush()
        # here, the index follows the order in sentences:
        self.doc.indexedDependency = relObj
        # verbal extraction part:
        # end. assign
        self.genVocabulary()
        # remained for the rest:
        return self.doc
    
    
    def genVocabulary(self):
        self.doc.vocab = list(set([key for key in self.doc.archive.keys()]))
    
    
    def embedding(self):
        # ./src/wv_model
        pass
    
    def keywordExtract(self):
        # prepare sentence-level corpus:
        indexedSegments = self.doc.indexedSegments
        indexedSegments = [[word[0] for word in sentence if word[1]!="w"] for sentence in indexedSegments]
        indexedSegments = [list(set(sentence)) for sentence in indexedSegments]
        # train word2vec model:
        model = gensim.models.word2vec.Word2Vec(indexedSegments)
        self.doc.wvmodel = model
        def predict_proba(oword, iword):
            iword_vec = model[iword]
            oword = model.wv.vocab[oword]
            oword_l = model.wv.syn0.T
            #oword_l = model.trainables.syn1neg.T
            dot = np.dot(iword_vec, oword_l)
            lprob = -sum(np.logaddexp(0, -dot) + 1*dot) 
            return lprob

        def keywords(s):
            s = [w for w in s if w in model]
            ws = {w:sum([predict_proba(u, w) for u in s]) for w in s} # N*N complexity
            return Counter(ws).most_common(n=10)
        # extract:
        indexedKeywords = []
        for s in indexedSegments:
            indexedKeywords += [keywords(s)]
        # end
        self.doc.keywords = indexedKeywords
        return self.doc


    def predefinedExtractor(self,relObj):
        """
        Pre-defined entity recognition
        :param relObj: Dependency Object
        Note: noun terms are pre-given and the retrieved one is a subset.
        """
        doc = self.doc
        df = pd.DataFrame(relObj.default_dependency)
        try:
            filepath = os.path.abspath(os.path.dirname(__file__))
            ref = open(filepath+"/Policy/src/hanlpNounTermRef.txt","r",encoding="utf8")
        except:
            ref = open("./src/hanlpNounTermRef.txt","r",encoding="utf8")
        # more efficient if using array other than hashmap
        terms = {each.split(",")[0]:each.split(",")[1] for each in ref.read().splitlines()}
        ref.close()
        
        for name,tag in zip(df["LEMMA"],df["POSTAG"]):
            if tag in terms:
                if tag == "nto":
                    doc[name] = Department(name,relObj.default_text)
                elif tag == "ntc":
                    doc[name] = Enterprise(name,relObj.default_text)
                elif tag.startswith("ns"):
                    doc[name] = Location(name,relObj.default_text)
                else:
                    doc[name] = Other(name,terms[tag],relObj.default_text)
        # end        
        self.doc = doc
    

    def rhetoricExtractor(self,relObj):
        doc = self.doc
        """ Rhetoric rule: 形容词和副词 
        :Caution: 在这里没有对修辞进行区分，存在表示不同情感和方向的修辞
        """
        # these are relatively small batches
        _adjRef = ["a","ad","an","ag","al"]
        _advRef = ["d"]
        df = pd.DataFrame(relObj.default_dependency)
        # basically, rhetoric represents "定中关系" in dependency        
        duplicates = pd.DataFrame()
        for each in (_adjRef+_advRef):
            adj = pd.DataFrame()
            sub = df[df["POSTAG"] == each]
            if not sub.empty:
                for i in range(len(sub)):
                    src = sub.iloc[i,]["LEMMA"]
                    srctype = sub.iloc[i,]["POSTAG"]
                    q = relObj.query_by_word(word=src,depth=1,direction="upward",ID=sub.iloc[i,]["ID"])[0]
                    # remove the symbols
                    if "w" in q["POSTAG"].tolist():
                        q = q.drop(index=q[q["POSTAG"]=="w"].index)
                    if not duplicates.empty:
                        if sub.iloc[i,]["ID"] not in duplicates["ID"].tolist():
                            if len(q) > 1:
                                q = q.drop(index=q[q["LEMMA"]==src].index)
                                tar = "".join(q["LEMMA"].tolist())
                                doc[src] = Rhetoric(src=src,tar=tar,srcType=srctype,sentence=relObj.default_text)
                    else:
                        if len(q) > 1:
                            q = q.drop(index=q[q["LEMMA"]==src].index)
                            tar = "".join(q["LEMMA"].tolist())
                            doc[src] = Rhetoric(src=src,tar=tar,srcType=srctype,sentence=relObj.default_text)
                # end
            # end
        # end
        self.doc = doc
    
    
    def nounExtractor(self,relObj):
        """ Noun extractor depends on dependency objects """
        # extract nouns by completion
        doc = self.doc
        df = pd.DataFrame(relObj.default_dependency)
        postags = df["POSTAG"].tolist()
        queryBox = []
        for index,pos in enumerate(postags):
            if pos.startswith("n"):
                row = df.iloc[index,]
                word = row["LEMMA"]
                query = relObj.query_by_word(word,1,ID=row["ID"])[0] # type: list
                if queryBox:
                    if len(query) > 1:
                        for index,each in enumerate(queryBox):
                            if set(query.index).intersection(set(each.index)):
                                if len(query) > len(each):
                                    queryBox.pop(index)
                                    queryBox += [query]
                                else:
                                    next
                            else:
                                queryBox += [query]
                        # end
                    else:
                        queryBox += [query]
                else:
                    queryBox += [query]
            else:
                next
        # end
        _dup = []
        for each in queryBox:
            each = each[each["POSTAG"]!="w"]
            name = "".join(each["LEMMA"].tolist())
            if name not in _dup:
                doc[name] = Noun(name,relObj.default_text)     
            _dup += [name]
            _dup = list(set(_dup))
        
        self.doc = doc
        
    
    def timeExtractor(self):
        # recommend: regexpr
        pass
    
    
    def entityExtractor(self,relObj):
        """ A number of rules: 动宾,并列, 主谓等 """
        # df = pd.DataFrame(dp.default_dependency),
        # `dependency.default_dependency` for query:
        # 动宾关系
        doc = self.doc
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
                    doc[v] = Entity(src=v,tar=obj,decoration=dec,sentence=relObj.default_text)
            else:
                doc[v] = Entity(src=v,tar=obj,decoration=dec,sentence=relObj.default_text)
            duplicates = duplicates.append(q)
        # end 
        self.doc = doc
        
    
    def __init__(self,doc):
        """ EntityExtractor extracts entity from Document 
            Document class will be updated with entities
        """
        self.doc = doc
        # doc contains a really large corpus:
        if not doc.sentences:
            raise ExtractorException("Update Document before execute Extractor.")
        # end 

