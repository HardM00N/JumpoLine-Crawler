# https://ssamko.tistory.com/9 과정 따라하기

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# -- 업종 검색 접속 -- #
driver = webdriver.Chrome('/Users/bjh/Documents/Macro/chromedriver')
url = 'https://www.jumpoline.com/_jumpo/jumpoListMaster.asp'        # 점포라인 > 권리금 점포 > 업종 검색
driver.get(url)
time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기

# -- 지역선택 : 서울시 -- #
driver.find_element(By.XPATH, '//*[@id="c1_11000"]/span').click()   # 서울시
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="B10_div"]').click()       # 카페 클릭 (첫 카테고리)

# # -- 전체 업종 순회 -- #
main_category_block = driver.find_element(By.XPATH, '//*[@id="tab_menu"]')
main_categories = main_category_block.find_elements(By.TAG_NAME, 'li')
for main_category in main_categories:
    if main_category == driver.find_element(By.XPATH, '//*[@id="Z_return_change_div"]'):
        break
    main_category.click()
    time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기

# pages = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# for page in pages:
#     time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기

#     for i in range(1, 61):
#         try:
#             title = driver.find_element(By.XPATH, '//*[@id="marketListTable"]/ul/li[{}]/div/div/div[1]/div[2]/div'.format(i))
#             print(title.text)
#             # if title.text == "공유매물 직거래":
#             #     title.click()
#             #     driver.switch_to.window(driver.window_handles[1])
#             #     time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기

#             #     main_number = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/div[1]/span[1]').text
#             #     print(main_number)
#             #     main_title = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/h3/div[2]/span[1]').text
#             #     print(main_title)

#             #     driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/div/p/input').click()
#             #     main_text = driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/textarea')
#             #     main_text.clear()
#             #     main_text.send_keys('test')
#             #     driver.find_element(By.XPATH, '//*[@id="input02"]').send_keys('1234')
#             #     driver.find_element(By.XPATH, '//*[@id="input03"]').send_keys('5678')
#             #     # driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/span[2]').click()
#             #     time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기
#             #     driver.close()
#             #     driver.switch_to.window(driver.window_handles[0])
        
#         except BaseException as ex1:
#             print(ex1)
#             break
#     try:
#         driver.find_element(By.XPATH, '//*[@id="dvPaging"]/div/div/a[{}]'.format(page)).click()
    
#     except BaseException as ex2:
#             print(ex2)
#             break

# title = driver.find_element(By.XPATH, '//*[@id="marketListTable"]/ul/li[1]/div/div/div[1]/div[2]/div')
# title.click()
# driver.switch_to.window(driver.window_handles[1])
# time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기

# main_number = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/div[1]/span[1]').text
# print(main_number)
# main_title = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/h3/div[2]/span[1]').text
# print(main_title)

# driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/div/p/input').click()
# main_text = driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/textarea')
# main_text.clear()
# main_text.send_keys('test')
# driver.find_element(By.XPATH, '//*[@id="input02"]').send_keys('1234')
# driver.find_element(By.XPATH, '//*[@id="input03"]').send_keys('5678')
# # driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/span[2]').click()
# time.sleep(5)   # 웹 페이지 로드를 보장하기 위해 5초 쉬기
# driver.close()
# driver.switch_to.window(driver.window_handles[0])

# //*[@id="dvPaging"]/div/div
# //*[@id="dvPaging"]/div/div/a[1]/span # 1 -> 2
# ...
# //*[@id="dvPaging"]/div/div/a[3]/span # 2 -> 3
# //*[@id="dvPaging"]/div/div/a[4]/span # 3 -> 4
# //*[@id="dvPaging"]/div/div/a[10]/span    # 9 -> 10
# //*[@id="dvPaging"]/div/div/a[11] # 10 -> 11

# //*[@id="dvPaging"]/div/div/a[3]/span # 11 -> 12
# //*[@id="dvPaging"]/div/div/a[4]/span # 12 -> 13
# ...
# //*[@id="dvPaging"]/div/div/a[11]/span # 19 -> 20
# //*[@id="dvPaging"]/div/div/a[12] # 20 -> 21

# driver.close()    # chrome 종료