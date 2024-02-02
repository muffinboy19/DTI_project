from pymongo import MongoClient
import certifi
import os

ca = certifi.where()
MONGO_PASS = os.getenv("MONGO_PASS")

client=MongoClient(MONGO_PASS, tlsCAFile=ca)
db=client.AnomAlert
users=db.users
cameras=db.cameras
