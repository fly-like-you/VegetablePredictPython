import pickle

import matplotlib.pyplot as plt
from crawlingSite import crawl_vegetable_price, get_after_date
from datetime import date

# 에러 코드
def create_error_rate_dict(data_dict):
    error_rate_dict = {}
    for date_key, date_dict in data_dict.items():
        # 해당 일자의 실제 가격 가져오기
        real_price = date_dict['실제가격']

        # 일별 오차율 계산하기
        for i in range(1, 8):
            # i일 전 예측가격 가져오기
            prediction_price = date_dict.get(f'{i}일전 예측가격', None)
            if prediction_price is not None and real_price != 0:
                # 실제가격과 예측가격의 차이 계산하기
                error = real_price - prediction_price

                # 오차율 계산하기
                error_rate = round(error / real_price * 100, 2)

                # 오차율 딕셔너리에 추가하기
                if date_key not in error_rate_dict:
                    error_rate_dict[date_key] = {}
                error_rate_dict[date_key][f'{i}일전 오차율'] = error_rate

    return error_rate_dict

def get_today():
    today = date.today()
    return today.strftime("%Y-%m-%d")

if '__main__' == __name__:
    today = get_today()
    # 해당 사이트에서 오늘 농산물의 가격은 제공되지않음 (하루 지나야 알 수 있음)
    date_dict = crawl_vegetable_price(get_after_date(today, -8), today)
    error_rate_dict = create_error_rate_dict(date_dict)

    # 데이터를 파일에 저장
    with open('data1.pickle', 'wb') as f:

        pickle.dump(date_dict, f)

    # 그래프 그리기
    x_values = list(range(1, 8))
    for date, errors in error_rate_dict.items():
        print(date)
        y_values = [errors[f'{i}일전 오차율'] for i in range(1, 8)]

        # 오차율이 100이 아닌 경우에만 그래프에 표시
        if 100 not in y_values:
            plt.plot(x_values, y_values, label=date, marker='o')

    plt.xlabel('Days Before')
    plt.ylabel('Error Rate')
    plt.xticks(x_values)
    plt.legend(loc='best')
    plt.show()
