#!/usr/bin/python3

from pymongo import MongoClient
import getpass
import json
import os
from bson import ObjectId
import pymongo

def main():
    #Get Password
    password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
    connection = "mongodb+srv://jlmingo:{}@cluster0-a5ym7.mongodb.net/test?retryWrites=true&w=majority".format(password)

    #Connect to DB
    client = MongoClient(connection)
    def connectCollection(database, collection):
        db = client[database]
        coll = db[collection]
        return db, coll

    db, coll = connectCollection('datamad1019','chats')

    with open('../../input/chats.json') as f:
        chats_json = json.load(f)
    coll.insert_many(chats_json)
    
    df = pd.DataFrame(list(coll.find({})))

    #Adding Participants column for each object
    df["Participants"] = df.idChat.apply(lambda x: list(df[df.idChat == x].idUser.unique()))

    #Updating Database in MongoDB
    for index, row in df.iterrows():
        setting = [int(e) for e in row["Participants"]]
        coll.update_one(
            { "_id": ObjectId(row["_id"]["$oid"]) },
            { "$set": { "Participants": setting} },
        )

if __name__ == "__main__":
    main()