# 이 페이지는 통계청 페이지에서 값을 가져오는 코드입니다.
# 통계청 페이지에서 값을 가져오고 난 뒤, 값은 엑셀로 ../data/Statustical_Office 폴더에 저장할 예정입니다.

import os
import random
from time import sleep
# from datetime import *
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

class Statistical_Office_Crawler(InfoCrawler):

    def __init__(self):
        super().__init__()
        self.base_url = "https://kosis.kr/"
        self.headers = {
            'User-Agent': '',
            'referer': "https://kosis.kr/",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.set_random_user_agent()
        # 다운로드 경로 설정
        download_path = os.path.join(os.getcwd(), 'data', 'Statistical_Office')
        # 해당 경로에 폴더가 없으면 생성
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        #
        options = ChromeOptions()
        options.add_argument(f"user-agent={self.headers['User-Agent']}")
        options.add_argument("lang=ko_KR")
        # 로그 레벨을 SEVERE로 설정   => 심각한 오류만 표기됨
        #options.add_argument('--log-level=3')
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

        # 로딩창 조건 대기용 함수
        def loading_invisible(driver):
            loading_element = driver.find_element(By.ID, "Loading")
            print("확인중")
            # 로딩 요소의 'display' 스타일 속성이 'none'일 때 True 반환
            return "display: none;" in loading_element.get_attribute("style")

        # 홍보센터 메뉴 찾기
        sleep(2)
        menu = self.driver.find_element(By.LINK_TEXT, "쉽게 보는 통계")
        menu.click()
        # 통계시각화콘텐츠이동
        sleep(2)
        menu2 = self.driver.find_element(By.LINK_TEXT, "통계시각화콘텐츠")
        menu2.click()
        # 세계속의 한국 메뉴 이동
        sleep(2)
        menu3 = self.driver.find_element(By.LINK_TEXT, "세계속의 한국")
        menu3.click()

        # 새 탭으로 전환
        sleep(2)  # 새 탭이 완전히 로드될 때까지 기다립니다.
        all_windows = self.driver.window_handles  # 모든 탭의 핸들을 가져옵니다.
        new_tab = all_windows[1]  # 새 탭의 핸들을 얻습니다. (0은 처음 탭, 1은 새 탭)
        self.driver.switch_to.window(new_tab)  # 새 탭으로 전환합니다.

        # 새 탭에서 작업을 계속합니다.
        sleep(2)
        menu4 = self.driver.find_element(By.LINK_TEXT, "1인당 국내총생산")
        menu4.click()

        # 통계표 보기 이동
        sleep(3)
        stat_table_button = self.driver.find_element(By.CLASS_NAME, "statgo2")
        stat_table_button.click()
        # 클릭시 새로운 크롬 창이 열림
        sleep(5)
        all_windows = self.driver.window_handles  # 모든 탭의 핸들을 가져옵니다.
        new_window = all_windows[-1]  # 새 탭의 핸들을 얻습니다. (0은 처음 탭, 1은 새 탭)
        self.driver.switch_to.window(new_window)  # 새 탭으로 전환합니다.

        # '시점' 버튼 클릭
        WebDriverWait(self.driver, 10).until(loading_invisible)
        print("로딩창 확인완료")
        sleep(3)
        # time_button = self.driver.find_element(By.ID, "btn_time")
        # time_button.click()

        sleep(5)
        select_element = self.driver.find_element(By.ID, "samePrdseYear_Y")
        select_object = Select(select_element)
        select_object.select_by_value("5")


        # 통계표 보기 이동
        sleep(2)
        menu6 = self.driver.find_element(By.LINK_TEXT, "다운로드")
        menu6.click()


        sleep(10)
        # 웹 드라이버 종료
        self.driver.quit()



crawler = Statistical_Office_Crawler()