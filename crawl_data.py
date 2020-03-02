import pickle
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=12&ncvContSeq=&contSeq=&board_id=&gubun='

number = []
information = []
inject_path = []
admit_date = []
hospital = []
contact = []
mov_paths_txt = []

driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
driver.implicitly_wait(3)

driver.get(url)

for i in range(9, 0, -1) :
    time.sleep(3)
    driver.find_element_by_css_selector(f'#content > div > div.paging > a:nth-child({i})').click()
    driver.find_element_by_id('pson_moveAll_open').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    persons = soup.select_one('#content > div > div.pson_move_list.mgt12 > div.in_list')

    for person in persons :
        print(person[0])
        person_info = person[0][0]
        mov_path = person[1][0]
        if mov_path.text == None:
            mov_paths_txt.append('not yet')
        else :
            mov_paths_txt.append(mov_path.text)
        for j in len(person_info) :
            num = person_info[j][2].text
            info = person_info[j][2].text
            path = person_info[j][2].text
            date = person_info[j][2].text
            hosptl = person_info[j][2].text
            connect = person_info[j][2].text

        number.append(num)
        information.append(info)
        inject_path.append(path)
        admit_date.append(date)
        hospital.append(hosptl)
        contact.append(connect)

    print('page complete')

# 일단 정보 및 이동경로만 가져옴. 추후 인원에 따른 이동경로로 가져오고 데이터 전처리가 필요함(시간, 장소, 증상, 기타 등으로 텍스트 구분)

frame = {'환자' : number, '인적사항' : information, '감염경로' : inject_path, '확진일자' : admit_date, '입원기관' : hospital, '접촉자수' : contact, '이동경로' : mov_paths_txt}
covid19 = pd.DataFrame(frame)

covid19.to_csv("covid19.csv")
    

