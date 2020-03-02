import pickle
import time
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=12&ncvContSeq=&contSeq=&board_id=&gubun='

mov_paths_txt = []

driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
driver.implicitly_wait(3)

driver.get(url)

for i in range(9, 0, -1) :
    time.sleep(3)
    driver.find_element_by_css_selector(f'#content > div > div.paging > a:nth-child({i})').click()
    driver.find_element_by_id('pson_moveAll_open').click()
    mov_paths = driver.find_elements_by_css_selector('div.info_mtxt > ul.s_listin_dot > li')
    for mov_path in mov_paths :
        if mov_path.text == None:
            continue
        else :
            mov_paths_txt.append(mov_path.text)
    print('page complete')
print(mov_paths_txt)

# 일단 이동경로만 가져옴. 추후 인원에 따른 이동경로로 가져오고 데이터 전처리가 필요함(시간, 장소, 증상, 기타 등으로 텍스트 구분)

with open('mov_paths.txt', 'wb') as f:
    pickle.dump(mov_paths_txt, f)

    

