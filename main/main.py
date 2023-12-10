# 이 페이지는 source 폴더 안에 들어 있는 소스코드를 한번에 제어 및 실행에 사용할 예정입니다.
# 프로젝트별 선택을 통해 결과물 확인 할 수 있도록 할 예정입니다.


# 아래 코드는 기존 데이터 있을 경우 압축 처리 진행해줄 코드입니다.

import os
import sys
import shutil
from datetime import datetime

# soure file import
current_directory = os.getcwd()
sys.path.insert(0, current_directory)
from source import air_crowling
from source import bungaganto
from source import data
from source import jounggonara
from source import naver_market


def compress_data_folder(root_folder):
    data_folder = os.path.join(root_folder, 'data')
    backup_folder = os.path.join(root_folder, 'backup_data')

    # backup_data 폴더가 없으면 생성
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # 현재 날짜와 시간을 기준으로 압축 파일 이름 생성
    now = datetime.now().strftime("%Y%m%d_%H%M")
    archive_name = os.path.join(backup_folder, f"data_backup_{now}")

    # /data 폴더가 존재하면 압축
    if os.path.exists(data_folder):
        shutil.make_archive(archive_name, 'zip', data_folder)
        # 압축 후 /data 폴더 삭제
        shutil.rmtree(data_folder)
        print(f"압축 완료: {archive_name}.zip")
    else:
        print("/data 폴더가 존재하지 않습니다.")

# 기존 data 폴더 삭제 및 삭제 
print("=============================================")
print("기존 데이터가 있는지 확인하고, 있을 경우 데이터 백업처리를 진행합니다.")
compress_data_folder(current_directory)

# air_crowling.py   실행
print("=============================================")
print("항공 데이터 crowling is start (onground)")
air_crowling.main()
print("항공 데이터 is complete")

# data.py   실행
print("=============================================")
print("항공 데이터 분석&시각화 is start (background)")
data.main()
print("항공 데이터 분석&시각화 is complete")

# naver_market.py 실행
print("=============================================")
print("네이버 마켓 crowling is start (background)")
naver_market.main()
print("네이버 마켓 is complete")

# bungaganto.py 실행
print("=============================================")
print("번개장터 crowling is start (background)")
bungaganto.main()
print("번개장터 is complete")

# jounggonara.py 실행
print("=============================================")
print("중고나라 crowling is start (background)")
jounggonara.main()
print("중고나라 is complete")

