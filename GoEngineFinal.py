# -*- coding: cp1252 -*-
# THIS FILE CONTAINS ALL THE BASIC FUNCITONS NEEDED TO SIMULATE A TWO PLAYER GAME OF GO INCLUDING BOARD DEFINITIONS, RULES AND SCORING DETAILS.
# AN ALGORITHM FOR INTELLIGENT MOVE SELECTION USING MONTE CARLO TREE SEARCH + UPPER CONFIDENCE BOUND APPLIED TO TREES HAS ALSO BEEN IMPLEMENTED.
# TWO PLAYER GAMES IN WHICH ONE OR BOTH PLAYERS MOVE INTELLIGENTLY OR RANDOMLY CAN BE SIMULATED, AND ZERO TO TWO HUMAN PLAYERS CAN PLAY AT A TIME.
# SIMULATIONS OF RANDOM V/S INTELLIGENT AND INTELLIGENT V/S INTELLIGENT WITH DIFFERENT VALUES OF PARAMETERS HELP RESEARCHING THE CONTRIBUTION OF
# INDIVIDUAL PARAMETERS TOWARDS THE PROBABILITY OF WINNING. 
#
# DEVELOPED BY DEEPIKA BABLANI IN DECEMBER, 2012 FOR AN UNDERGRADUATE COMPUTER PROJECT IN GAME AI FOR COURSE CREDIT AT BITS PILANI, INDIA.
#
# MAIN REFERENCE PAPER: S. Gelly, L. Kocsis, M. Schoenauer, M. Sebag, D. Silver, C. Szepesvari, and O. Teytaud. 'The grand challenge of computer Go: Monte Carlo tree search and extensions.'
# Communications of the ACM, 55(3):106–113, 2012.


import math	# for sqrt, log
import random	

SIZE = 9 #size of square board
MAXMOVES=100 #maximum number of moves by a player in a game
C=0.5 #UCT Constant

class Point: #tested
    
    def setXY(self, x, y):
        if (0<=x<SIZE) and (0<=y<SIZE): 
            self.x, self.y = x, y
        else: print 'x and y must be within the range'
    
    def setColor(self, color):
        a=['BLACK','WHITE','EMPTY']
        if color in a:
            self.color = color
        else: print color + ' is not a valid color. Choose from BLACK, WHITE and EMPTY only.'
 
    def getXY(self):
        return self.x, self.y
    
    def getColor(self):
        return self.color

