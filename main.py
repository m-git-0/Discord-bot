import discord
import os
import requests #allows to make an http request
import json #to work with return from api
import random

from replit import db
from keep_alive import keep_alive

my_secret = os.environ['env']

client = discord.Client()
#create a two lists, one for encuraging words and another for sad words
sad_words = ['sad','depressed','unhappy','angry',"kill","feeling down","upset","gloomy", "bleak", "dreary", "grim", "drab", "sombre", "dark", "dingy", "funereal", "miserable", "cheerless", "joyless", "comfortless", "uninviting"]
starter_encouragements = ["cheer up!","Hang in there.","You are a great person / bot!"]

if "responding" not in db.keys():
    #default value is true
    db["responding"] = True

    
#function to return a quote from the api
def get_quote():
    #use the request module
    response = requests.get('https://zenquotes.io/api/random/')
    #observe the use of json.loads() intead on json.load()
    json_data = json.loads(response.text)
    quote = json_data[0]['q']+" -"+json_data[0]['a']
    return quote

    
#function to add encouragements   
#accept an encouraging message as an argument
def update_encouragements(encouraging_message):
    #check if encouragements is a key in the database
    if 'encouragements' in db.keys():
        #if true, get alist of the stored encouragements
        encouragements = db["encouragements"]
        #then append the new encouragemtn to the list
        encouragements.append(encouraging_message)
        #save the list to the database uder the key
        db['encouragements'] = encouragements
    #if the key does not exist in in the database, we create it
    else:
        #add the encouraging message into th edatabse
        db['encouragements'] = [encouraging_message]

  
#function to delete encouragement message
#take an index as an urgument
def delete_encouragement(index):
    #get the list of encouragements from the databse
    encouragements = db['encouragements']
    #check if the length of the list is more than the index
    if len(encouragements)>index:
        #if true, delete the encouragement at that index
        del encouragements[index]
        #add thenew list of encouragements to the databse
        db["encouragements"]=encouragements
    else:
        print("database empty")

    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    #read the message typed on the channel
    msg = message.content
    #inore essages from the bot
    if message.author==client.user:
        return
    #text a random quote   
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    #advance the list of encouragements to load encouragements
    #from the databse
    #if responding is enabled for the bot
    if db["responding"]:
        options =  starter_encouragements
        if "encouragements" in db.keys():
            #concatenate the encouragements from the database and the list
            options = options + list(db["encouragements"])
    
        if any(word in msg for word in sad_words):
            rand_word = random.choice(options)
            await message.channel.send(rand_word)

    if msg.startswith('$new'):
        #get the encouraging message
        encouraging_message = msg.split('$new ',1)[1]
        update_encouragements(encouraging_message)

        await message.channel.send("New encouraging message saved")
        
    #add the ability for the user to delete an encouragement
    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del",1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(list(encouragements))
    #another functionality to list all the encouragements in the 
    #database
    if msg.startswith("$list"):
        encouragements=[]
        if "encouragements" in db.keys():
            encouragements = list(db["encouragements"])
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ",1)[1]
        if value.lower()=="true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db['responding'] = False
            await message.channel.send("Responding is off.")
keep_alive()
client.run(my_secret)
