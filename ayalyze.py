import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm # 中文字
from collections import Counter
import os

# 設置中文字
fontPath = 'data/微軟正黑體.ttf'
front = fm.FontProperties(fname=fontPath)
plt.rcParams['font.family'] = front.get_name() 

# 輸出
imgFolder = 'img'
if not os.path.exists(imgFolder):
    os.makedirs(imgFolder)
    print(f'{imgFolder} 已建立。')
else:
    print(f'{imgFolder} 已存在。')
class ana:
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
    def area(self):
        area = self.df.iloc[:, 5].str[:3] # 只取縣市
        areaCounts = area.value_counts().sort_values(ascending=False)
        # 繪製直方圖
        self.plotimg(xnames=areaCounts.index, nums=areaCounts.values, imgName="工作地區")
    def tool(self):
        tools = self.df['擅長工具'].apply(lambda x: x.split('、'))
        toolCounts = Counter([tool for sent in tools for tool in sent if '不拘' not in tool]) # 跌帶每個列表，再跌帶列表的list，並去除'不拘'
        toolCounts = sorted(toolCounts.items(), key=lambda x: x[1], reverse=True)[:20] # 結果為 list(tuple)
        # 繪製直方圖
        toolNames = [tool[0] for tool in toolCounts]
        toolNums = [tool[1] for tool in toolCounts]
        self.plotimg(xnames=toolNames, nums=toolNums, imgName="擅長工具")
    def ability(self):
        abilitys = self.df['工作技能'].apply(lambda x: x.split('、'))
        abilityCounts = Counter([ability for sent in abilitys for ability in sent if '不拘' not in ability]) # 跌帶每個列表，再跌帶列表的list，並去除'不拘'
        abilityCounts = sorted(abilityCounts.items(), key=lambda x: x[1], reverse=True)[:20] # 結果為 list(tuple)
        # 繪製直方圖
        abilityNames = [tool[0] for tool in abilityCounts]
        abilityNums = [tool[1] for tool in abilityCounts]
        self.plotimg(xnames=abilityNames, nums=abilityNums, imgName="工作技能")  
    def oneData(self, targetname):
        target = self.df[targetname] 
        targetCounts = target.value_counts().sort_values(ascending=False).head(20)
        # 繪製直方圖
        self.plotimg(xnames=targetCounts.index, nums=targetCounts.values, imgName=targetname)
    def listData(self, targetname):
        targets = self.df[targetname].apply(lambda x: x.split('、'))
        targetCounts = Counter([target for sent in targets for target in sent if '不拘' not in target]) # 跌帶每個列表，再跌帶列表的list，並去除'不拘'
        targetCounts = sorted(targetCounts.items(), key=lambda x: x[1], reverse=True)[:20] # 結果為 list(tuple)
        # 繪製直方圖
        targetNames = [tool[0] for tool in targetCounts]
        targetNums = [tool[1] for tool in targetCounts]
        self.plotimg(xnames=targetNames, nums=targetNums, imgName=targetname)  
    def plotimg(self, xnames, nums, imgName):
        plt.figure(figsize=(10, 12))
        plt.bar(xnames, nums, edgecolor='black')
        # # 添加數字顯示
        for i, count in enumerate(nums):
            plt.text(i, count, str(count), ha='center', va='bottom')
        # 設置標題
        plt.suptitle(f'資料數: {self.dataNums}', fontsize=16)
        plt.title(f'{self.dataName}{imgName}')
        plt.xlabel(imgName, labelpad=20)
        plt.ylabel('Counts')
        plt.xticks(rotation=90, ha='center') # 旋轉
        # 調整位置
        plt.subplots_adjust(bottom=0.2)
        # 儲存
        plt.savefig(f'{self.dataFolder}/{self.dataName}_{imgName}.jpg', format='jpg')
        # plt.show()
if __name__ == "__main__":
    data = ana("AI工程師")
    data.oneData("工作經歷")
    data.area()
    data.oneData("產業")
    data.oneData("經歷")
    data.listData("科系要求")
    data.listData("學歷要求")
    data.listData("擅長工具")
    data.listData("工作技能")
