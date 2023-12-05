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

class naver_market(InfoCrawler):

    def __init__(self):
        super().__init__()
        self.base_url = "https://search.shopping.naver.com/search/all?query="
        self.headers = {
            'User-Agent': self.set_random_user_agent(),
            'referer': "https://search.shopping.naver.com/search/all?query=",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.get_code()

    def get_code(self):
        query = "32QN650"
        target_URL = self.base_url + query
        response = requests.get(target_URL, headers=self.headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')

        first_selector = "div#content > div > div:nth-of-type(2) > div > div:nth-of-type(3) > div"
        items = soup.select(first_selector)

        second_selector_data = []  # 두 번째 선택자로 추출한 데이터를 저장할 리스트
        new_selector_data = []     # 새로운 선택자로 추출한 데이터를 저장할 리스트

        for item in items:
            # 두 번째 선택자
            second_selector = "div > div:nth-of-type(2) > div > a"
            second_elements = item.select(second_selector)
            for element in second_elements:
                second_selector_data.append(element.get_text())

            # 새로운 선택자
            new_selector = "div > div:nth-of-type(2) > div:nth-of-type(2) > strong > span > span > em"
            new_elements = item.select(new_selector)
            for new_element in new_elements:
                new_selector_data.append(new_element.get_text())

        return second_selector_data, new_selector_data

    def save_to_excel(self, second_data, new_data):
        max_length = max(len(second_data), len(new_data))
        
        # 두 데이터 리스트의 길이를 맞춤
        second_data += [''] * (max_length - len(second_data))
        new_data += [''] * (max_length - len(new_data))

        data = {
            'Second Selector Data': second_data,
            'New Selector Data': new_data
        }
        df = pd.DataFrame(data)
        current_directory = os.getcwd()
        directory = os.path.join(current_directory, 'data', 'naver_market')
        if not os.path.exists(directory):
            os.makedirs(directory)
        df.to_excel(os.path.join(directory, 'naver_market.xlsx'), index=False)

# 메인 실행 부분
if __name__ == "__main__":
    crawler = naver_market()
    second_data, new_data = crawler.get_code()  # 데이터 추출
    crawler.save_to_excel(second_data, new_data)  # 엑셀로 저장

