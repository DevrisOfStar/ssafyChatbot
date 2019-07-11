"""
챗봇으로 출력하는 부분
"""
from problemManager import *
from crawler import IsSolvedProblem
import random

# DB : 사용자 정보(userInfo.json or ..) - (Token, ID) -> Token : slack의 userID, ID : 백준 ID
#      데일리 여부 판단 (isDaily.json) - Problem 객체와 유사
#      문제 정보(ProblemInfo.json) - Problem 객체와 유사


def send_problem(classification=None, user_id=None):  # classification : 분류(ex. DFS, BFS, ...)별 문제 출력
    if classification == None:  # 미분류 문제
        return None
    elif classification == "Daily":  # Daily 문제
        a_problem = loadDaily()
        return a_problem[random.randrange(0, len(a_problem))]
    else :
        b_problem = loadProblems()
        b_problem = [pro_ for pro_ in b_problem if classification in pro_['classify'] and not IsSolvedProblem(pro_['number'], user_id)]
        r = random.randrange(3, len(b_problem) - 3)
        return b_problem[r-3:r]


def print_graph_classification_correction(userid):  # userid : 사용자 ID의 분류별 정답비율 그래프 출력
    pass


if __name__ == "__main__":
    print(send_problem("Daily", user_id="yh1483"))