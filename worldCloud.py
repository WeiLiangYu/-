import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.font_manager as fm # 中文字
from collections import Counter
import os
import re


# 設置中文字
fontPath = 'data/微軟正黑體.ttf'
front = fm.FontProperties(fname=fontPath)
plt.rcParams['font.family'] = front.get_name() 

# 指定辭典檔
jieba.set_dictionary('jieba_data/dict.txt.big')

# stop word
with open(file='jieba_data/stop_words2.txt', mode='r', encoding='utf-8') as file:
    stop_words = file.read().split('\n')
with open(file='jieba_data/allow_words.txt', mode='r', encoding='utf-8') as file:
    allow_words = file.read().split('\n')

# 輸出
imgFolder = 'img'
if not os.path.exists(imgFolder):
    os.makedirs(imgFolder)
    print(f'{imgFolder} 已建立。')
else:
    print(f'{imgFolder} 已存在。')

class textCloud:
    def __init__(self, dataName):
        # 導入資料
        self.dataName = dataName
        self.df = pd.read_excel(f'./data/{dataName}.xlsx') # 導入資料
        self.dataNums = len(self.df)
        self.dataFolder = imgFolder + '/' + dataName
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)
            print(f'{self.dataFolder} 已建立。')
        else:
            print(f'{self.dataFolder} 已存在。')
    def toolData(self, targetname):
        """"列出常用工具名稱"""
        targets = self.df[targetname].apply(lambda x: x.split('、'))
        targetCounts = Counter([target for sent in targets for target in sent if '不拘' not in target]) # 跌帶每個列表，再跌帶列表的list，並去除'不拘'
        targetCounts = sorted(targetCounts.items(), key=lambda x: x[1], reverse=True)[:20] # 結果為 list(tuple)
        targetNames = [tool[0] for tool in targetCounts]
        with open('jieba_data/allow_words.txt', 'a', encoding='utf-8') as f:
            for tool in targetNames:
                f.write(tool + '\n')
    def clean_Punctuation(self, text):
        """"刪除標標點符號"""
        text = re.sub(r'[^\w\s]','',text) 
        text = text.replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('[','').replace(']','')
        return text
    def jobContentCloud(self, target):
        seg_stop_words_list = []
        seg_words_list = []
        # 將專有名詞加入自定義詞
        # self.toolData('擅長工具')
        for word in allow_words:
            jieba.add_word(word)
        # 去除標點並jieba分詞
        [seg_words_list.extend(jieba.cut(self.clean_Punctuation(text))) for text in self.df[target]]
        # 過濾雜訊字
        for item in seg_words_list:
            if item not in stop_words:
                seg_stop_words_list.append(item)
        # 繪製文字雲
        seg_stop_counter = Counter(seg_stop_words_list)
        wordcloud = WordCloud(font_path='fonts/TaipeiSansTCBeta-Regular.ttf').generate_from_frequencies(seg_stop_counter)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(f"{imgFolder}/{self.dataName}/{self.dataName}_{target}.png")
        # plt.show()
        # plt.close()
if __name__ == "__main__":
    res = textCloud('資料工程師')
    res.jobContentCloud('工作內容')
    res.jobContentCloud('其他條件')