class Board(Point):
    def __init__(self):
        self.size = SIZE
        self.nextPlayer = 'BLACK' 	
        self.point=[[Point() for i in range(SIZE)]for j in range(SIZE)]
        self.emptyPoints = []
        self.movesPlayed=[]
        self.blackDead = 0		
        self.whiteDead = 0              
        for i in range(SIZE):
            for j in range(SIZE):
                self.point[i][j].setXY(i,j)
                self.point[i][j].setColor('EMPTY')
                
                
    def getNeighbours(self,x,y): #tested
        neighbours=[]
        for i in (1,-1):
            x=x+i
           
            if (0<=x<SIZE):
                neighbours.append(self.point[x][y].getXY())
            else :
                pass
            x=x-i
        
        for j in (1,-1):
            y=y+j
            if (0<=y<SIZE):
                neighbours.append(self.point[x][y].getXY())
            else :
                pass
            y=y-j
                
        return neighbours
    
    def copyBoard(self):   #tested

        copy=Board()
        for i in range(SIZE):
            for j in range(SIZE):
                copy.point[i][j].x = self.point[i][j].x
                copy.point[i][j].y = self.point[i][j].y
                copy.point[i][j].color = self.point[i][j].color

        copy.movesPlayed=self.movesPlayed
        copy.blackDead=self.blackDead
        copy.whiteDead=self.whiteDead
        copy.emptyPoints=self.emptyPoints

        return copy
 
    def getLiberties(self,x,y):  #tested
        copy=self.copyBoard()
        neighbours=copy.getNeighbours(x,y)
        liberties=[]
        p=Point()
        Point.setXY(p,x,y)
        color=copy.point[x][y].getColor()
        if color=='BLACK':
            copy.point[x][y].setColor('WHITE')
        elif color=='WHITE':
            copy.point[x][y].setColor('BLACK')
        else:
            print 'Point is empty.'
            return None

        for pt in neighbours:
            p1=Point()
            Point.setXY(p1,pt[0],pt[1])
            (x1,y1)=Point.getXY(p1)
            color1=copy.point[x1][y1].getColor()
            color2=color
            
            if (color1=='EMPTY'and (x1,y1) not in liberties):
                liberties.append((x1,y1))
         
            if (color1==color2)and(color1!='EMPTY'):
                liberties1=copy.getLiberties(x1,y1)
                for (a,b) in liberties1:
                    liberties.append((a,b))

        return liberties
    
    def isSuicide(self,x,y): #tested

       
        if self.getLiberties(x,y)==[]:
            return True

        else: return False

    def connectedPoints(self,x,y,c=[]): #tested
        
        copy=self.copyBoard()
        neighbours=copy.getNeighbours(x,y)
        
        color=copy.point[x][y].getColor()
        if color=='BLACK':
            copy.point[x][y].setColor('WHITE')
        elif color=='WHITE':
            copy.point[x][y].setColor('BLACK')
       
        c1=self.getLiberties(x,y)
        if c1==[]:
            c.append((x,y))
            for (a,b) in neighbours:
                if self.point[a][b].color==self.point[x][y].color:
                    copy.connectedPoints(a,b,c)
        return c
        
    def move(self,x,y):      #tested
        c=self.point[x][y].getColor()
        if (c !='EMPTY'):
            print 'That point is not empty. You cannot move there. Move elsewhere or pass your turn.'
            return None

        if self.nextPlayer=='WHITE':
            self.point[x][y].setColor('WHITE')
            
        elif self.nextPlayer=='BLACK':
            self.point[x][y].setColor('BLACK')
            
        if self.isSuicide(x,y)==True:
            self.point[x][y].setColor('EMPTY')
            print 'That move is a suicide. You cannot move there. Move elsewhere or pass your turn.'
            return None
        
        if self.nextPlayer=='WHITE':
            color='BLACK'
        else: color='WHITE'
        
        for (a,b) in self.getNeighbours(x,y):
            if self.point[a][b].color==color and self.getLiberties(a,b)==[]:
                c1=self.connectedPoints(a,b)
                for (l,m) in c1:
                    self.point[l][m].setColor('EMPTY')
                    if self.nextPlayer=='WHITE':
                        self.blackDead +=1
                    else: self.whiteDead +=1        

        if self.nextPlayer=='WHITE':
            self.nextPlayer='BLACK'
        else:
            self.nextPlayer='WHITE'

        self.movesPlayed.append((x,y))
  
    def passTurn(self):  #tested
        if (self.nextPlayer=='WHITE'):
            self.nextPlayer='BLACK'
            currentplayer='WHITE'
        else:
            self.nextPlayer='WHITE'
            currentplayer='BLACK'

        return currentplayer + ' passed. ' + self.nextPlayer + '\'s turn.'

    def blackScore(self):   #tested
        blackScore=0

        for i in range(SIZE):
            for j in range(SIZE):
                b1=[]
                if self.point[i][j].color=='BLACK':
                    blackScore +=1

                elif self.point[i][j].color=='EMPTY':
                    for (a,b) in self.getNeighbours(i,j):
                        if self.point[a][b].color=='BLACK':
                            b1.append((a,b))

                    if len(b1)==len(self.getNeighbours(i,j)):
                        blackScore +=1

        blackScore= blackScore + self.whiteDead

        return blackScore

    def whiteScore(self):   #tested
        whiteScore=0

        for i in range(SIZE):
            for j in range(SIZE):
                w1=[]
                if self.point[i][j].color=='WHITE':
                    whiteScore +=1

                elif self.point[i][j].color=='EMPTY':
                    for (a,b) in self.getNeighbours(i,j):
                        if self.point[a][b].color=='WHITE':
                            w1.append((a,b))

                    if len(w1)==len(self.getNeighbours(i,j)):
                        whiteScore +=1

        whiteScore= whiteScore + self.blackDead

        return whiteScore
                    
        
    def score(self): #tested
        
        b1=self.blackScore()
        w1=self.whiteScore()

        return 'BLACK\'s score is ' + str(b1) + ' and WHITE\'s score is ' +  str(w1) + '.'

    def winner(self):  #tested
       
        b1=self.blackScore()
        w1=self.whiteScore()

        if b1>w1:
            return 'BLACK'
        elif w1>b1:
            return 'WHITE'
        else:
            return 'DRAW'

    def valueOfGameBlack(self): #tested
        w=self.winner()
        if w=='BLACK':
            return 1
        elif w=='WHITE':
            return -1
        elif w=='DRAW':
            return 0

    def valueOfGameWhite(self): #tested
        w=self.winner()
        if w=='BLACK':
            return -1
        elif w=='WHITE':
            return 1
        elif w=='DRAW':
            return 0

    def listEmptyPoints(self):   #tested
        self.emptyPoints=[]
        for i in range(SIZE):
            for j in range(SIZE):
                if self.point[i][j].color=='EMPTY':
                    self.emptyPoints.append((i,j))

        return self.emptyPoints

    def listRandomEmptyPoint(self):  #tested
        list=self.listEmptyPoints()
        a=len(list)
        i=random.randint(0, a - 1)
        return (self.emptyPoints[i][0], self.emptyPoints[i][1])

    def playRandomMove(self):    #tested
        (a,b)=self.listRandomEmptyPoint()
        self.move(a,b)

    def identicalBoard(self,Board):  #tested
        value=0
        for i in range(SIZE):
            for j in range(SIZE):
                if self.point[i][j].color==Board.point[i][j].color:
                    value +=1
        if value==SIZE*SIZE:
            return True
        else:
            return False
                    
        
