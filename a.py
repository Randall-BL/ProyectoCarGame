'''
Created on Aug 9, 2014
Last worked on April 4, 2015

@author: Charles Engen

We are creating a basic battleship game, not only with full
sized ships but with it's full size board as well. You can have two computers duke it out
or you can play manually.

This little project was a means to an end. While building this program I learned a lot about Python and programming
    in general. That is why a lot of the code in not as neat as it could be but I do believe that I did the best
    could at the time.

'''

__author__ = 'Charles Engen'


# Imports
import collections
from random import randint


class GameWin():
    pass


class ShipError:
    pass


class LogWrappedFunction(object):
    def __init__(self, function):
        self.function = function

    def logAndCall(self, *arguments, **namedArgs):
        print "Calling %s with arguments %s and named arguments %s" % (self.function.func_name, arguments, namedArgs)
        self.function.__call__(*arguments, **namedArguments)


def logwrap(function):
    return LogWrappedFunction(function).logAndCall


############
#Creates a class object for future ships to inherit.
############
class shipBlueprint(object):
    #Creates variables so they can be passed to other functions later.
    def __init__(self, shipLength, shipName):
        self.shipLength = shipLength
        self.shipName = shipName

    #Returns the ship name when called
    def getName(self):
        return self.shipName

    #Returns the ship length when called
    def getLength(self):
        return self.shipLength

    #Returns the Ship's name and it's length when the object is called
    def __str__(self, *args, **kargs):
        return '%s is %s tiles long.' % (self.shipName, self.shipLength)

    def __call__(self):
        return self.shipName

    def __getitem__(self):
        return


###########
#The data structure that I am generating now is will look like
#    data = {
#    (1,1):'`Water',
#    (1,2):'ship',
#    (1,3):'shipDamaged'
#    ...
#    }
#
#    Uses the OrderedDict method from collections on the board to ordered the dict.
#   Creates a class Object for the board and assigns a method to print the board.
###########
class Board(object):
    def __init__(self, sides=11):
        self.sides = sides
        self.storedBoard = {(x, y): '~Water' for y in range(1, self.sides) for x in range(1, self.sides)}
        self.backedupBoard = self.storedBoard

    def print_board(self):
        printableBoard = collections.OrderedDict(sorted(self.storedBoard.items()))
        for y in range(1, self.sides):
            print ' '.join(str(printableBoard[x, y])[0] for x in range(1, self.sides))

    def getMap(self):
        return self.storedBoard

    def backupBoard(self):
        self.backupedBoard = dict(self.storedBoard)
        return self.backedupBoard

    def getBackUp(self):
        self.storedBoard = dict(self.backupedBoard)
        return self.storedBoard

    def realBackUp(self):
        self.getBackUp()
        self.getMap()


###########
#This function takes a variable and asks the user what number they would like to pick
###########
def askXY(var, count=0):
    while count < 100:
        while True:
            try:
                xy = int(raw_input('1-10 ' + str(var)))
                if xy > 10:
                    print 'Your response was out of range!'
                    break
                else:
                    if xy <= 0:
                        print 'Your response was out of range!'
                        break
                    else:
                        return xy
            except ValueError:
                print 'You failed to enter a number'
            except KeyError:
                print 'You failed to enter a number'
        count += 1


