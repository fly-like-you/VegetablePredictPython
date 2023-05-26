# 인터페이스 정의: 채소 데이터 다운로더
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# """
#     미나리(일반) 71번 3번째
#     풋고추(전체) 185번 1번째
#     청양고추 185번 2번째
#     깻잎(일반) 32번 2번째
#     시금치(일반) 105번 2번째
#     파프리카(일반) 181번 - 2페이지 1번째
#     양파(일반) 124번 2번째
#     토마토(일반) 176번 2번째
# """

vegetable_dict = {
    "미나리": {
        "vegetable_category": 2,
    },
    "풋고추": {
        "vegetable_category": 1,
    },
    "청양고추": {
        "vegetable_category": 2,
    },
    "깻잎": {
        "vegetable_category": 2,
    },
    "시금치": {
        "vegetable_category": 2,
    },
    "파프리카": {  # 파프리카는 2번째 페이지
        "vegetable_category": 4,
    },
    "양파": {
        "vegetable_category": 2,
    },
    "토마토": {
        "vegetable_category": 2,
    },
}

class VegetableDataDownloader:
    def __init__(self, driver, target_vegetable: str, sleep_time=2):
        self.driver = driver
        self.sleep_time = sleep_time
        self.target_vegetable = target_vegetable
        self.vegetable_dict = vegetable_dict

    def do_download(self):
        category_nth_child = self.vegetable_dict[self.target_vegetable]["vegetable_category"]
        nongnet_url = 'https://www.nongnet.or.kr/front/M000000049/content/view.do'

        if self.target_vegetable == '청양고추':
            self.target_vegetable = '풋고추'

        # 웹 페이지로 이동
        if self.driver.current_url != nongnet_url:
            self.driver.get(nongnet_url)

        # 검색 버튼 클릭
        self.click_search_button()

        # 데이터 넣기
        self.enter_search_text(self.target_vegetable)

        # 품목검색에서 데이터 선택
        self.select_vegetable()

        # 품목검색 확인 버튼 클릭
        self.click_confirm_button()

        # 최근 1년 조회 탭 클릭
        self.change_recent_360_data()

        # 품종 카테고리 선택
        self.select_vegetable_category(category_nth_child)

        # csv 파일 다운로드
        self.click_download_button()

    def click_search_button(self):
        search_btn = "#content > div > div.conGrid.gridStyle4 > div.item1 > div.filterTable > div.filterArea.imgData > div.titSearch > button"
        button = self.driver.find_element(By.CSS_SELECTOR, search_btn)
        button.click()

        sleep(self.sleep_time)

    def enter_search_text(self, search_text):
        input_field = self.driver.find_element(By.ID, 'inputDirectItemPumText')
        # 텍스트 입력
        input_field.send_keys(search_text)

        sleep(self.sleep_time - 1)

    def select_vegetable(self):
        # 특정 요소 내에서 텍스트를 검색할 태그 찾기
        container = self.driver.find_element(By.XPATH, '//*[@id="mCSB_4_container"]')
        click = 0
        # 특정 요소 내에서 텍스트를 포함하는 요소들 찾기
        if self.target_vegetable == '토마토':
            click = 1

        container.find_elements(By.XPATH, f".//*[contains(text(), '{self.target_vegetable}')]")[click].click()

        sleep(self.sleep_time - 1)

    def click_confirm_button(self):
        # 확인 버튼 선택
        x_path = '/html/body/div[6]/div/div/ul/li[2]/button'
        self.driver.find_element(By.XPATH, x_path).click()
        sleep(self.sleep_time)

    def change_recent_360_data(self):
        div = '//*[@id="content"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div/'

        button = div + 'p/button'
        self.driver.find_element(By.XPATH, button).click()

        sleep(self.sleep_time)

        li = div + 'ul/li[7]'
        self.driver.find_element(By.XPATH, li).click()


    def select_vegetable_category(self, nth_child):
        normal_vegetable = f'//*[@id="gcid_itemList"]/div/div/div[2]/ul/li[{nth_child}]'

        button = self.driver.find_element(By.XPATH, normal_vegetable)
        button.click()
        sleep(self.sleep_time)

    def click_download_button(self):
        price_selector = '/html/body/div[2]/main/div/article/div/div/div[2]/div[3]/div/div[2]/p/button[1]'
        trade_selector = '/html/body/div[2]/main/div/article/div/div/div[2]/div[4]/div/div[2]/p/button[1]'

        # 다운로드 버튼 클릭
        element = self.driver.find_element(By.XPATH, price_selector)
        self.driver.execute_script("arguments[0].click();", element)
        element = self.driver.find_element(By.XPATH, trade_selector)
        self.driver.execute_script("arguments[0].click();", element)

        sleep(self.sleep_time)



