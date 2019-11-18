# policy-reader
Policy reader is a handy toolkit for users to easily understand the components of a regulatory document, policy or legislation file etc. 



### Getting Started

Try examples in `./src` directory and run it in IDE environment:

```python
import logging

__LogFormat__ = "%(asctime)s %(levelname)s %(message)s"

logging.basicConfig(format=__LogFormat__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# change directory to the root of PolicyReader
doc = Document("./src/example_information_guangxi_135.txt")
doc = Parser(doc).parse()
doc = EntityExtractor(doc).dependencyExtract()

# run:
for index in range(1,10,1):
    _ = "*****************\n{}\n-------------------\n{}\n*****************".format("\n".join([each.__str__() for each in doc.entity[index]]),"\n".join([each.__str__() for each in doc.rhetoric[index]]))
    print(_)
```



### TODO List

- Automated labeling for paragraphs
- Improve the precision of extractions