#############
#Create a class system to generate boards and apply ships to the board.
#############
class Player(Board):
    def __init__(self):
        Board.__init__(self)
        self.deBUG = False
        self.playerType = self.askPlayerType()
        self.shipAircraftCarrier = shipBlueprint(5, 'Aircraft Carrier')
        self.shipBattleship = shipBlueprint(4, 'Battleship')
        self.shipSubmarine = shipBlueprint(3, 'Submarine')
        self.shipDestroyer = shipBlueprint(3, 'Destroyer')
        self.shipPatrolBoat = shipBlueprint(2, 'Patrol Boat')
        self.hitEnemyShips = 0
        self.fleet = [self.shipAircraftCarrier,
                      self.shipBattleship,
                      self.shipDestroyer,
                      self.shipPatrolBoat,
                      self.shipSubmarine
        ]

    @staticmethod
    def horizontal_or_vertical(z=0):
        while z < 100:
            while True:
                try:
                    hV = str(raw_input('Horizontal or Vertical')).lower()
                    if hV[0] == 'h':
                        h_v = 'horizontal'
                        return h_v
                    elif hV[0] == 'v':
                        h_v = 'vertical'
                        return h_v
                    else:
                        print 'You picked %s' % (hV)
                        break

                except ValueError:
                    print 'You failed to enter Horizontal or Vertical'
                except KeyError:
                    print 'You failed to enter Horizontal or Vertical'
                except IndexError:
                    print 'You failed to enter Horizontal or Vertical'
            z += 1

    #Asks Player Type
    @staticmethod
    def askPlayerType():
        playerType = raw_input('Are you man or machine?').lower()
        if 'man' in str(playerType):
            return playerType
        elif 'cheat' in str(playerType):
            deBUG = True
            playerType = 'man'
            return playerType, deBUG
        else:
            playerType = str('Machine')
            return playerType

    def placeShip(self, ship, X, Y):
        self.storedBoard[X, Y] = self.fleet[ship].getName()
        return self.storedBoard

    def placeVerticalShip(self, ship, X, Y):
        for i in range(self.fleet[ship].getLength()):
            if 'Water' not in self.storedBoard[X, Y + i]:
                raise StopIteration()
            else:
                self.placeShip(ship, X, Y + i)

    def placeHorizontal(self, ship, X, Y):
        for i in range(self.fleet[ship].getLength()):
            if 'Water' not in self.storedBoard[X + i, Y]:
                raise StopIteration()
            else:
                self.placeShip(ship, X + i, Y)

    def shipGen(self, ship, X, Y, hV):
        try:
            self.backupBoard()
            if hV % 2 == 0:
                if self.fleet[ship].getLength() + X <= 10:
                    self.placeHorizontal(ship, X, Y)
                else:
                    raise ShipError()
            elif hV % 2 != 0:
                if self.fleet[ship].getLength() + Y <= 10:
                    self.placeVerticalShip(ship, X, Y)
                else:
                    raise ShipError()
        except StopIteration:
            raise ShipError()
        except KeyError:
            raise ShipError()
        except IndexError:
            raise ShipError()

    def fleetGen(self, x=0):
        while x < 1:
            try:
                self.backupBoard()
                if 'man' in self.playerType:
                    for ship in range(len(self.fleet)):
                        self.backupBoard()
                        while True:
                            try:
                                print 'You are placing the %s' % (self.fleet[ship].getName())
                                X = askXY('Horizontal')
                                Y = askXY('Vertical')
                                hV = self.horizontal_or_vertical()
                                print 'You are placing %s at (%s, %s) %s' % (self.fleet[ship].getName(), X, Y, hV)
                                if 'h' in hV[0]:
                                    hV = 2
                                elif 'v' in hV[0]:
                                    hV = 3
                                self.shipGen(ship, X, Y, hV)
                            except ShipError:
                                self.realBackUp()
                                print 'Failed to place %s at (%s, %s)' % (self.fleet[ship].getName(), X, Y)
                                continue
                            break
                    else:
                        x += 1
                        return
                elif 'Machine' in self.playerType:
                    for ship in range(len(self.fleet)):
                        self.backupBoard()
                        while True:
                            try:
                                X = randint(1, 10)
                                Y = randint(1, 10)
                                hV = randint(1, 10)
                                self.shipGen(ship, X, Y, hV)
                            except ShipError:
                                self.realBackUp()
                                continue
                            break
                    else:
                        x += 1
                        return

            finally:
                print ''
                if 'machine' in self.playerType:
                    if 'debug' in self.deBUG:
                        self.print_board()
                        print 'Cheat Board Enabled, here is your opponent\'s board.'
                    print '%s has finished placing their Ships' % self.playerType
                else:
                    self.print_board()
                pass

    def printBoardOpposition(self):
        self.getMap()
        maskedShips = dict(self.storedBoard)
        for y in range(1, self.sides):
            for x in range(1, self.sides):
                for xFleet in range(len(self.fleet)):
                    if self.fleet[xFleet].getName() in maskedShips[x, y]:
                        maskedShips[x, y] = '~' + str(maskedShips[x, y])
                        if 'damage' in str(maskedShips[x, y]).lower():
                            maskedShips[x, y] = 'X'
                        elif 'miss' in str(maskedShips[x, y]).lower():
                            maskedShips[x, y] = '^'
        for y in range(1, self.sides):
            print ' '.join(str(maskedShips[x, y])[0] for x in range(1, self.sides))

    def __type__(self):
        return self.playerType

    def __str__(self, *args, **kargs):
        return 'You are a %s!!!' % self.playerType


