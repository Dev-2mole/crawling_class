# 이 페이지는 data 파일을 가져와서 데이터 비교를 진행할 예정입니다. 항공 data vs 통계청 data
# 결과물은 main.py 를 이용하여 전달(표현)할 예정입니다.
# 영어 주석 연습 중입니다.

import os
import platform
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

def main():
    downloaded_path = os.path.join(os.getcwd(), 'data', 'air')                  # Downloaded Data Location
    result_path =  os.path.join(os.getcwd(), 'data', 'air','result')            # Result Data Location
    # Check Folder Location
    if not os.path.exists(result_path):
                os.makedirs(result_path)
    
    # Different OS Font Settings
    os_platform = platform.system()         # Check OS
    # Mac OS : AppleGothic.ttf
    if os_platform == "Darwin":
        plt.rcParams['font.family'] = 'AppleGothic'
        plt.rcParams['axes.unicode_minus'] = False
    # Windows 10, 11 : Gulim.ttf
    elif os_platform == "Windows" and platform.release() in ["10", "11"]:
        plt.rcParams['font.family'] = 'Gulim'
        plt.rcParams['axes.unicode_minus'] = False
 
    # Path List Of Files
    file_paths = [downloaded_path+f'/{year}.xlsx' for year in range(2017, 2023)]

    # Create DataFrame By Each Files
    dfs = [pd.read_excel(path) for path in file_paths]

    # Convert '여객 출발' 및 '여객 도착' Columns To Integer
    for df in dfs:
        df['여객 출발'] = pd.to_numeric(df['여객 출발'], errors='coerce').fillna(0)
        df['여객 도착'] = pd.to_numeric(df['여객 도착'], errors='coerce').fillna(0)

    # Passenger Departures And Arrivals In The Top 5 Countries By Year
    for year in range(2017, 2023):
        annual_top5_departures = dfs[year - 2017].groupby('국가 국가')['여객 출발'].sum().sort_values(ascending=False).drop(index='합 계').head(5)
        annual_top5_arrivals = dfs[year - 2017].groupby('국가 국가')['여객 도착'].sum().sort_values(ascending=False).drop(index='합 계').head(5)

        # Make Graph
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Passenger Departure In Year Data 
        axes[0].bar(annual_top5_departures.index, annual_top5_departures.values, color='blue')
        axes[0].set_title(f'{year}년 여객 출발')
        axes[0].set_ylabel('여객 수')
        axes[0].set_xlabel('국가')

        # Passengers Arrival In Year Data
        axes[1].bar(annual_top5_arrivals.index, annual_top5_arrivals.values, color='green')
        axes[1].set_title(f'{year}년 여객 도착')
        axes[1].set_ylabel('여객 수')
        axes[1].set_xlabel('국가')

        # Save Graph to png
        image_name = result_path+"/"+f'{year}_top5_air_traffic.png'
        plt.tight_layout()
        plt.savefig(image_name)
        plt.close()

if __name__ == "__main__":
    main()