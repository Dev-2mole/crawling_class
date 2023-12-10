# 이 페이지는 data 파일을 가져와서 데이터 비교를 진행할 예정입니다. 항공 data vs 통계청 data
# 결과물은 main.py 를 이용하여 전달(표현)할 예정입니다.
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

def main():
        
    download_path = os.path.join(os.getcwd(), 'data', 'air')
    result_path =  os.path.join(os.getcwd(), 'data', 'air','result')
    if not os.path.exists(result_path):
                os.makedirs(result_path)
    # 'AppleGothic' 폰트를 matplotlib의 기본 폰트로 설정
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    # 파일 경로 리스트 생성
    file_paths = [download_path+f'/{year}.xlsx' for year in range(2017, 2023)]

    # 각 파일을 불러와 데이터 프레임 생성
    dfs = [pd.read_excel(path) for path in file_paths]

    # '여객 출발' 및 '여객 도착' 컬럼을 숫자형으로 변환
    for df in dfs:
        df['여객 출발'] = pd.to_numeric(df['여객 출발'], errors='coerce').fillna(0)
        df['여객 도착'] = pd.to_numeric(df['여객 도착'], errors='coerce').fillna(0)

    # 년도별 상위 5개 국가의 여객 출발 및 도착 시각화 및 저장
    for year in range(2017, 2023):
        annual_top5_departures = dfs[year - 2017].groupby('국가 국가')['여객 출발'].sum().sort_values(ascending=False).drop(index='합 계').head(5)
        annual_top5_arrivals = dfs[year - 2017].groupby('국가 국가')['여객 도착'].sum().sort_values(ascending=False).drop(index='합 계').head(5)

        # 그래프 생성
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # 여객 출발
        axes[0].bar(annual_top5_departures.index, annual_top5_departures.values, color='blue')
        axes[0].set_title(f'{year}년 여객 출발')
        axes[0].set_ylabel('여객 수')
        axes[0].set_xlabel('국가')

        # 여객 도착
        axes[1].bar(annual_top5_arrivals.index, annual_top5_arrivals.values, color='green')
        axes[1].set_title(f'{year}년 여객 도착')
        axes[1].set_ylabel('여객 수')
        axes[1].set_xlabel('국가')

        # 이미지 파일로 저장
        image_name = result_path+f'{year}_top5_air_traffic.png'
        plt.tight_layout()
        plt.savefig(image_name)
        plt.close()

