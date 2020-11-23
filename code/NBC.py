from __future__ import unicode_literals

import json
import jieba
from tqdm import tqdm
import math
import re
from pandas import Series,DataFrame
import pandas as pd
import numpy as np

classes =['烦恼', '游戏', '商业', '娱乐', '生活', '教育', '健康', '电脑', '体育', '汽车']   
classesMap ={'烦恼':0, '游戏':1, '商业':2, '娱乐':3, '生活':4, '教育':5, '健康':6, '电脑':7, '体育':8, '汽车':9 }        

def NBC(train,valid):
    wordSet = {} #所有出现过词
    classWordMap = {} #{"体育,全垒打":1024}
    wordTotal = 0 #词总数
    uniqueWordCount = 0 #不重复词总数
    classCountMap = {} #每个类的总词数
    classRatioMap = {} #每个类的词数/词总数
    print("3 2 1 Ready Go !\nTraining 🚗")
    for class1 in classes:
        classCountMap[class1] = 0
    with open(train, encoding='utf-8') as f:
        for line in tqdm(f.readlines()):
            js = json.loads(line)
            mainClass = js['mainCategory']
            word_list = js['content'].split(',')
            for word in word_list:
                wordTotal += 1
                # 更新classWordMap
                key = mainClass +','+ word
                if(key in classWordMap.keys()):
                    classWordMap[key] = classWordMap[key]+1
                else:
                    classWordMap[key] = 1
                # 更新wordSet
                if(word in wordSet.keys()):
                    wordSet[word] = wordSet[word]+1
                else:
                    wordSet[word] = 1
                # 更新classCountMap
                classCountMap[mainClass] += 1
    for class1 in classes:
        classRatioMap[class1] = classCountMap[class1] / wordTotal
    for _ in wordSet:
        uniqueWordCount += 1
    
    print('Validating 🚚')
    x1 = np.zeros((10,10),dtype=int) #矩阵用来记录正确率
    with open(valid,'r') as f:
        for line in tqdm(f.readlines()):
            posibility = {}
            js = json.loads(line)
            mainCategory = js['mainCategory']
            seg_list = js['content'].split(',')
            for class1 in classes:
                posib = math.log(classRatioMap[class1]) 
                for word in seg_list:
                    if word == '':
                        continue
                    key = class1 +','+ word
                    if key in classWordMap:  
                        posib += math.log((classWordMap[key]+1)/(classCountMap[class1]+uniqueWordCount))
                    else:
                        posib += math.log(1/(classCountMap[class1]+uniqueWordCount))
                posibility[class1] = posib
            trueCategory = mainCategory
            predictCategory = max(posibility, key=posibility.get)
            x1[classesMap[predictCategory]][classesMap[trueCategory]] += 1
    df = pd.DataFrame(columns=classes, index=classes, data=x1)
    df["行和"] =df.apply(lambda x:x.sum(),axis =1)
    df.loc["列和"] =df.apply(lambda x:x.sum()) 
    print(df)
    accuracy = {}
    recall = {}
    F1Score = {}
    for class1 in classes:
        accuracy[class1] = df[class1][class1] / df[class1]['列和']
        recall[class1] = df[class1][class1] / df['行和'][class1]
        F1Score[class1] = 2 * accuracy[class1] * recall[class1] / (accuracy[class1] + recall[class1])
    print("accuracy:",accuracy)
    print("recall:",recall)
    print("F1Score:",F1Score)
    print("accuracy_avg:",dict_Avg(accuracy))
    print("recall_avg:",dict_Avg(recall))
    print("F1Score_avg:",dict_Avg(F1Score))


def dict_Avg( Dict ) :
    L = len( Dict )						#取字典中键值对的个数
    S = sum( Dict.values() )				#取字典中键对应值的总和
    A = S / L
    return A

NBC('./data/train_cut.json','./data/valid_cut.json')



