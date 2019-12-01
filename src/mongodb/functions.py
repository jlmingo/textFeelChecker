from pymongo import MongoClient
import getpass
import pandas as pd
from bson import ObjectId
import pymongo

def connection(database, collection):
    password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
    connection = 'mongodb+srv://jlmingo:{}@cluster0-a5ym7.mongodb.net/test?retryWrites=true&w=majority'.format(password)
    client = MongoClient(connection)
    db = client[database]
    coll = db[collection]
    return db, coll

#updates Participants column
def updateParticipants(coll):
    df = pd.DataFrame(list(coll.find({})))
    if 'Participants' in df.columns:
     df.drop(['Participants'], axis=1, inplace=True)
    df["Participants"] = df.idChat.apply(lambda x: list(df[df.idChat == x].idUser.unique()))
    for index, row in df.iterrows():
        setting = [int(e) for e in row["Participants"]]
        coll.update_one(
            { "_id": ObjectId(row["_id"]["$oid"]) },
            { "$set": { "Participants": setting} },
        )
