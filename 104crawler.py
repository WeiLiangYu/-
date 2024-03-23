import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote # 轉為URL編碼
import time
import os

out_folder = "data"
if not os.path.exists(out_folder):
    os.makedirs(out_folder)
    print(f'{out_folder} 資料夾建立完成。')
else:
    print(f'{out_folder} 資料夾已存在。')
headers = {'Referer': 'https://www.104.com.tw/jobs/main/'}

def crawler104Jobs(jobWord, pages):
    keyword = quote(jobWord, encoding='utf-8')
    pages = list(range(1, pages+1))
    data_list = []
    for page in pages:
        url = f"https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword={keyword}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page={page}&mode=s&jobsource=cmw_redirect&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
        jobs = json.loads(requests.get(url=url, headers=headers).text)['data']['list']
        for job in jobs:
            # 從搜尋的 api 取得當頁所有職缺的簡介
            data = {}
            data.update({
                "職位": job['jobName'],
                "薪水": job['salaryDesc'],
                "公司": job['custName'],
                "領域": '、'.join(job['major'][:-1]) if job['major'] else '', # 把list使用"、"連接
                "地區": job['jobAddrNoDesc'],
                "產業": job['coIndustryDesc'],
                "規模": job['tags'].get('emp', {}).get('desc', '') if job['tags'] else " ",
                "學歷": job['optionEdu'] if job['optionEdu'] else " ",
                "經歷": job['periodDesc'],
                "應徵人數": job['applyDesc'],
                "link": 'https:' + job['link']['job'],
            })
            # 從每個職缺的詳細頁面取得工作內容...詳細內容
            detail = requests.get(data['link'], headers=headers)
            soup = BeautifulSoup(detail.text, 'html.parser')
            job_categorys_div = (soup.select('div.job-description-table.row div.col.p-0.list-row__data div.v-popper'))
            job_categorys = [div.get_text(strip=True) for div in job_categorys_div]
            requirements = soup.select('div.dialog.container-fluid div.job-requirement-table.row div.list-row.row.mb-2 div.t3.mb-0')
            data.update({
                '工作內容': soup.select('div.job-description p')[0].text,
                "職務類別": "、".join(job_categorys[:-1]) if job_categorys else '',
                '工作經歷': requirements[0].text.strip(),
                '學歷要求': requirements[1].text.strip(),
                '科系要求': requirements[2].text.strip(),
                '語文條件': requirements[3].text.strip(),
                '擅長工具': requirements[4].text.strip(),
                '工作技能': requirements[5].text.strip(),
                '其他條件': soup.select('div.col.p-0.job-requirement-table__data')[0].text
            })
            data_list.append(data)
            time.sleep(1)
        print(f'page: {page} Done.')
    if not os.path.exists(f'{out_folder}/{jobWord}.xlsx'):
        df = pd.DataFrame(data_list, columns=['職位', '薪水', '公司', '領域', '地區', '產業', '規模', '學歷', '經歷', '應徵人數', 'link', '工作內容', '工作經歷', '學歷要求', '科系要求', '語文條件', '擅長工具', '工作技能', '其他條件'])
        df.to_excel(f'{out_folder}/{jobWord}.xlsx', index=True, header=True)
        print('爬蟲完成。')
    else:
        print(f'{jobWord}檔案已存在')
if __name__ == "__main__":
    pages = 10 # 爬10頁
    keyword = "AI工程師" 
    crawler104Jobs(keyword, pages)