from src.classes import game
from src import consts
import requests
import datetime
from typing import List
from pymongo import MongoClient
import certifi
    

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
DB_URL = os.getenv('DB_URL')

def load():
    try:
        do_load()
    except:
        print("error in load...")
    
def do_load():
    # connect to db collection
    cluster = MongoClient(DB_URL,tlsCAFile=certifi.where())
    db = cluster["test"]
    game_collection = db["Games"]

    # reset games
    game_collection.drop()

    # request today's games 
    now = datetime.datetime.now()
    response = requests.get(
        consts.API_URL+"/games", 
        headers={
            'x-rapidapi-key': API_KEY
        },
        params={
            'league': consts.LEAGUE_ID,
            'timezone': 'Europe/Rome',
            'season': consts.YEAR,
            'date': now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
        }
    )

    gameresponse: game.GameResponse=response.json()
    response_games: List[game.Game]=gameresponse['response']

    
    for match in response_games:
        game_collection.insert_one(match)
        

