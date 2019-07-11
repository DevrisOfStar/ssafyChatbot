"""
문제의 자료형
"""
class Problem:
    def __init__(self, number, subject, info, cor, total, ratio, link=None, classify=None, is_samsung=False):
        self.number = number  # 문제 번호
        self.subject = subject  # 문제 제목
        self.info = info  # 문제 정보 : 정보, 태그
        self.cor = cor  # 정답 횟수
        self.total = total  # 제출 횟수
        self.ratio = ratio  # 정답 비율
        self.link = link  # 문제 링크
        if classify is None:
            self.classify = []  # 분류 : DFS, BFS, ...
        self.is_samsung = is_samsung  # 삼성 기출문제 여부

    def add_classify(self, classification):  # 분류 추가
        self.classify.append(classification)

if __name__ == "__main__":
    p = Problem(1, "제목", ["정보", "태그"], 100, 200, 0.2, is_samsung=True)  # example.
    p.add_classify("DFS")
    print(p.classify)
