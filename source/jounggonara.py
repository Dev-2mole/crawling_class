# 이 페이지는 중고나라 사이트에서 데이터를 가져오는데 사용할 예정입니다.
# 이 소스코드를 통한 부산물은 ../data/jounggonara에 저장할 예정입니다.


import requests
import random
from time import sleep

class InfoCrawler():
    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list = [
            #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',

            #Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/95.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/94.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/93.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/92.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/91.0'
        ]

    def set_random_user_agent(self):
        user_agent = random.choice(self.user_agent_list)
        self.headers['User-Agent'] = user_agent
        return user_agent

class bungaganto_Crawler(InfoCrawler):

    def __init__(self):
        super().__init__()
        self.base_url = "https://m.bunjang.co.kr/search/products?q="
        self.headers = {
            'User-Agent': self.set_random_user_agent(),
            'referer': "https://m.bunjang.co.kr/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.get_code()

    def get_code(self):
        print("testing")