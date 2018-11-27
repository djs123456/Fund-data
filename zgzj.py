import json
import requests
import simplejson
import csv
import time
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'2',
    'Content-Type':'application/json',
    'Host':'gs.amac.org.cn',
    'Origin':'http://gs.amac.org.cn',
    'Pragma':'no-cache',
    'Referer':'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    }
url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.895115134732553&page=%d&size=100'


def post(page):
    response = requests.post(url % (page-1), headers=headers, data='{}')
    try:
        fundlist = response.json()["content"]
        fundinfo = {}
        for fund in fundlist:
            fundinfo["基金名称"] = fund["fundName"]
            fundinfo["私募基金管理人名称"] = fund["managerName"]
            fundinfo["托管人名称"] = fund["mandatorName"]
            time1 = time.localtime(fund["establishDate"]/1000)
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", time1)
            fundinfo["成立时间"] = otherStyleTime
            time2 = time.localtime(fund["putOnRecordDate"]/1000)
            otherStyleTime2 = time.strftime("%Y--%m--%d %H:%M:%S", time2)
            fundinfo["备案时间"] = otherStyleTime2
            fundinfo["基金ID"] = fund["id"]
            header = ["基金名称", "私募基金管理人名称", "托管人名称", "成立时间", "备案时间", "基金ID"]
            try:

                with open('中国证券基金数据.csv', 'a', newline='') as f:  # a是追加
                    writer = csv.DictWriter(f, header)
                    writer.writerow(fundinfo)
            except UnicodeEncodeError as e:
                print(e)
                print("写入错误，已处理")


    except simplejson.errors.JSONDecodeError as b:
        print("获取不到json数据，已处理")
        print(b)
    except TypeError as t:
        print("时间的装换类型不对，已处理")
        print(t)

def page_indx():
        page = 0
        while True:
            page+=1
            response = requests.post(url % (page-1), headers=headers, data='{}')
            try:
                if response.json()["numberOfElements"] == 0:
                    break
                else:
                    post(page)
                    print("*" * 100)
                    print("正在爬取第%d页"%page)
                    print("*"*100)
            except simplejson.errors.JSONDecodeError as p:
                    print(p)
                    print("获取不到json数据，已处理掉")
if __name__ == '__main__':
    header = ["基金名称", "私募基金管理人名称", "托管人名称", "成立时间", "备案时间", "基金ID"]
    with open('中国证券基金数据.csv', 'w', newline='') as f:  # w是写入
        # 标头在这里传入，作为第一行数据
        writer = csv.DictWriter(f, header)
        writer.writeheader()
    page_indx()




