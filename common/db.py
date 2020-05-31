from pymongo import MongoClient

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

high_elo = ["DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
high_elo_data = collection.find({"tier": {"$in": high_elo}, "game_duration": {"$gte": 1200}})