def playRandomGameBlack(Board): #tested
    move=0
    listOfMoves=[]
    while move<MAXMOVES:
        listOfMoves.append(Board.playRandomMove())
        move += 1
    return Board.valueOfGameBlack()

def playRandomGameWhite(Board): #tested
    move=0
    listOfMoves=[]
    while move<MAXMOVES:
        listOfMoves.append(Board.playRandomMove())
        move += 1
    return Board.valueOfGameWhite()
         
def clear(Board): #tested
    Board.__init__()


def printBoard(Board):  #tested
    for i in range(SIZE):
       for j in range(SIZE):
           if Board.point[i][j].color=='WHITE':
               c='W'
           elif Board.point[i][j].color=='BLACK':
               c='B'
           else: c='.'
           print c,
           if j==(SIZE-1):
               print ' '


class Node(Board):
    def __init__(self,board):
        self.board = board.copyBoard()
        self.wins = 0
        self.visits = 0
        self.childrenNodes=[]
        self.untriedMoves=board.listEmptyPoints()
        self.parentNode=None
        self.x=-1
        self.y=-1
        
    def update(self, value):  #tested
        self.visits += 1
        self.wins += value

    def calcWinRate(self):   #tested
        if self.visits>0:
            winRate=self.wins/self.visits
            return winRate
        else:
            return 0
        
    def addChild(self,x,y):   #tested
        copy=self.board.copyBoard()
        copy.move(x,y)
        child=Node(copy)
        child.x=x
        child.y=y
        child.parent=self
        self.untriedMoves.remove((x,y))
        self.childrenNodes.append(child)
        return child
        
   
    def UCTSelectChild(self):    #tested
        list1=self.childrenNodes
        maxvalue=0
        for c in list1:
            
            winrate=c.calcWinRate()
            uctvalue=C*math.sqrt(math.log(self.visits+1)/ (c.visits+1))
            value=winrate + uctvalue

            if value>maxvalue:
                (child,maxvalue)=(c,value)

        return child

