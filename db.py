"""
@theme: Database
"""
import psycopg2
import hashlib
import pickle
import os
import re
import pandas as pd
from elasticsearch import Elasticsearch,helpers


import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DatabaseException(Exception):
    pass


class ElasticServer(object):
    def connect(self,index,doc_type):
        """ Locally connect to elasticsearch server with correct index and doc_type """
        self.es = Elasticsearch()
        self.index = index # if not existed, create new index automatically
        self.doc_type = doc_type
        return self
    
    
    def create(self,string,**kws):
        # **kws, allow different objects to input different params
        # by default, set value in the collection._source as list    
        if string in self.duplicates:
            return False
        else:
            collection = {
                    "_index":self.index,
                    "_type":self.doc_type,
                    "_id":self.to_md5(string),
                    "_source":{k:[v] for k,v in kws.items()},
                    }
            return collection
        
    
    def to_md5(self,string):
        return hashlib.md5(string.encode("utf8")).hexdigest()


    def exists(self,string):
        """ Return boolean """
        if self.es:
            return self.es.exists(index=self.index,doc_type=self.doc_type,id=self.to_md5(string))     


    def get(self,string):
        if self.es:
            return self.es.get(index=self.index,doc_type=self.doc_type,id=self.to_md5(string))        


    def update(self,string,**kws):
        # string : sentence, source etc. and string here existed
        if self.es:
            duplicates = []
            collection = self.get(string)
            source = collection["_source"]
            for k,v in kws.items():
                if source.get(k):
                    if v not in source[k]:
                        source[k] += [v]
                    else:
                        duplicates += [self.to_md5(string)]
                else:
                     raise DatabaseException("Failed update elasticsearch index: %s"%self.index)
            # end
            logger.warning("[ES update] find {} duplicates: {} ".format(len(duplicates),", ".join(duplicates)))
            
            
    def insert(self,tokenDict:dict):
        # example: tokenDict = {string:**kw}
        collections,updateLog = [],[]
        for token,value in tokenDict.items():
            if not self.exists(token):
                collections += [self.create(token,**value)]
            else:
                self.update(token,**value)
                updateLog += [self.to_md5(token)]
            
        self.response = helpers.bulk(self.es,collections)
        logger.info("[ES insert] insert {} tokens, update {} tokens ".format(len(collections),len(updateLog)))
        
        
    def __init__(self):
        """ Builder with DB Sync : ElasticSearch """
        self.es = ""
        self.duplicates = []

##################### Postgresql #########################

class PsqlServer(object):
    def connect(self,db,user,password,tablename,host,port):
        conn = psycopg2.connect(
                database=db, 
                user=user, 
                password=password, 
                host=host, 
                port=port)
        # connection
        self.table = tablename
        self.server = conn
        return self
        
    
    def close(self):
        if self.server.closed == 1: # 0 - open
            self.server.close()
        else:
            return
    
    def queryColumn(self):
        cursor = self.server.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='%s' and table_schema='public';"%self.table)
        data = cursor.fetchall()
        cursor.close()
        self.server.commit()
        columns = []
        for each in data: columns.append(each[0])
        # note: sql columns rank in a alphabet order
        return columns
    
    
    def queryAll(self):
        self.server.rollback()
        cursor = self.server.cursor()
        cursor.execute("select * from %s;"%self.table)
        data = cursor.fetchall()        
        df = pd.DataFrame(data) # don't allow column indexing
        if not df.empty:
            df.columns = self.queryColumn()
            
        cursor.close()
        self.server.commit()
        return df
    
    
    def exists(self,k,v):
        df = self.queryAll()
        if df.empty:
            return False
        
        if self.duplicates.get(k):
            if v in self.duplicates[k]:
                return True
            else:
                return False
        
        if k in df.columns:
            if v in df[k].tolist():
                logger.warning("[psql exists] {}: {}".format(k,v))
                return True
            else:
                return False
        else:
            raise DatabaseException("No existed column matches.")
    
    
    def to_md5(self,string):
        return hashlib.md5(string.encode("utf8")).hexdigest()

    
    def insert(self,**kws):
        """
        :param: **kws allows correct terms to be typed into server.
        """
        if not self.duplicates: # initialise
            self.duplicates = {k:"" for k in kws.keys()}
            
        if self.server.status:
            # compare current data and data in database:
            DUPLICATED = False
            keys,values = "",""
            for k,v in kws.items():
                keys = "{} {}".format(keys,k)
                values = "{} '{}'".format(values,v)
                if self.exists(k,v):
                    DUPLICATED = True
                    
                self.duplicates[k] = v                
            # syntax:
            if not DUPLICATED:
                try:
                    syntax = "INSERT INTO {} ({}) VALUES({});".format(self.table,keys.replace(" ",",").strip(","),values.replace(" ",",").strip(","))
                    cursor = self.server.cursor()
                    # syntax like: INSERT INTO ...
                    cursor.execute(syntax)
                    cursor.close()
                    self.server.commit()
                    logger.info("[psql insert] 1 record. ")
                except:
                    logger.info("[psql insert] find 1 duplication. ")
                
        else:
            raise DatabaseException("Invalid connection to PostgreSQL")
    
    
    def __init__(self,db,user,password,tablename,host="localhost",port="5432"):
        # local repeat check:
        self.duplicates = {}
        self = self.connect(db,user,password,tablename,host,port)
        if self.server.status:
            pass
        else:
            raise DatabaseException("Failed to connect to database.")


