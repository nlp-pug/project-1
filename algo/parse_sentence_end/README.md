## Usage

The interface is in ```EndParser.py```. Firstly, we need to import the method ```parse_sentence_end```.

```python
from EndParser import parse_sentence_end
result = parse_sentence_end(text)
```

## Example

**Input**

```
特雷莎·梅在《星期日邮报》上发表的一篇文章中声明，让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。

伊朗伊斯兰议会议长拉里·贾尼4日声明：“根据伊核协议，伊朗可以生产重水，这并不违反协议。我们将继续进行铀浓缩活动。”

据媒体报道，在周四（2日）的英国地方议会选举中，保守党失去了一千多个席位，而计划夺取数百席位的工党亦失去81席。

甚至连证监会分管国际合作的副主席方星海都在今年一月份的时候表示，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”。

“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”,证监会分管国际合作的副主席方星海都在今年一月份的时候表示。
```

**Output**

````
[{'author': '特雷莎·梅', 'content': '让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。'},
 {'author': '伊朗伊斯兰议会议长拉里·贾尼', 'content': '：“根据伊核协议，伊朗可以生产重水，这并不违反协议。'}, 
 {'author': '媒体', 'content': '在周四（2日）的英国地方议会选举中，保守党失去了一千多个席位，而计划夺取数百席位的工党亦失去81席。'},
 {'author': '连证监会分管国际的合作副主席方星海都', 'content': '“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”。'}, 
 {'author': '证监会分管国际的合作副主席方星海都', 'content': '“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”,证监会分管国际  合作的副主席方星海都在今年一月份的时候表示。'}]
````