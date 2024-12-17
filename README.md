# ui_tree_similarity
Determine page similarity based on page UI tree structure.

Reference [Li Jingyang, Zhang Bo. Method and device for determining the similarity of web page structure](https://wenku.baidu.com/view/72795fcddf36a32d7375a417866fb84ae55cc3e2?fr=xueshu&_wkts_=1734419226309)

Based on code implementation of [HTMLSimilarity](https://github.com/SPuerBRead/HTMLSimilarity).

[![PyV](https://img.shields.io/badge/python-3.9-brightgreen.svg)]()

Method of use
-----------

```
from utils import get_xml_similarity
from adapter import json2xml

is_similarity, value = get_xml_similarity(doc1, doc2)
```

See `main.py` for details on how to use it.

Three document types are supported:
1. `json` file exported by [Droidbot](https://github.com/honeynet/droidbot)
2. `xml` file exported by `adb uiautomator`
3. `html` file

Description
-----------

##### Input parameters:
* document 1
* document 2
* dimension after dimensionality reduction, default is 5000
* threshold, default is 0.1
* phrase type, default is `'xml'`, optionally `'lxml'`

##### Return value:
* whether or not it is similar
* similar value (similar for `value < tol`, not similar for `value > tol`)