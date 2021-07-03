import json  # for parsing json objects
import requests  # to make requests to our server
import ast  # for parsing and serialising
import typer  # for cli inputs and handling
import stdiomask  # for taking passwords as asterisks
import os  # for files and directory handling
import re  # for checking the emailid is valid or not
import smtplib
import ssl  # for email verification
import random  # for otp randomization
import math
import sqlite3  # for local db creation
from email.message import EmailMessage  # for creating an email object
import sys
import time  # for handling cli
import urllib.request

app = typer.Typer()

URL = 'https://ec54a29efd94.ngrok.io/'


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


@app.command("run")
def run():
    # load_animation()
    # checks if the user is registered based on a file's existence that is created at the time of registration
    if os.path.isfile('codate.db'):
        login()
    else:
        print("Let's get started and create you a new account!")
        register()

# for facilitating the input


def prompt(str_out, type=str, passw=0):
    if passw == 1:
        inp = stdiomask.getpass(prompt=f'{str_out}: ')
        return inp
    print(f'{str_out}:', end=" ")
    inp = type(input())
    return inp

# for displaying a cool animation..


def load_animation():

    print("<<---- Welcome to CLI-Tinder ---->>")
    # String to be displayed when the application is loading
    load_str = "loading application..."
    ls_len = len(load_str)

    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0

    # used to keep the track of
    # the duration of animation
    counttime = 0

    # pointer for travelling the loading string
    i = 0

    while (counttime != 40):

        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.1)

        # converting the string to list
        # as string is immutable
        load_str_list = list(load_str)

        # x->obtaining the ASCII code
        x = ord(load_str_list[i])

        # y->for storing altered ASCII code
        y = 0

        # if the character is "." or " ", keep it unaltered
        # switch uppercase to lowercase and vice-versa
        if x != 32 and x != 46:
            if x > 90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i] = chr(y)

        # for storing the resultant string
        res = ''
        for j in range(ls_len):
            res = res + load_str_list[j]

        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()

        # Assigning loading string
        # to the resultant string
        load_str = res

        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1

    # for windows OS
    if os.name == "nt":
        os.system("cls")

    # for linux / Mac OS
    else:
        os.system("clear")

# for sending the otp to users email address


def otp_sent(emailid):
    digits = "0123456789"
    OTP = ""
    for _ in range(6):
        OTP += digits[math.floor(random.random()*10)]

    # msg conaints the otp and the information to be mailed
    msg = EmailMessage()
    msg.set_content(f"{OTP} is your OTP.\n\nThanks for registering!")
    msg["Subject"] = "OTP from Codate"
    msg["From"] = "sudoschizo@gmail.com"
    msg["To"] = f"{emailid}"

    context = ssl.create_default_context()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls(context=context)
    # server.starttls()
    server.login("sudoschizo@gmail.com",
                 "#erctw%@e@VS3!@@#$d@fereqwrd#$@#$^f#$&")
    server.send_message(msg)
    server.quit()

    return OTP


def verify(emailid, count):
    # OTP here is the OTP sent to the user
    OTP = otp_sent(emailid)
    # a contains the OTP entered by the user
    a = prompt("Enter Your OTP ")
    # count is to keep the check and give limited chance to renter OTP to the user
    while a != OTP and count <= 3:
        print("Please Check your OTP again")
        cho = prompt(
            "Do you want us to resend the OTP?\n1. Yes 2. No 3.Retype the OTP ", type=int)
        count += 1
        if cho == 1:
            print("OTP resent")
            OTP = otp_sent(emailid)
            a = prompt("Enter Your OTP ")
        elif cho == 3:
            a = prompt("Enter Your OTP")
        else:
            print("You are not verified .. Try registering again !")
            exit(0)

    if a == OTP:
        print("Verified")
    elif count > 3:
        print("Sorry !! we could not verify you .. Try registering again !")
        exit(0)

# for validating mails


def check(emailid):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.search(regex, emailid)):
        return True
    else:
        return False

# takes all the required info form the user at the time of registeration


