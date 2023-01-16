import time
from threading import Timer
from src import game_updater
import schedule


from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DB_URL')

def main():
    print("starting...")
    game_updater.load_games()
    print("loading done...")
    # volleyball matches usually take between 60 and 90 minutes
    # last match usually starts at 20:30, so I will
    # poll until 22:30 to be safe
    schedule.every().day.at("00:05").do(game_updater.load_games)

    # 90 requests during match time
    for hour in range(17,23):
        for minute in range(0,15):
            min = minute*4
            if min < 10:
                schedule.every().day.at(str(hour)+":0"+str(min)).do(game_updater.update_games)
            else:
                schedule.every().day.at(str(hour)+":"+str(min)).do(game_updater.update_games)

    # 7 requests after 23 (games should almost never reach these late hours, but might sometimes)
    schedule.every().day.at("23:00").do(game_updater.update_games)
    schedule.every().day.at("23:05").do(game_updater.update_games)
    schedule.every().day.at("23:10").do(game_updater.update_games)
    schedule.every().day.at("23:15").do(game_updater.update_games)
    schedule.every().day.at("23:20").do(game_updater.update_games)
    schedule.every().day.at("23:25").do(game_updater.update_games)
    schedule.every().day.at("23:30").do(game_updater.update_games)
    
    schedule.every().day.at("23:45").do(game_updater.end_day)
    try:
        while(True):
            time.sleep(10)
            schedule.run_pending()
    finally:
        print("ending...")

def test():
    game_updater.end_day()

if __name__ == "__main__":
    main()
    #test()