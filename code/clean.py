from __future__ import unicode_literals

import json
import jieba
from tqdm import tqdm
import math
import re

classes =['烦恼', '游戏', '商业', '娱乐', '生活', '教育', '健康', '电脑', '体育', '汽车']
from tqdm import tqdm

#数据预处理
def MakeWordsSet(words_file):
    words_set = set()
    with open(words_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip()
            if len(word)>0 and word not in words_set: # 去重
                words_set.add(word)
    return words_set

stopwords_file = './data/cn_stopwords.txt'
stopwords_set = MakeWordsSet(stopwords_file)
with open('data/baike_qa_train.json','r') as f: 
    with open("svm_data.json", 'a') as ff: #这个是目标文件（训练集）
        for line in tqdm(f.readlines()):
            train = {}
            js = json.loads(line)
            mainCategory = js['category'].split('-')[0].split('/')[0]
            if mainCategory in classes:
                cleanString = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",js['title']+js['desc']+js['answer'])
                if len(cleanString) < 50: #清除字符串中的特殊字符、转义字符，并且删除过短的例子
                    continue
                train['mainCategory'] = mainCategory
                seg_list = jieba.cut(cleanString)  # 结巴分词
                content =''
                for word in seg_list:
                    if (word in stopwords_set) or ' ' in word or ',' in word  :
                        continue
                    else:
                        content += ',' + word
                train['content'] = content[1:]
                str = json.dumps(train, ensure_ascii=False)
                ff.write(str+'\n')
# with open('data/baike_qa_train.json','r') as f:
#     with open("data/valid_cut_2.json", 'a') as ff:
#         i = 0
#         for line in tqdm(f.readlines()):
#             i += 1
#             if i < 712227:
#                 continue
#             train = {}
#             js = json.loads(line)
#             mainCategory = js['category'].split('-')[0].split('/')[0]
#             if mainCategory in classes:
#                 cleanString = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",js['title']+js['desc']+js['answer'])
#                 if len(cleanString) < 100:
#                     continue
#                 train['mainCategory'] = mainCategory
#                 seg_list = jieba.cut(cleanString)  # 默认是精确模式
#                 content =''
#                 for word in seg_list:
#                     if (word in stopwords_set) or ' ' in word or ',' in word  :
#                         continue
#                     else:
#                         content += ',' + word
#                 train['content'] = content[1:]
#                 str = json.dumps(train, ensure_ascii=False)
#                 ff.write(str+'\n')


        
# wordSet = {} #所有出现过词
# with open('data/1_cut.json', encoding='utf-8') as f:
#     for line in tqdm(f.readlines()):
#         js = json.loads(line)
#         word_list = js['content'].split(',')
#         for word in word_list:
#             # 更新wordSet
#             if(word in wordSet.keys()):
#                 wordSet[word] = wordSet[word]+1
#             else:
#                 wordSet[word] = 1
# with open('data/2_cut.json', encoding='utf-8') as f:
#     for line in tqdm(f.readlines()):
#         js = json.loads(line)
#         word_list = js['content'].split(',')
#         for word in word_list:
#             # 更新wordSet
#             if(word in wordSet.keys()):
#                 wordSet[word] = wordSet[word]+1
#             else:
#                 wordSet[word] = 1
# orderWordSet = sorted(wordSet.items(), key = lambda kv:(kv[1], kv[0]))
# with open("data/new_stopwords.txt", 'a') as ff:  
#     lessOrmore = {}
#     for i in orderWordSet:
#         if i[1] > 18000 :
#             ff.write(i[0]+'\n')