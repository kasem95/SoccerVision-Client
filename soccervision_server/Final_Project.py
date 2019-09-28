import pyodbc
import re
import sys
import datetime
import time
import os

constr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=185.60.170.14;DATABASE=site09;UID=site09;PWD=Lsas171*'


class User:
    username = ""
    email = ""
    password = ""

    def checkEmail(self, email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (re.search(regex, email)):
            self.email = email

        else:
            self.email = ""

    def checkPass(self, password):
        flag = 0
        while True:
            if (len(password) < 8):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                self.password = password
                break

        if flag == -1:
            self.password = ""

    def __init__(self, username, email, password):
        self.username = username
        self.checkEmail(email)
        self.checkPass(password)



def Login(Email, password):
    try:
        con = pyodbc.connect(constr)
        cursor = con.cursor()
        cursor.execute("SELECT * From Python_UsersTB WHERE Email = '"
                       + Email + "' AND Password = '" + password + "'")

        data = cursor.fetchone()
        if data == None or len(data) == 0:
            cursor.close()
            return 0, "There is no such user!"
        if data != None and len(data) == -1:
            cursor.close()
            return 0, "Something wrong!"
        if data != None and len(data) > 0:
            username = data[1]
            userID = data[0]
            cursor.close()
            return 1, username, userID
    except pyodbc.Error as error:
        err_log = open('d:\\err_log.txt', 'a')
        err_log.write(str(error))
        err_log.write('\n----------------------------------\n')
        err_log.close()
        return 0, str(error)
    finally:
        con.close()


def Register(email, username, password):
    try:
        con = pyodbc.connect(constr)
        user = User(username, email, password)
        if user.email == "":
            return "email is not valid"
        if user.password == "":
            return "password is not valid"
        if user.username == "" or user.username == " ":
            return "username is not valid"

        cursor = con.cursor()
        cursor.execute("SELECT * FROM Python_UsersTB WHERE Email = '"
                       + email + "' OR Password = '" + password
                       + "' OR Username = '" + username + "'")
        data = cursor.fetchall()
        if data != None and len(data) > 0:
            cursor.close()
            return "this account is already exists"
        cursor.close()
        cursor = con.cursor()
        result = cursor.execute("INSERT INTO Python_UsersTB(Username,Email,Password, inMatch,Match_ID) VALUES ('"
                                + username + "','" + email + "','" + password + "',0, -1)")
        if result < 1:
            cursor.close()
            return "Something went wrong"
        con.commit()
        cursor.close()
        return "Register complete"
    except pyodbc.Error as error:
        err_log = open('d:\\err_log.txt', 'a')
        err_log.write(str(error))
        err_log.write('\n----------------------------------\n')
        err_log.close()
        return str(error)
    finally:
        con.close()



def MakeAMatch(matchName, userID, matchDate, matchTime, city, field, isPrivate, key):
    try:
        con = pyodbc.connect(constr)
        cursor = con.cursor()
        cursor.execute("SELECT inMatch FROM Python_UsersTB WHERE User_ID = "
                       + str(userid))
        data = cursor.fetchone()
        if data != None and data[0] == True:
            cursor.close()
            return 0, "You are already in match!"
        cursor.close()

        cursor = con.cursor()
        cursor.execute("SELECT * From Python_MatchesTB WHERE (User_ID = "
                       + str(userID) + " AND Match_Date = '" + matchDate + "') OR (Match_Time = '" + matchTime + "' AND Match_Date = '" + matchDate + "')")

        data = cursor.fetchone()
        if data != None and len(data) > 0:
            cursor.close()
            return 0, "your trying to make a match in unavaliable time!/or you have already made a match in this day"
        cursor.close()
        cursor = con.cursor()
        result = cursor.execute("INSERT INTO Python_MatchesTB(Match_Name,User_ID,IsPrivate,Match_Key,Match_Date,Match_Time,City,Field,Players,IsActive) VALUES ('"
                       + matchName + "'," + str(userID) + "," + str(isPrivate) + ",'"+key + "','" + matchDate + "','" + matchTime + "','" + city + "','" + field + "',1,1)")

        if result < 1:
            return 0,"Something went wrong!"
        con.commit()
        cursor.close()
        cursor = con.cursor()
        cursor.execute("SELECT Match_ID From Python_MatchesTB WHERE (User_ID = "
                       + str(userID) + " AND Match_Date = '" + matchDate + "')")

        data = cursor.fetchone()
        cursor = con.cursor()
        result = cursor.execute("UPDATE Python_UsersTB SET inMatch = '1', Match_ID = " + str(data[0]) + " WHERE User_ID = " + str(userid))
        if result < 1:
            cursor.close()
            return 0,"Something went wrong!"
        con.commit()
        cursor.close()
        return 1,"Matchmaking complete!"
    except pyodbc.Error as error:
        err_log = open('d:\\err_log.txt', 'a')
        err_log.write(str(error))
        err_log.write('\n----------------------------------\n')
        err_log.close()
        return 0,str(error)
    finally:
        con.close()


def getMatches():
    try:
        con = pyodbc.connect(constr)
        cursor = con.cursor()
        cursor.execute("SELECT * From Python_MatchesTB WHERE IsActive = 1")
        data = cursor.fetchall()
        return data
    except pyodbc.Error as error:
        err_log = open('d:\\err_log.txt', 'a')
        err_log.write(str(error))
        err_log.write('\n----------------------------------\n')
        err_log.close()
        return str(error)
    finally:
        con.close()



def joinMatch(userid, matchid):
    try:
        con = pyodbc.connect(constr)
        cursor = con.cursor()
        cursor.execute("SELECT inMatch FROM Python_UsersTB WHERE User_ID = "
                       + str(userid))
        data = cursor.fetchone()
        if data != None and data[0] == True:
            cursor.close()
            return 0, "You are already in match!"
        cursor.close()
        cursor = con.cursor()
        result = cursor.execute("UPDATE Python_UsersTB SET inMatch = '1', Match_ID = " + str(matchid) + "WHERE User_ID = " + str(userid))
        if result < 1:
            cursor.close()
            return 0, "Something went wrong!"
        con.commit()
        cursor.close()
        cursor = con.cursor()
        result = cursor.execute("UPDATE Python_MatchesTB SET players = (players + 1) WHERE Match_ID = " + str(matchid))
        if result < 1:
            cursor.close()
            return 0, "Something went wrong!"
        con.commit()
        cursor.close()
        return 1,"You have joined Match number " + str(matchid)

    except pyodbc.Error as error:
        err_log = open('d:\\err_log.txt', 'a')
        err_log.write(str(error))
        err_log.write('\n----------------------------------\n')
        err_log.close()
        return 0,str(error)
    finally:
        con.close()


def checkMatchesTimes():
    try:
        con = pyodbc.connect(constr)
        cursor = con.cursor()
        cursor.execute("SELECT * From Python_MatchesTB WHERE IsActive = 1")
        data = cursor.fetchall()
        cursor.close()
        if data != None:
            for match in data:
                if datetime.datetime.today().date() == match.Match_Date and datetime.datetime.now().strftime(
                        "%H:%M") >= match.Match_Time:
                    cursor = con.cursor()
                    result = cursor.execute(
                        "UPDATE Python_MatchesTB SET IsActive = 0 WHERE Match_ID = " + str(match.Match_ID))
                    if result < 1:
                        cursor.close()
                        return 0, "Something went wrong!"
                    con.commit()
                    cursor.close()
                    cursor = con.cursor()
                    result = cursor.execute(
                        "UPDATE Python_UsersTB SET inMatch = 0, Match_ID = -1 WHERE Match_ID = " + str(match.Match_ID))
                    if result < 1:
                        cursor.close()
                        return 0, "Something went wrong!"
                    con.commit()
                    cursor.close()
                elif datetime.datetime.today().date() > match.Match_Date:
                    cursor = con.cursor()
                    result = cursor.execute(
                        "UPDATE Python_MatchesTB SET IsActive = 0 WHERE Match_ID = " + str(match.Match_ID))
                    if result < 1:
                        cursor.close()
                        return 0, "Something went wrong!"
                    con.commit()
                    cursor.close()
                    cursor = con.cursor()
                    result = cursor.execute(
                        "UPDATE Python_UsersTB SET inMatch = 0, Match_ID = -1 WHERE Match_ID = " + match.Match_ID)
                    if result < 1:
                        cursor.close()
                        return 0, "Something went wrong!"
                    con.commit()
                    cursor.close()

    except pyodbc.Error as error:
        err_log = open('d:\\err_log.txt', 'a')
        err_log.write(str(error))
        err_log.write('\n----------------------------------\n')
        err_log.close()
        return str(error)
    finally:
        con.close()




flag = 1
username = ""
userid = -1


while flag == 1:
    while flag == 1:
        os.system("cls")
        checkMatchesTimes()
        print ("----  SoccerVision ----\n"
               + "1.  Login to app.\n"
               + "2.  Register.\n"
               + "3.  Exit.\n\n")
        choice = raw_input()
        if choice == '1':
            checkMatchesTimes()
            email = raw_input("Email:        ")
            password = raw_input("Password:     ")
            result = Login(email, password)
            if result[0] == 0:
                print result[1]
                flag = 1
            else:
                print "Welcome  -  " + result[1]
                username = result[1]
                userid = result[2]
                flag = 0
        elif choice == '2':
            checkMatchesTimes()
            usernameForRegister = raw_input("Username:      ")
            emailForRegister = raw_input("Email:         ")
            passwordForRegister = raw_input("Password:      ")
            result = Register(emailForRegister, usernameForRegister, passwordForRegister)
            print result
        elif choice == '3':
            checkMatchesTimes()
            print "Bye!!!"
            sys.exit()
        else:
            print "Wrong input... enter 1(Login), 2(Register) or 3{Exit)!"

    while flag == 0:
        os.system("cls")
        checkMatchesTimes()
        print ("----- WELCOME " + username + " -----\n"
               + "1.  Make a match.\n"
               + "2.  Join a match.\n"
               + "3.  Log out.\n")
        choice = raw_input()
        if choice == '1':
            checkMatchesTimes()
            key = ""
            matchName = raw_input("Match name:    ")
            matchDate = datetime.datetime.strptime(raw_input("Match date (dd-mm-yy):    "),'%d-%m-%y')
            matchDate = matchDate.strftime("%Y-%m-%d %H:%M:%S")
            matchTime = time.strptime(raw_input("Match time (hour:minute):    "),'%H:%M')
            matchTime = time.strftime('%H:%M',matchTime)
            city = raw_input("City:    ")
            field = raw_input("field:    ")
            isPrivate = raw_input("Private?(if yes type 'true')   ") == "true"
            if isPrivate == True:
                isPrivate = 1
                key = raw_input("Enter key for match:    ")
            else:
                isPrivate = 0

            result = MakeAMatch(matchName,userid,matchDate,matchTime,city,field,isPrivate,key)
            print result[1]
        elif choice =='2':
            checkMatchesTimes()
            matches = getMatches()
            if matches != None:
                for match in matches:
                    print (str(match.Match_ID) + ". match name: " + str(match.Match_Name) + " ,match date: "+ str(match.Match_Date) + " ,match time: " + str(match.Match_Time)
                           + " ,city: "+ str(match.City)+ " ,field: "+ str(match.Field)+ " ,players: "+ str(match.Players))
                f = 1
                flagForChoose = 0
                while flagForChoose == 0:
                    while f == 1:
                        try:
                            matchNum = int(raw_input("Choose a match to join.(type match number)  "))
                            f = 0
                        except ValueError as error:
                            print str(error)
                            print "try again"

                    checkingFlag = 0
                    for match in matches:
                        if int(match.Match_ID) == matchNum:
                            if match.IsPrivate == False:
                                result = joinMatch(userid, match.Match_ID)
                                print result[1]
                                checkingFlag = 1
                                flagForChoose = 1
                            else:
                                fl = 1
                                while fl == 1:
                                    k = raw_input("this match is private, enter the key:   ")
                                    if k == match.Match_Key:
                                        result = joinMatch(userid, match.Match_ID)
                                        print result[1]
                                        checkingFlag = 1
                                        fl = 0
                                        flagForChoose = 1
                                    else:
                                        print "Wrong!"
                                        ans = raw_input("Try again ? (y/n)   ")
                                        if ans != "y":
                                            fl = 0
                        else:
                            flagForChoose = 1



                if checkingFlag == 0:
                    print "no match have that number"
            else:
                print "No matches avaliable!"

        elif choice == '3':
            checkMatchesTimes()
            userid = -1
            flag = 1
        else:
            print "Wrong input... enter 1(Make a match), 2(Join a match) or 3{Log out)!"



