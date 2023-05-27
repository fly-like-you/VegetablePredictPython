import glob
import os
import numpy as np
import pandas as pd
from datetime import datetime

csv_path = '../../price_predict/vegetable_price/original_vegetable_csv/'
csv_files = glob.glob(csv_path + '*.csv')

def create_today_df():
    today = datetime.today().strftime('%Y-%m-%d')
    # 날짜 범위를 데이터프레임에 추가합니다.
    date_range = pd.date_range(start='2023-01-01', end=today)
    return pd.DataFrame(date_range, columns=['일자'])

class VegetablePriceReader:
    # csv_file를 받아서 초기화하는 생성자 함수
    def __init__(self, csv_file):
        self.vege_name = os.path.basename(csv_file.split()[0])
        self.df = pd.read_csv(csv_file)
        self.df = self.df.drop(self.df.columns[1], axis=1).fillna(0)

    # '일자' 열을 확인하고 오늘 날짜 이전의 모든 행을 필터링하는 함수
    def filter_rows(self):
        self.df['일자'] = pd.to_datetime(self.df['일자'].astype(str), format='%Y%m%d')
        today = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        self.df = self.df[self.df['일자'] <= today]

    # 위의 네 가지 함수를 순서대로 실행하는 함수
    def process(self):
        col_name = self.df.columns[1]
        self.df = self.df.rename(columns={col_name: self.vege_name + " " + col_name})
        self.filter_rows()

        all_dates = create_today_df()
        # 원래 데이터프레임과 all_dates를 병합
        df = pd.merge(all_dates, self.df, on='일자', how='left')
        df['일자'] = df['일자'].dt.strftime('%Y-%m-%d')
        return df.iloc[:,1]