def register():
    usernames = requests.get(URL+'paticularcolsdatac',
                             data={"col_name": "username"}).json()
    prevUsernames = []
    # check if ussername already exists in our database
    for i in usernames:
        prevUsernames.append(i['username'])

    username = prompt("Enter a username")
    while(username in usernames):
        print("Sorry this username has already been taken. Choose another!")
        username = prompt("Enter a username")

    password = prompt("Create a password", passw=1)
    confirmpassword = prompt("Confirm the password", passw=1)

    while not password == confirmpassword:
        print("We could not confirm the password.. Try again!")
        password = prompt("Create a password", passw=1)
        confirmpassword = prompt("Confirm the password", passw=1)

    name = prompt("Tell us your name!")

    genderChoices = prompt(
        "Choose your pronouns : 1. He/Him 2. She/Her 3. They/Them ", type=int)

    if genderChoices == 1:
        gender = 'Male'
    elif genderChoices == 2:
        gender = 'Female'
    else:
        gender = 'Others'

    print("Let's verify you ..")
    emailid = prompt("Please enter your email id ")
    chk = prompt(
        "Is your email correct? ?\n1. To continue further 2. Re-enter email id", type=int)
    if chk == 2:
        emailid = prompt("Please enter your email id again")
    while not check(emailid):
        emailid = prompt("Please enter a valid email id ")
    # choice  = prompt("Do you want to continue with this email id ? 1.Yes 2.No", int)

    verify(emailid, 0)

    print(f'Write your best code and amaze people with your brain..\nLeave a blank line to indicate the end of your code..\n')

    code = ''
    while(True):
        temp = input()
        if temp == '':
            break
        code += temp + '\n'

    dataObj = {
        "username": username,
        "password": password,
        "name": name,
        "gender": gender,
        "emailid": emailid,
        "code": code,
    }

    req = requests.post(URL + 'registerc', data=dataObj)

    if req.status_code != 200:
        print("We could not register you! Try again with unique details..")
        exit

    print(f'Hey {name}, Thanks for registering with us!')

    createdb()


@app.command('login')
# for taking inputd while logging a user in
def login():
    print("Log In : ")
    username = prompt("Enter your username")
    password = prompt("Enter your password", passw=1)
    dataObj = {
        "username": username,
        "password": password
    }

    req = requests.post(URL+'loginc', data=dataObj).json()
    # print(req)
    while not req:
        print("Invalid username or password. Try again!")
        login()

    print(f'Hey {req[0]["name"]}')

    afterlogin(req[0])

# creating a db that's used to determine if the user has also registerd or not.
# initially planned to log other users details who the user interacted with and use it to never show the same profile again..but dropped the plan


def createdb():
    conn = sqlite3.connect('codate.db')
    c = conn.cursor()
    # c.execute('CREATE TABLE user(likesyou text, matches text)')
    conn.commit()
    conn.close

# def getfromlocaldb():
#     conn = sqlite3.connect('codate.db')
#     c = conn.cursor()
#     c.execute('SELECT likesyou,matches FROM user')
#     data = c.fetchall()
#     conn.commit()
#     conn.close()
#     return data

# def insertintolocaldb(col, val):
#     conn = sqlite3.connect('codate.db')
#     c = conn.cursor()
#     if col == 'likesyou':
#         c.execute(f'INSERT INTO users (likesyou) VALUES ({val})')
#     else:
#         c.execute(f'INSERT INTO users (matches) VALUES ({val})')
#     conn.commit()
#     conn.close()

# after the user logs in or registers on our app.. this function is executed...


def afterlogin(mydata):
    likesyou = ast.literal_eval(mydata['likesyou'])
    matches = ast.literal_eval(mydata['matches'])
    print(
        f'You have {len(matches)} matches and {len(likesyou)} people have liked your profile.')

    # asking user which profiles he/she wants to browse through.
    choice = prompt(
        "1. See Feed and New People\n2. See the coders I matched With\nEnter your choice - ", type=int)
    if choice == 1:
        feed(mydata)
    elif choice == 2:
        matched(mydata)
    else:
        print("Umm.. Wrong Choice")

