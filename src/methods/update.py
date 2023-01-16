from src.classes import game
from src import consts
import requests
import datetime
from pymongo import MongoClient
import certifi
from typing import List

from src.methods.load import do_load

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
DB_URL = os.getenv('DB_URL')

def update():
    try:
        do_update()
    except:
        print("error in update...")

def do_update():
    cluster = MongoClient(DB_URL,tlsCAFile=certifi.where())
    db = cluster["test"]
    game_collection = db["Games"]
    season_collection = db["Season"]

    # request updated games 
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
        game_collection.update_one({'id':match['id']}, {"$set": match}, upsert=False)
        season_collection.update_one({'id':match['id']}, {"$set": match}, upsert=False)