#!/bin/bash
cd stanford-corenlp-full-2018-10-05
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -props StanfordCoreNLP-chinese.properties -port 9000 -timeout 30000
