
from EndParser import parse_sentence_end


res1 = parse_sentence_end("特雷莎·梅在《星期日邮报》上发表的一篇文章中声明，让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。 据媒体报道，在周四（2日）的英国地方议会选举中，保守党失去了一千多个席位，而计划夺取数百席位的工党亦失去81席。")
res2 = parse_sentence_end("特雷莎·梅在《星期日邮报》上发表的一篇文章中声明，让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。 伊朗伊斯兰议会议长拉里·贾尼4日声明：“根据伊核协议，伊朗可以生产重水，这并不违反协议。我们将继续进行铀浓缩活动。”")

print(res1)
print(res2)
