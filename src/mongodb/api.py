#!/usr/bin/env python3

import requests
from bottle import route, run, post, request
from functions import connect, updateParticipants, updateSentiment
from bson.json_util import dumps
from bson import ObjectId
import pymongo
import datetime
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bottle import static_file

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
    # sentiment = {}
    # messages = list(collection.find({"idChat": chat_id}, {"idMessage": 1, "text": 1, "_id":0, "Sentiment":1}))
    # for one_message in messages:
    #     sentiment[one_mesage["idMessage"]] = {
    #         "text": [one_message][""]
    #     }
    updateSentiment(collection)
    return dumps(collection.find({"idChat": chat_id}))

@route('/user/recommend')
def sentiment():
    user_id = str(request.forms.get("user_id"))
    unique_users = collection.distinct("idUser")
    dict_users = {}
    for user in unique_users:
        try:
            dict_users[str(user)] = " ".join([e["text"] for e in list(collection.find({"idUser": user}, {"text": 1, "_id":0}))])
        except:
            pass
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(dict_users.values())
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=dict_users.keys())
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=dict_users.keys(), index=dict_users.keys())
    recommendation = list(sim_df.sort_values(by=[user_id]).index[0:3])
    return {"recommendation": recommendation}


database, collection = connect('datamad1019','chats')
run(host='localhost', port=8080, debug=True)

# To be implemented
# @route('/plot/users')
# def server_static():
#     dic = list(collection.find({"idChat": 0},{"Sentiment":1, "_id":0, "userName": 1}))
#     polarity = [e["Sentiment"][0] for e in dic]
#     subjectivity = [e["Sentiment"][1] for e in dic]
#     labels = [e["userName"] for e in dic]
#     df = pd.DataFrame(list(zip(subjectivity, polarity)), columns=["subjectivity", "polarity"])
#     sns.set()
#     cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
#     fig, ax = plt.subplots(figsize=(8,5))
#     ax = sns.scatterplot(x="polarity", y="subjectivity", size="subjectivity", hue="polarity",
#                         palette=cmap, sizes=(80, 200),
#                         data=df, legend="brief")
#     fig.savefig("output.png")
#     return static_file("output.png", root=f'./output.png')