# 이 페이지는 중고나라 사이트에서 데이터를 가져오는데 사용할 예정입니다.
# 이 소스코드를 통한 부산물은 ../data/jounggonara에 저장할 예정입니다.


import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
import os


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

class jounggonara_Crawler(InfoCrawler):

    def __init__(self):
        super().__init__()
        self.base_url = "https://web.joongna.com/search/"
        self.headers = {
            'User-Agent': self.set_random_user_agent(),
            'referer': "https://web.joongna.com/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.get_code()

    def get_code(self):
        query = "32QN650"
        target_URL = self.base_url + query
        response = requests.get(target_URL, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('#__next > div > main > div:nth-child(1) > div:nth-child(2) > ul > li')
        return items

    def parse_items(self, items):
        data = []
        for item in items:
            title = item.find('h2', class_='line-clamp-2').get_text(strip=True) if item.find('h2', class_='line-clamp-2') else '제목 없음'
            price = item.find('div', class_='font-semibold').get_text(strip=True) if item.find('div', class_='font-semibold') else '가격 정보 없음'

            reservation_div = item.find('div', string='예약중')
            reservation_status = '예약중' if reservation_div else '없음'

            data.append({
                'title': title,
                'price': price,
                'reservation_status': reservation_status
            })
        return data


    def save_to_excel(self, data):
        df = pd.DataFrame(data)
        current_directory = os.getcwd()
        directory = os.path.join(current_directory, 'data', 'jounggonara')
        if not os.path.exists(directory):
            os.makedirs(directory)
        df.to_excel(os.path.join(directory, 'jounggonara_data.xlsx'), index=False)

def main():
    crawler = jounggonara_Crawler()
    items = crawler.get_code()
    data = crawler.parse_items(items)
    crawler.save_to_excel(data)

if __name__ == "__main__":
    main()