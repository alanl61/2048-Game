import random
import sys
import copy


### Updates the Board contating the data to be displayed with the actual board containing the current game data ###
def updateBoard(theBoard, displayBoard):
    for f, s in theBoard:
        
        # x gives the different spacing required for proper print format of the playing board
        x = len(str(theBoard[f,s]))
        if theBoard[f,s] == 0:
            plug = '    '
        elif x == 1:
            plug = '  ' + str(theBoard[f,s]) + ' '
        elif x == 2:
            plug = ' ' + str(theBoard[f,s]) + ' '
        elif x == 3:
            plug = ' ' + str(theBoard[f,s])
        else:
            plug = str(theBoard[f,s])
            
        # updates the display board with the correct string format
        displayBoard[f,s] = plug



### Prints out the playing board ###
def display(displayBoard, sumList):

    # update the playing board with the current board data
    updateBoard(theBoard, displayBoard)
    print(' ')
    print(str(displayBoard[1,4]) + ' | ' + str(displayBoard[2,4]) + ' | ' + str(displayBoard[3,4]) + ' | ' + str(displayBoard[4,4]) + '  Score: ' + str(sumList[0]))
    print('-----+------+------+-----')      
    print(str(displayBoard[1,3]) + ' | ' + str(displayBoard[2,3]) + ' | ' + str(displayBoard[3,3]) + ' | ' + str(displayBoard[4,3]))
    print('-----+------+------+-----')   
    print(str(displayBoard[1,2]) + ' | ' + str(displayBoard[2,2]) + ' | ' + str(displayBoard[3,2]) + ' | ' + str(displayBoard[4,2]))
    print('-----+------+------+-----')   
    print(str(displayBoard[1,1]) + ' | ' + str(displayBoard[2,1]) + ' | ' + str(displayBoard[3,1]) + ' | ' + str(displayBoard[4,1]))



### Handles user inputs ###
def userInput():
    while True:
        choice = input('Enter a direction: ')
        choice = choice.lower()
        if choice == 'w' or choice == 'a' or choice == 's' or choice == 'd':
            return choice
        else:
            print('Enter a valid direction')
            continue



### Generate a new tile onto the board, and determines if the game is over (Win/Loss) ###
def generate(theBoard):
    if 2048 in theBoard.values():
        return 1
    choiceNumber = random.randint(1,10)
    if choiceNumber == 10:
        number = 4
    else:
        number = 2

    # find all empty spaces in the data board and store its position in tempList
    tempList = []
    for y in range(1,5):
        for x in range(1,5):
            if theBoard[x,y] == 0:
                a = str(x) + ',' + str(y)
                tempList.append(a)

    # select a position from tempList randomly, spawn the new number there
    choice = random.choice(tempList)
    x = int(choice[0])
    y = int(choice[2])
    theBoard[x,y] = number

    # if the board is now full, check if any valid move exist
    if len(tempList) == 1:
        tempBoard = copy.deepcopy(theBoard)

        # no valid move exist, return 0 (loss signal), else return None
        if movement('w', tempBoard, 1) == 1 or movement('a', tempBoard, 1) == 1:
            return None
        else:
            return 0



### Determines the direction of the merge of the tiles (verticle and horizontal), returns a value if required ###
def movement(direction, theBoard, check):
    if direction == 'w' or direction == 's':
        # putting all column elements into vList
        for x in range(1,5):
            vList = []
            for y in range(1,5):
                if theBoard[x,y] != 0:  
                    vList.append(theBoard[x,y])
                    theBoard[x,y] = 0
            output = combine(direction, vList, theBoard, x, check)
            if check == 1 and output == 1:
                return 1
            
    if direction == 'a' or direction == 'd':
        # putting all row elements into hList
        for y in range(1,5):
            hList = []
            for x in range(1,5):
                if theBoard[x,y] != 0:
                    hList.append(theBoard[x,y])
                    theBoard[x,y] = 0
            output = combine(direction, hList, theBoard, y, check)
            if check == 1 and output == 1:
                return 1