# shows users profiles of opposite sex..


def feed(data):
    if(data['gender'] == 'Male'):
        req = requests.get(
            URL+'datacol', data={"col_name": "gender", "condition": 'Female'}).json()
    else:
        req = requests.get(
            URL+'datacol', data={"col_name": "gender", "condition": 'Male'}).json()

    for user in req:
        listhere = ast.literal_eval(user['likesyou'])
        if data['username'] not in listhere:
            nextuser = show_user(data, user, listhere)
            if(nextuser == False):
                break

    if(nextuser == True):
        print("\nThat's all the people who have registered on our platform. Thanks for being a part of it!\nSee ya!")

# shows profiles of users that the user matched with..


def matched(data):
    matcheslist = ast.literal_eval(data['matches'])
    print("Here are the coders you connected with -\n")
    for match in matcheslist:
        req = requests.get(URL+'specialget', data={
                           "colname": "username", "condition": match, "colstoget": {"name", "emailid"}}).json()
        print(f"Name : {req[0]['name']}\nEmail : {req[0]['emailid']}\n")

# template for showing individual profiles of other users..


def show_user(data, user, listhere):
    print("\n")
    print("Username: ", user['username'], "\nName: ", user['name'], "\nCode :")
    codeTemplate(user['code'])
    print('\n', end='')
    a = prompt("1. LEFT SWIPE\n2. RIGHT SWIPE\n3. EXIT\nChoose wisely, It can be smartest brain you will come across - ", type=int)
    if a == 2:
        listhere.append(data['username'])
        query = f'UPDATE cliusers SET likesyou = "{listhere}" WHERE username="{user["username"]}"'
        requests.post(URL+'customquery', data={"query": query})
        if user['username'] in data['likesyou']:
            print("YAYY!!!  It's a MATCH !\nYou both are surely made for each other\n We hope you two code better together !!\n\nHappy coding with",
                  user['name'], "(", user['username'], ")", " with email ", user['emailid'])

            # adding the current user id to the likes profile's matches column
            list_match = ast.literal_eval(user['matches'])
            list_match.append(data['username'])
            query = f'UPDATE cliusers SET matches = "{list_match}" WHERE username="{user["username"]}"'
            requests.post(URL+'customquery', data={"query": query})

            # adding the liked profile's username to current user's matches column
            list_match = ast.literal_eval(data['matches'])
            list_match.append(user['username'])
            query = f'UPDATE cliusers SET matches = "{list_match}" WHERE username="{data["username"]}"'
            requests.post(URL+'customquery', data={"query": query})

            print("\n\nWant to continue?\n")
            choice = prompt(
                "Press 1 for YES and any other number for NO - ", type=int)
            if choice == 1:
                return True
            else:
                print(
                    "We know you feel complete with you matched coding buddies.\n Happy Coding :)")
                return False
    elif a == 3:
        return False
    elif a != 1:
        print("umm.. Wrong choice")
        nextuser = show_user(data, user, listhere)
        if(nextuser == True):
            return True
        else:
            return False
    print(" \nWant to continue?")
    choice = prompt("Press 1 for YES and any other number for NO - ", type=int)
    if choice == 1:
        return True
    else:
        return False

# template to print users' code inside a box


def codeTemplate(code):
    codeList = list(code.split('\n'))
    maxlen = 0
    for i in codeList:
        if len(i)-i.count('\n') > maxlen:
            maxlen = len(i)-i.count('\n')
    length = maxlen + 4
    print(" "+'_'*(length), end="\n")
    print('|' + " "*(length) + "|")
    for i in codeList:
        toPrint = '|'+" "*2 + i
        toPrint = toPrint + " "*(length-len(toPrint)+1) + '|'
        if i != '':
            print(toPrint)
    print('|' + "_"*(length) + "|")


# our cli is called here
if __name__ == '__main__':
    # checks if the user is connected to internet and shows a msg if he/she's not..
    if(connect()):
        app()
    else:
        print("<<--- PLEASE MAKE SURE YOU HAVE A INTERNET CONNECTION --->>\n")
