"""
챗봇으로 출력하는 부분
"""

# DB : 사용자 정보(userInfo.json or ..) - (Token, ID) -> Token : slack의 userID, ID : 백준 ID
#      데일리 여부 판단 (isDaily.json) - Problem 객체와 유사
#      문제 정보(ProblemInfo.json) - Problem 객체와 유사



def send_problem(classification = None):  # classification : 분류(ex. DFS, BFS, ...)별 문제 출력
    if classification == None:  # 미분류 문제
        return
    elif classification == "Daily":  # Daily 문제
        return
    else :
        return


def print_graph_classification_correction(userid):  # userid : 사용자 ID의 분류별 정답비율 그래프 출력
    pass
