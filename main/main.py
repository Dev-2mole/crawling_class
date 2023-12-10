# 이 페이지는 source 폴더 안에 들어 있는 소스코드를 한번에 제어 및 실행에 사용할 예정입니다.
# 프로젝트별 선택을 통해 결과물 확인 할 수 있도록 할 예정입니다.


# 아래 코드는 기존 데이터 있을 경우 압축 처리 진행해줄 코드입니다.
# 영어 주석 연습중이라 많이 이상합니다..

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

# Data Backup Folder 
def backup_data_folder(root_folder):
    # Folder Location
    data_folder = os.path.join(root_folder, 'data')
    backup_folder = os.path.join(root_folder, 'backup_data')

    # Folder Check
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # File Name Format : YYYYMMDD_HHMM
    now = datetime.now().strftime("%Y%m%d_%H%M")
    archive_name = os.path.join(backup_folder, f"data_backup_{now}")

    # Data Folder Compressing for backup  
    if os.path.exists(data_folder):
        shutil.make_archive(archive_name, 'zip', data_folder)
        shutil.rmtree(data_folder)                      # delete data folder
        print(f"압축 완료: {archive_name}.zip")
    else:
        print("/data 폴더가 존재하지 않습니다.")

# Data Clean & Backup
print("=============================================")
print("기존 데이터가 있는지 확인하고, 있을 경우 데이터 백업처리를 진행합니다.")
backup_data_folder(current_directory)

# Run air_crowling.py 
print("=============================================")
print("항공 데이터 crowling is start (onground)")
air_crowling.main()
print("항공 데이터 is complete")

# Run data.py
print("=============================================")
print("항공 데이터 분석&시각화 is start (background)")
data.main()
print("항공 데이터 분석&시각화 is complete")

# Run naver_market.py
print("=============================================")
print("네이버 마켓 crowling is start (background)")
naver_market.main()
print("네이버 마켓 is complete")

# Run bungaganto.py
print("=============================================")
print("번개장터 crowling is start (background)")
bungaganto.main()
print("번개장터 is complete")

# Run jounggonara.py
print("=============================================")
print("중고나라 crowling is start (background)")
jounggonara.main()
print("중고나라 is complete")

# Program end
print("=============================================")