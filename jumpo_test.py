#################### -- jumpo_macro 설명서 -- ####################
'''
1. selenium, chromedriver_autoinstall, pandas, openpyxl 라이브러리가 설치되어 있어야 합니다. 
2. 프로그램 실행 후 [검색 키워드]와 [반경]을 띄어쓰기(공백)로 구분해 입력하셔야 합니다. 
    2-1. [검색 키워드]를 입력 중 오타가 나서 지우다가 안 지워지면 아래 터미널에서 [ctrl + c] 키를 눌러 프로그램을 종료하고 다시 실행하세요. 
    2-2. [반경]의 경우 [250m], [500m], [1km] 중 정확히 입력하셔야 하며, 잘못 입력하시면 프로그램이 종료됩니다.
3. 점포라인 지도서비스 자체적인 로딩 지연으로, 지도를 불러오지 못하는 현상이 발생할 수 있습니다.
    3-1. 이 경우 30초 정도 기다리시면 프로그램이 자동 종료되거나
    3-2. 빠른 종료를 원하신다면 아래 터미널에서 [ctrl + c] 키를 눌러 프로그램을 종료하고 다시 실행하세요. 
4. 정상적으로 작동한다면 아래와 같이 작동합니다. 
    4-1. 입력한 [검색 키워드]와 [반경]에 등록된 [공유매물]에 한해 전송되고, 
    4-2. 전송과 동시에 해당 매물의 정보를 읽어들여 아래 터미널에 출력합니다. 
    4-3. 매물 탐색이 끝나면 읽어들였던 매물들의 정보를 Excel 파일로 저장하고, 프로그램을 종료합니다. 
    4-4. 엑셀 파일명은 [검색 키워드], [반경], [프로그램 작동 일시]로 이루어집니다.
'''

#################### -- 필수 라이브러리 import -- ####################
from selenium import webdriver  # 설치 요망
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
import chromedriver_autoinstaller   # 설치 요망
import webbrowser
import time
from datetime import datetime
import pandas as pd # 설치 요망
# import는 안 하지만, 파이썬 엑셀 라이브러리인 openpyxl 설치 요망


#################### -- 검색 키워드, 반경 입력 받기 -- ####################
rad_list = ['250m', '500m', '1km']
keyword, radius = input('검색 키워드와 지도 반경을 공백으로 구분해 입력하세요. (반경은 250m, 500m, 1km로 입력) : ').split()
if radius not in rad_list:
    print('반경을 잘못 입력하셨습니다. 다시 실행 후 반경을 정확히 입력해주세요. ')
    exit()


#################### -- chrome headless 설정 -- ####################
options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 주석 해제하면 headless로 동작


#################### -- 점포라인 지도서비스 접속 -- ####################
try: 
    path = chromedriver_autoinstaller.install() # selenium에 필요한 chromedriver 자동 설치
    driver = webdriver.Chrome(service=Service(path), options=options)
    driver.get('https://map.jumpoline.com/main?mcode=&scode=')
    driver.implicitly_wait(30)
except FileNotFoundError as err:
    print("크롬 브라우저를 찾을 수 없습니다. 설치 후 재시도하시기 바랍니다.")
    webbrowser.open('https://www.google.com/intl/ko/chrome/')


#################### -- 검색 키워드, 반경 입력 적용하기 -- ####################
search_box = driver.find_element(By.XPATH, '//*[@id="searchVal"]')
search_box.send_keys(keyword, '\n')
for idx in range(len(rad_list)):
    if rad_list[idx] == radius:
        driver.find_element(By.XPATH, '//*[@id="mapArea"]/div[8]/ul[3]/li[{}]'.format(idx + 1)).click()
        time.sleep(10)


#################### -- 매물 목록 읽어오기 -- ####################
driver.find_element(By.XPATH, '//*[@id="side"]/span').click()   # 사이드바 오픈
time.sleep(5)

sortMarketList = driver.find_element(By.XPATH, '//*[@id="sortMarketList"]') # 사이드바의 매물 목록 순회
market_cards = sortMarketList.find_elements(By.CLASS_NAME, 'market-card')

tmp, cnt = 1, 1
cnts = []               # 매물순번 저장할 리스트
item_numbers = []       # 매물번호 저장할 리스트
item_titles = []        # 매물명 저장할 리스트
item_names = []         # 매도인 성명 저장할 리스트
item_contacts = []      # 매도인 연락처 저장할 리스트
address_zips = []       # 지번 주소 저장할 리스트
address_roads = []      # 도로명 주소 저장할 리스트
deposits = []           # 보증금 저장할 리스트
rents = []              # 월세 저장할 리스트
maintenance_fees = []   # 관리비 저장할 리스트
premiums = []           # 권리금 저장할 리스트
sum_fees = []           # 합계 저장할 리스트

