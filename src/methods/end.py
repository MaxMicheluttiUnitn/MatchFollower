from src.classes import game
from src import consts
from pymongo import MongoClient
import certifi
import requests
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
DB_URL = os.getenv('DB_URL')

def end():
    try:
        # remove today games
        # connect to db collection
        cluster = MongoClient(DB_URL,tlsCAFile=certifi.where())
        db = cluster["test"]
        game_collection = db["Games"]
        standings_collection = db["Standings"]

        # update standings
        res = requests.get(
            consts.API_URL+"/standings", 
            headers={
                'x-rapidapi-key': API_KEY
            },
            params={
                'league': consts.LEAGUE_ID,
                'season': consts.YEAR,
            }
        )

        response: game.StandingResponse = res.json()
        positions: List[game.Position] = response['response'][0]

        for position in positions:
            team_id = position['team']['id']
            standings_collection.update_one({'team.id':team_id},{"$set": position},upsert=False)

        # reset games
        game_collection.drop()
    except:
        print("error in end...")