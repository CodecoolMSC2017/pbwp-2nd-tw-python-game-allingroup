import random
import os
import datetime
import itertools
import threading
import sys
import time


# here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    # sys.stdout.write('\rDone!     ')

done = False
t = threading.Thread(target=animate)
t.start()


# long process here
time.sleep(1)
done = True


# write userdata to user.txt
def writedata(user_data):
    with open("user.txt", "w") as data:
        data.write(user_data)


# ask for name give 1000 token to start and give data to write to text
def newuser(pot=30):
    username = input("Give me your name:\n(minimum 5 character)\n")
    if len(username) < 5:
        newuser()
    else:
        token = 1000
        list_user = username + " " + str(token) + " " + str(pot)
        writedata(list_user)
        return list_user


def gamemodes(modenum):
    with open("modes.txt", "r") as data:
        modes = data.readlines()
        mode = modes[0] if modenum == "b" else modes[1]
    return mode


# checking user.txt what contains the username and money of user
def userdata():
    try:
        with open("user.txt", "r") as data:
            list_user = data.read()
            if len(list_user) == 0:
                newuser()
    except:
        list_user = newuser()
    return list_user


# header
def poker():
    print("\033[0;30;47m\n")
    print("""
    _|_|_|              _|                            
    _|    _|    _|_|    _|  _|      _|_|    _|  _|_|  
    _|_|_|    _|    _|  _|_|      _|_|_|_|  _|_|      
    _|        _|    _|  _|  _|    _|        _|        
    _|          _|_|    _|    _|    _|_|_|  _|        """)

    print("\033[0;29;48m  \n")


# value of combos
combos = {
	'high': '1',
    'pair': '2',
    'drill': '3',
    'four of a kind': '4',
    'straight': '5',
    'nocombo': '0'
}


# value of the cards
cardvals = {
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    'J': '11',
    'Q': '12',
    'K': '13',
    'A': '14'
}


prizecard = """
             @@@
            @. .@
            @\=/@
            .- -.
           /(.|.)\ 
           \ ).( /
           '( v )`
             \|/
             (|)
             '-`"""


# check userinput is number
def checkinput(userinput):
    try:
        float(userinput)
        return True
    except:
        return False


def read_pack():
    with open("pack.txt", "r") as pack:
        packtxt = pack.readlines()
    thepack = []
    for i in range(len(packtxt)):
        thepack.append(packtxt[i].strip().split(","))

    return thepack

# choose x random card from the pack
# append cards to hand
# remove choosen card from pack
def newhand(x, package, hand=0):
    hand = []
    
    if len(package) - 1 <= x:
        package = read_pack()
    cardoptions = len(package) - 1
    while len(hand) < x:
        card = random.randint(1, cardoptions)
        hand.append(package[card][0])
        package.remove(package[card])
        cardoptions -= 1
    return [hand, package]


# make terminal clear
def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


# get card from list by its num
def getcardval(hand):
    c = 0
    cards = []
    while c < len(hand):
        card = hand[c]
        nextcard = cardvals[card]
        cards.append(nextcard)
        c += 1
    return cards


# check if high card
def straight(hand):
    maxcard = max(hand)
    mincard = min(hand)
    handlen = len(hand)
    
    if int(maxcard) - int(mincard) == 4 and handlen == 5:
        pair_check = pair(hand)
        drill_check = drill(hand)
        four_check = four_of_kind(hand)
        if pair_check[0] or drill_check[0] or four_check[0]:
            straight_is = [False, 0]
        else:
            straight_is = [True, maxcard]

    else:
        straight_is = [False, 0]
    return straight_is


# check if four of kind
def four_of_kind(hand):
    j = 0
    N = len(hand)
    four_is = []
    while j < N - 3:
        if hand[j] == hand[j+1] and hand[j+1] == hand[j+2] and hand[j+2] == hand[j+3]:
            four_is = [True, hand[j]]
            break
        else:
            four_is = [False, 0]
        j = j + 1
    return four_is


# check if high card
def high(hand):
    if int(hand[4]) > 10:
        high_is = True
    else:
        high_is = False
    return [high_is, hand[4]]


