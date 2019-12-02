from pymongo import MongoClient
import getpass
import json
import os
from functions import connect
# from functions import updateParticipants



def main():

    db, coll = connect('datamad1019','chats')

    with open('./chats.json') as f:
        chats_json = json.load(f)
        for chatmsg in chats_json:
            coll.insert_one(chatmsg)

    # updateParticipants(coll)
    # df = pd.DataFrame(list(coll.find({})))

    # #Adding Participants column for each object
    # df["Participants"] = df.idChat.apply(lambda x: list(df[df.idChat == x].idUser.unique()))

    # #Updating Database in MongoDB
    # for index, row in df.iterrows():
    #     setting = [int(e) for e in row["Participants"]]
    #     coll.update_one(
    #         { "_id": ObjectId(row["_id"]["$oid"]) },
    #         { "$set": { "Participants": setting} },
    #     )

if __name__ == "__main__":
    main()