import schedule
import time
import threading
from output import send_problem
"""
daily 문제를 전송하기 위한 클래스 : timer 필요
"""
# timer = timer
class Scheduler:
    def send_daily(self):  # daily 문제 전송
        send_problem("daily")

    def daily_problem_schedule(self):  # daily 문제 전송 스케쥴
        schedule.every().day.at("08:00").do(self.send_daily)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def update_problem(self):
        pass


    def problem_update_schedule(self):
        THREE_HOURS = 60 * 60 * 3
        schedule.every(12).hours.do(self.send_daily)

        while True:
            schedule.run_pending()
            time.sleep(THREE_HOURS)

    def __init__(self, _type=0):
        if _type == 0:  # daily 문제 전송
            alarm_thread = threading.Thread(target=self.daily_problem_schedule)
            alarm_thread.start()
        elif _type == 1:  # 문제 최신 업데이트
            alarm_thread = threading.Thread(target=self.problem_update_schedule)
            alarm_thread.start()


if __name__ == "__main__":
    Scheduler()
