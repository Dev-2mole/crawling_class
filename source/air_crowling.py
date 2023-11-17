# 이 페이지는 인천 국제 항공 공사의 지역별 여객 데이터를 가져올 예정입니다.
# 가져온 데이터는 엑셀로 받아와 ../data/air 폴더에 저장할 예정입니다.

import random
from time import sleep
# from datetime import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

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

        options = ChromeOptions()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")  # 수정된 부분
        options.add_argument("lang=ko_KR")
        # headless 모드 비활성화
        # options.add_argument('headless')
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")

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
        
        # hint
        #print("페이지 소스 코드:")
        #print(self.driver.page_source)

        sleep(10)
        # 웹 드라이버 종료
        self.driver.quit()


crawler = air_Crawler()