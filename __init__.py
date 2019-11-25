"""
		Policy Reader Toolkit (v1.0)
This toolkit contains a list of components helping with parse context and extract useful entities in a Policy or regulatory document.

"""
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


""" for test
doc = Document("./src/example_information_guangxi_135.txt")
doc = Parser(doc).parse()
doc = EntityExtractor(doc).dependencyExtract()
for index in range(100,120,1):
    _ = "*****************\n{}\n-------------------\n{}\n*****************".format("\n".join([each.__str__() for each in doc.entity[index]]),"\n".join([each.__str__() for each in doc.rhetoric[index]]))
    print(_)
""" 

