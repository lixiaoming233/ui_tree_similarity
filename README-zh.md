# ui_tree_similarity
根据页面UI树结构判断页面相似性

参考 [李景阳, 张波. 网页结构相似性确定方法及装置](https://wenku.baidu.com/view/72795fcddf36a32d7375a417866fb84ae55cc3e2?fr=xueshu&_wkts_=1734419226309)
与 [HTMLSimilarity](https://github.com/SPuerBRead/HTMLSimilarity) 的代码实现

[![PyV](https://img.shields.io/badge/python-3.9-brightgreen.svg)]()

使用方法
-----------

```
from utils import get_xml_similarity
from adapter import json2xml

is_similarity, value = get_xml_similarity(doc1, doc2)
```

详细的使用方法参见 `main.py`

支持三种文档类型：
1. [Droidbot](https://github.com/honeynet/droidbot) 导出的 `json` 文件
2. `adb uiautomator` 导出的 `xml` 文件
3. `html` 文件

说明
-----------

##### 输入参数：
* 文档1
* 文档2
* 降维后的维数，默认是5000
* 阈值，默认是0.1
* phrase类型，默认是 `'xml'` ，可选 `'lxml'`

##### 返回值：
* 是否相似
* 相似值（`value < tol`时相似，`value > tol`时不相似）