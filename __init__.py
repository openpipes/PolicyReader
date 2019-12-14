import os
import numpy as np

try:
    from .planning import Document
except:
    pass

module_path = os.path.dirname(os.path.abspath(__file__))

def read(str_file_dir,*args,**kwargs):
    """ Automatically read Document
    :param: file_or_dir input invalid path of file or folder
    :*args: supporting arguments
    :**kwargs: supporting setting
    """
    if os.path.isfile(str_file_dir) or os.path.isdir(str_file_dir):
        doc = Document(path=str_file_dir)
    else:
        doc = Document(string=str_file_dir)
        
    module_path = os.path.dirname(os.path.abspath(__file__))
    doc.module_path = module_path
    doc.parse()
    return doc
    

def outline(str_file_dir,*args,**kwargs):
    """ Automatically outline Document
    to be continued : 第一章 第二章...
    """
    pass


def keywords(str_file_dir,topn=10,*args,**kwargs):
    """ Automated keywords extraction
    :param: topn controls the number of keywords extracted
    """
    if os.path.isfile(str_file_dir):
        doc = Document(path = str_file_dir)
    else:
        doc = Document(string = str_file_dir)
    doc.parse()
    # keywords:
    keys = [[item[0] for item in each] for each in doc.keywords[:topn]]
    array = np.array(keys)
    keys = list(array.reshape(array.shape[0] * array.shape[1]))
    print("[Keywords] "+", ".join(keys))


def demo():
    module_path = os.path.dirname(os.path.abspath(__file__))
    demo = module_path + "/src/demo.txt"
    doc = read(demo)
    doc.summary()
    