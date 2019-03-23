import requests
from lxml import etree
import re
from pprint import pprint
import json

class Bili(object):
    def __init__(self,url_num):
        self.name = "av号"+str(url_num)
        self.url = "https://www.bilibili.com/video/av{}".format(url_num)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

    def parse(self, url):
        response = requests.get(url,headers=self.headers)
        res = response.content.decode()
        return res

    def get_content(self,res):
        html = etree.HTML(res)
        item = {}
        item["title"] = html.xpath("//div[@id='viewbox_report']/h1/@title")[0] if len(html.xpath("//div[@id='viewbox_report']/h1/@title"))>0 else None
        if item["title"]:
            item["cid"] = re.findall(r"\"pages\"\:\[\{\"cid\":(.*?)\,", res, re.S)[0] 
        else:
            return None
        print(item)
        return item

    def get_url(self, item):
        cid = item["cid"]
        danmu_url = "https://comment.bilibili.com/{}.xml".format(cid)
        print(danmu_url)
        return danmu_url

    def get_danmu(self, res, item):
        # pprint(res)
        html = etree.HTML(res.encode())
        item["弹幕"] = html.xpath("//d/text()")
        # pprint(item)
        return item

    def save(self, name, content):
        with open("{}.json".format(name),"a",encoding="utf-8")as f:
            f.write(json.dumps(content,ensure_ascii=False,indent=4))
            print("保存成功")

    def run(self):
        item = {}
        # 1 获取url
        # 2 发送请求，获取相应
        res = self.parse(self.url)
        # 3 提取cid和标题
        item = self.get_content(res)
        if item==None:
            print("vid号不正确，请重新输入。")
            return
        # 4 组合弹幕url
        danmu_url = self.get_url(item)
        # 5 发送请求获取相应
        res_danmu = self.parse(danmu_url)
        # 6 提取
        end = self.get_danmu(res_danmu, item)
        # 7 保存
        self.save(self.name,end)
        print("程序结束")


if __name__ == '__main__':
    url_num = input("请输入8位视频av号:")
    print("url_num=",url_num)
    b = Bili(url_num)
    b.run()