### Merges consequtive numbers in the list if they are the same number, increment score if merge occured and update the data board (return a value if required) ###
def combine(direction, tempList, theBoard, z, check):
    # limit on the length of the list to merge
    limit = 2

    # for Up movement
    if direction == 'w':
        start = -1
        while len(tempList) >= limit:
            if tempList[start] == tempList[start - 1]:
                tempList[start] += tempList[start - 1]
                del tempList[start - 1]
                score(tempList[start])

            # change the position to merge to
            start -= 1

            # change the limit on the list to merge since position to merge to changed
            limit += 1

        # if a valid move is made, return 1
        if check == 1 and len(tempList) != 4:
            return 1

        # Update the data board
        start = -1
        for i in range(len(tempList)):
            y = 4 - i
            theBoard[z,y] = tempList[start]
            start -= 1

    # (rest are similar in structure)
    if direction == 's':
        start = 0
        while len(tempList) >= limit:
            if tempList[start] == tempList[start + 1]:
                tempList[start] += tempList[start + 1]
                del tempList[start + 1]
                score(tempList[start])
            start += 1
            limit += 1
        if check == 1 and len(tempList) != 4:
            return 1
        start = 0
        for i in range(len(tempList)):
            y = i + 1
            theBoard[z,y] = tempList[start]
            start += 1

    if direction == 'a':
        start = 0
        while len(tempList) >= limit:
            if tempList[start] == tempList[start + 1]:
                tempList[start] += tempList[start + 1]
                del tempList[start + 1]
                score(tempList[start])
            start += 1
            limit += 1
        if check == 1 and len(tempList) != 4:
            return 1
        start = 0
        for i in range(len(tempList)):
            x = i + 1
            theBoard[x,z] = tempList[start]
            start += 1

    if direction == 'd':
        start = -1
        while len(tempList) >= limit:
            if tempList[start] == tempList[start - 1]:
                tempList[start] += tempList[start - 1]
                del tempList[start - 1]
                score(tempList[start])
            start -= 1
            limit += 1
        if check == 1 and len(tempList) != 4:
            return 1
        start = -1
        for i in range(len(tempList)):
            x = 4 - i
            theBoard[x,z] = tempList[start]
            start -= 1



### Add to the total score count ###
def score(addValue):
    sumList[0] += addValue



### Takes input to determine whether to run the program again or not ###
def playAgain():
    while True:
        play = input('Do you want to play again? [y/n]')
        if play == 'y':
            return 1
        elif play == 'n':
            return 0
        else:
            continue


        
### main ###
while True:
    # print welcome messages, set up an empty board
    print('Welcome to 2048')
    print('Control is [w/a/s/d]')
    displayBoard = {(1,4): '    ', (2,4): '    ', (3,4): '    ', (4,4): '    ',
                    (1,3): '    ', (2,3): '    ', (3,3): '    ', (4,3): '    ',
                    (1,2): '    ', (2,2): '    ', (3,2): '    ', (4,2): '    ',
                    (1,1): '    ', (2,1): '    ', (3,1): '    ', (4,1): '    '}

    theBoard = {(1,4): 0, (2,4): 0, (3,4): 0, (4,4): 0,
                (1,3): 0, (2,3): 0, (3,3): 0, (4,3): 0,
                (1,2): 0, (2,2): 0, (3,2): 0, (4,2): 0,
                (1,1): 0, (2,1): 0, (3,1): 0, (4,1): 0}

    # list to store the total store
    sumList = [0]
    
    generate(theBoard)
    generate(theBoard)
    display(displayBoard, sumList)
    while True:
        # make a copy of the data board to test if next movement is valid
        tempBoard = copy.deepcopy(theBoard)
        while True:
            direction = userInput()
            movement(direction, theBoard, 0)
            if tempBoard == theBoard:
                print("Can't go that way")
                continue
            else:
                break
        final = generate(theBoard)
        display(displayBoard, sumList)
        if final == 1:
            print('Congratz you reached 2048!!')
            if playAgain() == 1:
                break
            else:
                print('Thanks for playing.')
                sys.exit()
        elif final == 0:
            print('You lost! Gameover.')
            if playAgain() == 1:
                break
            else:
                print('Thanks for playing.')
                sys.exit()
        else:
            continue

