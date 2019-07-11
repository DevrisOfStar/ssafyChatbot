"""
크롤링 하는 함수들 모듈
"""
import urllib.request
from bs4 import BeautifulSoup
# define header for urllib request
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/58.0.3029.110 Safari/537.36'
hds = {'User-Agent': user_agent}
hds_json = {'User-Agent': user_agent, 'Content-Type': 'Application/json'}

### 백준 방화벽 뚫어서 soup 가져오기 위한 함수
def get_soup_from_url(url):
    req = urllib.request.Request(url, headers=hds)
    temp = 0
    while temp < 10:
        try:
            fp = urllib.request.urlopen(req, timeout=10)
            break
        except:
            temp += 1
    source = fp.read()
    fp.close()
    return BeautifulSoup(source, "lxml")


def crawling(url=None):  # 크롤링 함수 : url 변수를 이용해서 크롤링
    if url is None:
        return
    
   ### 태그
    # 문제 번호
    list_problem_id = []
    # 문제
    list_QName = []
    # 문제 정보
    list_Info = []
    # 정답 제출자 수
    list_SuccessNum = []
    # 제출자 수
    list_SubmitNum = []
    # 정답률
    list_PercentCorrect = []

    #삼성 문제집 URL
    SamsungQuestionURL = "https://www.acmicpc.net/workbook/view/1152"
    soup = get_soup_from_url(SamsungQuestionURL)

    # 태그를 나누기 위한 idx
    idx = 0
    for i in soup.find("table", class_="table table-striped table-bordered").find_all("tr")[1:]:
        for j in i:
            if idx == 0:
                list_problem_id.append(j.get_text())
            elif idx == 1:
                list_QName.append(j.get_text())
            elif idx == 2:
                list_Info.append(j.get_text())
            elif idx == 3:
                list_SuccessNum.append(j.get_text())
            elif idx == 4:
                list_SubmitNum.append(j.get_text())
            elif idx == 5:
                list_PercentCorrect.append(j.get_text())
            if idx == 5:
                idx = 0
            else:
                idx += 1


def crawlProblem():  # 해당 문제 크롤링
    problems = []

    return problems

# problem_id : 문제 번호 #user_id : 유저 아이디
def IsSolvedProblem(problem_id,user_id):   # 문제 풀이 여부 확인
    URL = "https://www.acmicpc.net/status?problem_id="+str(problem_id)+"&user_id="+user_id + "&language_id=-1&result_id=-1"
    soup = get_soup_from_url(URL)
    is_check = False

    # 시도한 횟수 검사
    count = len(soup.find("table", class_="table table-striped table-bordered").find_all("span", class_="result-text"))
    for i in soup.find("table", class_="table table-striped table-bordered").find_all("span", class_="result-text"):
        if i.get_text() == "맞았습니다!!":
            is_check = True
    if count != 0:
        if is_check:
            print("맞춘 문제")
        else:
            print("틀린 문제")
    else:
        print("시도하지 않은 문제")
    return True


if __name__ == "__main__":  # 없는번호에 대해선 유효성검사가 안됨
    IsSolvedProblem(7100, "yh1483")