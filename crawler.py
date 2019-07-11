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
    if temp < 10:
        source = fp.read()
        fp.close()
    else:
        return False
    return BeautifulSoup(source, "lxml")


def crawling(url=None, Tags ="None"):  # 크롤링 함수 : url 변수를 이용해서 크롤링
    problems = []
    problem = []
    if url is None:
        #삼성 문제집 URL
        SamsungQuestionURL = "https://www.acmicpc.net/workbook/view/1152"
        soup = get_soup_from_url(SamsungQuestionURL)
    else:
        soup = get_soup_from_url(url)
    # 태그를 나누기 위한 idx
    idx = 0
    if soup.find("ul",class_ = "pagination"):
        url_list = []
        for i in soup.find("ul",class_ = "pagination"):
            if i.find('a'):
                url_list.append(i.a.get("href"))
        for i in url_list:
            url = "https://www.acmicpc.net/" + i
            soup = get_soup_from_url(url)
            if soup == False:
                continue
            else:
                for z in soup.find("div", class_="table-responsive").find_all("tr")[1:]:
                    for j in z:
                        problem.append(j.get_text())
                        # 문제 URL
                        QustionURL = ""
                        if idx == 1:
                            QustionURL = "https://www.acmicpc.net" + j.a.get("href")
                        if idx == 5:
                            idx = 0
                            problem.append(QustionURL)
                            # 태그
                            problem.append(Tags)
                            problems.append(problem.copy())
                            problem.clear()
                        else:
                            idx += 1
    else:
        for i in soup.find("div", class_="table-responsive").find_all("tr")[1:]:
            for j in i:
                problem.append(j.get_text())

                # 문제 URL
                QustionURL = ""
                if idx == 1:
                    QustionURL = "https://www.acmicpc.net" + j.a.get("href")
                if idx == 5:
                    idx = 0
                    problem.append(QustionURL)
                    # 태그
                    problem.append(Tags)
                    problems.append(problem.copy())
                    problem.clear()
                else:
                    idx += 1
    return problems


def crawlProblem():  # 해당 문제 크롤링
    problems = []
    # 삼성 문제집 URL
    BOJ_TAG_URL = "https://www.acmicpc.net/problem/tags"
    soup = get_soup_from_url(BOJ_TAG_URL)

    # 태그를 나누기 위한 idx
    url_list = []

    # 태그 모음
    TagName_list = []
    for i in soup.find_all("td"):
        if i.find('a'):
            url_list.append(i.a.get("href"))
            TagName_list.append(i.get_text())
    for i in range(len(url_list)):
        url = "https://www.acmicpc.net/"+url_list[i]
        problems = crawling(url, TagName_list[i])
        print(problems)
        print("==== New Tags ====")
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
    crawlProblem()
