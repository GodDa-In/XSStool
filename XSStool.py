#XSStool.py
import argparse
import Scraping as scrap
import Scan as scan
import multiprocessing
from multiprocessing import Pool

class XSSTool:
    def __init__(self):
        # 명령행 인자 parser 생성
        self.parser = argparse.ArgumentParser(description='XSS 자동화 도구')
        # URL을 받기 위한 옵션 추가
        self.parser.add_argument('-u', '--url', type=str, help='URL')
        # 세션 쿠키 값을 받기 위한 옵션 추가
        self.parser.add_argument('-c', '--cookie', type=str, help='세션 쿠키 값')
        self.args = None

    def parse_arguments(self):
        # 명령행 인자를 파싱하여 args에 저장
        self.args = self.parser.parse_args()

    def run(self):
        if not self.args.url:
            # URL이 주어지지 않은 경우 에러 출럭 후 종료
            print("URL을 지정해야 합니다.")
            return

        url = self.args.url

        # XSS 도구 실행 메시지
        print(f"XSS 테스트를 실행합니다. URL: {url}")
        
        
        if self.args.cookie != None :
            # 쿠키가 주어진 경우 쿠키 파싱
            cookie = self.args.cookie
            cookie_string = cookie
            cookies = {}

            # 쿠키를 파싱하여 딕셔너리로 변환
            for item in cookie_string.split(';'):
                key, value = item.strip().split('=', 1)
                cookies[key] = value
            cookie = cookies
            
            # Selenium이 요구하는 형식에 맞게 변환
            cookie = [{'name': name, 'value': value } for name, value in cookie.items()]
            
            return url, cookie        
        else :            
            # 쿠키가 주어지지 않은 경우 None 반환
            result = [url, None]
            return url, None

#멀티 프로세싱 할 함수    
def scan_line(args):
    line, url, cookie = args
    
    # 스크래핑 객체 생성
    scraping = scrap.WebScraper(url, cookie)
    scraping.scrape() # 스크래핑 시작
    scanner = scan.Scanner(scraping) # 스크래핑 결과물을 받아 스캐너 객체 생성
    scanner.setCookie() # 셀레니움의 쿠키 설정
    line = line.replace('\n', '') # 줄바꿈 제거
    scanner.DirAtk(line) # 사전 공격 수행
   

def main():
    # XSSTool 객체 생성(도구 시작)
    xss_tool = XSSTool()
    xss_tool.parse_arguments() # 인자 파싱
    url, cookie = xss_tool.run() # URL과 쿠키 설정

    # 프로세스 시작하는 방법 설정 (일반적으로 Window에서는 spawn)
    multiprocessing.set_start_method('spawn')
    
    lines = []
    
    # 사전 파일 가져오기
    with open('./wordlist/wordlist.txt', 'r', encoding='utf-8') as file:
        # 한 줄씩 읽어와서 lines 배열에 저장
        lines = file.readlines() # XSS wordlist
    
    # 시스템의 CPU 코어 수 확인
    num_processes = multiprocessing.cpu_count()
    #num_processes = 1 
    
    # wordlist를 cpu 개수 만큼 나눔
    part = chunkify(lines, num_processes)
    
    
    #멀티 프로세싱
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 각 프로세스에서 독립적으로 생성할 매개변수 추가
        args = [(line, url, cookie) for line in lines]
        pool.map(scan_line, args) # 함수와 매개변수를 매핑하여 병렬 실행
      
def chunkify(lst, num_chunks):
    chunk_size = len(lst) // num_chunks # 사전 파일 나눌 크기 계산
    chunks = [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)] # 리스트를 청크로 나눔
    # 나머지 항목을 마지막 청크에 추가
    chunks[-1].extend(lst[num_chunks*chunk_size:])
    return chunks

if __name__ == '__main__':
    info = main() # 메인 함수 실행