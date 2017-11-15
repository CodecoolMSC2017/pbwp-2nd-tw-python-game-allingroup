import random
from time import sleep
import os
import datetime

#header
poker = '---------------------------------------\n|    -----------------------------    |\n|    | HHH    H   H  H HHHH HHH  |    |\n|    | H  H  HHH  H  H H    H  H |    |\n|    | HHHH H   H HHH  HHHH HHH  |    |\n|    | H     HHH  H H  H    H H  |    |\n|    | H      H   H  H HHHH H  H |    |\n|    -----------------------------    |\n|                                     |'
left_side = "|               START                 |\n|               RESULT                |\n|               QUIT                  |\n|                                     |\n|                                     |"

#value of combos
combos = {
	'high': '1',
    'pair': '2',
    'drill': '3',
    'straight': '4',
    'nocombo': '0'
}

#value of the cards
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

#choose x random card from the pack
#append cards to hand
#remove choosen card from pack
def newhand(x):
    hand = []
    while len(hand) < x:
        val = len(pack) - 1
        card = random.randint(0,val)
        hand.append(pack[card][0])
        pack.remove(pack[card])
    return hand

#make terminal clear
def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')

#change cards if user wants
def changecards(change):
    if change >= '1':
        change = len(change)
    else:
        pass
    newcards = newhand(change)
    return newcards
    
#get card from list by its num
def getcardval(hand):
    c = 0
    cards = []
    while c < len(hand):
        card = hand[c]
        nextcard = cardvals[card]
        cards.append(nextcard)
        c += 1
    return cards

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

#check if high card
def high(hand):
    
    if int(hand[4]) > 10:

        return [True, hand[4]]
    else:
        return [False, 0]

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
        else:
            drill_is = [False, 0]
        j = j + 1
    return drill_is






def analyze(hand):
    hand.sort()
    res = 0
    
    straight_true = straight(hand)
    pair_true = pair(hand)
    drill_true = drill(hand)
    high_true = high(hand)
    if straight_true[0]:
        res = [ "straight", straight_true[1]] 
    elif drill_true[0]:
        res = ["drill", drill_true[1]]
    elif pair_true[0]:
        res = ["pair", pair_true[1]]
    elif high_true[0]:
        res = ["high", high_true[1]]
    else:
        res = ["nocombo", 0]

    return res



# check the results
def rating(g,p,gcn,pcn):
    g = int(g)
    p = int(p)

    if g > p:
        winner = "You Win with: " + gcn + "!"
    elif g == p:
        winner = "ITS DRAW"
    else:
        winner = "The computer win with: " + pcn + "!"
    return winner

def result():
    clrscr()
    print(poker)
    with open("result.txt") as results:
        content = results.readlines()
        if len(content) > 0:
            content.reverse()
            for i in range(5):
                print(content[i])
        else:
            print("No results")
        back = input("Press b to go back:\n")
        if back == "b":
            main()

def makesimple(cl):
    s = ""
    for c in cl:
        s += " " + str(c)
    return s

def change(guesthand):
    msg = "type here the number(s) of the card(s) you want to change: (max 3 cards)\n"
    change = input(msg)
    if len(change) > 3 and len(change) < 5:
        print("try again with a number between 1 and 3")
        change = input(msg)
    else:
        newcards = changecards(change)
        current = 1
        for g in guesthand:
            for c in change:
                if current == c:
                    guesthand[current - 1] = c
            current += 1
    return guesthand

def writeresults(guestval,winner):
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    with open("result.txt","a+") as f:
        f.write(str(guestval) +"|" + str(now) +"|" + str(winner)+"\n")


# get the hands, analyze and says who the winner
def game():
    clrscr()
    print(poker)
    guesthand = newhand(5)
    pchand = newhand(5)
    
    #make string from cards list
    gh = makesimple(guesthand)
    ph = makesimple(pchand)

    print("your cards are:\n")
    print(gh)
    option = input("do you wanna change cards? (y/n)\n")

    #if user wanna change cards, ask for nums of the cards, and change it 
    if option == "y":
        clrscr()
        guesthand = change(guesthand)

    #make string from cards list
    gh = makesimple(guesthand)
    ph = makesimple(pchand)

    clrscr()
    print(poker)
    print("now, your cards are:\n")
    print(gh + "\n")
    
    print("and the computers cards are:\n")
    print(ph)

    guestcardval = getcardval(guesthand)
    pccardval = getcardval(pchand)

    #get the highest combo name
    #analyze return list what contains the comboname
    #and the highest card value from the combo
    guestcomboresult = analyze(guestcardval)
    pccomboresult = analyze(pccardval)
    
    #get the highest combo value
    guestcombores = combos[guestcomboresult[0]]
    pccombores = combos[pccomboresult[0]]

    guestval = str(guestcombores) + guestcomboresult[1]
    pcval = str(pccombores) + guestcomboresult[1]

    """for i in range(len(guesthand)):
        guestval += int(guestcardval[i])

    
    for i in range(len(pchand)):
        pcval += int(pccardval[i])"""

    #print("guestval: " + str(guestval) + "\npcval: " + str(pcval))
    #print("guestcomboname: " + guestcomboname + "\npccomboname: " + pccomboname)
    winner = rating(guestval,pcval,guestcomboresult[0],pccomboresult[0])
    writeresults(guestval,winner)

    print(winner)

#the program
def main():
    clrscr()
    print(poker)
    print(left_side)
    keys = input("|Press s to start,                    |\n|r for result,                        |\n|q to quit                            |\n---------------------------------------\n")
    if keys == "s":
        game()
    elif keys == "r":
        result()
    elif keys == "q":
        exit()
    else:
        print("Please enter s, r or q")

main()
