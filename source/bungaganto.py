# 이 페이지는 번개장터 페이지에서 데이터를 받아올 소스코드입니다.
# 페이지 결과는 ../data/bungaganto 폴더에 저장될 예정입니다.
# 영어 주석 연습중입니다.
# joungonara.py의 main()과 bungaganto.py의 main()이 유사합니다. 

import os
import random
import pandas as pd

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


# Crawling User Setting
class InfoCrawler():
    def __init__(self):
        self.base_url = ""
        self.headers = {}
        # The target server checks the version information. Old user agents do not allow to access them.
        # So, I'm done update my User_Agent list
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

# Crawling & Download Data
class bungaganto_Crawler(InfoCrawler):
    # Define Crawling Setting
    def __init__(self):
        super().__init__()
        self.base_url = "https://m.bunjang.co.kr/search/products?q="            # Target
        self.headers = {
            'User-Agent': self.set_random_user_agent(),
            'referer': "https://m.bunjang.co.kr/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.get_code()

    # Crawling Code
    def get_code(self):
        # Define ChromeOptions
        options = ChromeOptions()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")
        options.add_argument("lang=ko_KR")
        options.add_argument('headless')                                        # Run Background
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")

        # Install and route the latest Chrome driver from Chrome Driver Manager
        service = ChromeService(executable_path=ChromeDriverManager().install())
        # Set chrome driver
        self.driver = webdriver.Chrome(service=service, options=options)
        
        
        query = "32QN650"                   # Product Serial Number To Search 
        URL = self.base_url + query         # Set URL Query
        self.driver.get(URL)                # Open Target URL Selenium
        sleep(5)                            # Waiting Page Load & Completed JavaScript

        index = 1           # Number Of Products In Page (Start : 1)
        product_data = []   # Prouduct_data List

        # Repeat for each product on the page
        while True:
            try:
                # Find item With index number
                item_xpath = f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{index}]/a'
                item_element = self.driver.find_element(By.XPATH, item_xpath)

                # Remove "배송비포함" In item
                item_info = item_element.text.split('\n')
                item_info = [info for info in item_info if "배송비포함" not in info]

                # Only Find Products That are not "광고"(AD)
                if len(item_info) >= 2 and "광고" not in item_info[-1]:
                    product_name = item_info[0]
                    product_price = item_info[1]
                    # Check Product Sale Status 
                    status_images = item_element.find_elements(By.XPATH, ".//img[@alt='예약중' or @alt='판매 완료']")
                    status = '판매중' if not any(status_images) else ', '.join(img.get_attribute('alt') for img in status_images)
                    # Product Link
                    product_link = item_element.get_attribute('href')
                    # Add Product Data
                    product_data.append({
                        '상품명': product_name,
                        '가격': product_price,
                        '상태': status,
                        '링크': product_link
                    })
                index += 1  # next Product

            # No more product on the page is End
            except NoSuchElementException:
                break

        # Quit Selenium Driver
        self.driver.quit()
        return product_data

# Save Data to Excel
def save_to_excel(data, filename):
    # Specify Excel Columns And Put In Data
    df = pd.DataFrame(data, columns=['상품명', '가격', '상태', '링크','가격 비교'])
    # Download Data Location
    directory = os.path.join(os.getcwd(), 'data', 'bungaganto')
    # Check Folder Location
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)            # Add Filename To Download Path
    df.to_excel(filepath, index=False)                      # Save Excel

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
    # Extract Only Price Info
    b2_value_str = naver_market_df.iloc[0, 1]  # B2 
    lowest_price_product = int(b2_value_str.replace(',', ''))  # Convert Integer After Remove ',' 
    
    # Run Crawler
    crawler = bungaganto_Crawler()
    data = crawler.get_code()

    for item in data:
        price_str = item['가격'].replace('원', '').replace(',', '')             # Extraction Price Data
        price = int(price_str) if price_str.isdigit() else 0                # Enter 0 if there is a non-integer value when switching to integer type
        if price < lowest_price_product / 2:                                # Lower Than Half the Lowest Price of Naver_Market
            item['가격 비교'] = '너무 가격이 낮음'
        elif price > lowest_price_product * 2:                              # Higher Than Double the Lowest Price of Naver_Market
            item['가격 비교'] = '너무 가격이 높음'
        else:
            item['가격 비교'] = '가격 특이점 없음'

    # Price Data Extraction And Integer Type Conversion
    prices = [int(item['가격'].replace('원', '').replace(',', '')) for item in data]

    # Calculate The Overall Average Price
    average_price = int(sum(prices) / len(prices)) if prices else 0

    # Filtering "가격 특이점 없음" items And Extracting Price Data
    normal_items = [item for item in data if item['가격 비교'] == '가격 특이점 없음' and item['상태'] == '판매중']
    normal_prices = [int(item['가격'].replace('원', '').replace(',', '')) for item in normal_items]

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
    print(f"기준치 이내 중 판매중인 항목의 평균 가격: {average_normal_price}")
    print(f"평균 가격 차이: {price_difference}")

    print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격: {highest_price}")
    print(f"기준치 이내 중 판매중인 항목 중 가장 높은 가격을 가지는 아이템의 URL: {highest_price_url}")

    print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격: {lowest_price}")
    print(f"기준치 이내 중 판매중인 항목 중 가장 낮은 가격을 가지는 아이템의 URL: {lowest_price_url}")

    # Save to Excel
    save_to_excel(data, 'bungaganto_data.xlsx')


if __name__ == "__main__":
    main()
