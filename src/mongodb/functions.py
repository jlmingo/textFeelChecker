from pymongo import MongoClient
import getpass

def connection(database, collection):
    password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
    connection = 'mongodb+srv://jlmingo:{}@cluster0-a5ym7.mongodb.net/test?retryWrites=true&w=majority'.format(password)
    client = MongoClient(connection)
    db = client[database]
    coll = db[collection]
    return db, coll
    