# 이 페이지는 인천 국제 항공 공사의 지역별 여객 데이터를 가져올 예정입니다.
# 가져온 데이터는 엑셀로 받아와 ../data/air 폴더에 저장할 예정입니다.

import os
import random
from time import sleep
# from datetime import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# 기본적인 크롤링에 필요한 우회 계정 정보 (수정 필요 없음)
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

class air_Crawler(InfoCrawler):

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.airport.kr/co/"
        self.headers = {
            'User-Agent': '',
            'referer': "https://www.airport.kr/co/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.set_random_user_agent()
        # 다운로드 경로 설정
        download_path = os.path.join(os.getcwd(), 'data', 'air')
        # 해당 경로에 폴더가 없으면 생성
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        #
        options = ChromeOptions()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")
        options.add_argument("lang=ko_KR")
        # 로그 레벨을 SEVERE로 설정   => 심각한 오류만 표기됨
        options.add_argument('--log-level=3')
        # headless 모드 비활성화
        # options.add_argument('headless')
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_experimental_option('prefs', {
            "download.default_directory": download_path,  # 다운로드 경로 설정
            "download.prompt_for_download": False,  # 다운로드시 자동으로 저장
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # 크롬 드라이버 최신 버전 설정
        service = ChromeService(executable_path=ChromeDriverManager().install())

        # chrome driver
        self.driver = webdriver.Chrome(service=service, options=options)

        # 항공청사 웹 페이지 열기
        self.driver.get(self.base_url)

        # 홍보센터 메뉴 찾기
        sleep(2)
        menu = self.driver.find_element(By.LINK_TEXT, "홍보센터")

        # 클릭 이벤트
        menu.click()

        # 홍보센터 메뉴 찾기
        menu2 = self.driver.find_element(By.LINK_TEXT, "항공통계")
        # 클릭 이벤트
        menu2.click()

        # 인천공항통계 보기
        menu3 = self.driver.find_element(By.LINK_TEXT, "인천공항 통계보기")
        menu3.click()

        # 지역별통계 보기
        menu4 = self.driver.find_element(By.LINK_TEXT, "지역별통계")
        menu4.click()

        # 여기 아래부터는 직접 생각해보시면서 작성해보세요
        # 남은건 날짜 (월, 년별 지정하는 것, 검색버튼 누르기 , 출력된 결과값들을 가져오기)
        
        start_year = 2017
        end_year = 2022
        # 연도별 옵션 인덱스 계산 (역순)
        for year in range(start_year, end_year + 1):
            year_option_index = end_year - year + 2

            # 시작 연도 선택
            self.driver.find_element(By.CSS_SELECTOR, "#S_YEAR")
            self.driver.find_element(By.XPATH, f'//*[@id="S_YEAR"]/option[{year_option_index}]').click()

            # 시작 월 선택 (1월 고정)
            self.driver.find_element(By.CSS_SELECTOR, "#S_MONTH")
            self.driver.find_element(By.XPATH, '//*[@id="S_MONTH"]/option[1]').click()

            # 종료 연도 선택
            self.driver.find_element(By.CSS_SELECTOR, "#E_YEAR")
            self.driver.find_element(By.XPATH, f'//*[@id="E_YEAR"]/option[{year_option_index}]').click()

            # 종료 월 선택 (12월 고정)
            self.driver.find_element(By.CSS_SELECTOR, '#E_MONTH')
            self.driver.find_element(By.XPATH, '//*[@id="E_MONTH"]/option[12]').click()
            sleep(3)
            # 검색 버튼 클릭
            self.driver.find_element(By.ID,"btnSearch").click()
            # 갱신된 html 코드 다운로드
            # 이후 html 에서 execel 추출
            # 페이지의 HTML 코드 가져오기
            page_source = self.driver.page_source

            # HTML 콘텐츠를 파싱합니다
            soup = BeautifulSoup(page_source, 'html.parser')

            # 지정된 클래스를 가진 테이블을 찾습니다
            table = soup.find('table', {'class': 'table vt-dark pd0'})

            # HTML 테이블을 문자열로 변환한 후 StringIO 객체에 래핑합니다
            table_html = str(table)
            table_io = StringIO(table_html)

            # HTML 테이블을 DataFrame으로 변환합니다
            df = pd.read_html(table_io)[0]

            # 멀티레벨 컬럼 헤더를 단일 레벨로 평탄화합니다
            df.columns = [' '.join(col).strip() for col in df.columns.values]

            # 수정된 DataFrame을 Excel 파일로 저장합니다
            excel_path = download_path +"/"+ str(year_option_index+2015)+'.xlsx'
            df.to_excel(excel_path, index=False)

            #sleep(30)
            # 다운로드 버튼 클릭
            #self.driver.find_element(By.CLASS_NAME, "btn-type-small.point.ico.download").click()
        
        sleep(10)
        # 웹 드라이버 종료
        self.driver.quit()

def main():
    crawler = air_Crawler()

main();