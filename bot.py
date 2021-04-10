import discord
import threading
import time
import datetime
import asyncio
from UsersReminders import UsersReminders
import sqlite3
#from discord.ext import commands

#==== On Program Startup ===================================================================================================================================
con = sqlite3.connect('DiscordReminders.db')

cur = con.cursor()

cur.execute("CREATE TABLE if not exists Reminders (User text, Day text, Hour text, Minute text, Message text)")

cur.execute("DELETE FROM Reminders")
con.commit()

for row in cur.execute('SELECT * FROM Reminders'):
    # our reminder fields
    RmUser = row[0]
    RmDay = row[1]
    RmHour = row[2]
    RmMinute = row[3]
    RmMessage = row[4]

    # instead of just printing, add these to the open reminders
    print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)
#===========================================================================================================================================================


test = []
client = discord.Client()
commandSymbol = '!'
default_channel = 812184884218953743#server-id = 812184884218953738
index = 0


async def time_check():
    await client.wait_until_ready()
    #print("working")
    while True:
        await asyncio.sleep(40)
        #print("working")
        now = datetime.datetime.now()
        for x in test:
            for i in x.dates[datetime.datetime.today().weekday()]:
                if now.hour == i[0].hour and now.minute == i[0].minute:
                    #print(now.hour == i.hour)
                    await client.get_channel(default_channel).send("[%s] %s" % (x.messageauthor.mention, i[1]))

def contains(test, messageauthor):
    for x in test:    
        if x.messageauthor == messageauthor:
            return True
    return False

def day(date): #!add monday 14
    day = date[date.find(' ') + 1: date.find(' ', 5)]
    day = day.upper()

    if day == "MONDAY":
        return 0
    if day == "TUESDAY":
        return 1
    if day == "WEDNESDAY":
        return 2
    if day == "THURSDAY":
        return 3
    if day == "FRIDAY":
        return 4
    if day == "SATURDAY":
        return 5
    if day == "SUNDAY":
        return 6
    
    return -1

def hour(date):
    print(date[date.find(' ', 5) + 1 : ])
    hour = date[date.find(' ', 5) + 1 : date.find(':')]
    hour = int(hour)
    if hour > 23:
        hour = 23
    
    if hour < 0:
        hour = 0

    return hour

def minute(date):
    minute = date[date.find(':') + 1 : date.find(' ', date.find(':'))]
    minute = int(minute)

    if minute > 59:
        minute = 59
    
    if minute < 0:
        minute = 0

    return minute

def msgContent(msg):
    tmpMsg = msg[msg.find(' ', msg.find(':')) + 1:]
    print(tmpMsg)
    return tmpMsg

# thread = threading.Thread(target = check_time, args = ())
# thread.start()

@client.event
async def on_ready():
    print('Bot is ready.')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
#    if message.content.startswith(commandSymbol + 'displayreminders'):
#        for row in cur.execute('SELECT * FROM Reminders'):
##            # our reminder fields
 #           RmUser = row[0]
 #           RmDay = row[1]
 #           RmHour = row[2]
 #           RmMinute = row[3]
 #           RmMessage = row[4]
 #
#            print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)


    if message.content.startswith(commandSymbol + "channelid"):
        default_channel = int(message.content[11: len(message.content)]) #client.get_channel()
        print(message.content[11: len(message.content)])
        await message.channel.send('Channel set to: ' + str(default_channel))
    
    if message.content.startswith(commandSymbol + 'ping'):
        await message.channel.send('Pinging {}'.format(message.author.mention))

    if message.content.startswith(commandSymbol + 'add'):
        if (day(message.content) == -1):
            await message.channel.send("Invalid day, please try again\n $add day hour(24hr):minute")
        elif not contains(test, message.author):# If the user has not entered a reminder yet, this is called
            test.append(UsersReminders(message.author))
            test[len(test) - 1].add(day(message.content), hour(message.content), minute(message.content), msgContent(message.content))

            await message.channel.send("{} reminder added".format(message.author.mention))
        elif contains(test, message.author):# If the user has already entered a different reminder, this is called.  BONUS FEATURE: This always adds the reminder under the most recent previous reminder's user
            test[len(test) - 1].add(day(message.content), hour(message.content), minute(message.content), msgContent(message.content))
            await message.channel.send("{} reminder added".format(message.author.mention))




    
client.loop.create_task(time_check())
client.run('ODEyMTg2Mzg4NDIxODA0MDMy.YC9FhA.TqYJpOQ4C9NiE2qZ8UDxPDoLZjo')