###########
#Damages the ship
###########
def fireShot(player1, player2, t=0):
    while True:
        try:
            if t == 0:
                x = 0
                y = 0
                if 'man' in player1.__type__():
                    x = askXY('Horizontal')
                    y = askXY('Vertical')
                elif 'Machine' in player1.__type__():
                    x = randint(1, 10)
                    y = randint(1, 10)
                if 'damage' in str(player2.storedBoard[x, y]).lower() or 'miss' in str(
                        player2.storedBoard[x, y]).lower():
                    print 'You already Shot here!'
                else:
                    if 'water' in str(player2.storedBoard[x, y]).lower():
                        player2.storedBoard[x, y] += 'Missed'
                        print 'You Missed!'
                        t += 1
                        player2.getMap()
                        return False
                    else:
                        for xFleet in range(len(player2.fleet)):
                            if player2.fleet[xFleet].getName() in player2.storedBoard[x, y]:
                                print 'You hit the' + '', player2.fleet[xFleet].getName()
                                player2.storedBoard[x, y] = player2.fleet[xFleet].getName() + 'Damaged'
                                t += 1
                                player1.hitEnemyShips += 1
                                checkSink(p2, p1, xFleet)
                                checkIfWin(player1, player2)
                                player2.getMap()
                                return False
        except KeyError:
            print 'KeyError'
            break
        except IndexError:
            print 'indexError'
            break

    checkIfWin(player1, player2)


def checkSink(player1, player2, ship):
    shipHp = 0
    for i in range(1, player1.sides):
        for j in range(1, player1.sides):
            if player2.fleet[ship].getName() in player2.storedBoard[i, j] and 'Damaged' in player2.storedBoard[i, j]:
                shipHp += 1

    if shipHp == player2.fleet[ship].getLength():
        print'You sunk %s \'s %s' % (player2.playerType, player2.fleet[ship].getName())


def checkIfWin(player1, player2):
    if player1.hitEnemyShips == 17:
        print '%s has won the game over %s' % (player1.playerType, player2.playerType)
        player2.print_board()
        a = raw_input('Press Enter to Continue')
        raise GameWin


###########
#Instantiates the mechanics of the game.
###########
def startGame(x=0):
    print 'This is BattleShip the Game!'
    print 'There are two players present. Assign player one now.'
    #Here we assign a global var for player one and assign the class player to it.
    global p1
    p1 = Player()
    #We then check if the player want it to be a computer or a human player.
    #I have it automatically place the ships if it's a computer
    #Down the line it will also play with the person or against the computer.
    p1.fleetGen()
    print 'Now assign player 2'
    #Here we assign a global var for player two and assign the class player to it.
    global p2
    p2 = Player()
    p2.fleetGen()
    print 'Now we will start the game, '
    global turns
    turns = 0
    while x == 0:
        while True:
            try:
                #This is when we start to actually fire shots at the other players board
                if turns % 2 == 0:
                    print 'Place your shot Player 1'
                    fireShot(p1, p2)
                    turns += 1
                    print p2.printBoardOpposition()
                    print 'Player Two\'s known Board, on turn %s' % (turns)
                elif turns % 2 != 0:
                    print ('Place your shot Player 2')
                    fireShot(p2, p1)
                    turns += 1
                    print p1.printBoardOpposition()
                    print 'Player One\'s Known Board, on turn %s' % (turns)
                if p1.deBUG or p2.deBUG:
                    print 'Cheaters always prosper!'
                    print ''
                    if turns % 2 == 0:
                        p2.print_board()
                    else:
                        p1.print_board()
            except KeyError:
                print 'KeyError'
                return
            #This special error is raised if the Win condition is met.
            except GameWin:
                x += 1
                return False

#############
#initialize Script
#############
if __name__ == '__main__':
    #do something
    startGame()