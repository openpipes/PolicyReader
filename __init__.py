import os

__INFO__ = """
		Policy Reader Toolkit (v1.1)
This toolkit contains a list of components helping with parse context and extract useful entities in a Policy or regulatory document.

*************** demo ***************
# import PolicyReader as pr
pr.demo()
# prefer manual operation?
demo_string = "经济综合实力跃上新台阶，地区生产总值、固定资产投资、规模以上工业总产值、金融机构存贷款余额等指标超过万亿元，预计2015年地区生产总值达到1.68万亿元，年均增长10.1%。经济结构调整步伐加快，千亿元产业增至10个，新兴产业加快成长，服务业增加值比重提高，农业农村发展态势良好，城镇化水平提升，“双核驱动、三区统筹”区域发展协调推进。"
doc = pr.read(string=demo_string)
doc.summary()
"""
print(__INFO__)

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


def keywords(str_file_dir,topn=20,*args,**kwargs):
    """ Automated keywords extraction
    :param: topn controls the number of keywords extracted
    """
    doc = Document(str_file_dir)
    doc.parse()
    print("[Keywords] "+", ".join(doc.keywords[:20]))


def demo():
    module_path = os.path.dirname(os.path.abspath(__file__))
    demo = module_path + "/src/demo.txt"
    doc = read(demo)
    doc.summary()
    