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
            reservation_status = '예약중' if reservation_div else '판매중'

            # 하이퍼링크 추출을 위한 수정된 선택자
            link_element = item.select_one('a')  # 각 항목 내의 첫 번째 <a> 태그 선택
            link = link_element['href'] if link_element else '링크 없음'
            # 하이퍼링크에 url 추가
            product_link = "https://web.joongna.com/"+link

            data.append({
                'title': title,
                'price': price,
                'reservation_status': reservation_status,
                'link': product_link  # 하이퍼링크 추가
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
    # naver_market.xlsx에서 B2 셀의 값을 읽기
    naver_market_directory = os.path.join(os.getcwd(), 'data', 'naver_market')
    naver_market_file = os.path.join(naver_market_directory, 'naver_market.xlsx')
    naver_market_df = pd.read_excel(naver_market_file)
    b2_value_str = naver_market_df.iloc[0, 1]  # B2 셀의 값 (문자열)
    b2_value = int(b2_value_str.replace(',', ''))  # 문자열에서 쉼표 제거 후 정수로 변환

    # 크롤링 및 데이터 처리
    crawler = jounggonara_Crawler()
    items = crawler.get_code()
    data = crawler.parse_items(items)

    # 가격 비교 및 새로운 열 추가
    for item in data:
        price_str = item['price'].replace('원', '').replace(',', '')  # 가격에서 '원'과 쉼표 제거
        price = int(price_str) if price_str.isdigit() else 0  # 정수 변환
        if price < b2_value / 2:
            item['price_comparison'] = '너무 가격이 낮습니다.'
        elif price > b2_value * 2:
            item['price_comparison'] = '너무 가격이 높습니다.'
        else:
            item['price_comparison'] = '이상없음'

    # 가격 데이터 추출 및 변환
    prices = [int(item['price'].replace('원', '').replace(',', '')) if '원' in item['price'] else 0 for item in data]

    # 전체 평균 가격 계산
    average_price = int(sum(prices) / len(prices)) if prices else 0

    # "이상없음" 항목 필터링 및 가격 데이터 추출
    normal_items = [item for item in data if item['price_comparison'] == '이상없음' and item['상태'] == '판매중']
    normal_prices = [int(item['price'].replace('원', '').replace(',', '')) if '원' in item['price'] else 0 for item in normal_items]

    # "이상없음" 항목의 평균 가격 계산
    average_normal_price = int(sum(normal_prices) / len(normal_prices)) if normal_prices else 0

    # 평균 가격 차이 계산
    price_difference = abs(average_normal_price - average_price)

   # '이상없음' 항목 중 가장 높은 가격과 가장 낮은 가격을 찾기
    highest_price_item = None
    lowest_price_item = None
    highest_price = 0
    lowest_price = float('inf')  # 무한대 값으로 초기화

    for item in data:
        price_str = item['price'].replace('원', '').replace(',', '')  # 가격에서 '원'과 쉼표 제거
        price = int(price_str) if price_str.isdigit() else 0  # 정수 변환

        if item['price_comparison'] == '이상없음':
            if price > highest_price:
                highest_price = price
                highest_price_item = item
            if price < lowest_price:
                lowest_price = price
                lowest_price_item = item

    # 결과 출력
    print(f"전체 평균 가격: {average_price}")
    print(f"기준치 이내 항목의 평균 가격: {average_normal_price}")
    print(f"평균 가격 차이: {price_difference}")

    if highest_price_item:
        highest_price_url = highest_price_item['link']
        print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격: {highest_price}")
        print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격을 가지는 아이템의 URL: {highest_price_url}")

    if lowest_price_item:
        lowest_price_url = lowest_price_item['link']
        print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격: {lowest_price}")
        print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격을 가지는 아이템의 URL: {lowest_price_url}")


    # 엑셀 파일로 저장
    crawler.save_to_excel(data)


if __name__ == "__main__":
    main()
