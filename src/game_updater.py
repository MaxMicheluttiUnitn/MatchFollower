from src.classes import game
import threading
from src.methods import load, end, update

def load_games():
    print("starting day...")
    thread=threading.Thread(target=load.load)
    thread.start()

def update_games():
    print("updating...")
    thread=threading.Thread(target=update.update)
    thread.start()

def end_day():
    print("ending day...")
    thread=threading.Thread(target=end.end)
    thread.start()