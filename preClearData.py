from __future__ import unicode_literals

import json
import jieba
from tqdm import tqdm
import numpy as np
import pandas as pd

classes =['烦恼', '游戏', '商业', '娱乐', '生活', '教育', '育儿', '健康', '文化', '电脑', '社会民生', '电子数码', '体育', '汽车']

def MakeWordsSet(words_file):
    words_set = set()
    with open(words_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip()
            if len(word)>0 and word not in words_set: # 去重
                words_set.add(word)

    return words_set

def MakeDF(classes,wordSet,wordMap):

    # 构建dataframe
    df = pd.DataFrame(0, classes, wordSet)
    
    # 字典转df
    for key,value in tqdm(wordMap.items()):
        class1 = key.split(',')[0]
        word = key.split(',')[1]
        df[word][class1] = value
    print("正在写入")
    # 保存
    df.to_csv("tzzs_data.csv")



# def write_json_data(json_line,target):
#   #写入json文件
#   str = json.dumps(json_line, ensure_ascii=False)
#   with open(target, 'a') as f:
#       f.write(str+'\n')
#       f.close

# cla ={}

def preClear(source):
    wordSet = {} #所有出现过词
    wordMap = {}
    # 加载停用词表
    stopwords_file = './datasource/cn_stopwords.txt'
    stopwords_set = MakeWordsSet(stopwords_file)
    i = 0
    with open(source, encoding='utf-8') as f:
        while True:
            i+=1
            if i%512 == 0:
                print(i)
            line = f.readline()
            if not line: # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)

            # 求大类
            category = js['category']
            mainCategory = category.split('-')[0].split('/')[0]
            
            # 只计算14个大类的数据
            if mainCategory in classes:
                #结巴分词
                seg_list = jieba.cut(js['answer'])  # 默认是精确模式
                # 统计每个词出现的次数。
                for word in seg_list:
                    #去除停用词
                    if (word in stopwords_set) or word ==' ':
                        continue
                    else:
                        # 更新wordMap
                        key = mainCategory +','+ word
                        if(key in wordMap.keys()):
                            wordMap[key] = wordMap[key]+1
                        else:
                            wordMap[key] = 1
                        # 更新wordSet
                        if(word in wordSet.keys()):
                            wordSet[word] = wordSet[word]+1
                        else:
                            wordSet[word] = 1
            # 统计大类出现次数
            # if(category_top in cla.keys()):
            #     cla[category_top] = cla[category_top]+1
            # else:
            #     cla[category_top] = 1
    with open("./wordMap.json", 'w', encoding="utf-8") as ff:
        json.dump(wordMap, ff, ensure_ascii=False)
    with open("./wordSet.json", 'w', encoding="utf-8") as fff:
        json.dump(wordSet, fff, ensure_ascii=False)
    
    MakeDF(classes,wordSet,wordMap)
    print('Done!')
    # print (cla)


preClear('./datasource/baike_qa_valid.json')

