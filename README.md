# PolicyReader

Policy reader is a handy toolkit for users to easily understand the components of a regulatory document. :smile:

This project is anchored at a key Research Plan under the framework of Institutes of Science and Development, Chinese Academy of Sciences (Beijing).

### Getting Started

Try examples in `./src` directory and run it. Before executing the codes, change your directory to the root of `PolicyReader`:

```python
import sys
sys.path.append("./")
from PolicyReader.type import *
from PolicyReader.parser import Parser,DependencyParser
from PolicyReader.extractor import EntityExtractor

# make sure the working directory is the root of PolicyReader
doc = Document("./src/example_information_guangxi_135.txt")
doc = Parser(doc).parse()
doc = EntityExtractor(doc).dependencyExtract()

# display:
for index in range(1,10,1):
    _ = "{}\n{}\n{}\n-------------".format(
        "\n".join([each.__str__() for each in doc.entity[index]]),
        "\n".join([each.__str__() for each in doc.rhetoric[index]]),
        "\n".join([each.__str__() for each in doc.noun[index]]))
    print(_)
```



### TODO List

- Automated labeling for paragraphs
- Improve the precision of extractions