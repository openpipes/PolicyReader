"""
@theme: NLP
@author: Mario
@date: 2019-12-11
"""
import os
import gensim
import time
import numpy as np
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

############## Word2Vec model ###############
class WVError(Exception):
    pass


class WVOptions(object):
    """ Opts for word2vec where update dicts or change parameters. """
    initOpt = {"sg":1,\
            "size":100,\
            "window":3,\
            "min_count":2,\
            "negative":3,\
            "sample":0.001,\
            "hs":1,\
            "workers":4}
    
    trainOpt = {"total_examples":None,
                "epochs":10
                }
    
    def _setTrainOpt(self,**kwargs):
        for k,v in kwargs.items():
            if k in self.trainOpt:
                self.trainOpt[k] = v
            else:
                next
    
    
    def _setInitOpt(self,**kwargs):
        for k,v in kwargs.items():
            if k in self.initOpt:
                self.initOpt[k] = v
            else:
                next
                
        
    def __init__(self):
        pass


class WVModel(WVOptions):
    def __init__(self,model_path=None):
        super(WVModel,self).__init__()
        if model_path: 
            self.model_path = model_path
        else:
            self.model_path = "./model/"
    
    
    def buildVocabCorpus(self,doc:object):
        corpus = {}
        for token in doc.vocab:
            for obj in doc[token]:
                if obj.sentence in corpus:
                    corpus[obj.sentence] += [token]
                else:
                    corpus[obj.sentence] = [token]
                    
                corpus[obj.sentence] = list(set(corpus[obj.sentence]))
        # end
        # transform from corpus to array:
        corpus = list(corpus.values())
        return corpus
    
    
    def buildSegmentCorpus(self,doc:object):
        """
        Build infavorable corpus using Document Object.
        Make sure Document object is parsed by .parse()
        """
        corpus = []
        for segment in doc.indexedSegments:
            if len(segment) > 0:
                corpus += [[each[0] for each in segment if each[1]!='w']]
        # end
        return corpus
    
    
    def loadModel(self,model_path=None):
        """ Check models at ./model/ """
        # .model file exists:
        if model_path and os.path.isfile(model_path):
            self.model_path = model_path
        
        if any([True for each in os.listdir(self.model_path) if each.endswith(".model")]):
            model_check = [(self.model_path + each,os.path.getctime(self.model_path + each)) for each in os.listdir(self.model_path)]
            model_check = sorted(model_check,key=lambda x:x[1],reverse=True)
            model_name = model_check[-1][0]
            model = gensim.models.word2vec.Word2Vec.load(model_name)
            self.model_name = model_name
            self.model = model
            return True
        else:
            return False
    
    
    def setInitOpt(self,**kwargs):
        self._setInitOpt(**kwargs)
    
    
    def setTrainOpt(self,**kwargs):
        self._setTrainOpt(**kwargs)
        
    
    def updateModel(self,corpusArray:list):
        if self.model:
            self.model.build_vocab(corpusArray, update=True)
            # reset number of examples:
            self.setTrainOpt(total_examples=len(corpusArray))
            self.model.train(corpusArray,**self.trainOpt)
            if not self.model_name:
                self.model_name = self.model_path+"m%s.model"%time.strftime("%Y%m%d%H%M%S",time.localtime())
            self.model.save(self.model_name)
            # save model
            logger.info("[Update Model] model updated at %s "%self.model_name)
            return True
        else:
            return False
            # raise WVError("call .initModel() / .loadModel() first to get model. ")
    
    
    def initModel(self,corpusArray:list):
        """
        Initilise word2vec model iteratively
        :corpusArray: tokenised corpus arranged in a list with article-rows
        """
        # verify the corpusArray:
        if isinstance(corpusArray,list):
            if isinstance(corpusArray[0],list):
                pass
            else:
                raise WVError("Invalid corpus input: only accept two-dimensional array/list. ")
        else:
            raise WVError("Invalid corpus input: only accept two-dimensional array/list. ")
        """corpusArray2=[]
        for each in corpusArray:
            each = list(filter(str.strip, each))
            corpusArray2.append(each)
        corpusArray = corpusArray2"""
        model = gensim.models.word2vec.Word2Vec(corpusArray,**self.initOpt)
        # save model to default folder
        save_path = self.model_path+"m%s.model"%time.strftime("%Y%m%d%H%M%S",time.localtime())
        model.save(save_path)
        logger.info("[Word2vec Model] save model to %s"%save_path)
        self.model = model
        return True
    
    
class Synonmy(WVModel):
    """
    Inherit from WVModel and give Synonmy query
    """
    topn = 5  # default number of synonmy words
    def __init__(self,model_path=None):
        super(Synonmy,self).__init__(model_path)
        pass
    
    def queryOne(self,token) -> dict:
        # load model:
        if self.loadModel():
            if token in self.model.wv.vocab:
                res = self.model.wv.most_similar(token,topn=self.topn)
                # jsonify:
                results = []
                for each in res:                    
                    results += [{"synonmy":each[0],"similarity":each[1]}]
                # end
                qjson = {"q_synonmy":token,"results":results}
                return qjson
            else:
                logger.warning("[Synonmy] no token matches. ")
                return {}
        else: # loaded model
            pass
    
    def queryWords(self,*tokens) -> dict:
        
        pass


class Semantic(object):
    """
    Semantic query: use VOB pattern to find results
    """