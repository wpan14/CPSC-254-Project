import datetime
import discord
import sqlite3

class UsersReminders:
    def __init__(self, messageauthor): #username
        # dates = {
        #     0 : monhours[], #monday
        #     1 : tuehours[], #tuesday
        #     2 : wedhours[], #wednesday
        #     3 : thuhours[], #thursday
        #     4 : frihours[], #friday
        #     5 : sathours[], #saturday
        #     6 : sunhours[] #sunday
        # }
        self.dates = dict.fromkeys(range(7), [])
        self.messageauthor = messageauthor
        print(self.dates)

    def add(self, day, hour, minute, msg):
        self.dates[day].append([datetime.time(hour, minute), msg])

        #==== On New Reminder ======================================================================================================================================
        con = sqlite3.connect('DiscordReminders.db')

        cur = con.cursor()

        ReminderRecord = (str(self.messageauthor), day, hour, minute, msg)

        cur.execute('INSERT INTO Reminders VALUES (?,?,?,?,?)', ReminderRecord)
        con.commit()

        for row in cur.execute('SELECT * FROM Reminders'):
            # our reminder fields
            RmUser = row[0]
            RmDay = row[1]
            RmHour = row[2]
            RmMinute = row[3]
            RmMessage = row[4]

            print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)

        #===========================================================================================================================================================
