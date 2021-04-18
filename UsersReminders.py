import datetime
import discord
import sqlite3

class UsersReminders:
    def __init__(self, db_name): #username
        # dates = {
        #     0 : monhours[], #monday
        #     1 : tuehours[], #tuesday
        #     2 : wedhours[], #wednesday
        #     3 : thuhours[], #thursday
        #     4 : frihours[], #friday
        #     5 : sathours[], #saturday
        #     6 : sunhours[] #sunday
        # }
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()
        self.cur.execute("CREATE TABLE if not exists Reminders (User text, Day date, Hour text, Minute text, Message text)")
        print("========= Initial data in database on startup =========")
        for row in self.cur.execute('SELECT * FROM Reminders'):
            # our reminder fields
            RmUser = row[0]
            RmDay = row[1]
            RmHour = row[2]
            RmMinute = row[3]
            RmMessage = row[4]

            print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)

        print("=========== Deleting old reminder records ============")
        self.cur.execute("DELETE FROM Reminders WHERE datetime(Day,'+' || Hour || ' hours','+' || Minute ||' minutes') < datetime()")
        self.db.commit()    

        #self.cur.execute("DELETE FROM Reminders;")      # Delete to save previous results
        #self.dates = dict.fromkeys(range(7), [])
        #   self.messageauthor = messageauthor
        #   print(self.dates)

    def __del__(self):
        self.db.commit()
        self.db.close()

    def add(self, author, day, hour, minute, msg):
        #self.dates[day].append([datetime.time(hour, minute), msg])

        #==== On New Reminder ======================================================================================================================================
        #cur = con.cursor()

        ReminderRecord = (str(author), day, hour, minute, msg)

        self.cur.execute('INSERT INTO Reminders VALUES (?,?,?,?,?)', ReminderRecord)
        self.db.commit()

        for row in self.cur.execute('SELECT * FROM Reminders'):
            # our reminder fields
            RmUser = row[0]
            RmDay = row[1]
            RmHour = row[2]
            RmMinute = row[3]
            RmMessage = row[4]

            print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)

        #display all current reminders to console.  remove this later
        print()

        #===========================================================================================================================================================
    def getReminders(self, day, hour, minute):
        tmpList = []
        tmp =  self.cur.execute('SELECT * FROM Reminders WHERE Day=? AND Hour=? AND Minute=?;', (day, hour, minute))
        for x in tmp:
            tmpList.append(x)
        return tmpList

    def deleteReminder(self, user, day, hour, minute, message):
        self.cur.execute('DELETE FROM Reminders WHERE User=? AND Day=? AND Hour=? AND Minute=? AND Message=?;', (user, day, hour, minute, message))
        self.db.commit()