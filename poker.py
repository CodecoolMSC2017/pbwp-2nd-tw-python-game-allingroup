import random
from time import sleep
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


def writedata(user_data,pot):
    with open("user.txt", 'a+') as data:
        data.write(user_data + " " + str(pot))

# checking user.txt what contains the username and money of user
def userdata(pot):
    try:
        with open("user.txt", "r") as data:
            list_user = data.read()
    except:
        username = input("Give me your name:\n")
        token = 1000
        list_user = username + " " + str(token + " " + str(pot))
        writedata(list_user)
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

# pack of cards
pack = [
    ['2', 'club'], ['2', 'diamond'], ['2', 'heart'], ['2', 'spade'],
    ['3', 'club'], ['3', 'diamond'], ['3', 'heart'], ['3', 'spade'],
    ['4', 'club'], ['4', 'diamond'], ['4', 'heart'], ['4', 'spade'],
    ['5', 'club'], ['5', 'diamond'], ['5', 'heart'], ['5', 'spade'],
    ['6', 'club'], ['6', 'diamond'], ['6', 'heart'], ['6', 'spade'],
    ['7', 'club'], ['7', 'diamond'], ['7', 'heart'], ['7', 'spade'],
    ['8', 'club'], ['8', 'diamond'], ['8', 'heart'], ['8', 'spade'],
    ['9', 'club'], ['9', 'diamond'], ['9', 'heart'], ['9', 'spade'],
    ['10', 'club'], ['10', 'diamond'], ['10', 'heart'], ['10', 'spade'],
    ['J', 'club'], ['J', 'diamond'], ['J', 'heart'], ['J', 'spade'],
    ['Q', 'club'], ['Q', 'diamond'], ['Q', 'heart'], ['Q', 'spade'],
    ['K', 'club'], ['K', 'diamond'], ['K', 'heart'], ['K', 'spade'],
    ['A', 'club'], ['A', 'diamond'], ['A', 'heart'], ['A', 'spade']
]

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

# choose x random card from the pack
# append cards to hand
# remove choosen card from pack
def newhand(x):
    hand = []
    while len(hand) < x:
        val = len(pack) - 1
        card = random.randint(0, val)
        hand.append(pack[card][0])
        pack.remove(pack[card])
    return hand


# make terminal clear
def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


# change cards if user wants
def changecards(change):
    if change >= '1':
        change = len(change)
    else:
        pass
    newcards = newhand(change)
    return newcards


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
    high_is = []
    if int(maxcard) - int(mincard) == 4 and handlen == 5:
        high_is = [True, maxcard]
    else:
        high_is = [False, 0]
    return high_is


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
    

#check if high card
def high(hand):
    if int(hand[4]) > 10:
        high_is = True
    else:
        high_is = False
    return [high_is, hand[4]]
    

#check if there is a pair
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

#check if there is a drill
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


def analyze(hand):
    for i in range(len(hand)):
        hand[i] = int(hand[i])
    hand = sorted(hand)
    for i in range(len(hand)):
        hand[i] = str(hand[i])
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
def rating(guesthandvalue,pchandvalue,gcombo,pcombo):
    ghv = int(guesthandvalue)
    phv = int(pchandvalue)
    gcname = gcombo[0]
    pcname = pcombo[0]
    gcval = int(gcombo[1])
    pcval = int(pcombo[1])
    
    if ghv > phv:
        winner = "You Win with: " + gcname + "!"
        print(prizecard)
    elif ghv == phv:
        if gcval > pcval:
            winner = "You Win with: " + gcname + "!"
        elif gcval == pcval:
            winner = "ITS DRAW WITH " + gcname + "!"
        else:
            "The computer win with: " + pcnanem + "!"
    else:
        winner = "The computer win with: " + pcname + "!"
        
    return winner


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
#return hand
def change(hand):
    msg = "How many cards you wanna change? (max 3)\n"
    notgoodnummsg = "Try again with a number between 1 and 3\n"
    askforcard = "Which number you wanna change?\n"
    notgoodmsg = "This is not a number or not between 1 and 5\n"
    
    changenum = input(msg)

    if checkinput(changenum):
        changenum = int(changenum)
        if changenum > 3 and changenum < 1:
            print(notgoodmsg)
            change(hand) 
        else:
            numlist = []
            for c in range(changenum):
                cardnum = input(askforcard)
                numlist.append(cardnum)

            current = 1
            for g in hand:
                for num in numlist:
                    if current == num:
                        hand[current - 1] = c
                current += 1

            return hand
    else:
        print(notgoodmsg)
        change(hand)
 
# if user wanna change cards, ask for nums of the cards, and change it 
def askforchange(hand):
    question = "\nWhat you wanna do?\n\n k - keep cards\n c - change cards\n n - newhand\n"
    option = input(question)
    if option == "c":
        hand = change(hand)
    elif option == "n":
        hand = newhand(5)
    elif option == "k":
        hand = hand
    else:
        askforchange(hand)
    return hand


# write result to txt
def writeresults(guestval,winner):
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    with open("result.txt","a+") as f:
        f.write(str(guestval) + "|" + str(now) + "|" + str(winner) + "|" + "\n")

def checktokens(pot,token):
    if int(token) - (int(pot) + 50) > 0:
        return True
    else:
        return False

# get the hands, analyze and says who's the winner
def game(userdata,pot):
    user = userdata.split(" ")
    username = user[0]
    usertoken = user[1]

    if len(user) > 2:
        pot = int(user[2]) + 50

    canplay = checktokens(pot,usertoken)

    if canplay:
        replaymsg = "Do you wanna play another game?\n n - new game\n f - finish game\n"
        clrscr()
        poker()
        guesthand = newhand(5)
        pchand = newhand(5)
        
        #make string from cards list
        gh = makesimple(guesthand)
        ph = makesimple(pchand)
        print("Welcome " + username + "!\nYou have " + str(usertoken) + " tokens.")
        print("The pot in this round is: " + str(pot) + "\n")
        print("Your cards are:\n")
        print(gh)

        guesthand = askforchange(guesthand)
        
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
        # and the highest card value from the combo
        guestcomboresult = analyze(guestcardval)
        pccomboresult = analyze(pccardval)
        

        # get the highest combo value
        guestcombovalue = combos[guestcomboresult[0]]
        pccombovalue = combos[pccomboresult[0]]

        # sum of combovalue and highest card value from the combo
        guestval = guestcombovalue + guestcomboresult[1]
        pcval = pccombovalue + guestcomboresult[1]


        # get and print the winner name and winner combo name
        winner = rating(guestcombovalue,pccombovalue,guestcomboresult,pccomboresult)
        writeresults(guestval,winner)
        userdata = username + " " + str(usertoken)
        writedata(userdata,pot)
        print(winner)

        newgame = input(replaymsg)
        if newgame == "n":
            game(userdata,pot)
        elif newgame == "f":
            main()
        
        return pot
    else:
        print("You don't have enough money to play!")

# the program
def main():
    pot = 50
    inputmsg = "Press s to start,\n r for result,\n q to quit\n"
    clrscr()
    poker()
    user = userdata(pot)

    keys = input(inputmsg)
    if keys == "s":
        game(user,pot)
    elif keys == "r":
        result()
    elif keys == "q":
        exit()
    else:
        main()

if __name__ == "__main__":
    main()
