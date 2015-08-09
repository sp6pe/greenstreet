import os 
import sys
import datetime
from datetime import timedelta

#dependencies
import pymongo
import requests
# from bson import json_util


def getenv(key):
   val = os.environ.get(key)
   if val:
       return val
   elif os.path.isfile('.env'):
       f = open('.env')
       s = f.read()
       f.close()
       for line in s.strip().split('\n'):
           k, v = line.split('=')
           if k == key:
               return v
   return None


def connect_db(url, app_name):
   client = pymongo.MongoClient(getenv(url))
   db = client[getenv(app_name)]

   return db