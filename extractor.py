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
import numpy as np
from collections import Counter

try:
    from .type import *
    from .parser import *
    from .nlp import WVModel
except:
    pass
#Verb,Entity,Rhetoric,Noun,Department,Enterprise,Location,University,Other

import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# get __file__ path:
__MODULEPATH__ = os.path.dirname(os.path.abspath(__file__))


class ExtractorException(Exception):
    pass


class EntityExtractor(object):
    def dependencyExtract(self):
        # sentences should be a list of corpus:
        corpus = self.doc.sentences
        # call ._default_parser
        relObj = []
        for index,each in enumerate(corpus):
            _rel = DependencyParser().default_parser(each)
            # pre-defined entities like: org, people, loc...
            self.verbalExtractor()            
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
    
    
    def verbalExtractor(self):
        # v::动词 vd::副动词	vf::趋向动词	vg::动词性语素 vi::不及物动词（内动词）	
        # vl::动词性惯用语	 vn::名动词	vshi::动词“是” x::形式动词	vyou::动词“有”
        _verbalRef = ["v","vd","vf","vg","vi","vl","vn","vx"]
        for index,sentence in enumerate(self.doc.indexedSegments):
            for token in sentence:                   
                if token[1] in _verbalRef:
                    self.doc[token[0]] = Verb(token[0],token[1],self.doc.sentences[index])
            # end for
        # end for
    
    
    def keywordExtract(self):
        # prepare sentence-level corpus:
        indexedSegments = self.doc.indexedSegments
        indexedSegments = [[word[0] for word in sentence if word[1]!="w"] for sentence in indexedSegments]
        indexedSegments = [list(set(sentence)) for sentence in indexedSegments]
        # train word2vec model:
        wvm = WVModel(self.doc.module_path + "/model/")
        # wvm.initModel(wvm.buildSegmentCorpus(self.doc))
        wvm.initModel(wvm.buildVocabCorpus(self.doc))
        model = wvm.model

        def predict_proba(oword, iword):
            iword_vec = model[iword]
            oword = model.wv.vocab[oword]
            oword_l = model.wv.syn0.T
            #oword_l = model.trainables.syn1neg.T
            dot = np.dot(iword_vec, oword_l)
            lprob = -sum(np.logaddexp(0, -dot) + 1*dot) 
            return lprob

        def keywords(s,topn=3):
            s = [w for w in s if w in model]
            ws = {w:sum([predict_proba(u, w) for u in s]) for w in s} # N*N complexity
            return Counter(ws).most_common(n=topn)
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
            ref = open(doc.module_path+"/src/hanlpNounTermRef.txt","r",encoding="utf8")
        except:
            ref = open(self.module_path+"/src/hanlpNounTermRef.txt","r",encoding="utf8")
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
        tagger = lambda x:True if x.startswith("n") else False
        subPostag = df[[tagger(each) for each in df["POSTAG"].tolist()]]
        
        if subPostag.empty:
            return None
        
        qTree = {} # insert the tree
        for i,word in zip(subPostag["ID"].tolist(),subPostag["LEMMA"].tolist()):
            keys = qTree.keys()
            query = relObj.query_by_word(word,1,"downward",i)
            leaf = query[0].ID.tolist()
            leaf.remove(i)
            if set(leaf).intersection(set(keys)):
                # if leaf is contained in qLeaf:
                delete = list(set(leaf).intersection(set(keys)))
                [qTree.pop(each) for each in delete]
            # append to the Tree:
            qTree[i] = query[0].ID.tolist()
                
        # end
        skip = []
        IDer = lambda x:[each-1 for each in x]
        treeVec = list(qTree.values())
        treeVec.reverse()
        for v in treeVec:
            if v in skip:
                next
            else:
                if len(v)>2: # more reasonable word sequence:
                    seq = list(range(v[0],v[-1]+1,1))
                    extra = list(set(seq).difference(set(v)))
                    if list(extra) in treeVec:
                        skip += [list(extra)]
                else:
                    seq = v
                    
                each = df.iloc[IDer(seq)]
                each = each[each["POSTAG"]!="w"]
                name = "".join(each["LEMMA"].tolist())
                doc[name] = Noun(name,relObj.default_text)
                
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
        
    
    def __init__(self,doc,module_path=__MODULEPATH__):
        """ EntityExtractor extracts entity from Document 
            Document class will be updated with entities
        """
        self.module_path = module_path
        self.doc = doc
        # doc contains a really large corpus:
        if not doc.sentences:
            raise ExtractorException("Update Document before execute Extractor.")
        # end 

