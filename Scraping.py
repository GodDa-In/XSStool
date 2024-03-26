#Scraping.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import Scan as scan


class WebScraper:
    def __init__(self, url, cookie = None):
        self.url = url # 스크래핑할 URL
        self.cookie = cookie # 세션 쿠키
        self.title = None # 페이지 타이틀
        self.first_paragraph = None # 첫번째 단락
        self.tags = [] #input, textarea 태그들을 모으는 배열
        self.btn = '' #input(type = 'submit'), button 태그들을 모으는 배열
        self.t_info = [] # 입력폼과 버튼 정보를 모으는 배열

    def scrape(self):
        session = requests.Session() # 세션 생성
        if self.cookie != None:
            for cookie in self.cookie :
                # 세션 쿠키 설정
                session.cookies.set(cookie['name'], cookie['value'])
        
        response = session.get(self.url) # URL로 GET 요청
        soup = BeautifulSoup(response.text, 'html.parser') # HTML 파싱
        
        input_array = ["input", "textarea", "button"] # 입력 폼 태그들
        
        forms = soup.find_all('form') # 모든 폼 태그 찾기
        
        for form in forms : # 페이지 내에 존재하는 form 태그 만큼 반복
            w_tag = form.find_all(input_array) # 폼 안의 입력 폼, 버튼 태그 찾기
            
            for element in w_tag:
                if element.get('type') == 'submit' :
                    self.btn = element # 제출 버튼 태그 저장
                elif element.get('type') != 'file' : # input 타입 중 type이 file 태그가 아니면
                    self.tags.append(element.get('name')) # 입력 폼 태그 저장         
            
            # 입력 폼과 제출 버튼을 딕셔너리로 묶어 저장
            if len(self.tags) != 0:
                r_temp = {"tags" : self.tags, "btn" : self.btn}
                self.t_info.append(r_temp)
            
            self.tags = [] # 다음 form 태그를 위해 초기화
            self.btn = '' # 다음 form 태그를 위해 초기화
            
    






































    #def scan_part(self, lines):
    #    log = ''
    #    for line in lines:
    #        scanner = scan.Scanner(self, line)
    #        scanner.DirAtk()
    #        log += scanner.getLog()
        
        
    #def getTags(self):
    #    return self.tags