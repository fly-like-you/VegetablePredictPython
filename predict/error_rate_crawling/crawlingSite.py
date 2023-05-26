import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

vegetable = {
    '청양고추': [],
    '풋고추': [],
    '꽈리고추': [],
    '깻잎': [],
    '햇마늘 난지': [],
    '양파': [],
    '장희 딸기': [],
    '매향 딸기': [],
    '설향 딸기': [],
    '죽향 딸기': [],
    '파프리카': [],
    '양상추': [],
    '일반부추': [],
    '시금치': [],
    '애호박': [],
    '쥬키니호박': [],
}


def create_date_dict(start_date, end_date):
    # datetime 형식으로 변환
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # 빈 딕셔너리 생성
    date_dict = {}

    # start_date부터 end_date까지 하루씩 증가하면서 딕셔너리에 추가
    current_date = start_date
    while current_date <= end_date:
        date_key = current_date.strftime('%Y-%m-%d')
        date_dict[date_key] = {'실제가격': 0, '1일전 예측가격': 0, '2일전 예측가격': 0, '3일전 예측가격': 0, '4일전 예측가격': 0, '5일전 예측가격': 0,
                               '6일전 예측가격': 0, '7일전 예측가격': 0}
        current_date += timedelta(days=1)

    return date_dict


def get_after_date(date_str, days):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    next_date = date + timedelta(days=days)
    return next_date.strftime('%Y-%m-%d')


def is_within_range(date_str, start_date_str, end_date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    return start_date <= date <= end_date

def crawl_vegetable_price(start_date_str, end_date_str):
    url = 'https://www.gyeongnam.go.kr/bigdatafarm/priceList.es?search1=&mid=a10101000000&search2='
    date_dict = create_date_dict(start_date_str, end_date_str)

    current_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    while current_date <= end_date:

        date_key = current_date.strftime('%Y-%m-%d')
        # 검색할 페이지 url
        search_url = url + date_key

        # 페이지 요청
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # script 태그에서 데이터 추출
        script = soup.select_one("#grpv-1 > div > div > div > div > script").string

        # data1: 일간 예측 가격, data3: 실제 가격
        data1_match = re.search(r"\['data1'[\s*,.*\d(null)]*\]", script)
        if data1_match:
            data1 = data1_match.group(0)
            search_val = re.findall(r'(\d+\.*\d*)|null', data1)
            prediction_prices = [int(x) if x != '' else 0 for x in search_val]
            del prediction_prices[0]
            for i in range(8, 15):
                j = i - 7
                dict_date = get_after_date(date_key, j)
                if is_within_range(dict_date, start_date_str, end_date_str):
                    dict_key = f'{j}일전 예측가격'
                    date_dict[dict_date][dict_key] = prediction_prices[i]


        data3_match = re.search(r"\['data3'[\s*,.*\d(null)]*\]", script)
        if data3_match:
            data3 = data3_match.group(0)
            search_val = re.findall(r'(\d+\.*\d*)|null', data3)
            real_prices = [int(x) if x != '' else 0 for x in search_val]

            dict_date = get_after_date(date_key, -1)
            if is_within_range(dict_date, start_date_str, end_date_str):
                date_dict[dict_date]['실제가격'] = real_prices[7]

        current_date += timedelta(days=1)
    return date_dict

