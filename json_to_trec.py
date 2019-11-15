# -*- coding: utf-8 -*-
# if you are using python 3, you should 
#import urllib2
import urllib.request 
import json

# query = urllib.parse.quote_plus("Russia's intervention in Syria")
# print(query)
query_file = 'test_queries.txt'
queries = open(query_file, encoding="utf8").read().splitlines()
# queries = queries.read().splitlines()
query_set = dict()
for query in queries:
    word = query.split()
    word_length = len(word)
    if word_length>1:
        query_set[word[0]] = ' '.join(word[1:])
print(query_set)
print(len(query_set))
#Output File
IRModel ='BM25'                                      #Change according to model
output_filename = IRModel + '_Model.txt'
query_id = 1
qid = "00" + str(query_id)
length = len(query_set)
#Process and write to output file
for i in range(1,length+1):
    if i < 10:
        id = "00" + str(i)
        filename = str(i) + '.txt'
    else:
        id = "0" + str(i)
        filename = str(i) + '.txt'
    output_for_each_query = open(filename, 'a+', encoding="utf8")
    query_line = query_set[id]
    final_query_text = ''
    for i in query_line:
        if i == ":":
            final_query_text += '\:'
        else:
            final_query_text += i
    query = urllib.parse.quote_plus(final_query_text)
    query = "("+query+")"
    inurl = 'http://localhost:8983/solr/'+IRModel+'/select?q=text_unified_lang%3A' + query + '&qs=100&fl=id%2Cscore%2Ctext_unified_lang&wt=json&indent=true&rows=20&defType=edismax&qf=text_unified_lang^5'
    # inurl = 'http://localhost:8983/solr/'+ IRModel +'/select?q=text_en:'+ query +'&fl=id%2Cscore&wt=json&indent=true&rows=20'
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    doc_length = len(docs)
    rank = 1
    for doc in docs:
        output_for_each_query.write(id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    output_for_each_query.close()