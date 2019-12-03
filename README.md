# textFeelChecker

## Project description

The project consists on deploying a chat database in Atlas MongoDB, and being able to check the data as well as adding users, chats and messages. It also uses the use TextBlob library to check sentiment of messages. Finally, it recommends top3 related user to a selected user.

## Brief description of files

**testApi** This is a Jupyter Notebook with an example of the requests that can be made to the API.

**erase** to delete the whole database from Atlas. Use it carefully :(

**functions** includes functions used to connect to Atlas and update fields of Participants by chat and Sentiment by message.

**api** includes the basic functions of the API

## API instructions

Requesting whole database:

`requests.get("http://localhost:8080/data").json()`

Creating user:

`usuario = {
    "name": "Prueba33"
}
requests.post("http://localhost:8080/user/create", data=usuario)`

Creating chat:

`participants = {
    "participants": [3,4]
}`

`requests.post("http://localhost:8080/user/create", data=participants)`

Getting messages from certain chat:

`chat = {
    "chat_id": 0,
}`

`requests.get("http://localhost:8080/chat/list", data=chat)`

Adding message:

`message = {
    "username": "John Wick",
    "idChat": 0,
    "text": "I'm John Wick, prepare to die"
}`

`requests.post("http://localhost:8080/chat/addmessage", data=message)`

Testing chat/sentiment route:

`chat = {
    "chat_id": 0,
}`

`requests.get("http://localhost:8080/chat/sentiment", data=chat).json()`

## Next steps
Following improvements to be implemented are:
 1) Managing error handling
 2) Deploying the API in Docker / Heroku
 3) Getting bubble chart. There is a function to get a bubble chart that shows the feeling of several users. Positive comments are at the right and have a darker colour, while more subjective comments increase with y axis and are bigger in size. It was not possible to send it by request this time, but this is a point to implement, as well as selecting the chart by user, chat, and so on.

![Image](https://raw.githubusercontent.com/jlmingo/textFeelChecker/master/src/mongodb/output.png)