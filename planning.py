"""
@theme: Planning
"""
try:
    from .parser import Parser,DependencyParser
    from .extractor import EntityExtractor
    from .type import *
except:
    pass

class TypeException(Exception):
    pass


class Document(Parser,EntityExtractor):
    archive = {} # store vocabulatry and its properties 
    content = ""
    doctype = "" # planning, notification
    indexedSegments = []
    name = "" # equivalent to title
    sentences = []
    title = "" # either extraction, customisation
    
    def sync(self,host,port,user,pwd,db,table):
        """ Sync with database: mySQL and ES """
        #syn = Sync(host,port,user,pwd,db,table)
        pass
    
    
    def parse(self):
        self = EntityExtractor(self).dependencyExtract()
        
    
    def query(self,*args):
        """ Return matched tokens in a list """
        notInVocab = []
        inVocab = []
        for arg in args:
            if arg in self.vocab:
                inVocab += vocab[arg]
            else:
                notInVocab += [arg]
        # end for
        print("[Outlier Words] {}".format(",".join(notInVocab)))
        return inVocab
    
    
    def __contains__(self,key):
        """ Mask for `key in class` function """
        return self[key] is not None
    
    
    def __setitem__(self,key,value):
        # value can be Classes
        if isinstance(value,(Verb,Entity,Noun,Rhetoric,Other)):
            if self.archive.get(key):
                self.archive[key] += [value]
            else:
                self.archive[key] = [value]
                
        elif isinstance(value,(str,Department,Enterprise,Location,University)):
            self.archive[key] = [value]
        
        else:
            raise TypeException("Invalid value for archive.")
            
        
    def __getitem__(self,key):
        if self.archive[key]:
            return self.archive[key]
        else:
            return None
            
        
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
        
        # gen basic elements through Parser
        self = Parser(self).parse()
            
    
    def __str__(self):
        LIMIT = 50
        return "[Document] : {}...\nwith {} tokens in vocabulary.".format(self.content[:LIMIT],len(self.archive))
    
    
    def loader(self,path):
        try:
            f = open(path,"r",encoding="utf8")
            lines = f.read().splitlines()
        except:
            f = open(path,"r",encoding="gbk")
            lines = f.read().splitlines()
        f.close()
        return "\n".join(lines)
