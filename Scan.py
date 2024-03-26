#Scan.py
import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager


class Scanner:
    def __init__(self, obj):
        self.url = obj.url # URL
        self.cookie = obj.cookie # 세션 쿠키
        self.tags = [] # 입력 폼 태그들을 담는 배열
        self.submit = '' # 버튼 태그
        self.exploit = '' # 공격 문자열
        self.log = '' # 스캔 로그
        self.t_info = obj.t_info # 입력폼과 버튼 정보
        
        print(self.t_info) # 입력 폼과 버튼 정보
        
        self.options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
        self.options.add_argument('--headless')
        self.options.add_argument('no-sandbox')  # 브라우저를 숨깁니다.
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) #필요없는 로그 출력 안함
        self.driver = webdriver.Chrome(options=self.options) # 크롬 웹 드라이버 객체 생성

    # 쿠키 설정 함수
    def setCookie(self) :
        if self.cookie != None: # 쿠키가 있다면
            self.driver.get(self.url) # URL로 이동
            
            # alert가 뜬다면 alert다 지우기 
            # 쿠키 설정할때 alert가 나와있으면 쿠키가 적용 안되는 현상이 있음
            while True:
                try:
                    # alert가 나타날 때까지 대기합니다.
                    WebDriverWait(self.driver, 0).until(EC.alert_is_present())

                    # alert를 스위치하고 accept를 클릭합니다.
                    alert = self.driver.switch_to.alert
                    alert.accept()
                except:
                    # alert가 더 이상 나타나지 않으면 반복문을 종료합니다.
                    break
            
            # 각 쿠키 적용
            for cookie in self.cookie :
                self.driver.delete_cookie(cookie['name']) # 이미 해당 쿠키가 있다면 지움
                self.driver.add_cookie(cookie)

            self.driver.get(self.url) # URL로 다시 이동
            
        else :
            self.driver.get(self.url) # URL로 이동
            

        
    def DirAtk(self, exploit) :
        self.exploit = exploit # 공격 문자열 설정
        
        for infos in self.t_info : # 찾은 태그들 만큼 반복
            self.tags = infos["tags"] # 입력 폼 태그
            self.submit = infos["btn"] # 제출 버튼 태그

            print(self.submit.text) # 버튼 텍스트 출력
            
            if len(self.tags) != 0 : # 입력 폼이 존재하면
                WebDriverWait(self.driver, 1) # 웹이 로딩될때 까지 대기
                    
                #각 입력 폼에 구문 입력    
                for tag in self.tags : 
                    input_element = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.NAME, tag))) # 입력폼이 요소 찾기
                    input_element.clear() # 입력폼 내용 지움
                    input_element.send_keys(self.exploit) # 공격 구문 삽입   

            
                if self.submit:
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']") # 제출 버튼 찾기

                    for button in submit_buttons: # 각 버튼에 대해
                        try :
                            if button.text == self.submit.text: # 버튼 텍스트가 일치하는 경우
                                button.click() # 제출 버튼 클릭
                                #print(button.get_attribute('innerText'), self.submit.text)
                                
                                print("testing : " + self.exploit) # 테스트 출력                   
                                
                                try:
                                    WebDriverWait(self.driver, 2).until(EC.alert_is_present()) # alert 대기

                                    while True:

                                        alert = self.driver.switch_to.alert # alert 가져오기

                                        alert_text = alert.text # alert 텍스트

                                        if alert_text == '1': # alert 내용이 1일 경우
                                            #self.log += str(self.exploit)
                                            alert.accept() # alert 확인 버튼 클릭
                                            print("취약점 확인") # 취약점 확인 메세지 출력
                                            
                                            #성공한 구문 csv 저장
                                            csv_file = './database.csv'  # CSV 파일 경로

                                            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                                                writer = csv.DictWriter(file, fieldnames=['구문'])
                                                
                                                # 파일이 비어있을 경우 필드 이름을 추가
                                                file.seek(0, 2)  # 파일의 끝으로 이동
                                                file_empty = file.tell() == 0  # 파일의 위치가 0이면 파일이 비어있는 것으로 판단
                                                if file_empty:
                                                    writer.writeheader() # 필드 이름 추가
                                                
                                                writer.writerow({'구문': self.exploit}) # 구문을 CSV 파일에 쓰기
                                            
                                            break # 반복문 종료
                                        
                                        alert.accept()  # 확인 버튼을 누름

                                except TimeoutException: # 시간 초과 예외처리
                                    print("Alert가 발생하지 않았습니다.") # alert가 발생하지 않았다는 메세지 출력
                                    pass
                                
                                except NoAlertPresentException: # Alert가 없는 경우 예외 처리
                                    print("Alert가 발생하지 않았습니다.") # 메세지 출력
                                    pass

                                except UnexpectedAlertPresentException: # 예상치 못한 알림이 나타난 경우 예외 처리
                                    pass
                                
                            else : # 버튼 텍스트가 일치하지 않는 경우
                                print("해당 버튼이 아닙니다.") # 메세지 출력
                                continue # 다음 버튼으로 넘어감
                            
                        except UnexpectedAlertPresentException : # 예상치 못한 알림이 나타난 경우 예외 처리
                            pass
                   
                        except StaleElementReferenceException : # 참조된 요소가 없는 경우 예외 처리
                            pass       
            
            
            self.driver.quit()
        
    def getLog(self) :
        return self.log