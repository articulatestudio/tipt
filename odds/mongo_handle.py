import pymongo
from pymongo import MongoClient
import json
#DATABASE_NAME = 'heroku_b2v9lgzf'
DATABASE_NAME = 'heroku_1c3055cr'
DATABASE_Addr = '46.101.39.247'
DATABASE_PORT = 27017
#DATABASE_URL = 'mongodb://eleven:eleven11@ds133771-a0.mlab.com:33771,ds133771-a1.mlab.com:33771/heroku_b2v9lgzf?replicaSet=rs-ds133771'
DATABASE_URL = 'mongodb://heroku_1c3055cr:q3pqj2elcqj6n6g7dp64t29bt2@ds145659.mlab.com:45659/heroku_1c3055cr'

class mongodb():
    """
    Mongodb connection and process to fetch data.
    """

    def __init__(self):
        self.db = None
        try:
            self.client = MongoClient(DATABASE_URL)
            print ("Connected successfully!!!")
        except Exception as e:
            print ("Could not connect to MongoDB: %s" % e)
            self.client = None

    def get_collections(self, db_name):
        """
        Get collections from database
        """
        if self.client is not None:
            self.db = self.client[db_name]
            # Get collections from DATABASE_NAME
            collections = self.db.collection_names()
            return collections

        return []

    def get_data(self, collections):
        """
        Get data from all collections
        """
        races_data = []
        odds_data = []
        tournaments_data = []
        horses_data = []
        predict_data = []
        for col in collections:

            tmp = []
            for obj in self.db[col].find():
                tmp.append(obj)
            if "tournaments" in col:
                tournaments_data = tmp
            elif "odds" in col:
                odds_data = tmp
            elif "horses" in col:
                horses_data = tmp
            elif "races" in col:
                races_data = tmp
            elif "predict" in col:
                predict_data = tmp

        return races_data, odds_data, tournaments_data, horses_data, predict_data

mongo = mongodb()

if __name__ == '__main__':
    collections = mongo.get_collections(DATABASE_NAME)
    data = mongo.get_data(collections)