# check if there is a pair
def pair(hand):
    i = 0
    N = len(hand)
    mypairrev = hand[::-1]
    high_incombo = 0
    while i < N - 1:
        if mypairrev[i] == mypairrev[i+1]:
            high_incombo = mypairrev[i]
            pair_is = True
            break
        else:
            pair_is = False
        i = i + 1
    return [pair_is, high_incombo]


# check if there is a drill
def drill(hand):
    j = 0
    N = len(hand)
    drill_is = []
    while j < N - 2:
        if hand[j] == hand[j+1] and hand[j+1] == hand[j+2]:
            drill_is = [True, hand[j]]
            break
        else:
            drill_is = [False, 0]
        j = j + 1
    return drill_is


# check hand to get combo
def analyze(hand):
    for i in range(len(hand)):
        hand[i] = int(hand[i])
    hand = sorted(hand)
    res = 0
    straight_true = straight(hand)
    pair_true = pair(hand)
    drill_true = drill(hand)
    high_true = high(hand)
    four_true = four_of_kind(hand)

    if straight_true[0]:
        res = ["straight", straight_true[1]]
    elif four_true[0]:
        res = ["four of a kind", four_true[1]]
    elif drill_true[0]:
        res = ["drill", drill_true[1]]
    elif pair_true[0]:
        res = ["pair", pair_true[1]]
    elif high_true[0]:
        res = ["high", high_true[1]]
    else:
        res = ["nocombo", max(hand)]
    return res


# check the results
def rating(gcombo, pcombo, pcboost, token, pot=50):
    gcomboval = int(combos[gcombo[0]])
    pcomboval = int(combos[pcombo[0]])
    pcomboval += int(pcboost)
    gcname = gcombo[0]
    pcname = pcombo[0]
    gcardval = int(gcombo[1])
    pcardval = int(pcombo[1])
    token = int(token)

    if gcomboval > pcomboval:
        winner = "You Win with: " + gcname + "!"
        token += pot
        print(prizecard)
    elif gcomboval == pcomboval:
        if gcardval > pcardval:
            winner = "You Win with: " + gcname + "!"
            token += pot
        elif gcardval == pcardval:
            winner = "ITS DRAW WITH " + gcname + "!"
        else:
            winner = "The computer win with: " + pcname + "!"
            token -= pot
    else:
        winner = "The computer win with: " + pcname + "!"
        token -= pot
    return [winner, token, pot]


# open result and print last 5 result or all if less
def printresults(noresmsg):
    msg = "Press 'b' to go back to main menu!\n"
    with open("result.txt") as results:
        content = results.readlines()
        contentnum = len(content) if len(content) < 5 else 5
        if len(content) > 0:
            content.reverse()
            for i in range(contentnum):
                print(content[i])
        else:
            print(noresmsg)
        userinput = input(msg)
        if userinput == "b":
            main()
        else:
            print(msg)


# check result.txt
def result():
    clrscr()
    poker()
    noresmsg = "Play with our poker and you will see your results here"
    try:
        printresults(noresmsg)
    except:
        print(noresmsg)
    clrscr()
    poker()


def makesimple(cardlist):
    string = ""
    for card in cardlist:
        string += " " + str(card)
    return string


# ask how many cards user wanna change
# change hand with new cards
# return hand
def change(hand, package):
    msg = "How many cards you wanna change? (max 3)\n"
    notgoodnummsg = "Try again with a number between 1 and 3\n"
    askforcard = "Which number you wanna change?\n"
    notgoodmsg = "This is not a number or not between 1 and 5\n"

    changenum = input(msg)

    if checkinput(changenum):
        changenum = int(changenum)
        if changenum > 3:
            print(notgoodnummsg)
            change(hand)
        elif changenum < 1:
            print(notgoodnummsg)
            change(hand)
        else:
            numlist = []
            for c in range(changenum):
                cardnum = input(askforcard)
                numlist.append(cardnum)
            result = newhand(changenum, package)
            newcards = result[0]
            package = result[1]
            changelist = []
            current = 0
            for h in range(len(hand)):
                for n in numlist:
                    if int(h) + 1 == int(n):
                        hand[h] = newcards[current]

                        print(hand[h])
                        current += 1
            return [hand, package]
    else:
        print(notgoodmsg)
        change(hand, package)


