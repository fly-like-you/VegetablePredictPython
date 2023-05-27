import glob
import pandas as pd
csv_path = '../price_predict/vegetable_price/original_vegetable_csv/'

a = glob.glob(csv_path + '*.csv')
import pandas as pd
from datetime import datetime


class VegetablePriceReader:
    # csv_file를 받아서 초기화하는 생성자 함수
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    # '일자' 열을 확인하고 오늘 날짜 이전의 모든 행을 필터링하는 함수
    def filter_rows(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.df = self.df[self.df['일자'] <= today]

    # 첫 번째와 세 번째 열을 DataFrame에서 삭제하는 함수
    def drop_columns(self):
        self.df = self.df.drop(self.df.columns[[0, 2]], axis=1)

    # 최종 DataFrame을 JSON 파일로 저장하는 함수
    def save_as_json(self):
        self.df.to_json('output.json', orient='records')

    # 위의 네 가지 함수를 순서대로 실행하는 함수
    def process(self):
        self.filter_rows()
        self.drop_columns()
        self.save_as_json()


# 이 클래스를 사용하는 예시 코드
# 'input.csv'라는 파일을 읽어와서 필요한 처리를 한 후 'output.json' 파일로 저장합니다.
reader = VegetablePriceReader('input.csv')
reader.process()
