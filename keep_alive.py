#import flask and use it as the webserver
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
#return hello, i am alive to anyone who visits the server
def home():
    return "Hello i am alive"

def run():
    app.run(host='0.0.0.0',port=8080)
    
#the server will run on a separate thread from our bot
#this is the code that runs our webserver
def keep_alive():
    t = Thread(target=run)
    t.start()