# 이 페이지는 중고나라 사이트에서 데이터를 가져오는데 사용할 예정입니다.
# 이 소스코드를 통한 부산물은 ../data/jounggonara에 저장할 예정입니다.
# 영어 주석 연습중입니다.

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
        query = "32QN650"                                               # Product Serial Number To Search 
        target_URL = self.base_url + query                              # Set URL Query
        response = requests.get(target_URL, headers=self.headers)       # Get Target URL Request
        soup = BeautifulSoup(response.text, 'html.parser')              # Start Parsing HTML Code 

        first_selector = "div#content > div > div:nth-of-type(2) > div > div:nth-of-type(3) > div"
        items = soup.select(first_selector)                             # item is Save the data in (div)

        Product_name_data = []          # Product Name 
        Product_price_data = []         # Product Price

        for item in items:
            # Find Product Name
            second_selector = "div > div:nth-of-type(2) > div > a"
            second_elements = item.select(second_selector)
            for element in second_elements:
                Product_name_data.append(element.get_text())

            # Find Product Price
            new_selector = "div > div:nth-of-type(2) > div:nth-of-type(2) > strong > span > span > em"
            new_elements = item.select(new_selector)
            for new_element in new_elements:
                Product_price_data.append(new_element.get_text())

        return Product_name_data, Product_price_data

# Save Data to Excel
def save_to_excel(Product_name_data, Product_price_data):
    max_length = max(len(Product_name_data), len(Product_price_data))
    
    # Set Length Of Both Data Lists [to 1]
    Product_name_data += [''] * (max_length - len(Product_name_data))
    Product_price_data += [''] * (max_length - len(Product_price_data))
    data = {
        '제품명': Product_name_data,
        '최저가': Product_price_data
    }
    df = pd.DataFrame(data)
    # Download Data Location
    directory = os.path.join(os.getcwd(), 'data', 'naver_market')
    # Check Folder Location
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_excel(os.path.join(directory, 'naver_market.xlsx'), index=False)                  # Add Filename To Download Path & Save Excel

def main():
    # Run Crawler
    crawler = naver_market()
    Product_name_data, Product_price_data = crawler.get_code() 
    product = Product_name_data[0]                                          # Convert Product Name List To String
    price = int(Product_price_data[0].replace(',', ''))                     # Convert Product Price List To String After Remove ','

    price_with_comma = "{:,}".format(price)                                 # Add commas every thousand units
    lower_result = price // 2
    higher_result = price * 2

    print("제품명     : " + product)
    print("네이버 최저가  : " + price_with_comma+"원")
    print("데이터 이상치 범위 : " + "{:,}".format(lower_result) + " ~ " + "{:,}".format(higher_result))

    save_to_excel(Product_name_data, Product_price_data)  # Save to Excel


if __name__ == "__main__":
    main()