# 이 페이지는 번개장터 페이지에서 데이터를 받아올 소스코드입니다.
# 페이지 결과는 ../data/bungaganto 폴더에 저장될 예정입니다.

import random
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os

class InfoCrawler():
    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list = [
            #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',

            #Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
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
        options = ChromeOptions()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")
        options.add_argument("lang=ko_KR")
        # headless 모드 비활성화
        options.add_argument('headless')
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")

        # 크롬 드라이버 최신 버전 설정
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        query = "32QN650"
        URL = self.base_url + query 
        self.driver.get(URL)
        sleep(5)

        index = 1
        product_data = []
        while True:
            try:
                item_xpath = f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{index}]/a'
                item_element = self.driver.find_element(By.XPATH, item_xpath)

                item_info = item_element.text.split('\n')
                item_info = [info for info in item_info if "배송비포함" not in info]

                if len(item_info) >= 2 and "광고" not in item_info[-1]:
                    product_name = item_info[0]
                    product_price = item_info[1]

                    status_images = item_element.find_elements(By.XPATH, ".//img[@alt='예약중' or @alt='판매 완료']")
                    status = '판매중' if not any(status_images) else ', '.join(img.get_attribute('alt') for img in status_images)

                    product_link = item_element.get_attribute('href')

                    product_data.append({
                        '상품명': product_name,
                        '가격': product_price,
                        '상태': status,
                        '링크': product_link
                    })

                index += 1

            except NoSuchElementException:
                break

        self.driver.quit()
        return product_data
    
    def save_to_excel(self, data, filename):
        # 데이터프레임 생성
        df = pd.DataFrame(data, columns=['상품명', '가격', '상태', '링크','가격 비교'])
        directory = os.path.join(os.getcwd(), 'data', 'bungaganto')
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        df.to_excel(filepath, index=False)

def find_extreme_price_item(items, key, is_highest=True):
    extreme_item = None
    extreme_price = float('-inf') if is_highest else float('inf')

    for item in items:
        price_str = item[key].replace('원', '').replace(',', '')
        price = int(price_str) if price_str.isdigit() else 0

        if is_highest:
            if price > extreme_price:
                extreme_price = price
                extreme_item = item
        else:
            if price < extreme_price:
                extreme_price = price
                extreme_item = item

    return extreme_item, extreme_price

def main():
    naver_market_directory = os.path.join(os.getcwd(), 'data', 'naver_market')
    naver_market_file = os.path.join(naver_market_directory, 'naver_market.xlsx')
    naver_market_df = pd.read_excel(naver_market_file)
    b2_value_str = naver_market_df.iloc[0, 1]  # B2 셀의 값
    b2_value = int(b2_value_str.replace(',', ''))  # 쉼표 제거 후 정수 변환

    crawler = bungaganto_Crawler()
    data = crawler.get_code()

    for item in data:
        price_str = item['가격'].replace('원', '').replace(',', '')  # '가격' 키를 사용하여 접근
        price = int(price_str) if price_str.isdigit() else 0
        if price < b2_value / 2:
            item['가격 비교'] = '너무 가격이 낮음'
        elif price > b2_value * 2:
            item['가격 비교'] = '너무 가격이 높음'
        else:
            item['가격 비교'] = '이상없음'

    # 가격 데이터 추출 및 변환
    prices = [int(item['가격'].replace('원', '').replace(',', '')) for item in data]

    # 전체 평균 가격 계산
    average_price = int(sum(prices) / len(prices)) if prices else 0

    # "이상없음" 항목 필터링 및 가격 데이터 추출
    normal_items = [item for item in data if item['가격 비교'] == '이상없음' and item['상태'] == '판매중']
    normal_prices = [int(item['가격'].replace('원', '').replace(',', '')) for item in normal_items]

    # "이상없음" 항목의 평균 가격 계산
    average_normal_price = int(sum(normal_prices) / len(normal_prices)) if normal_prices else 0

    # 평균 가격 차이 계산
    price_difference = abs(average_normal_price - average_price)

    # "이상없음" 항목 중 가장 낮은 가격을 가지는 아이템 찾기
    lowest_price_item, lowest_price = find_extreme_price_item(normal_items, '가격', is_highest=False)

    # "이상없음" 항목 중 가장 높은 가격을 가지는 아이템 찾기
    highest_price_item, highest_price = find_extreme_price_item(normal_items, '가격', is_highest=True)

    # 결과 출력
    print(f"전체 평균 가격: {average_price}")
    print(f"기준치 이내 중 판매중인 항목의 평균 가격: {average_normal_price}")
    print(f"평균 가격 차이: {price_difference}")
    if highest_price_item:
        highest_price_url = highest_price_item['링크']
        print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격: {highest_price}")
        print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격을 가지는 아이템의 URL: {highest_price_url}")
    else:
        print("가장 높은 가격을 가지는 아이템이 없습니다.")
    
    if lowest_price_item:
        lowest_price_url = lowest_price_item['링크']
        print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격: {lowest_price}")
        print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격을 가지는 아이템의 URL: {lowest_price_url}")
    else:
        print("가장 낮은 가격을 가지는 아이템이 없습니다.")

    crawler.save_to_excel(data, 'bungaganto_data.xlsx')


if __name__ == "__main__":
    main()
