#!/usr/bin/env python3

import requests
from bottle import route, run, post, request
from functions import connect, updateParticipants, updateSentiment
from bson.json_util import dumps
from bson import ObjectId
import pymongo
import datetime
from textblob import TextBlob

@route('/data')
def data():
    updateSentiment(collection)
    return dumps(collection.find({}))

@post('/user/create')
def newUser():
    name = str(request.forms.get("name"))
    new_id = max(collection.distinct("idUser")) + 1
    new_user = {
        "idUser": new_id,
        "userName": name
    }
    collection.insert_one(new_user)
    print(f"{name} added to collection with id {new_id}") #this is not working :(

@post('/chat/create')
def chatCreate():
    participants = list(request.forms.getlist("partic"))
    participants = [int(e) for e in participants]
    if set(participants).issubset(set(collection.distinct("idUser"))):
        new_id = max(collection.distinct("idChat")) + 1
        new_chat = {
            "idChat": new_id,
            "Participants": participants
        }
        collection.insert_one(new_chat)
        updateParticipants(collection)
    else:
        return {"Error": "Please input existing users."}
    # return dumps(idChat)

@route('/chat/list')
def data():
    chat_id = int(request.forms.get("chat_id"))
    return dumps(collection.find({"idChat": chat_id}, {"idChat": 1, "text": 1, "Sentiment": 1}))

@post("/chat/addmessage")
def addMessage():
    user = request.forms.get("username")
    id_Chat = int(request.forms.get("idChat"))
    text = request.forms.get("text")
    if id_Chat in collection.find({"userName": user}).distinct("idChat"):
        new_id_message = max(collection.distinct("idMessage")) + 1
        new_message = {
            "idUser": collection.find({"userName": user}, {"idUser": 1, "_id": 0}).distinct("idUser")[0],
            "userName": user,
            "idChat": id_Chat,
            "datetime": datetime.datetime.utcnow(),
            "text": text,
        }
        collection.insert_one(new_message)
        updateParticipants(collection)
        updateSentiment(collection)
    else:
        raise ValueError("The user is not in that chat or he does not exist yet.")

@route('/chat/sentiment')
def sentiment():
    chat_id = int(request.forms.get("chat_id"))
    sentiment = {}
    messages = list(collection.find({"idChat": chat_id}, {"idMessage": 1, "text": 1, "_id":0}))
    for one_message in messages:
        sentiment[one_mesage["idMessage"]] = {
            "text": [one_message][""]
        }
    return dumps(collection.find({"idChat": chat_id}))

database, collection = connect('datamad1019','chats')
run(host='localhost', port=8080, debug=True)


# - (POST) `/chat/<chat_id>/addmessage` 
#   - **Purpose:** Add a message to the conversation. 
# Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.
#   - **Params:**
#     - `chat_id`: Chat to store message
#     - `user_id`: the user that writes the message
#     - `text`: Message text