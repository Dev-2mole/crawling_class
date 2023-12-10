# 이 페이지는 중고나라 사이트에서 데이터를 가져오는데 사용할 예정입니다.
# 이 소스코드를 통한 부산물은 ../data/jounggonara에 저장할 예정입니다.
# 영어 주석 연습중입니다.
# joungonara.py의 main()과 bungaganto.py의 main()이 유사합니다. 

import os
import random
import requests
import pandas as pd

from bs4 import BeautifulSoup


# Crawling User Setting
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
# Crawling & Download Data
class jounggonara_Crawler(InfoCrawler):
    # Define Crawling Setting
    def __init__(self):
        super().__init__()
        self.base_url = "https://web.joongna.com/search/"           # Target
        self.headers = {
            'User-Agent': self.set_random_user_agent(),
            'referer': "https://web.joongna.com/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.get_code()

    # Crawling Code
    def get_code(self):
        query = "32QN650"                           # Product Serial Number To Search 
        target_URL = self.base_url + query          # Set URL Query
        response = requests.get(target_URL, headers=self.headers)       # Get Target URL Request
        soup = BeautifulSoup(response.text, 'html.parser')              # Start Parsing HTML Code 
        items = soup.select('#__next > div > main > div:nth-child(1) > div:nth-child(2) > ul > li') # item is Save the data in (li)
        return items

    def parse_items(self, items):
        data = []
        for item in items:
            # Find Product name  & Product Price
            title = item.find('h2', class_='line-clamp-2').get_text(strip=True) if item.find('h2', class_='line-clamp-2') else '제목 없음'
            price = item.find('div', class_='font-semibold').get_text(strip=True) if item.find('div', class_='font-semibold') else '가격 정보 없음'
            # Check Product Sale Status
            reservation_div = item.find('div', string='예약중')
            reservation_status = '예약중' if reservation_div else '판매중'
            # Product Link
            link_element = item.select_one('a') 
            link = link_element['href'] if link_element else '링크 없음'
            product_link = "https://web.joongna.com/"+link
            # Add Product Data
            data.append({
                '상품명': title,
                '가격': price,
                '상태': reservation_status,
                '링크': product_link 
            })
        return data

# Save Data to Excel
def save_to_excel(data):
    # Specify Excel Columns And Put In Data
    df = pd.DataFrame(data)
    current_directory = os.getcwd()
    # Download Data Location
    directory = os.path.join(current_directory, 'data', 'jounggonara')
    # Check Folder Location
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_excel(os.path.join(directory, 'jounggonara_data.xlsx'), index=False)      # Add Filename To Download Path & Save Excel

# Find Price Lower & Higher In items
def find_price_item(items, key, is_highest=True):
    unique_item = None
    unique_price = float('-inf') if is_highest else float('inf')    # Price Comparison (-/+)
    # Repeat item in items
    for item in items:
        price_str = item[key].replace('원', '').replace(',', '')        # Extraction Price Data
        price = int(price_str) if price_str.isdigit() else 0            # Enter 0 if there is a non-integer value when switching to integer type

        if is_highest:                      # Higer Price Comparison
            if price > unique_price:
                unique_price = price
                unique_item = item
        else:                               # Lower Price Comparison
            if price < unique_price:
                unique_price = price
                unique_item = item

    return unique_item, unique_price

# Run Crawling And Analyzing Value
def main():
    # Data Extraction From Naver_Market Data Files
    naver_market_directory = os.path.join(os.getcwd(), 'data', 'naver_market')
    naver_market_file = os.path.join(naver_market_directory, 'naver_market.xlsx')
    naver_market_df = pd.read_excel(naver_market_file)
    b2_value_str = naver_market_df.iloc[0, 1]  # B2 
    lowest_price_product = int(b2_value_str.replace(',', ''))  # Convert Integer After Remove ',' 

    # Run Crawler
    crawler = jounggonara_Crawler()
    items = crawler.get_code()
    data = crawler.parse_items(items)

    for item in data:
        price_str = item['가격'].replace('원', '').replace(',', '')         # Extraction Price Data
        price = int(price_str) if price_str.isdigit() else 0            # Enter 0 if there is a non-integer value when switching to integer type
        if price < lowest_price_product / 2:                            # Lower Than Half the Lowest Price of Naver_Market
            item['가격 비교'] = '너무 가격이 낮습니다.'
        elif price > lowest_price_product * 2:                          # Higher Than Double the Lowest Price of Naver_Market
            item['가격 비교'] = '너무 가격이 높습니다.'
        else:
            item['가격 비교'] = '가격 특이점 없음'

    # Price Data Extraction And Integer Type Conversion
    prices = [int(item['가격'].replace('원', '').replace(',', '')) if '원' in item['가격'] else 0 for item in data]

    # Calculate The Overall Average Price
    average_price = int(sum(prices) / len(prices)) if prices else 0

    # Filtering "가격 특이점 없음" items And Extracting Price Data
    normal_items = [item for item in data if item['가격 비교'] == '가격 특이점 없음' and item['상태'] == '판매중']
    normal_prices = [int(item['가격'].replace('원', '').replace(',', '')) if '원' in item['가격'] else 0 for item in normal_items]

    # Calculate Average Price Of "가격 특이점 없음" item
    average_normal_price = int(sum(normal_prices) / len(normal_prices)) if normal_prices else 0

    # Calculate Average Price Difference
    price_difference = abs(average_normal_price - average_price)

    # Find items With The Lowest Price Among "가격 특이점 없음" items 
    lowest_price_item, lowest_price = find_price_item(normal_items, '가격', is_highest=False)
    lowest_price_url = lowest_price_item['링크']

    # Find items With The Highest Price Among "가격 특이점 없음" items
    highest_price_item, highest_price = find_price_item(normal_items, '가격', is_highest=True)
    highest_price_url = highest_price_item['링크']

    # Result Print
    print(f"전체 평균 가격: {average_price}")
    print(f"기준치 이내 항목의 평균 가격: {average_normal_price}")
    print(f"평균 가격 차이: {price_difference}")

    print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격: {highest_price}")
    print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격을 가지는 아이템의 URL: {highest_price_url}")
    
    print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격: {lowest_price}")
    print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격을 가지는 아이템의 URL: {lowest_price_url}")

    # 엑셀 파일로 저장
    save_to_excel(data)


if __name__ == "__main__":
    main()
