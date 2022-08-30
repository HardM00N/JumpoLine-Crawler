from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')

# -- 업종 검색 접속 -- #
driver = webdriver.Chrome(service=Service('/Users/bjh/Documents/Macro/chromedriver'), options=options)
url = 'https://www.jumpoline.com/_jumpo/jumpoListMaster.asp'        # 점포라인 > 권리금 점포 > 업종 검색
driver.get(url)
driver.implicitly_wait(20)   # 웹 페이지 로드를 보장하기 위해 20초 쉬기

# -- 지역선택 : 서울시 -- #
driver.find_element(By.XPATH, '//*[@id="c1_11000"]/span').click()   # 서울시
driver.implicitly_wait(20)

# -- 페이지 이동을 위한 리스트 선언 -- #
pages = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


# -- 전체 업종 순회 -- #
main_category_block = driver.find_element(By.XPATH, '//*[@id="tab_menu"]')
main_categories = main_category_block.find_elements(By.TAG_NAME, 'li')
for main_category in main_categories:
    if main_category == driver.find_element(By.XPATH, '//*[@id="Z_return_change_div"]'):    # 마지막 '전체' 탭에 도달하면 종료
        break
    main_category.click()

    # -- 업종별 페이지 순회 -- #
    for page in pages:
        time.sleep(10)

        # -- 페이지별 목록 순회 -- #
        for i in range(1, 61):
            try:
                title = driver.find_element(By.XPATH, '//*[@id="marketListTable"]/ul/li[{}]/div/div/div[1]/div[2]/div'.format(i))
                if title.text == "공유매물 직거래":
                    title.click()
                    driver.switch_to.window(driver.window_handles[1])   # 새 탭으로 전환
                    driver.implicitly_wait(20)

                    main_number = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/div[1]/span[1]').text
                    print(main_number)
                    main_title = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/h3/div[2]/span[1]').text
                    print(main_title)

                    driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/div/p/input').click()
                    main_text = driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/textarea')
                    main_text.clear()   # textbox에 미리 입력된 내용 비우기
                    main_text.send_keys('test')
                    driver.find_element(By.XPATH, '//*[@id="input02"]').send_keys('1234')
                    driver.find_element(By.XPATH, '//*[@id="input03"]').send_keys('5678')
                    # driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/span[2]').click()
                    # driver.implicitly_wait(20)
                    driver.close()  # 현재 탭 닫고
                    driver.switch_to.window(driver.window_handles[0])   # 기존 탭으로 전환
            except BaseException as ex1:
                print(ex1)
                break
        try:
            driver.find_element(By.XPATH, '//*[@id="dvPaging"]/div/div/a[{}]'.format(page)).click()
        except BaseException as ex2:
                print(ex2)
                break

driver.close()    # chrome 종료