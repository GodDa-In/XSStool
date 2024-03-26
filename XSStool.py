#XSStool.py
import argparse
import Scraping as scrap
import Scan as scan
import multiprocessing
from multiprocessing import Pool

class XSSTool:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='XSS 자동화 도구')
        self.parser.add_argument('-u', '--url', type=str, help='URL')
        self.parser.add_argument('-c', '--cookie', type=str, help='세션 쿠키 값')
        self.args = None

    def parse_arguments(self):
        self.args = self.parser.parse_args()

    def run(self):
        if not self.args.url:
            print("URL을 지정해야 합니다.")
            return

        url = self.args.url
        print(f"XSS 테스트를 실행합니다. URL: {url}")
        
        
        if self.args.cookie != None :
            cookie = self.args.cookie
            
            cookie_string = cookie

            cookies = {}
            for item in cookie_string.split(';'):
                key, value = item.strip().split('=', 1)
                cookies[key] = value
            
            cookie = cookies
            
            #'domain' : url
            cookie = [{'name': name, 'value': value } for name, value in cookie.items()]
            #cookie = cookie[0]
            
            #print(cookie)
            
            
            return url, cookie        
        else :            
            result = [url, None]
            
            return url, None

#멀티 프로세싱 할 함수    
def scan_line(args):
    line, url, cookie = args
    #line = line.replace('\n', '')
    #print(line)
    scraping = scrap.WebScraper(url, cookie)
    scraping.scrape()
    scanner = scan.Scanner(scraping)
    scanner.setCookie()
    line = line.replace('\n', '')
    scanner.DirAtk(line)
   

def main():
    xss_tool = XSSTool()
    xss_tool.parse_arguments()
    url, cookie = xss_tool.run()

    
    
    multiprocessing.set_start_method('spawn')
    
    lines = []
    
    with open('./wordlist/wordlist.txt', 'r', encoding='utf-8') as file:
        # 한 줄씩 읽어와서 lines 배열에 저장
        lines = file.readlines() # XSS wordlist
    
    num_processes = multiprocessing.cpu_count()
    
    #num_processes = 1 
        
    part = chunkify(lines, num_processes)
    
    #print(part[0])
    
    #멀티 프로세싱
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 각 프로세스에서 독립적으로 생성할 매개변수 추가
        args = [(line, url, cookie) for line in lines]
        pool.map(scan_line, args)
      
    
    
def chunkify(lst, num_chunks):
    chunk_size = len(lst) // num_chunks
    chunks = [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
    # 나머지 항목을 마지막 청크에 추가
    chunks[-1].extend(lst[num_chunks*chunk_size:])
    return chunks



if __name__ == '__main__':
    info = main()