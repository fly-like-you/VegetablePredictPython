from predict.nongnet_crawling.utils.VegetablePriceReader import VegetablePriceReader, create_today_df
import glob
import pandas as pd
class PriceJsonParser:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def parse_csv_to_json(self):
        csv_files = glob.glob(self.csv_path + '*.csv')

        df = create_today_df()
        for csv_path in csv_files:
            reader = VegetablePriceReader(csv_path)
            new_df = reader.process()
            df = pd.concat([df, new_df], axis=1)

        df['일자'] = df['일자'].astype(str)

        self.save(df)

    def save(self, df):
        df.set_index('일자').to_json('output.json', orient='index')