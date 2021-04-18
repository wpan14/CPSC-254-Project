import discord
import threading
import time
import datetime
from datetime import timedelta
import asyncio
from UsersReminders import UsersReminders
from discord.ext import commands

#client = discord.Client()
commandSymbol = '!'
bot = commands.Bot(command_prefix='!')
default_channel = 812184884218953743#server-id = 812184884218953738
index = 0

reminders = UsersReminders('DiscordReminders.db')

async def time_check():
    await bot.wait_until_ready()
    #print("working")
    while True:
        now = datetime.datetime.now()
        reminderDate = now + timedelta(minutes=1)
        diff = reminderDate.replace(second=0) - now
        totalSeconds = diff.seconds
        await asyncio.sleep(totalSeconds)

        now = datetime.datetime.now()
        for row in reminders.getReminders(datetime.date.today(), str(now.hour), str(now.minute)):
            print(row)
            await bot.get_channel(default_channel).send("[%s] %s" % (row[0], row[4]))
            #delete reminder after reminder is sent
            reminders.deleteReminder(row[0], row[1], row[2], row[3], row[4])

def day(date): #(string) return date
    day = date[date.find(' ') + 1: date.find(' ', 5)]  #!add Saturday 15:03 test1  MM/DD/YYYY
    day = day.upper()

    today = datetime.date.today()
    currentWeekDay = datetime.date.weekday(today) #int monday = 0

    if day == "MONDAY":
        return nextWeekDayDate(currentWeekDay,0)
    if day == "TUESDAY":
        return nextWeekDayDate(currentWeekDay,1)
    if day == "WEDNESDAY":
        return nextWeekDayDate(currentWeekDay,2)
    if day == "THURSDAY":
        return nextWeekDayDate(currentWeekDay,3)
    if day == "FRIDAY":
        return nextWeekDayDate(currentWeekDay,4)
    if day == "SATURDAY":
        return nextWeekDayDate(currentWeekDay,5)
    if day == "SUNDAY":
        return nextWeekDayDate(currentWeekDay,6)
    
    try:
        targetDate = datetime.datetime.strptime(day, '%m-%d-%Y').date()
        return targetDate
    except:
        try:
            targetDate = datetime.datetime.strptime(day, '%m/%d/%Y').date()
            return targetDate
        except:
            return -1

        return -1

    return -2 # you should never see this

def nextWeekDayDate(currentWeekDay, targetWeekDay): #(int,int) return date
    if currentWeekDay > targetWeekDay:
        return (datetime.date.today() + timedelta(days=(7-(currentWeekDay-targetWeekDay))))
    elif currentWeekDay < targetWeekDay:
        return (datetime.date.today() + timedelta(days=(targetWeekDay-currentWeekDay)))
    elif currentWeekDay == targetWeekDay:
        return (datetime.date.today())

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

@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command(name ='jazz')
async def jazz(ctx):  # link to 24/7 livestream of jazz music
    await ctx.send('https://www.youtube.com/watch?v=Dx5qFachd3A')


@bot.command(name ='pop')
async def pop(ctx):  # link to 24/7 livestream of pop music
    await ctx.send('https://www.youtube.com/watch?v=tmpWVmsAtOw')


@bot.command(name ='eswing')  # link to 24/7 livestream of electro swing music
async def eswing(ctx):
    await ctx.send('https://www.youtube.com/watch?v=bGZIeVsaQ5Y')


@bot.command(name ='classical')  # link to 24/7 livestream of classical music
async def classical(ctx):
    await ctx.send('https://www.youtube.com/watch?v=_3IphE64yRA')


@bot.command(name ='funk')  # link to 24/7 livestream of funk music
async def funk(ctx):
    await ctx.send('https://www.youtube.com/watch?v=L1vXBMmH-Fw')




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        '''
    if message.content.startswith(commandSymbol + "channelid"):
        default_channel = int(message.content[11: len(message.content)]) #client.get_channel()
        print(message.content[11: len(message.content)])
        await message.channel.send('Channel set to: ' + str(default_channel))'''
    

    if message.content.startswith(commandSymbol + 'add'):
        if (day(message.content) == -1):
            await message.channel.send("Invalid day, please try again\n $add day hour(24hr):minute")
        else:
            reminders.add(message.author.mention, day(message.content), hour(message.content), minute(message.content), msgContent(message.content))
            await message.channel.send("{} reminder added".format(message.author.mention))
    else:
        await bot.process_commands(message)




bot.loop.create_task(time_check())
bot.run('ODEyMTg2Mzg4NDIxODA0MDMy.YC9FhA.TqYJpOQ4C9NiE2qZ8UDxPDoLZjo')