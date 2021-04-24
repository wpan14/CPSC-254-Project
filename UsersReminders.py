import datetime
import discord
import sqlite3

class UsersReminders:
    def __init__(self, db_name): #username
        self.db = sqlite3.connect(db_name) # connect to databse.  if database with name "db_name" does not exist, it will be created
        self.cur = self.db.cursor()
        self.cur.execute("CREATE TABLE if not exists Reminders (User text, Day date, Hour text, Minute text, Message text)") # create reminders table if it doesn't already exist
        print("========= Initial data in database on startup =========")
        for row in self.cur.execute('SELECT * FROM Reminders'):
            # our reminder fields
            RmUser = row[0]
            RmDay = row[1]
            RmHour = row[2]
            RmMinute = row[3]
            RmMessage = row[4]
            print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)

        print()
        print("=========== Deleting old reminder records ============")
        self.cur.execute("DELETE FROM Reminders WHERE datetime(Day,'+' || Hour || ' hours','+' || Minute ||' minutes') < datetime('now', 'localtime')")
        self.db.commit()    
        #display remaining records
        for row in self.cur.execute("SELECT * FROM Reminders WHERE datetime(Day,'+' || Hour || ' hours','+' || Minute ||' minutes') < datetime()"):
            # our reminder fields
            RmUser = row[0]
            RmDay = row[1]
            RmHour = row[2]
            RmMinute = row[3]
            RmMessage = row[4]
            print(RmUser +','+ RmDay +','+ RmHour +','+ RmMinute +','+ RmMessage)



    def __del__(self):
        self.db.commit()
        self.db.close()

    # adds new reminder to database
    def add(self, author, day, hour, minute, msg):
        ReminderRecord = (str(author), day, hour, minute, msg)

        self.cur.execute('INSERT INTO Reminders VALUES (?,?,?,?,?)', ReminderRecord) # insert into reminder table
        self.db.commit()
        print("reminder added: "+str(author) +','+ str(day) +','+ str(hour) +','+ str(minute) +','+ msg)

    # returns all reminders with specified date and time
    def getReminders(self, day, hour, minute): #(string,string,string) return list (of table rows)
        tmpList = []
        tmp =  self.cur.execute('SELECT * FROM Reminders WHERE Day=? AND Hour=? AND Minute=?;', (day, hour, minute))
        for x in tmp:
            tmpList.append(x)
        return tmpList

    # deletes reminder with specified user, day, time, and message
    def deleteReminder(self, user, day, hour, minute, message): #(string,string,string,string,string) return nothing
        self.cur.execute('DELETE FROM Reminders WHERE User=? AND Day=? AND Hour=? AND Minute=? AND Message=?;', (user, day, hour, minute, message))
        self.db.commit()