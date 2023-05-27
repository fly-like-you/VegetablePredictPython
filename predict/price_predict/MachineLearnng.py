from ML_classes import *
from datetime import timedelta
import json
from datetime import datetime
def run():
    # 크롤링한 데이터 가져오기
    original_path = './vegetable_price/original_vegetable_csv/'
    test_path = './vegetable_price/test.csv'
    train_path = './vegetable_price/train.csv'

    vegetable_names = ['청양', '시금치(일반)', '토마토(일반)', '파프리카(일반)', '깻잎(일반)', '미나리(일반)', '양파(일반)', '풋고추(전체)']

    vegetable_price_dict = {x: None for x in vegetable_names}
    vegetable_trade_dict = {x: None for x in vegetable_names}

    for vegetable in vegetable_names:
        trade_path_args = [original_path, vegetable, " 거래물량 정보.csv"]
        price_path_args = [original_path, vegetable, " 평균가격 정보.csv"]

        vegetable_price_dict[vegetable] = get_vegetable_price_dict(price_path_args)
        vegetable_trade_dict[vegetable] = get_vegetable_trade_dict(trade_path_args)

    # test 파일 전처리
    test = pd.read_csv(test_path, encoding='ANSI').replace(np.NaN, 0)

    # 유효한 날짜 형식을 가지는 행만 선택
    test['date'] = pd.to_datetime(test['date'], errors='coerce')
    test = test.dropna(subset=['date'])

    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

    # 오늘의 날짜를 얻습니다.
    today = datetime.today()


    # DataFrame의 마지막 날짜를 얻습니다.
    last_date = test['date'].iloc[-1] + timedelta(days=1)


    while True:
        if last_date.date() > today.date():
            break
        li = [last_date, weekdays[last_date.weekday()]]
        for col in vegetable_trade_dict.keys():
            li.append(vegetable_trade_dict[col][last_date.date()])
            li.append(vegetable_price_dict[col][last_date.date()])
        test.loc[len(test)] = li
        last_date += timedelta(days=1)
    test['date'] = pd.to_datetime(test['date']).dt.strftime('%Y-%m-%d')
    test.to_csv(test_path, encoding='ANSI', index=False)

    # train 파일 전처리
    train_csv = pd.read_csv(train_path, encoding='ANSI')
    train = pd.concat([train_csv, test], axis=0)

    train.date = pd.to_datetime(train.date)
    train = pd.concat([train, pd.get_dummies(train['요일'])], axis=1)
    feature = train.columns[2:]
    train = train.reset_index(drop=True)
    train = train[1:].replace(0, np.NaN).fillna(method='ffill').fillna(0)

    vegetable_data_frame = train.drop(columns=['금요일', '목요일', '수요일', '월요일', '일요일', '토요일', '화요일'])

    df2 = vegetable_data_frame[0:-2]
    vegetable_today = vegetable_data_frame[-1:]

    # 머신러닝 실행!
    days = [1,2,3,4,5,6,7]
    features = ['청양고추', '시금치', '토마토', '파프리카', '깻잎', '미나리', '양파', '풋고추']

    day1=[]
    day2=[]
    day3=[]
    day4=[]
    day5=[]
    day6=[]
    day7=[]

    for day in days:
        for feature in features:
            my_nong1 = Nong1(df2, vegetable_today)
            my_nong1.set_feature(feature)
            my_nong1.set_target(day)
            my_nong1.set_model()
            if day == 1:
              day1.append(my_nong1.get_price())
            if day == 2:
              day2.append(my_nong1.get_price())
            if day == 3:
              day3.append(my_nong1.get_price())
            if day == 4:
              day4.append(my_nong1.get_price())
            if day == 5:
              day5.append(my_nong1.get_price())
            if day == 6:
              day6.append(my_nong1.get_price())
            if day == 7:
              day7.append(my_nong1.get_price())


    c = [day1[0], day2[0], day3[0], day4[0], day5[0], day6[0], day7[0]]
    s = [day1[1], day2[1], day3[1], day4[1], day5[1], day6[1], day7[1]]
    t = [day1[2], day2[2], day3[2], day4[2], day5[2], day6[2], day7[2]]
    p = [day1[3], day2[3], day3[3], day4[3], day5[3], day6[3], day7[3]]
    g = [day1[4], day2[4], day3[4], day4[4], day5[4], day6[4], day7[4]]
    m = [day1[5], day2[5], day3[5], day4[5], day5[5], day6[5], day7[5]]
    y = [day1[6], day2[6], day3[6], day4[6], day5[6], day6[6], day7[6]]
    u = [day1[7], day2[7], day3[7], day4[7], day5[7], day6[7], day7[7]]
    models = dict(zip(['청양고추', '시금치', '토마토', '파프리카', '깻잎', '미나리', '양파', '풋고추'], [c, s, t, p, g, m, y, u]))

    # 오늘 날짜를 yyyy-mm-dd 형식의 문자열로 변환
    today = datetime.today().strftime('%Y-%m-%d')

    # JSON 파일 이름 설정
    filename = f"predict_from_{today}.json"

    # 딕셔너리를 JSON으로 변환하고 파일로 저장
    with open("../data/" + filename, 'w') as f:
        json.dump(models, f)

if __name__ == '__main__':
    run()
