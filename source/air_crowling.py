# 이 페이지는 인천 국제 항공 공사의 지역별 여객 데이터를 가져올 예정입니다.
# 가져온 데이터는 엑셀로 받아와 ../data/air 폴더에 저장할 예정입니다.
# 영어 주석 연습중입니다!

import os
import random
import pandas as pd

from time import sleep
from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


# Crawling User Setting
class InfoCrawler():
    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list = [
            #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            #Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
    def set_random_user_agent(self):
        user_agent = random.choice(self.user_agent_list)
        self.headers['User-Agent'] = user_agent
        return user_agent

# Crawling & Download Data
class air_Crawler(InfoCrawler):
    def __init__(self):
        # Define Crawling Setting
        super().__init__()
        self.base_url = "https://www.airport.kr/co/"                # Target
        self.headers = {
            'User-Agent': '',
            'referer': "https://www.airport.kr/co/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        # Define ChromeOptions
        options = ChromeOptions()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")        # Use Random User in User Setting
        options.add_argument("lang=ko_KR")
        options.add_argument('--log-level=3')           # Logging Mark Serious Errors Only
        # options.add_argument('headless')              # Run Onground
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")

        # Install and route the latest Chrome driver from Chrome Driver Manager
        service = ChromeService(executable_path=ChromeDriverManager().install())

        # Set chrome driver
        self.driver = webdriver.Chrome(service=service, options=options)

        # Download Data Location
        download_path = os.path.join(os.getcwd(), 'data', 'air')
        # Check Folder Location
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Open Target URL in Selenium
        self.driver.get(self.base_url)

        # Find Menu "홍보센터" & Click
        sleep(2)
        menu = self.driver.find_element(By.LINK_TEXT, "홍보센터")
        menu.click()

        # Find Menu "항공통계" & Click
        menu2 = self.driver.find_element(By.LINK_TEXT, "항공통계")
        menu2.click()

        # Find Menu "인천공항 통계보기" & Click
        menu3 = self.driver.find_element(By.LINK_TEXT, "인천공항 통계보기")
        menu3.click()

        # Find Menu "지역별통계" & Click
        menu4 = self.driver.find_element(By.LINK_TEXT, "지역별통계")
        menu4.click()


        # Setting year range want to download
        start_year = 2017
        end_year = 2022

        # Search & Parsing for Data
        for year in range(start_year, end_year + 1):
            # Calculation for element index (reverse)
            # example : 2017 => 2(index)
            year_option_index = end_year - year + 2

            # Set Start Year
            self.driver.find_element(By.CSS_SELECTOR, "#S_YEAR")
            self.driver.find_element(By.XPATH, f'//*[@id="S_YEAR"]/option[{year_option_index}]').click()

            # Set Start Month (January)
            self.driver.find_element(By.CSS_SELECTOR, "#S_MONTH")
            self.driver.find_element(By.XPATH, '//*[@id="S_MONTH"]/option[1]').click()

            # Set End Year
            self.driver.find_element(By.CSS_SELECTOR, "#E_YEAR")
            self.driver.find_element(By.XPATH, f'//*[@id="E_YEAR"]/option[{year_option_index}]').click()

            # Set End Month (December)
            self.driver.find_element(By.CSS_SELECTOR, '#E_MONTH')
            self.driver.find_element(By.XPATH, '//*[@id="E_MONTH"]/option[12]').click()
            sleep(1)

            # Find Search Botton & Click
            self.driver.find_element(By.ID,"btnSearch").click()
            
            # Get Page HTML Code
            page_source = self.driver.page_source

            # Start Parsing HTML Code 
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find Table Class Have Aviation Statistics Data
            table = soup.find('table', {'class': 'table vt-dark pd0'})

            # Convert HTML Table to String
            table_html = str(table)
            # Using StringIO, Data is Upload In Memory Buffer like file
            table_io = StringIO(table_html)

            # Convert HTML Table to DataFrame
            df = pd.read_html(table_io)[0]

            # 다중 인덱스 컬럼을 단일 인덱스 컬럼으로 변환(KR)
            # Converting Multiple Index Columns To Single Index Columns(EN)     
            df.columns = [' '.join(col).strip() for col in df.columns.values]

            # Save Converted DataFrame To Excel
            # Location : ../data/air/{year}.xlsx
            excel_path = download_path +"/"+ str(year_option_index+2015)+'.xlsx'
            df.to_excel(excel_path, index=False)
        
        sleep(2)
        # Quit Selenium Driver
        self.driver.quit()

# main
def main():
    crawler = air_Crawler()


if __name__ == "__main__":
    main()