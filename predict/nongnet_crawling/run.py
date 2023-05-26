import time
from selenium import webdriver
from predict.nongnet_crawling.VegetableDataDownloader import VegetableDataDownloader

destination_path = '/predict/vegetable_price/original_vegetable_csv'
title_table = [" 거래물량 정보.csv", " 평균가격 정보.csv"]
vegetable_table = ['토마토(일반)', '양파(일반)', '파프리카(일반)', '시금치(일반)', '깻잎(일반)', '청양', '풋고추(전체)', '미나리(일반)']


def enable_download(driver):
    print('백그라운드 다운로드 기능 활성화')
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': f'{destination_path}'}}
    driver.execute("send_command", params)


def setting_chrome_options():
    options = webdriver.ChromeOptions()

    # 다운로드 폴더 설정
    prefs = {'download.default_directory': destination_path}
    options.add_experimental_option('prefs', prefs)

    # 백그라운드 작업
    options.add_argument('headless')

    return options


if __name__ == '__main__':

    # Selenium 웹 드라이버 경로
    webdriver_path = 'chromedriver_win32/chromedriver.exe'
    nongnet_url = 'https://www.nongnet.or.kr/front/M000000049/content/view.do'

    # Chrome 드라이버 시작
    driver = webdriver.Chrome(chrome_options=setting_chrome_options())
    enable_download(driver)
    driver.get(nongnet_url)

    time.sleep(3)
    vegetable_list = ['미나리', '풋고추', '청양고추', '깻잎', '시금치', '파프리카', '양파', '토마토']

    for vege in vegetable_list:
        downloader = VegetableDataDownloader(driver, vege)
        downloader.do_download()

    driver.quit()
