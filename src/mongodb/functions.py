from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pandas as pd
from bson import ObjectId
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
from textblob import TextBlob

mongodbUrl = os.getenv("CLIENT")
client = MongoClient(mongodbUrl)
try:
    print(f"connecting to {mongodbUrl[0:12]}")
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected")
except ConnectionFailure:
    raise Exception("Server not available")


def connect(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll

#updates Participants column
def updateParticipants(coll):
    df = pd.DataFrame(list(coll.find()))
    if 'Participants' in df.columns:
        df.drop(['Participants'], axis=1, inplace=True)
    df["Participants"] = df.idChat.apply(lambda x: list(df[((df.idChat == x) & (df.idUser.isnull() == False))].idUser.unique()))
    for index, row in df.iterrows():
        setting = [int(e) for e in row["Participants"]]
        coll.update_one(
            { "_id": row["_id"] },
            { "$set": { "Participants": setting} },
        )
#updates Sentiment column
def updateSentiment(coll):
    df = pd.DataFrame(list(coll.find()))
    if 'Sentiment' in df.columns:
        df.drop(['Sentiment'], axis=1, inplace=True)
    df["Sentiment"] = df[df["text"].isnull() == False]["text"].map(lambda x: TextBlob(str(x)).sentiment)
    for index, row in df.iterrows():
        # setting = [e for e in row["Sentiment"]]
        coll.update_one(
            { "_id": row["_id"] },
            { "$set": { "Sentiment": row["Sentiment"]} },
        )