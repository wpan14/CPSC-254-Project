import discord
import threading
import time
import datetime
from datetime import timedelta
import asyncio
from UsersReminders import UsersReminders
from UsersReminders import timer

from discord.ext import commands
import youtube_dl

commandSymbol = '!' # symbol to denote a call to the bot
bot = commands.Bot(command_prefix='!')
default_channel = 812184884218953743#server-id = 812184884218953738
index = 0

# TimerList
timeList = []

# iniialize reminders database
reminders = UsersReminders('DiscordReminders.db')

# Checks reminders stored in database every minute to determine if there is one that must be displayed
async def time_check():
    await bot.wait_until_ready()
    while True:
        now = datetime.datetime.now()
        reminderDate = now + timedelta(minutes=1)
        diff = reminderDate.replace(second=0) - now
        totalSeconds = diff.seconds
        await asyncio.sleep(totalSeconds)

        now = datetime.datetime.now()
        for row in reminders.getReminders(datetime.date.today(), str(now.hour), str(now.minute)): # loops though all reminders with a datetime now
            print(row)
            await bot.get_channel(default_channel).send("[%s] %s" % (row[0], row[4])) # sends reminder in discord

            reminders.deleteReminder(row[0], row[1], row[2], row[3], row[4]) #delete reminder after reminder is sent


# parses date/day of reminder out of the message to the bot.  returns date of the reminder
def day(msg): #(string) return date
    day = msg[msg.find(' ') + 1: msg.find(' ', 5)] #finds substring that should be day/date
    day = day.upper()

    today = datetime.date.today()
    currentWeekDay = datetime.date.weekday(today)

    # if weekday was found instead of a date, return the date of the next found weekday
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
        targetDate = datetime.datetime.strptime(day, '%m-%d-%Y').date() # checks for date formatted like month-day-year
        return targetDate
    except: # if month-day-year not found
        try:
            targetDate = datetime.datetime.strptime(day, '%m/%d/%Y').date() # checks for date formatted like month/day/year
            return targetDate
        except: # if month/day/year not found
            return -1 # this means no valid weekday or date was found.

        return -2 # you should never see this

    return -2 # you should never see this

# returns next date of weekday
def nextWeekDayDate(currentWeekDay, targetWeekDay): #(int,int) return date
    if currentWeekDay > targetWeekDay:
        return (datetime.date.today() + timedelta(days=(7-(currentWeekDay-targetWeekDay))))
    elif currentWeekDay < targetWeekDay:
        return (datetime.date.today() + timedelta(days=(targetWeekDay-currentWeekDay)))
    elif currentWeekDay == targetWeekDay:
        return (datetime.date.today())

# parses hour of reminder out of the message to the bot.  returns int of the hour
def hour(msg): #(string) return int
    hour = msg[msg.find(' ', 5) + 1 : msg.find(':')] # finds substring that should be hour
    hour = int(hour)
    if hour > 23:
        hour = 23

    if hour < 0:
        hour = 0

    return hour

# parses minute of reminder out of the message to the bot.  returns int of the minute
def minute(msg): #(string) return int
    minute = msg[msg.find(':') + 1 : msg.find(' ', msg.find(':'))] # finds substring that should be minute
    minute = int(minute)

    if minute > 59:
        minute = 59

    if minute < 0:
        minute = 0

    return minute

# parses reminder text of reminder out of the message to the bot.  returns string of the reminder text
def msgContent(msg): #(string) return string
    tmpMsg = msg[msg.find(' ', msg.find(':')) + 1:] # finds substring that should be reminder text (everything left over after the date/day and time)
    return tmpMsg

# thread = threading.Thread(target = check_time, args = ())
# thread.start()

@bot.event
async def on_ready():
    print('Bot is ready.')

#=== links to music playlists on YouTube ===================================================================================================
@bot.command(name='jazz')
async def jazz(ctx):  # link to 24/7 livestream of jazz music
    await ctx.send('https://www.youtube.com/watch?v=Dx5qFachd3A')


@bot.command(name='pop')
async def pop(ctx):  # link to 24/7 livestream of pop music
    await ctx.send('https://www.youtube.com/watch?v=tmpWVmsAtOw')


@bot.command(name='eswing')
async def eswing(ctx): # link to 24/7 livestream of electro swing music
    await ctx.send('https://www.youtube.com/watch?v=bGZIeVsaQ5Y')


@bot.command(name='classical')
async def classical(ctx): # link to 24/7 livestream of classical music
    await ctx.send('https://www.youtube.com/watch?v=_3IphE64yRA')


@bot.command(name='funk')
async def funk(ctx): # link to 24/7 livestream of funk music
    await ctx.send('https://www.youtube.com/watch?v=L1vXBMmH-Fw')


#Constants for youtube audio downloader
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_FormOpts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_FormOpts)

#Youtuber audio downloader
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


# command lets bot join voice channel
@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("BotBot has joined the voice channel.")
    else:  # Error message shown if user enters the join command without being in a voice channel.
        await ctx.send(
            "Error. User is not in Voice Channel. User need to be in a Voice Channel for this command to work.")


# command makes bot leave voice channel.
@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("BotBot has left the voice channel")
    else:  # Error message shown if the bot is not in a voice channel.
        await ctx.send("Error: BotBot is not in a voice channel.")


# command plays music when given url by user
@bot.command(name='play')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("BotBot is not connected to a voice channel.")


# command pauses the song that's currently playing
@bot.command(name='pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("BotBot is not playing anything at the moment.")


# command plays music that is currently paused
@bot.command(name='resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("BotBot was not playing anything before this; use !play <YouTube URL> to play a song")


# command stops music from playing
@bot.command(name='stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("BotBot is not playing anything at the moment.")


#===========================================================================================================================================

# Timer List check
async def timeList_check():
    await bot.wait_until_ready()
    while True:
            await asyncio.sleep(1)

            for x in timeList:
                if x.time > 0: # Any timers with time left is reduced by 1 second
                    x.time = x.time - 1
                if x.time == 0: # Prints timer is done for the user, then removes the timer
                    await bot.get_channel(default_channel).send("Timer done for {}".format(x.msgAuthor))
                    timeList.remove(x)



@bot.event
async def on_message(message):
    if message.author == bot.user: # prevents bot from ever calling itself
        return
    if message.content.startswith(commandSymbol + 'timer'): #Timer function call
        timeList.append(timer(message.author.mention, message.content))
        await message.channel.send("{} timer set".format(message.author.mention))
    if message.content.startswith(commandSymbol + 'add'): # if user calls the add function to add a new reminder
        if (day(message.content) == -1): # invalid day/date
            await message.channel.send("Invalid day, please try again\n $add day hour(24hr):minute")
        else: # add the reminder
            reminders.add(message.author.mention, day(message.content), hour(message.content), minute(message.content), msgContent(message.content))
            await message.channel.send("{} reminder added".format(message.author.mention))
    else:
        await bot.process_commands(message)



bot.loop.create_task(time_check())
bot.loop.create_task(timeList_check())
bot.run('ODEyMTg2Mzg4NDIxODA0MDMy.YC9FhA.TqYJpOQ4C9NiE2qZ8UDxPDoLZjo')
