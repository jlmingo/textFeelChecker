#!/usr/bin/env python3

import requests
from bottle import route, run, post, request
from functions import connection
from bson.json_util import dumps


@route('/data')
def data():
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
    participants = list(request.forms.get("participants"))
    new_id = max(collection.distinct("idChat")) + 1
    new_chat = {
        "idChat": new_id,
        "Participants": participants
    }
    collection.insert_one(new_chat)
    # return dumps(idChat)

# @post("/chat/<chat_id>/addmessage")
# def addMessage():
#     participants = list(request.forms.get("participants"))
#     new_id = max(collection.distinct("idChat")) + 1
#     new_chat = {
#         "idChat": new_id,
#         "Participants": participants
#     }
#     collection.insert_one(new_chat)
    
database, collection = connection('datamad1019','chats')
run(host='localhost', port=8080, debug=True)
