# PolicyReader v1.2

Policy Reader is a handy toolkit for users to easily understand the components of a regulatory document. :smile:

This project is issued by the Key Research Plan under the framework of Institutes of Science and Development, Chinese Academy of Sciences (Beijing).

### Getting Started

Try examples in `./src` directory and run it. Before executing the codes, append your module path into `sys.path` with the root of `PolicyReader`:

```python
import sys
sys.append("directory/of/PolicyReader/")
import PolicyReader as pr

# Try demo:
pr.demo()

# Try a random string:
demo_string = "经济综合实力跃上新台阶，地区生产总值、固定资产投资、规模以上工业总产值、金融机构存贷款余额等指标超过万亿元，预计2015年地区生产总值达到1.68万亿元，年均增长10.1%。经济结构调整步伐加快，千亿元产业增至10个，新兴产业加快成长，服务业增加值比重提高，农业农村发展态势良好，城镇化水平提升，“双核驱动、三区统筹”区域发展协调推进。"
doc = pr.read(demo_string)
doc.summary()

# Try a piece of corpus:
doc = pr.read("path/to/PolicyReader/src/example_information_guangxi_135.txt")
doc.summary()
```

### TODO List
In the next stage, semantic search will be added and also the front-end. 

- API services
- Semantic tools