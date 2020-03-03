import pickle
import re
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=12&ncvContSeq=&contSeq=&board_id=&gubun='

pattern = re.compile(r'\s+') # 공백제거할 패턴

driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
driver.implicitly_wait(3)
driver.get(url)

number = []
information = []
inject_path = []
admit_date = []
hospital = []
contact = []
mov_paths_txt = []

for i in range(9, 0, -1) :
    time.sleep(3)
    driver.find_element_by_css_selector(f'#content > div > div.paging > a:nth-child({i})').click()
    time.sleep(3)
    driver.find_element_by_id('pson_moveAll_open').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    persons = soup.select_one('#content > div > div.pson_move_list.mgt12 > div.in_list').find_all('div', {"class":"onelist open"})

    for person in persons :
        person_info = person.find_all("ul")[0].find_all('li')
        if len(person.find_all("ul")) == 1:
            mov_path = 'not yet'
            mov_paths_txt.append(mov_path)
        else :
            mov_path = person.find_all("ul")[1]
            mov_paths_txt.append(mov_path.text)
        
        num = person_info[0].find_all('span')[1].text
        info = person_info[1].find_all('span')[1].text
        path = person_info[2].find_all('span')[1].text
        date = person_info[3].find_all('span')[1].text
        date = re.sub(pattern, '', date) 
        hosptl = person_info[4].find_all('span')[1].text
        connect = person_info[5].find_all('span')[1].text
        connect = re.sub(pattern, '', connect)
        print('num : '+num+', info : '+info+', path : '+path+', date : '+date+', hosptl : '+hosptl+', conncect : '+connect+', mov_path : '+mov_path)
                
        number.append(num)
        information.append(info)
        inject_path.append(path)
        admit_date.append(date)
        hospital.append(hosptl)
        contact.append(connect)
        print('person complete')
        print('='*50)
    print('page complete')
    print('='*100)

# 일단 정보 및 이동경로만 가져옴. 추후 인원에 따른 이동경로로 가져오고 데이터 전처리가 필요함(시간, 장소, 증상, 기타 등으로 텍스트 구분)

frame = {'환자' : number, '인적사항' : information, '감염경로' : inject_path, '확진일자' : admit_date, '입원기관' : hospital, '접촉자수' : contact, '이동경로' : mov_paths_txt}
covid19 = pd.DataFrame(frame)

covid19.to_csv("covid19.csv")
    

