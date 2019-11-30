import requests
from bottle import route, run
from functions import connection
from bson.json_util import dumps


@route('/data')
def data():
    return dumps(collection.find())

database, collection = connection('datamad1019','chats')
run(host='localhost', port=8080, debug=True)
