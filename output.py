"""
챗봇으로 출력하는 부분
"""
from problemManager import *
from crawler import IsSolvedProblem
import random
from main import *
# DB : 사용자 정보(userInfo.json or ..) - (Token, ID) -> Token : slack의 userID, ID : 백준 ID
#      데일리 여부 판단 (isDaily.json) - Problem 객체와 유사
#      문제 정보(ProblemInfo.json) - Problem 객체와 유사


def send_problem(classification=None, user_id=None):  # classification : 분류(ex. DFS, BFS, ...)별 문제 출력
    if classification == None:  # 미분류 문제
        return None
    elif classification == "Daily":  # Daily 문제
        global slack_web_client
        global channel_list

        a_problem = loadDaily()
        t = a_problem[random.randrange(0, len(a_problem))]
        print(channel_list)
        for channel in channel_list:
            slack_web_client.chat_postMessage(
            channel= channel,
            text = "\n문제 번호 : "+str(t.get("number"))+"\n문제 이름 : "+\
                                    str(t.get("subject"))+"\n정답자 / 제출자 : "+ str(t.get(
                                "cor"))+"/"+str(t.get("total")) +"\n링크 : "+ \
                                    str(t.get("link"))+"\n"

            )
    else :
        b_problem = loadProblems()
        b_problem = [pro_ for pro_ in b_problem if classification in pro_['classify']]
        if len(b_problem) <= 3:
            return b_problem
        problems = []
        while len(problems) < 3:
            r = random.randrange(0, len(b_problem))
            if IsSolvedProblem(b_problem[r]['number'], user_id) or b_problem[r] in problems:
                pass
            else:
                problems.append(b_problem[r])

        return problems


def print_graph_classification_correction(userid):  # userid : 사용자 ID의 분류별 정답비율 그래프 출력
    pass


if __name__ == "__main__":
    print(send_problem("다이나믹 프로그래밍", user_id="yh1483"))