import tensorflow as tf
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from tensorflow.keras import Sequential
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
from statsmodels.tsa.seasonal import STL

from matplotlib import pyplot as plt
from tqdm import tqdm

def get_vegetable_trade_dict(trade_path_args):
    return get_dict_from_csv(trade_path_args, '거래물량(톤)')

def get_vegetable_price_dict(price_path_args):
    return get_dict_from_csv(price_path_args, '평균가격(원/kg)')

def get_dict_from_csv(path_args, col_name):
    path = ''.join(path_args)

    target = pd.read_csv(path, encoding='utf-8').replace(np.NaN, 0)
    target['일자'] = pd.to_datetime(target['일자'], format='%Y%m%d')

    target_dict = {}
    # 오늘 날짜 얻기
    today = datetime.today().date()
    # 행을 반복하며 '일자' 확인
    for index, row in target.iterrows():
        date = row['일자'].date()
        target_dict[date] = row[col_name] if col_name == '평균가격(원/kg)' else row[col_name] * 1000

        # '일자'가 오늘 날짜와 같으면 반복 중지
        if row['일자'].date() == today:
            break
    return target_dict

class Nong1:
    def __init__(self, df, test):
        self.test = test
        self.df = pd.concat([df, self.test], axis=0)[1:].replace(0, np.NaN).fillna(method='ffill').fillna(0)

        self.df.date = pd.to_datetime(self.df.date)
        self.df = pd.concat([self.df, pd.get_dummies(self.df['요일'])], axis=1)
        self.feature = self.df.columns[2:]
        self.df = self.df.reset_index(drop=True)

    def set_feature(self,name):
        self.name = name
        self.name1 = name+"_가격(원/kg)"
        self.name2 = name+"_거래량(kg)"
        self.feature = [self.name1, self.name2, '금요일',   '목요일',   '수요일',   '월요일',   '일요일',   '토요일',   '화요일', 'resid']

    def set_target(self,day):
        if day == 1:
            self.df['target'] = self.df[self.name1].shift(-2)
        elif day == 2:
            self.df['target'] = self.df[self.name1].shift(-3)
        elif day == 3:
            self.df['target'] = self.df[self.name1].shift(-4)
        elif day == 4:
            self.df['target'] = self.df[self.name1].shift(-5)
        elif day == 5:
            self.df['target'] = self.df[self.name1].shift(-6)
        elif day == 6:
            self.df['target'] = self.df[self.name1].shift(-7)
        elif day == 7:
            self.df['target'] = self.df[self.name1].shift(-8)
        self.df['resid'] = 0
        stl = STL(self.df[['date', self.name1]].set_index('date'), period=12)
        res = stl.fit()
        self.df['resid'] = res.resid.values

    def set_model(self):
        self.scaler = MinMaxScaler()
        self.df[self.feature] = self.scaler.fit_transform(self.df[self.feature])
        self.df_learn = self.df[self.df['target'].notnull()]
        self.X = self.df_learn[self.feature].values.reshape(-1,1,len(self.feature))
        self.y = self.df_learn['target'].values.reshape(-1,1,1)

        with tf.device('/device:GPU:0'):
            self.model = Sequential()
            self.model.add(layers.Activation('relu'))
            self.model.add(tf.compat.v1.keras.layers.LSTM(100, input_shape=(21,len(self.feature)), return_sequences=True))
            self.model.add(Dropout(0.1))
            self.model.add(layers.Dense(30))
            self.model.add(Dropout(0.1))
            self.model.add(layers.Dense(1))
            self.model.compile(optimizer='adam', loss='mse')
            self.early_stopping = EarlyStopping(patience=30)

            # tqdm을 사용하여 진행 상태 표시
            # tqdm을 사용하여 진행 상태 표시
            with tqdm(total=1000, desc="Epochs", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
                self.model.fit(
                    self.X, self.y, epochs=1000, batch_size=32, validation_split=0.1,
                    callbacks=[
                        self.early_stopping,
                        tf.keras.callbacks.LambdaCallback(on_epoch_end=lambda batch, logs: pbar.update(1))
                    ],
                    verbose=0
                )
    def get_plot(self):
        self.y_pred = self.model.predict(self.X)
        self.MAE = mean_absolute_error(self.y.reshape(-1,1), self.y_pred.reshape(-1,1))
        plt.figure(figsize=(20, 10), dpi=300)
        plt.title(self.name + ' 가격 예측 결과'+   '   MAE : ' + str(self.MAE)[:7])
        plt.ylabel(self.name + ' 가격')
        plt.plot(np.array(self.y.reshape(-1,1)), alpha = 0.9, label = 'Real')
        plt.plot(self.model.predict(self.X).reshape(-1,1), alpha = 0.6, linestyle = "--", label = 'Predict')
        plt.legend()
        plt.show()

    def get_price(self):
        self.price = self.model.predict(self.df[self.feature].iloc[len(self.df)-1].values.reshape(-1,1,len(self.feature)))
        return self.price[0][0][0]