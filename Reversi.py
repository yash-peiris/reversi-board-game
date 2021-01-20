#Name:Yasheen Mateesha Peiris
#Player 1 is Black
#Player 2 is White

from copy import *

def new_board() : #this function is used to initialise a new board
    defaultBoard = [[0] * 8 , 
                    [0] * 8,
                    [0] * 8,
                    [0,0,0,2,1,0,0,0,],     
                    [0,0,0,1,2,0,0,0],
                    [0] * 8,
                    [0] * 8,
                    [0] * 8]
    return defaultBoard


def print_board(board): #this function is used to bring the state of the current board
    a=1
    for outerList in board :
        print("")
        print(a,"|", end ="")
        for innerList in outerList :
            if (innerList==0):
                print("__|", end = "")
                
            elif (innerList==1):
                print("B_|", end ="")

            elif (innerList==2):
                print ("W_|", end = "")
        a+=1
    print("")
    print("  |a |b |c |d |e |f |g |h ")

            
def score(board):  #this function is used to print the score of the current board
    whiteCounter = 0
    blackCounter = 0
    for outerList in board :
        for innerList in outerList :
            if (innerList==1):
                blackCounter = blackCounter + 1    
            elif (innerList==2):
                whiteCounter= whiteCounter + 1
    return blackCounter,whiteCounter


def enclosing(board,player,pos,direc): #this function is used to check if the players stone encloses the opponents stone in all directions
    row,column=pos
    if(player == 1):
        opponent=2
    elif (player == 2):
        opponent =1
    else:
        return False
    vertical,horizontal = direc
    newVertical = row+vertical    #this is used to the check the adjascent stone in a given direction 
    newHorizontal = column+horizontal
    found = False
    while found==False: #keep checking the stones in the given direction repeatedly to see if it encloses 
        if(newVertical>=0 and newVertical<=7 and newHorizontal>=0 and newHorizontal<=7):  #to prevent out of index erros
            if(board[newVertical][newHorizontal]==opponent):
                newVertical = newVertical+vertical
                newHorizontal = newHorizontal+horizontal
                if (newVertical>=0 and newVertical<=7 and newHorizontal>=0 and newHorizontal<=7 and board[newVertical][newHorizontal]==player):
                    return True
            else:
                return False
        else:
            return False
        

def position(string):  #converts the given board position to row and column indexes
    string = string.upper()  #converts the paramter in board position to upper case
    positionlength = len(string)
    if (positionlength==2):
        if (string[0] == "A"):
            column = 0
        elif (string[0] == "B"):
            column = 1
        elif (string[0] == "C"):
            column = 2
        elif (string[0] == "D"):
            column = 3
        elif(string[0] == "E"):
            column = 4
        elif (string[0] == "F"):
            column = 5
        elif (string[0] == "G"):
            column = 6
        elif(string[0] == "H"):
            column = 7
        else :
            return None
        if(string[1].upper()>="A" and string[1].upper()<="Z" ):
            return None
        
        row = int(string[1])
        if (row>0 and row <= 8 ):
            row = row -1
        else:
            return None
        return row,column
    else :
        return None

        
def directionToIndex(direction):
    direction = direction.upper()
    if (direction== "U"):
        dr  =  -1
        dc = 0
        return dr,dc
    elif(direction == "D"):
        dr = 1
        dc = 0
        return dr,dc
    elif(direction == "R"):
        dr = 0
        dc = 1
        return dr,dc
    elif(direction == "L"):
        dr = 0
        dc = -1
        return dr,dc
    elif(direction == "DUR"):
        dr = -1
        dc = 1
        return dr,dc
    elif(direction == "DUL"):
        dr = -1
        dc = -1
        return dr,dc
    elif(direction == "DDR"):
        dr = 1
        dc = 1
        return dr,dc
    elif(direction == "DDL"):
        dr = 1
        dc = -1
        return dr,dc
    else:
        print("Please enter a valid direction")

def valid_moves(board,player): #gives out a list of all valid moves
    count=0
    validDirections=["U","D","R","L","DUR","DUL","DDR","DDL"]
    validPositions =[]
    for i in range(8):
        for j in range (8):
            if (board[i][j]==0):
                for x in validDirections:  #checks for valid moves in all directions
                    possibleDirection=directionToIndex(x)
                    found = enclosing(board,player,(i,j),possibleDirection)                    
                    if found == True:                   
                        validPositions.append((i,j))
    return(validPositions)


def next_state(board,player,pos):    
    row,column=pos
    if (player==1):  #determines next player
        nextPlayer =2
    elif (player==2):
        nextPlayer = 1  
    possibleMoves = valid_moves(board,player)
    if ((row,column) in possibleMoves): #used to check if the move is valid
        board[row][column]=player
        validDirections=["U","D","R","L","DUR","DUL","DDR","DDL"]
        for x in validDirections: #changes opponents stones in all possible directions
            possibleDirection=directionToIndex(x)
            vertical,horizontal = possibleDirection
            if (enclosing(board,player,(row,column),possibleDirection)==True):   #checks if stone is enclosed in given direction
                newVertical = row+vertical
                newHorizontal = column+horizontal
                found=False
                while found==False: #repeatedly flips the opponents stones              
                    if(board[newVertical][newHorizontal]==nextPlayer):              
                        board[newVertical][newHorizontal]=player  
                        newVertical = newVertical+vertical
                        newHorizontal = newHorizontal+horizontal
                        if (board[newVertical][newHorizontal]==player):   
                            found=True
                    else:
                         found=True
        possibleMovesNextPlayer = valid_moves(board,nextPlayer) #checks if next player has any possible moves
        if(len(possibleMovesNextPlayer)==0):
            nextPlayer=0
        return board,nextPlayer
    else:
        return board,nextPlayer