class Sync(PsqlServer,ElasticServer):
    """ Document Sync function """
    def __init__(self,doc:object):
        """
        Basic sync object: update Document with Database dynamics
        :param: Document object
        """
        self.doc = doc
    
    def appendPickle(self,token,obj):
        pass
    
    def existsPickle(self,token):
        pass
    
    
    def syncPickle(self,token,obj):
        """ Local .pkl sync with Document """
        hashValue = hashlib.md5(token.encode("utf8")).hexdigest()
        objectpath = self.doc.module_path+"/objects/"
        
        if not os.path.isdir(objectpath):
            os.makedirs(objectpath)
            logger.warning("[Sync pickle] make folder: %s "%objectpath)
            
        with open("{}{}.pkl".format(objectpath,hashValue),"wb") as pfile:
            pickle.dump(obj,pfile)
        pfile.close()
        logger.info("[Sync pickle] pickled %s "%hashValue)
    
        # if exists, append to pickle file
    
        
    def sync(self,**config):
        # syncToPsql:
        psql = PsqlServer(config.get("db"),config.get("user"),config.get("password"),config.get("tablename"),config.get("host"),config.get("port"))
        
        # syncToES:
        esToken = ElasticServer().connect(index="token",doc_type="policyreader")
        esSentence = ElasticServer().connect(index="sentence",doc_type="policyreader")
        esArticle = ElasticServer().connect(index="article",doc_type="policyreader")
        
        # count:
        get_classname = lambda x:re.findall("'.+\..+'",str(type(x)))[0].split(".")[-1].strip("'") if re.findall("'.+\..+'",str(type(x))) else False
        
        count_object,count_token = {},{}
        tokenDict = {}
        for token in self.doc.vocab:
            # toPsql:
            value = {"token_md5":psql.to_md5(token),"token_value":token}
            psql.insert(**value)
            
            # .md5 shoud be attribute of Document
            objList = self.doc[token]
            articleDict = {self.doc.md5:{"article":self.doc.content}}
            
            # count token:
            omit_obj = 0
            omit = ["Verb"]
            for obj in objList:
                sentenceDict = {
                    esToken.to_md5(obj.sentence):
                        {
                            "sentence":obj.sentence,
                            "article":self.doc.md5
                        }
                    }
                # count objects
                objname = get_classname(obj)
                if objname:
                    if count_object.get(objname):
                        count_object[objname] += 1
                    else:
                        count_object[objname] = 1  
                if objname not in omit:
                    omit_obj += 1
                # count token:
                count_token[token] = omit_obj
                    
            tokenValue = {
                    "token":token,
                    "sentence":list(sentenceDict.keys()),
                    "article":[self.doc.md5]}
            
            tokenDict[esToken.to_md5(token)] = tokenValue            
            # sync sentence:
            esSentence.insert(sentenceDict)
            # sync article:
            esArticle.insert(articleDict)
            # sync object pickling
            self.syncPickle(token,objList)
        # end
        self.doc.countObjects = sorted(count_object.items(),key = lambda x:x[1],reverse=True)
        self.doc.countTokens = sorted(count_token.items(),key = lambda x:x[1],reverse=True)
        psql.close()
        esToken.insert(tokenDict)
        return self.doc