for market_card in market_cards:
    title = market_card.find_element(By.XPATH, '//*[@id="sortMarketList"]/div[{}]/div[1]/p'.format(tmp))
    if title.text == "공유매물직거래":
        market_card.click()
        time.sleep(1)
        
        driver.find_element(By.XPATH, '//*[@id="marketInfo_img"]').click()
        driver.switch_to.window(driver.window_handles[1])   # 새 탭으로 전환
        driver.implicitly_wait(30)
        
        
        #################### -- 매물 상세 정보 읽어오기 -- ####################
        item_number = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/div[1]/span[1]').text
        print('\n오늘 연락한 누적 매물 순번 : ', cnt)
        item_numbers.append(item_number)    # 매물번호 리스트에 저장
        print(item_number)
        item_title = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[1]/h3/div[2]/span[1]').text
        item_titles.append(item_title)  # 매물명 리스트에 저장
        print('매물명 : ', item_title)
        item_name = driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[3]/div[2]/div[1]').text
        item_names.append(item_name)
        print('매도인 성명 : ', item_name)
        item_contact = driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[3]/div[2]/div[2]').text
        item_contacts.append(item_contact)
        print('매도인 연락처 : ', item_contact)
        
        if driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[2]/th').text == "지번 주소":
            address_zip = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div').text
            address_zips.append(address_zip)
            print('지번 주소 : ', address_zip)
            address_road = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/div').text
            address_roads.append(address_road)
            print('도로명 주소 : ', address_road)
            deposit = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[5]/td[1]/span').text
            deposits.append(deposit)
            print('보증금 : ', deposit)
            rent = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/span/span').text
            rents.append(rent)
            print('월세 : ', rent)
            maintenance_fee = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[6]/td[2]/span').text
            maintenance_fees.append(maintenance_fee)
            print('관리비 : ', maintenance_fee)
            premium = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[7]/td/span').text
            premiums.append(premium)
            print('희망 권리금 : ', premium)
            sum_fee = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[8]/td/span').text
            sum_fees.append(sum_fee)
            print('합계 : ', sum_fee)
        
        elif driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[2]/th').text == "프랜차이즈":
            address_zip = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/div').text
            address_zips.append(address_zip)
            print('지번 주소 : ', address_zip)
            address_road = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[4]/td/div').text
            address_roads.append(address_road)
            print('도로명 주소 : ', address_road)
            deposit = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[6]/td[1]/span').text
            deposits.append(deposit)
            print('보증금 : ', deposit)
            rent = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[6]/td[2]/span/span').text
            rents.append(rent)
            print('월세 : ', rent)
            maintenance_fee = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[7]/td[2]/span').text
            maintenance_fees.append(maintenance_fee)
            print('관리비 : ', maintenance_fee)
            premium = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[8]/td/span').text
            premiums.append(premium)
            print('희망 권리금 : ', premium)
            sum_fee = driver.find_element(By.XPATH, '//*[@id="detailbox"]/div[1]/div[2]/table/tbody/tr[1]/td/table/tbody/tr[9]/td/span').text
            sum_fees.append(sum_fee)
            print('합계 : ', sum_fee)

        
        #################### -- 홍보 메시지, 연락처 기입하기  -- ####################
        driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/div/p/input').click()  # 체크박스 클릭
        text_box = driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/textarea')
        text_box.clear()   # text_box에 미리 입력된 내용 비우기
        text_box.send_keys("test0")
        driver.find_element(By.XPATH, '//*[@id="input02"]').send_keys('1234')   # 전화번호 중간 4자리
        driver.find_element(By.XPATH, '//*[@id="input03"]').send_keys('5678')   # 전화번호 마지막 4자리
        time.sleep(1)   # 잘 입력됐는지 체크하기 위한 시간
        
        
        #################### -- 실제 전송 버튼 클릭  -- ####################
        driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/span[2]').click()   # 직거래 상담 전송 버튼 클릭
        time.sleep(3)
        al = Alert(driver)
        al.accept() # 전송 완료 알림 확인 누르기
        
        
        text_box.clear()   # text_box에 미리 입력된 내용 비우기
        text_box.send_keys("test1")

        #################### -- 실제 전송 버튼 클릭  -- ####################
        driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/span[2]').click()   # 직거래 상담 전송 버튼 클릭
        time.sleep(3)
        al = Alert(driver)
        al.accept() # 전송 완료 알림 확인 누르기


        text_box.clear()   # text_box에 미리 입력된 내용 비우기
        text_box.send_keys("test2")

        #################### -- 실제 전송 버튼 클릭  -- ####################
        driver.find_element(By.XPATH, '//*[@id="box0"]/div[2]/div[1]/div/div/form/div[1]/p[1]/span[2]').click()   # 직거래 상담 전송 버튼 클릭
        time.sleep(3)
        al = Alert(driver)
        al.accept() # 전송 완료 알림 확인 누르기

        driver.close()  # 현재 탭 닫고
        driver.switch_to.window(driver.window_handles[0])   # 기존 탭으로 전환
        
        cnts.append(cnt)
        cnt += 1

    time.sleep(1)   # 다음 매물 로딩 안정을 위한 시간    
    tmp += 1

#################### -- 결과 엑셀 파일로 저장 -- ####################
result = pd.DataFrame()
result['순번'] = cnts
result['매물번호'] = item_numbers
result['매물명'] = item_titles
result['매도인 성명'] = item_names
result['매도인 연락처'] = item_contacts
result['지번 주소'] = address_zips
result['도로명 주소'] = address_roads
result['보증금'] = deposits
result['월세'] = rents
result['관리비'] = maintenance_fees
result['희망 권리금'] = premiums
result['합계'] = sum_fees

now = datetime.now()
result.to_excel('/Users/bjh/Documents/{}_{}_'.format(keyword, radius) + now.strftime('%Y-%m-%d_%H시%M분') + '.xlsx', index=False)   # 저장 경로 설정
print('현재 시간 기준으로 엑셀 파일이 성공적으로 저장되었습니다. ')