def validate_player(pPlayer): #check if the player entered is valid
    pPlayer = pPlayer.upper()
    if (len(pPlayer)==1):
        if(pPlayer>="A" and pPlayer<="Z"):
            return False
        elif(int(pPlayer)!=1 and int(pPlayer)!=2):
            return False
        else:
            return True
    else:
        return False



def run_single_player():
    newBoard = new_board()
    userInput="play"
    player=1
    blackScore,whiteScore=score(newBoard)
    stonePosition=""
    while (userInput!="q"): #loop repeats until q is entered or until neither player has any moves left
        print_board(newBoard)
        if (player==1): #player 1 is the user
            found=False
            possibleMoves= valid_moves(newBoard,player)
            if(len(possibleMoves)>0): #checks if the user has any possible moves, if not his turn is skipped
                while (found==False): #loop repeats until a valid position is entered
                    stonePosition = input("Enter position to drop stone in the format columnrow (such as d4): ")
                    if (stonePosition=="q"):
                        break
                    while (position(stonePosition)==None):    
                        stonePosition = input("Invalid stone position entered please re enter a stone position: ")
                        if (stonePosition=="q"):
                            break
                    if(stonePosition=="q"):
                        break
                    stonePosition=position(stonePosition)
                    
                    
                    if ((len(possibleMoves)>0) and (stonePosition not in possibleMoves)): #repeats until a valid move is entered   
                            print("Invalid Move")
                    else:
                        found = True
                if(stonePosition=="q"):
                    break
                newBoard,player=next_state(newBoard,player,stonePosition) #changes the state of the current board
                blackScore,whiteScore=score(newBoard)
            else:
                player=2
                print("No valid moves, your turn is Skipped")
            
            
        elif(player==2):
            tempBoard=deepcopy(newBoard)
            tempPlayer=1
            maxScore=0
            possibleMoves = valid_moves(newBoard,player)
            if(len(possibleMoves)>0): #checks if player has any valid moves, else turn is skipped
                for i in range(len(possibleMoves)): #checks all possible moves, calculate the score, move with the highest score is implemented
                    tempBoard,tempPlayer=next_state(tempBoard,player,possibleMoves[i])
                    blackScore,whiteScore=score(tempBoard)
                    #print(whiteScore)
                    if (maxScore<whiteScore):
                        maxScore=whiteScore
                        maxIndex=i
                    tempBoard=deepcopy(newBoard)
                    #print("maximum is",possibleMoves[maxIndex])
                    
                newBoard,player=next_state(newBoard,player,possibleMoves[maxIndex])
                blackScore,whiteScore=score(newBoard)
            else:
                player=1
                print("No valid moves, your turn is skipped")
        elif (player == 0):
            userInput= "q"
        print("Player 1's score is ",blackScore)
        print("Player 2's score is ",whiteScore)
    print("Thank you for playing")
    
def run_two_players():
    newBoard = new_board()
    userInput="play"
    while (userInput!="q"):
        print_board(newBoard)
        player = input("Is it Player 1's or Player 2's turn? Enter 1 or 2: ")
        if (player=="q"):
            break
        while (validate_player(player)==False):    
            player = input("Invalid player entered. Please enter 1 or 2: ")
            if (player=="q"):
                break
        if (player=="q"):
            break
        player = int(player)
        found=False
        possibleMoves= valid_moves(newBoard,player)
        if(len(possibleMoves)>0): #checks if the user has possible moves else his turn is skipped
            while (found==False): #loop repeats until a valid position is entered
                stonePosition = input("Enter position to drop stone in the format columnrow (such as d4): ")
                if (stonePosition=="q"):
                    break
                while (position(stonePosition)==None):  #loops until valid stone position is entered  
                    stonePosition = input("Invalid stone position entered please re enter a stone position: ")
                    if (stonePosition=="q"):
                        found=True
                        break
                if (stonePosition=="q"):
                        break
                stonePosition=position(stonePosition)
                if ((len(possibleMoves)>0) and (stonePosition not in possibleMoves)):    
                        print("Invalid Move")
                else:
                    found = True
            if (stonePosition=="q"):
                break
            newBoard,player=next_state(newBoard,player,stonePosition)
            blackScore,whiteScore=score(newBoard)
            print("Player 1's score is ",blackScore)
            print("Player 2's score is ",whiteScore)
            if (player == 0):
                userInput= "q"  
        else:
            print("No valid moves your turn is skipped")
            
    print("Thank you for playing")
                                  
        
run_single_player()
    
                
                
    
                        
                






