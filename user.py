import json

"""
정보 입력 및 시작부분 : User data 저장, 불러오기, 초기화, 유효성검사
"""

class USER:
    def __init__(self, _token):  # 생성자
        self.token = _token
        self.userid = None


    def register(self):  # json에 등록
        feeds = dict()
        with open('./database/userInfo.json', 'r', encoding='utf-8') as json_file:
            feeds = json.load(json_file)

        with open('./database/userInfo.json', 'w', encoding='utf-8') as json_file:
            userid = input("User ID를 입력해주세요. : ")
            # 사용자아이디 유효성 검사 필요
            self.userid = str(userid)
            feeds[self.token] = self.userid
            json.dump(feeds, json_file)

    def isExistUser(self, token):  # DB에 존재하는지 판단하기
        with open('./database/userInfo.json', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

            if token in json_data.keys():
                self.userid = json_data[token]
                return True
            else:
                return False

    def getid(self):
        return self.userid

    def setid(self):  # 사용자 정보를 저장 혹은 불러오기 : 사용자 정보가 DB에 없으면, DB에 저장 및 _userid 변수에 넣기. 있으면 DB 불러와서 넣기.
        if self.isExistUser(self.token):  # id가 db에 존재하는 경우
            print(self.userid + "님, 반갑습니다.")  # 데이터를 넘겨 줄 예정
        else:   # id가 db에 존재하지 않는 경우
            self.register()
            print("사용자가 등록되었습니다.")

    def init_id(self):  # id 초기화
        print("초기화되었습니다.\n")
        self.register()
        print("사용자가 재등록 되었습니다.")


if __name__ == "__main__":
    user = USER("token3")
    user.setid()
