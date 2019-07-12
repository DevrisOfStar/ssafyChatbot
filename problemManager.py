# -*- coding: utf-8 -*-
"""
크롤링한 문제들을 DB에 저장, DB로부터 불러오기, 업데이트 구현
"""
from crawler import crawlProblem, crawling
import array as arr
import json

def getProblems(isDaily=False):  #  crawling한 문제들을 json 방식으로 return
    if isDaily:
        problems = crawling()
    else:
        problems = crawlProblem() + crawling()
    pros_ = []  # json list
    for problem in problems:
        classify = [problem[7]]
        is_samsung = problem[8]
        flag = 0
        for gpro_ in pros_:
            if int(problem[0]) == gpro_['number']:
                print(problem[0], end=" ")
                print(classify)
                classify += gpro_['classify']
                is_samsung |= gpro_['is_samsung']
                flag = 1
        if flag == 0:
            pro_ = \
            {
                'number': int(problem[0]),  # 문제 번호
                'subject': problem[1],   # 문제 제목
                'info': problem[2],   # 문제 정보 : 정보태그
                'cor': int(problem[3]),   # 정답 횟수
                'total': int(problem[4]),   # 제출 횟수
                'ratio': float(problem[5][:-1]) / 100.0,   # 정답 비율
                'link': problem[6],  # 문제 링크
                'classify': classify, # 분류 : DFS, BFS, ...
                'is_samsung': problem[8]  # 삼성 기출문제 여부
            }
            pros_.append(pro_)
    return pros_


def saveProblems(filename="problemInfo.json"):   # db에 저장
    problems = getProblems()
    with open('./database/' + filename, 'w') as json_file:
        json.dump(problems, json_file)

def saveDaily(filename="isDaily.json"):
    problems = getProblems(isDaily=True)
    with open('./database/' + filename, 'w') as json_file:
        json.dump(problems, json_file)

def loadDaily(filename="isDaily.json"):
    with open('./database/' + filename, 'r') as json_file:
        return json.load(json_file)

def loadProblems():  # db로 부터 불러옴
    with open('./database/problemInfo.json', 'r') as json_file:
        problems = json.load(json_file)
        return problems

def getclassifylist():
    problems = loadProblems()
    l = []
    for problem in problems:
        for classify in problem['classify']:
            if classify in l:
                pass
            elif classify!="None":
                l.append(classify)
    return l



if __name__ == "__main__" :
    # saveProblems()
    print(getclassifylist())