def UCTBlack(Board,iterations):  #tested
    
    rootNode=Node(Board)

    for i in range(iterations):
        print i
        node = rootNode
        state = Board.copyBoard()
        
        # Selection
        while node.untriedMoves == [] and node.childrenNodes != []: 
            node = node.UCTSelectChild()
            state.move(node.x, node.y)
               
        # Expansion
        if node.untriedMoves != []: 
            m = random.choice(node.untriedMoves)
            x=m[0]
            y=m[1]
            state.move(x,y)
            node = node.addChild(x,y)

        # Simulation
        for i in range(MAXMOVES):
            state.playRandomMove()
 
        # Backpropagation
        while node != None:
            node.update(state.valueOfGameBlack())
            node = node.parentNode
 
    x=sorted(rootNode.childrenNodes, key = lambda c: c.visits, reverse=True)[-1].x
    y=sorted(rootNode.childrenNodes, key = lambda c: c.visits, reverse=True)[-1].y

    return (x,y)

def UCTWhite(Board,iterations):  #tested
    
    rootNode=Node(Board)

    for i in range(iterations):
        print i
        node = rootNode
        state = Board.copyBoard()

        #Selection
        while node.untriedMoves == [] and node.childrenNodes != []: 
            node = node.UCTSelectChild()
            print (node.x, node.y)
            state.move(node.x, node.y)

       #Expansion
        if node.untriedMoves != []: 
            m = random.choice(node.untriedMoves)
            x=m[0]
            y=m[1]
            state.move(x,y)
            node = node.addChild(x,y)
            
        # Simulation
        for i in range(MAXMOVES):
            state.playRandomMove()

        # Backpropagation
        while node != None:
            node.update(state.valueOfGameWhite())
            node = node.parentNode
                    
    x=sorted(rootNode.childrenNodes, key = lambda c: c.visits, reverse=True)[-1].x
    y=sorted(rootNode.childrenNodes, key = lambda c: c.visits, reverse=True)[-1].y
   
    return (x,y)

    
def fullGame1(Board): #black-mcts+uct white-random moves
    
    i=0
    while i<100:
        if Board.nextPlayer=='BLACK':
            (a,b)=UCTBlack(Board,100)
            print (a,b)
            Board.move(a,b)
            printBoard(Board)
            i=(i+1)
        elif Board.nextPlayer=='WHITE':
            Board.playRandomMove()
            print Board.movesPlayed[-1]

        print 'round ' +str(i)+ ' over'
 
    return Board.winner()

def tenFullGames(Board): #black-MCTS+UCT, white-random moves
    i=0
    result=[]
    while i<10:
        result.append(fullGame1(b1))
        print 'game ' +str(i) + ' over'
        i=(i+1)

    print result

def bothPlayersUCT(Board):   #Both players MCTS+UCT, but with different parameters (number of iterations per turn, MAXMOVES-depth of simulation)
    i=0
    while i<100:
        if Board.nextPlayer=='BLACK':
            (a,b)=UCTBlack(Board,200)
            print (a,b)
            Board.move(a,b)
            printBoard(Board)
            i=(i+1)
        elif Board.nextPlayer=='WHITE':
            (a,b)=UCTWhite(Board,300)
            print (a,b)
            Board.move(a,b)
            printBoard(Board)

        print 'round ' +str(i)+ ' over'

    return Board.winner()

def fiveFullUCT(Board):   #Five games of both players UCT
    i=0
    result=[]
    while i<5:
        result.append(bothPlayersUCT(Board))
        print 'game ' +str(i) + ' over'
        i=(i+1)

    print result

    
        
    














                




    
    

    

    
        
        
        
        
        
               
                
        
        
    

    
        

    
    
        
        
