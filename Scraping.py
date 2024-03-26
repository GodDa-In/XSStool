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
        self.url = url
        self.cookie = cookie
        self.title = None
        self.first_paragraph = None
        self.tags = [] #input, textarea 태그들을 모으는 배열
        self.btn = '' #input(type = 'submit'), button 태그들을 모으는 배열
        self.t_info = []

    def scrape(self):
        
        session = requests.Session()
        if self.cookie != None:

            for cookie in self.cookie :
                session.cookies.set(cookie['name'], cookie['value'])
                
        response = session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        input_array = ["input", "textarea", "button"]
        
        
        #for t_input in input_array :
        forms = soup.find_all('form')
        
        for form in forms : #입력폼, 버튼 찾기
            w_tag = form.find_all(input_array)
            #xpath = form.xpath('ancestor-or-self::form')  
            
            for element in w_tag:
                if element.get('type') == 'submit' :
                    self.btn = element
                elif element.get('type') != 'file' :
                    self.tags.append(element.get('name'))            
            
            if len(self.tags) != 0:
                r_temp = {"tags" : self.tags, "btn" : self.btn}
                self.t_info.append(r_temp)
            
            self.tags = []
            self.btn = ''
            
    
            
    #def scan_part(self, lines):
    #    log = ''
    #    for line in lines:
    #        scanner = scan.Scanner(self, line)
    #        scanner.DirAtk()
    #        log += scanner.getLog()
        
        
    #def getTags(self):
    #    return self.tags