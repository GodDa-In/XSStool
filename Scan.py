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
        self.url = obj.url
        self.cookie = obj.cookie
        self.tags = []
        self.submit = ''
        self.exploit = ''
        self.log = ''
        self.t_info = obj.t_info
        
        print(self.t_info)
        
        #print(self.url)
        
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('no-sandbox')  # 브라우저를 숨깁니다.
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) #필요없는 로그 출력 안함
        self.driver = webdriver.Chrome(options=self.options)

    
    def setCookie(self) :

        if self.cookie != None:
            self.driver.get(self.url)
            

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

            for cookie in self.cookie :
                self.driver.delete_cookie(cookie['name'])
                self.driver.add_cookie(cookie)

            self.driver.get(self.url)
            
        else :
            self.driver.get(self.url)
            

        
    def DirAtk(self, exploit) :
        self.exploit = exploit

        
        for infos in self.t_info :
            self.tags = infos["tags"]
            self.submit = infos["btn"]

            print(self.submit.text)
            
            if len(self.tags) != 0 :
                WebDriverWait(self.driver, 1)

                    
                    
                #각 입력 폼에 구문 입력    
                for tag in self.tags : 
                    input_element = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.NAME, tag)))

                    input_element.clear()

                    input_element.send_keys(self.exploit) # 공격 구문 삽입
                    
                    #input_element.send_keys(str("1"))   

            
                if self.submit:
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
                

                    for button in submit_buttons:
                        try :
                            if button.text == self.submit.text:
                                #print(button.get_attribute('innerText'), self.submit.text)
                                button.click()
                                
                                print("testing : " + self.exploit)                                
                                
                                try:
                                    WebDriverWait(self.driver, 2).until(EC.alert_is_present())

                                    while True:

                                        alert = self.driver.switch_to.alert

                                        alert_text = alert.text

                                        if alert_text == '1':
                                            self.log += str(self.exploit)
                                            alert.accept()
                                            print("취약점 확인")
                                            
                                            #성공한 구문 csv 저장
                                            csv_file = './database.csv'  # CSV 파일 경로

                                            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                                                writer = csv.DictWriter(file, fieldnames=['구문'])
                                                
                                                # 파일이 비어있을 경우 필드 이름을 추가
                                                file.seek(0, 2)  # 파일의 끝으로 이동
                                                file_empty = file.tell() == 0  # 파일의 위치가 0이면 파일이 비어있는 것으로 판단
                                                if file_empty:
                                                    writer.writeheader()
                                                
                                                writer.writerow({'구문': self.exploit})
                                            
                                            break
                                        
                                        alert.accept()  # 확인 버튼을 누름

                                except TimeoutException:
                                    print("Alert가 발생하지 않았습니다.")
                                    pass
                                
                                except NoAlertPresentException:
                                    print("알림 상자가 존재하지 않습니다.")
                                    pass

                                except UnexpectedAlertPresentException:
                                    pass
                                
                            else :
                                print("해당 버튼이 아닙니다.")
                                continue
                            
                        except UnexpectedAlertPresentException :
                            pass
                   
                        except StaleElementReferenceException :
                            pass       
            
            
            self.driver.quit()
        
    def getLog(self) :
        return self.log