# if user wanna change cards, ask for nums of the cards, and change it
def askforchange(hand, package):
    question = "\nWhat you wanna do?\n"
    options = "\n k - keep cards\n c - change cards\n n - newhand\n"
    option = input(question + options)
    if option == "c":
        result = change(hand, package)
        hand = result[0]
        package = result[1]
    elif option == "n":
        result = newhand(5, package)
        hand = result[0]
        package = result[1]
    elif option == "k":
        hand = hand
    else:
        askforchange(hand, package)
    return [hand, package]


# write result to txt
def writeresults(guestval, winner):
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    with open("result.txt", "a+") as f:
        f.write(str(guestval) + "|" + str(now) + "|" + str(winner) + "\n")


def checktokens(pot, token):
    if int(token) - (int(pot) + 50) > 0:
        return True
    else:
        return False


def table():
    tablewidth = 54
    tableheader = "_" * tablewidth


# get the hands, analyze and says who's the winner
def game(userdata):
    pack = read_pack()
    modemsg = "\nChoose how hardcore are you:"
    modeoptions = "\nb - beginner\np - pro\n"
    user = userdata.split(" ")
    username = user[0]

    if len(user) > 1:
        usertoken = user[1]
    else:
        userdata = newuser()
        game(userdata)

    mode = input(modemsg + modeoptions)

    if mode == "b" or mode == "p":
        playmode = gamemodes(mode)
    else:
        game(userdata)

    modedata = playmode.split(" ")
    potboost = modedata[1]
    pcboost = modedata[2]

    if len(user) > 2:
        pot = int(user[2]) + int(potboost)
    else:
        pot = 50 if mode == "p" else 30

    canplay = checktokens(pot, usertoken)

    if canplay:
        replaymsg = "Do you wanna play another game?\n"
        options = "n - new game\nf - finish game\n"
        clrscr()
        poker()
        result = newhand(5, pack)
        guesthand = result[0]
        pack = result[1]
        result = newhand(5, pack)
        pchand = result[0]
        pack = result[1]

        # make string from cards list
        gh = makesimple(guesthand)
        ph = makesimple(pchand)
        print("Welcome " + username + "!\n")
        print("You have " + str(usertoken) + " tokens.")

        print("The pot in this round is: " + str(pot) + "\n")
        print("Your cards are:\n")
        print(gh)

        result = askforchange(guesthand, pack)
        guesthand = result[0]
        pack = result[1]

        # make string from cards list
        gh = makesimple(guesthand)

        clrscr()
        poker()

        print("now, your cards are:\n")
        print(gh + "\n")

        print("and the computers cards are:\n")
        print(ph)

        guestcardval = getcardval(guesthand)
        pccardval = getcardval(pchand)

        # get the highest combo name
        # analyze return list what contains the comboname
        guestcombores = analyze(guestcardval)
        pccombores = analyze(pccardval)

        # get the highest combo value
        guestcombovalue = combos[guestcombores[0]]
        pccombovalue = combos[pccombores[0]]

        # sum of combovalue and highest card value from the combo
        guestval = sum([int(guestcombovalue), int(guestcombores[1])])

        # get and print the winner name and winner combo name
        roundres = rating(guestcombores, pccombores, pcboost, usertoken, pot)

        winner = roundres[0]
        usertoken = roundres[1]
        writeresults(guestval, winner)
        userdatas = username + " " + str(usertoken) + " " + str(pot)
        writedata(userdatas)
        time.sleep(1)
        print("\n" + winner)

        newgame = input("\n" + replaymsg + options)
        if newgame == "n":
            main(restart=1)
        elif newgame == "f":
            main()
        else:
            print("Wrong answer!")
            time.sleep(1)
            main()
    else:
        print("You don't have enough money to play!")
        print("But if you can't stop playing you can make a new user")
        time.sleep(5)
        main()


# the program
def main(restart=0):
    clrscr()
    poker()
    user = userdata()

    if restart == 0:
        print("MENU")
        print("Choose an option and press enter")
        inputmsg = "s - start\nr - result\nn - new user\nq - quit\n"
        keys = input(inputmsg)
        if keys == "s":
            game(user)
        elif keys == "r":
            result()
        elif keys == "n":
            user = newuser()
            game(user)
        elif keys == "q":
            exit()
        else:
            main()
    else:
        game(user)

if __name__ == "__main__":
    main()
