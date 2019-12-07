"""
@theme: Planning
"""
import os
import re
import hashlib

try:
    from .parser import Parser,DependencyParser
    from .extractor import EntityExtractor
    from .type import *
    from .db import Sync
    from .utils import FileLoader
except:
    pass

import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TypeException(Exception):
    pass


class Document(Parser,EntityExtractor,Sync,FileLoader):
    archive = {} # store vocabulatry and its properties 
    content = ""
    doctype = "" # planning, notification
    indexedSegments = []
    name = "" # equivalent to title
    sentences = []
    title = "" # either extraction, customisation
    md5 = ""
    countTokens = {}
    countObjects = {}
    
    def summary(self):
        if self.countTokens:
            pass
        else:
            get_classname = lambda x:re.findall("'.+\..+'",str(type(x)))[0].split(".")[-1].strip("'") if re.findall("'.+\..+'",str(type(x))) else False
            count_object,count_token = {},{}
            for token in self.vocab:
                # count token:
                if count_token.get(token):
                    count_token[token] += 1
                else:
                    count_token[token] = 1
                # count objects:
                for obj in self.archive[token]:
                    objname = get_classname(obj)
                    if objname:
                        if count_object.get(objname):
                            count_object[objname] += 1
                        else:
                            count_object[objname] = 1
                # end
            # end
            self.countTokens = sorted(count_token.items(),key = lambda x:x[1],reverse=True)
            self.countObjects = sorted(count_object.items(),key = lambda x:x[1],reverst=True)
        # end
        sticker = lambda counts:["{}:{}".format(tup[0],tup[1]) for tup in counts]
        token_stat = """
        ** Top tokens **
        {}
        ** Top token objects **
        {}
        """.format(", ".join(sticker(self.countTokens[:10])),", ".join(sticker(self.countObjects[:10])))
        print(token_stat)
    
    
    def sync(self,db,user,password,tablename,host="localhost",port="5432"): # need checking
        """ Sync with database: mySQL and ES """
        postConfig = {
                "db":db,
                "user":user,
                "password":password,
                "tablename":tablename,
                "host":host,
                "port":port
                }
        self = Sync(self).sync(**postConfig)
        
        
    def parse(self):
        self = EntityExtractor(self).dependencyExtract()
        
    
    def query(self,*args):
        """ Return matched tokens in a list """
        # fuzzy query !!!!
        notInVocab = []
        inVocab = []
        for arg in args:
            if arg in self.vocab:
                inVocab += self.vocab[arg]
            else:
                notInVocab += [arg]
        # end for
        logger.info("[Outlier Words] {}".format(",".join(notInVocab)))
        return inVocab
    
    
    def __contains__(self,key):
        """ Mask for `key in class` function """
        return self[key] is not None
    
    
    def __setitem__(self,key,value):
        # value can be Classes
        if isinstance(value,(Verb,Entity,Noun,Rhetoric)):
            if self.archive.get(key):
                # true: same sentence but diff type; false: same sentence + same type
                old = [True if (each.sentence == value.sentence) and (type(value) == type(each)) else False for each in self.archive[key]]
                
                if not any(old): # duplicated
                    self.archive[key] += [value]
            else:
                self.archive[key] = [value]
                
        elif isinstance(value,(str,Department,Enterprise,Location,University,Other)):
            self.archive[key] = [value]
        
        else:
            raise TypeException("Invalid value for archive.")
            
        
    def __getitem__(self,key):
        if self.archive[key]:
            return self.archive[key]
        else:
            return None
            
        
    def __init__(self,path=None,title="",string=""):
        if path:
            self.__docpath__ = path
            self.content = self.loader(path)
        else:
            self.content = string
        # self.content is surely a string. 
        
        """ Title of document should be recognised """
        if title:
            self.title = title
        else:
            self.title = re.sub("\s+|[\n\t]"," ",self.content[:20]).strip() + "..."
        # gen basic elements through Parser
        self = Parser(self).parse()
        
        logger.info("[LexicalParser] processing %s "%self.title)
        # md5 temporarily assigned by filename
        if path:
            self.md5 = hashlib.md5(os.path.basename(path).encode("utf8")).hexdigest()
        else:
            self.md5 = hashlib.md5(string.encode("utf8")).hexdigest()
            
    
    def __str__(self):
        LIMIT = 50
        return "[Document] : {}...\nwith {} tokens in vocabulary.".format(self.content[:LIMIT],len(self.archive))
    
    
    def loader(self,path):
        return FileLoader(path).load()
