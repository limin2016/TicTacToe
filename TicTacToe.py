import requests
from fake_useragent import UserAgent
import time
import numpy as np
import copy

class Board(object):
    def __init__(self):
        self.board = np.array([['-'] * 12 for i in range(12)])
        self.score = 0
        self.next = []
        self.newX = 0
        self.newY = 0

class TicTacToe(object):
    def __init__(self, userid, teamId):
        self.userid = userid
        self.board = Board()
        self.consecutive = 6
        self.teamId = teamId
        self.useragent = UserAgent().random
        self.CNT = 0
        self.waiting = 600
        self.layer = 0
        self.numberOfBoard = 0
        self.symbol = 'O'
        self.opponentSymbol = 'X'
        self.lengthOfRow = 12
        self.maxScore = 10001
        self.minScore = -10001

    def createAGame(self, teamId1, teamId2):
        # use API to create a game
        url = "https://www.notexponential.com/aip2pgaming/api/index.php"

        payload = {'teamId1': teamId1,
                   'teamId2': teamId2,
                   'type': 'game',
                   'gameType': 'TTT'}
        files = [

        ]
        headers = {
            'x-api-key': '7164ae0eb2158cb09c9c',
            'userid': '860',
            'User-Agent': self.useragent
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.json()['code']=='FAIL':
            print(response.json()['message'])
        return response.json()

    def makeAMove(self, move, gameId):
        # use API to make a move
        url = "https://www.notexponential.com/aip2pgaming/api/index.php"

        payload = {'teamId': self.teamId,
                   'move': move,
                   'type': 'move',
                   'gameId': gameId}
        files = [

        ]
        headers = {
            'x-api-key': '7164ae0eb2158cb09c9c',
            'userid': '860',
            'User-Agent': self.useragent
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response.json()

    def getMoves(self, gameID, count):
        # use API to get moves
        url = "https://www.notexponential.com/aip2pgaming/api/index.php?type=moves"+"&gameId="+gameID+"&count="+count

        payload = {}
        headers = {
            'x-api-key': '7164ae0eb2158cb09c9c',
            'userid': self.userid,
            'User-Agent': self.useragent
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def getBoardString(self, gameId):
        # use API to get board string
        url = "https://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=+"+gameId

        payload = {}
        headers = {
            'x-api-key': '7164ae0eb2158cb09c9c',
            'userid': self.userid,
            'User-Agent': self.useragent

        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def getBoardMap(self, gameId):
        # use API to get board map
        url = "https://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId="+gameId

        payload = {}
        headers = {
            'x-api-key': '7164ae0eb2158cb09c9c',
            'userid': self.userid,
            'User-Agent': self.useragent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def checkIfWin(self, board):
        myChess = 0
        opponentChess = 0
        # check row
        for i in board:
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            for j in i:
                if j == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif j == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0

        # check column
        for i in range(len(board)):
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            for column in board[:, i]:
                if column == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif column == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0

        # diagonal
        lengthOfRow = self.lengthOfRow
        for i in range(self.consecutive-1, lengthOfRow):
            x = i
            y = 0
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x - 1
                y = y - 1

        for i in range(1, lengthOfRow-self.consecutive+1):
            x = lengthOfRow - 1
            y = i
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x - 1
                y = y - 1

        for i in range(lengthOfRow-self.consecutive+1)[::-1]:
            x = 0
            y = i
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x + 1
                y = y + 1

        for i in range(1, lengthOfRow-self.consecutive+1):
            x = i
            y = 0
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x + 1
                y = y + 1
        flag = 0
        for i in board:
            for j in i:
                if j=='-':
                    flag = 1
                    break
            if flag==1:
                break

        if myChess<6 and opponentChess<6 and flag==0:
            return 0 # draw
        elif opponentChess==6:
            return 1 # opponent win
        elif myChess==6:
            return 2 # you win
        return -1

    def checkIfoverFlow(self, num):
        if num>=0 and num<self.lengthOfRow:
            return True
        return False

    def one(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                if currentChess=='-':
                    continue
                # from top to bot
                for i in range(1,3):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1,4):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess1==self.consecutive:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 10000)
                    else:
                        rlt = min(rlt, -10000)
                # from left to right
                numberOfCurrentChess2 = 1
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        flag = 1
                        break
                for i in range(1, 4):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess2==self.consecutive:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 10000)
                    else:
                        rlt = min(rlt, -10000)
                # from top left to bot right
                numberOfCurrentChess3 = 1
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 4):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess3==self.consecutive:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 10000)
                    else:
                        rlt = min(rlt, -10000)
                # form bot left to top right
                numberOfCurrentChess4 = 1
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 4):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess4 == self.consecutive:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 10000)
                    else:
                        rlt = min(rlt, -10000)

        if rlt==100000:
            return 0 #represent there is no LianWu
        else:
            return rlt

    def two(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                if currentChess=='-':
                    continue
                # from top to bot
                for i in range(1,3):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1,3):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess1==5:
                    if self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfRow+3):
                        if board[indexOfRow - 3][indexOfColumn] == '-' and board[indexOfRow + 3][indexOfColumn] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9800)
                            else:
                                rlt = min(rlt, -9900)
                        elif board[indexOfRow - 3][indexOfColumn] == '-' or board[indexOfRow + 3][indexOfColumn] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9400)
                            else:
                                rlt = min(rlt, -9800)

                # from left to right
                numberOfCurrentChess2 = 1
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess2 == 5:
                    if self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfColumn+3):
                        if board[indexOfRow][indexOfColumn - 3] == '-' and board[indexOfRow][indexOfColumn + 3] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9800)
                            else:
                                rlt = min(rlt, -9900)
                        elif board[indexOfRow][indexOfColumn - 3] == '-' or board[indexOfRow][indexOfColumn + 3] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9400)
                            else:
                                rlt = min(rlt, -9800)

                # from top left to bot right
                numberOfCurrentChess3 = 1
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess3==5:
                    if self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfColumn+3):
                        if board[indexOfRow - 3][indexOfColumn - 3] == '-' and board[indexOfRow + 3][indexOfColumn + 3] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9800)
                            else:
                                rlt = min(rlt, -9900)
                        elif board[indexOfRow - 3][indexOfColumn - 3] == '-' or board[indexOfRow + 3][indexOfColumn + 3] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9400)
                            else:
                                rlt = min(rlt, -9800)

                # form bot left to top right
                numberOfCurrentChess4 = 1
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess4 == 5:
                    if self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfColumn+3):
                        if board[indexOfRow + 3][indexOfColumn - 3] == '-' and board[indexOfRow - 3][indexOfColumn + 3] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9800)
                            else:
                                rlt = min(rlt, -9900)
                        elif board[indexOfRow + 3][indexOfColumn - 3] == '-' or board[indexOfRow - 3][indexOfColumn + 3] == '-':
                            if currentChess == self.symbol:
                                rlt = min(rlt,9400)
                            else:
                                rlt = min(rlt, -9800)
        if rlt==100000:
            return 0
        else:
            return rlt

    def three(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                # from top to bot
                if self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfRow-3):
                    if board[indexOfRow+3][indexOfColumn]=='-' and board[indexOfRow-3][indexOfColumn]=='-':
                        cntOfMyChess = 0
                        cntOfOpponentChess = 0
                        cntOfBlank = 0
                        for i in range(0, 3):
                            x = indexOfRow - i
                            y = indexOfColumn
                            if self.checkIfoverFlow(x):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y]==self.symbol:
                                    cntOfMyChess = cntOfMyChess+1
                                else:
                                    cntOfBlank = cntOfBlank+1
                            else:
                                break
                        for i in range(1, 3):
                            x = indexOfRow + i
                            y = indexOfColumn
                            if self.checkIfoverFlow(x):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y] == self.symbol:
                                    cntOfMyChess = cntOfMyChess + 1
                                else:
                                    cntOfBlank = cntOfBlank + 1
                            else:
                                break
                        if cntOfBlank==1:
                            if cntOfMyChess==4:
                                rlt = min(9550, rlt)
                            elif cntOfOpponentChess==4:
                                rlt = min(rlt, -9800)
                # from left to right
                if self.checkIfoverFlow(indexOfColumn+3) and self.checkIfoverFlow(indexOfColumn-3):
                    if board[indexOfRow][indexOfColumn+3]=='-' and board[indexOfRow][indexOfColumn-3]=='-':
                        cntOfMyChess = 0
                        cntOfOpponentChess = 0
                        cntOfBlank = 0
                        # from top to bot
                        for i in range(0, 3):
                            x = indexOfRow
                            y = indexOfColumn-i
                            if self.checkIfoverFlow(x):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y]==self.symbol:
                                    cntOfMyChess = cntOfMyChess+1
                                else:
                                    cntOfBlank = cntOfBlank+1
                            else:
                                break
                        for i in range(1, 3):
                            x = indexOfRow
                            y = indexOfColumn+i
                            if self.checkIfoverFlow(x):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y] == self.symbol:
                                    cntOfMyChess = cntOfMyChess + 1
                                else:
                                    cntOfBlank = cntOfBlank + 1
                            else:
                                break
                        if cntOfBlank==1:
                            if cntOfMyChess==4:
                                rlt = min(rlt, 9550)
                            elif cntOfOpponentChess==4:
                                rlt = min(-9800, rlt)
                # from top left to bot right
                if self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfColumn+3):
                    if board[indexOfRow+3][indexOfColumn+3]=='-' and board[indexOfRow-3][indexOfColumn-3]=='-':
                        cntOfMyChess = 0
                        cntOfOpponentChess = 0
                        cntOfBlank = 0
                        # from top to bot
                        for i in range(0, 3):
                            x = indexOfRow-i
                            y = indexOfColumn-i
                            if self.checkIfoverFlow(x):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y]==self.symbol:
                                    cntOfMyChess = cntOfMyChess+1
                                else:
                                    cntOfBlank = cntOfBlank+1
                            else:
                                break
                        for i in range(1, 3):
                            x = indexOfRow+i
                            y = indexOfColumn+i
                            if self.checkIfoverFlow(x):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y] == self.symbol:
                                    cntOfMyChess = cntOfMyChess + 1
                                else:
                                    cntOfBlank = cntOfBlank + 1
                            else:
                                break
                        if cntOfBlank==1:
                            if cntOfMyChess==4:
                                rlt = min(rlt, 9550)
                            elif cntOfOpponentChess==4:
                                rlt = min(rlt, -9800)
                #from bot left to top right
                if self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfColumn+3):
                    if board[indexOfRow+3][indexOfColumn-3]=='-' and board[indexOfRow-3][indexOfColumn+3]=='-':
                        cntOfMyChess = 0
                        cntOfOpponentChess = 0
                        cntOfBlank = 0
                        # from top to bot
                        for i in range(0, 3):
                            x = indexOfRow+i
                            y = indexOfColumn-i
                            if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y]==self.symbol:
                                    cntOfMyChess = cntOfMyChess+1
                                else:
                                    cntOfBlank = cntOfBlank+1
                            else:
                                break
                        for i in range(1, 3):
                            x = indexOfRow-i
                            y = indexOfColumn+i
                            if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                                if board[x][y] == self.opponentSymbol:
                                    cntOfOpponentChess = cntOfOpponentChess + 1
                                elif board[x][y] == self.symbol:
                                    cntOfMyChess = cntOfMyChess + 1
                                else:
                                    cntOfBlank = cntOfBlank + 1
                            else:
                                break
                        if cntOfBlank==1:
                            if cntOfMyChess==4:
                                rlt = min(rlt, 9550)
                            elif cntOfOpponentChess==4:
                                rlt = min(rlt, -9800)

        if rlt==100000:
            return 0 #represent there is no LianWu
        else:
            return rlt

    def four(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess1 == 4:
                    if self.checkIfoverFlow(indexOfRow - 2) and self.checkIfoverFlow(indexOfRow + 3):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow - 2][indexOfColumn] == self.symbol and board[indexOfRow + 3][
                                indexOfColumn] == self.symbol:
                                rlt = min(rlt, 9751)
                            elif board[indexOfRow - 2][indexOfColumn] == self.symbol or board[indexOfRow + 3][
                                indexOfColumn] == self.symbol:
                                rlt = min(rlt, 9750)
                        else:
                            if board[indexOfRow - 2][indexOfColumn] == self.opponentSymbol or board[indexOfRow + 3][
                                indexOfColumn] == self.opponentSymbol:
                                rlt = min(rlt, 9300)

                # from left to right
                numberOfCurrentChess2 = 1
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess2 == 4:
                    if self.checkIfoverFlow(indexOfColumn - 2) and self.checkIfoverFlow(indexOfColumn + 3):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow][indexOfColumn - 2] == self.symbol and board[indexOfRow][
                                indexOfColumn + 3] == self.symbol:
                                rlt = min(rlt, 9751)
                            elif board[indexOfRow][indexOfColumn - 2] == self.symbol or board[indexOfRow][
                                indexOfColumn + 3] == self.symbol:
                                rlt = min(rlt, 9750)
                        else:
                            if board[indexOfRow][indexOfColumn - 2] == self.opponentSymbol or board[indexOfRow][
                                indexOfColumn + 3] == self.opponentSymbol:
                                rlt = min(rlt, 9300)
                # from top left to bot right
                numberOfCurrentChess3 = 1
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess3 == 4:
                    if self.checkIfoverFlow(indexOfRow - 2) and self.checkIfoverFlow(
                            indexOfColumn - 2) and self.checkIfoverFlow(indexOfRow + 3) and self.checkIfoverFlow(
                            indexOfColumn + 3):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow - 2][indexOfColumn - 2] == self.symbol and board[indexOfRow + 3][
                                indexOfColumn + 3] == self.symbol:
                                rlt = min(rlt, 9751)
                            elif board[indexOfRow - 2][indexOfColumn - 2] == self.symbol or board[indexOfRow + 3][
                                indexOfColumn + 3] == self.symbol:
                                rlt = min(rlt, 9750)
                        else:
                            if board[indexOfRow - 2][indexOfColumn - 2] == self.opponentSymbol or board[indexOfRow + 3][
                                indexOfColumn + 3] == self.opponentSymbol:
                                rlt = min(rlt, 9300)

                # form bot left to top right
                numberOfCurrentChess4 = 1
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess4 == 4:
                    if self.checkIfoverFlow(indexOfRow + 3) and self.checkIfoverFlow(
                            indexOfColumn - 3) and self.checkIfoverFlow(indexOfRow - 2) and self.checkIfoverFlow(
                            indexOfColumn + 2):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow + 3][indexOfColumn - 3] == self.symbol and board[indexOfRow - 2][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9751)
                            elif board[indexOfRow + 3][indexOfColumn - 3] == self.symbol or board[indexOfRow - 2][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9750)
                        else:
                            if board[indexOfRow + 3][indexOfColumn - 3] == self.opponentSymbol or board[indexOfRow - 2][
                                indexOfColumn + 2] == self.opponentSymbol:
                                rlt = min(rlt, 9300)
        if rlt == 100000:
            return 0
        else:
            return rlt

    def five(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                if currentChess=='-':
                    continue
                # from top to bot
                for i in range(1,3):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1,3):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess1==5:
                    if self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfRow+3):
                        if board[indexOfRow - 3][indexOfColumn] == self.symbol and board[indexOfRow + 3][indexOfColumn] == self.symbol:
                            if currentChess == self.opponentSymbol:
                                rlt = min(rlt, 9900)
                        elif board[indexOfRow - 3][indexOfColumn] == self.opponentSymbol and board[indexOfRow + 3][indexOfColumn] == self.opponentSymbol:
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9000)

                # from left to right
                numberOfCurrentChess2 = 1
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess2 == 5:
                    if self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfColumn+3):
                        if board[indexOfRow][indexOfColumn - 3] == self.symbol and board[indexOfRow][indexOfColumn + 3] == self.symbol:
                            if currentChess == self.opponentSymbol:
                                rlt = min(rlt, 9900)
                        elif board[indexOfRow][indexOfColumn - 3] == self.opponentSymbol and board[indexOfRow][indexOfColumn + 3] == self.opponentSymbol:
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9000)


                # from top left to bot right
                numberOfCurrentChess3 = 1
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess3==5:
                    if self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfColumn+3):
                        if board[indexOfRow - 3][indexOfColumn - 3] == self.symbol and board[indexOfRow + 3][indexOfColumn + 3] == self.symbol:
                            if currentChess == self.opponentSymbol:
                                rlt = min(rlt, 9900)
                        elif board[indexOfRow - 3][indexOfColumn - 3] == self.opponentSymbol and board[indexOfRow + 3][indexOfColumn + 3] == self.opponentSymbol:
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9000)

                # form bot left to top right
                numberOfCurrentChess4 = 1
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess4 == 5:
                    if self.checkIfoverFlow(indexOfRow+3) and self.checkIfoverFlow(indexOfColumn-3) and self.checkIfoverFlow(indexOfRow-3) and self.checkIfoverFlow(indexOfColumn+3):
                        if board[indexOfRow + 3][indexOfColumn - 3] == self.symbol and board[indexOfRow - 3][indexOfColumn + 3] == self.symbol:
                            if currentChess == self.opponentSymbol:
                                rlt = min(rlt, 9900)
                        elif board[indexOfRow + 3][indexOfColumn - 3] == self.opponentSymbol and board[indexOfRow - 3][indexOfColumn + 3] == self.opponentSymbol:
                            if currentChess == self.symbol:
                                rlt = min(rlt, 9000)
        if rlt==100000:
            return 0
        else:
            return rlt

    def six(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess1 == 3:
                    if self.checkIfoverFlow(indexOfRow - 2) and self.checkIfoverFlow(indexOfRow + 2):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow - 2][indexOfColumn] == self.symbol and board[indexOfRow + 2][
                                indexOfColumn] == self.symbol:
                                rlt = min(rlt, 9761)
                            elif board[indexOfRow - 2][indexOfColumn] == self.symbol or board[indexOfRow + 2][
                                indexOfColumn] == self.symbol:
                                rlt = min(rlt, 9760)
                        else:
                            if board[indexOfRow - 2][indexOfColumn] == self.opponentSymbol or board[indexOfRow + 2][
                                indexOfColumn] == self.opponentSymbol:
                                rlt = min(rlt, 9200)

                # from left to right
                numberOfCurrentChess2 = 1
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess2 == 3:
                    if self.checkIfoverFlow(indexOfColumn - 2) and self.checkIfoverFlow(indexOfColumn + 2):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow][indexOfColumn - 2] == self.symbol and board[indexOfRow][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9761)
                            elif board[indexOfRow][indexOfColumn - 2] == self.symbol or board[indexOfRow][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9760)
                        else:
                            if board[indexOfRow][indexOfColumn - 2] == self.opponentSymbol or board[indexOfRow][
                                indexOfColumn + 2] == self.opponentSymbol:
                                rlt = min(rlt, 9200)
                # from top left to bot right
                numberOfCurrentChess3 = 1
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess3 == 3:
                    if self.checkIfoverFlow(indexOfRow - 2) and self.checkIfoverFlow(
                            indexOfColumn - 2) and self.checkIfoverFlow(indexOfRow + 2) and self.checkIfoverFlow(
                        indexOfColumn + 2):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow - 2][indexOfColumn - 2] == self.symbol and board[indexOfRow + 2][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9761)
                            elif board[indexOfRow - 2][indexOfColumn - 2] == self.symbol or board[indexOfRow + 2][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9760)
                        else:
                            if board[indexOfRow - 2][indexOfColumn - 2] == self.opponentSymbol or board[indexOfRow + 2][
                                indexOfColumn + 2] == self.opponentSymbol:
                                rlt = min(rlt, 9200)

                # form bot left to top right
                numberOfCurrentChess4 = 1
                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess4 == 3:
                    if self.checkIfoverFlow(indexOfRow + 2) and self.checkIfoverFlow(
                            indexOfColumn - 2) and self.checkIfoverFlow(indexOfRow - 2) and self.checkIfoverFlow(
                        indexOfColumn + 2):
                        if currentChess == self.opponentSymbol:
                            if board[indexOfRow + 2][indexOfColumn - 2] == self.symbol and board[indexOfRow - 2][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9761)
                            elif board[indexOfRow + 2][indexOfColumn - 2] == self.symbol or board[indexOfRow - 2][
                                indexOfColumn + 2] == self.symbol:
                                rlt = min(rlt, 9760)
                        else:
                            if board[indexOfRow + 2][indexOfColumn - 2] == self.opponentSymbol or board[indexOfRow - 2][
                                indexOfColumn + 2] == self.opponentSymbol:
                                rlt = min(rlt, 9200)
        if rlt == 100000:
            return 0
        else:
            return rlt

    #du qiang
    def seven(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfCurrentChess1 = 1
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess1 = numberOfCurrentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess1 == 4:
                    if self.checkIfoverFlow(indexOfRow+3)==False and self.checkIfoverFlow(indexOfRow-2):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow-2][indexOfColumn]==self.symbol:
                                rlt = min(rlt, 9780)

                    if self.checkIfoverFlow(indexOfRow-2)==False and self.checkIfoverFlow(indexOfColumn+3):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow+3][indexOfColumn]==self.symbol:
                                rlt = min(rlt, 9780)

                # from left to right
                numberOfCurrentChess2 = 1
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess2 = numberOfCurrentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess2 == 4:
                    if self.checkIfoverFlow(indexOfColumn - 2)==False and self.checkIfoverFlow(indexOfColumn + 3):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow][indexOfColumn+3]==self.symbol:
                                rlt = min(rlt, 9780)

                    if self.checkIfoverFlow(indexOfColumn+3)==False and self.checkIfoverFlow(indexOfColumn-2):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow][indexOfColumn-2]==self.symbol:
                                rlt = min(rlt, 9780)

                # from top left to bot right
                numberOfCurrentChess3 = 1
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess3 = numberOfCurrentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess3 == 4:
                    if (self.checkIfoverFlow(indexOfRow-2)==False or self.checkIfoverFlow(indexOfColumn-2)==False) and self.checkIfoverFlow(indexOfRow + 3) and self.checkIfoverFlow(indexOfColumn+3):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow+3][indexOfColumn+3]==self.symbol:
                                rlt = min(rlt, 9780)

                    if (self.checkIfoverFlow(indexOfRow+3)==False or self.checkIfoverFlow(indexOfColumn+3)==False) and self.checkIfoverFlow(indexOfRow-2) and self.checkIfoverFlow(indexOfColumn-2):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow-2][indexOfColumn-2]==self.symbol:
                                rlt = min(rlt, 9780)

                # form bot left to top right
                numberOfCurrentChess4 = 1
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == currentChess:
                            numberOfCurrentChess4 = numberOfCurrentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfCurrentChess4 == 4:
                    if (self.checkIfoverFlow(indexOfRow-2)==False or self.checkIfoverFlow(indexOfColumn+2)==False) and self.checkIfoverFlow(indexOfRow + 3) and self.checkIfoverFlow(indexOfColumn-3):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow+3][indexOfColumn-3]==self.symbol:
                                rlt = min(rlt, 9780)

                    if (self.checkIfoverFlow(indexOfRow+3)==False or self.checkIfoverFlow(indexOfColumn-3)==False) and self.checkIfoverFlow(indexOfRow-2) and self.checkIfoverFlow(indexOfColumn+2):
                        if currentChess==self.opponentSymbol:
                            if board[indexOfRow-2][indexOfColumn+2]==self.symbol:
                                rlt = min(rlt, 9780)

        if rlt == 100000:
            return 0
        else:
            return rlt

    #XXOXXX
    def eight(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 4):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 4):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 4):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)


                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 4):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)


        if rlt == 100000:
            return 0  # represent there is no LianWu
        else:
            return rlt

    #XXXOXX
    def nine(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 4):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 4):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 4):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 4):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)


        if rlt == 100000:
            return 0  # represent there is no LianWu
        else:
            return rlt

    #XXXXOX
    def ten(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 5):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 5):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 5):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 5):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)


        if rlt == 100000:
            return 0  # represent there is no LianWu
        else:
            return rlt

    #XOXXXX
    def eleven(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess == '-':
                    continue
                # from top to bot
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1, 5):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 5):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 5):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)

                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 5):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 5:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9790)


        if rlt == 100000:
            return 0  # represent there is no LianWu
        else:
            return rlt

    #XXOXX
    def twelve(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess=='-':
                    continue
                # from top to bot
                for i in range(1,3):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1,3):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        flag = 1
                        break
                for i in range(1, 3):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 3):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 3):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 4:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9775)

        if rlt==100000:
            return 0 #represent there is no LianWu
        else:
            return rlt

    #XXXOx
    def thirteen(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess=='-':
                    continue
                # from top to bot
                for i in range(1,4):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1,2):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 4):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        flag = 1
                        break
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 4):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 4):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 4:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9775)

        if rlt==100000:
            return 0 #represent there is no LianWu
        else:
            return rlt

    #XOXXX
    def fourteen(self, board):
        rlt = 100000
        for indexOfRow, valueOfRow in enumerate(board):
            for indexOfColumn, valueOfColumn in enumerate(valueOfRow):
                currentChess = valueOfColumn
                numberOfOpponentChess1 = 0
                if currentChess=='-':
                    continue
                # from top to bot
                for i in range(1,2):
                    x = indexOfRow - i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            flag = 1
                            break
                    else:
                        break
                for i in range(1,4):
                    x = indexOfRow + i
                    y = indexOfColumn
                    if self.checkIfoverFlow(x):
                        if board[x][y]==self.opponentSymbol:
                            numberOfOpponentChess1 = numberOfOpponentChess1 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess1==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # from left to right
                numberOfOpponentChess2 = 0
                for i in range(1, 2):
                    x = indexOfRow
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        flag = 1
                        break
                for i in range(1, 4):
                    x = indexOfRow
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess2 = numberOfOpponentChess2 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess2==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # from top left to bot right
                numberOfOpponentChess3 = 0
                for i in range(1, 2):
                    x = indexOfRow - i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                for i in range(1, 4):
                    x = indexOfRow + i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess3 = numberOfOpponentChess3 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess3==4:
                    if currentChess ==self.symbol:
                        rlt = min(rlt, 9775)

                # form bot left to top right
                numberOfOpponentChess4 = 0
                for i in range(1, 2):
                    x = indexOfRow + i
                    y = indexOfColumn - i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break
                for i in range(1, 4):
                    x = indexOfRow - i
                    y = indexOfColumn + i
                    if self.checkIfoverFlow(x) and self.checkIfoverFlow(y):
                        if board[x][y] == self.opponentSymbol:
                            numberOfOpponentChess4 = numberOfOpponentChess4 + 1
                        else:
                            break
                    else:
                        break

                if numberOfOpponentChess4 == 4:
                    if currentChess == self.symbol:
                        rlt = min(rlt, 9775)

        if rlt==100000:
            return 0 #represent there is no LianWu
        else:
            return rlt

    def evaluationFunction(self, board):
        myChess = 0
        opponentChess = 0
        # check row
        for i in board:
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            for j in i:
                if j == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif j == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0

        # check column
        for i in range(len(board)):
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            for column in board[:, i]:
                if column == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif column == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0

        # diagonal
        lengthOfRow = self.lengthOfRow
        for i in range(self.consecutive - 1, lengthOfRow):
            x = i
            y = 0
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x - 1
                y = y - 1

        for i in range(1, lengthOfRow - self.consecutive + 1):
            x = lengthOfRow - 1
            y = i
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x - 1
                y = y - 1

        for i in range(lengthOfRow - self.consecutive + 1)[::-1]:
            x = 0
            y = i
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x + 1
                y = y + 1

        for i in range(1, lengthOfRow - self.consecutive + 1):
            x = i
            y = 0
            consecutiveMyChess = 0
            consecutiveOpponentChess = 0
            while (x >= 0 and x < lengthOfRow and y >= 0 and y < lengthOfRow):
                if board[x][y] == self.symbol:
                    consecutiveMyChess = consecutiveMyChess + 1
                    myChess = max(consecutiveMyChess, myChess)
                    consecutiveOpponentChess = 0
                elif board[x][y] == self.opponentSymbol:
                    consecutiveOpponentChess = consecutiveOpponentChess + 1
                    opponentChess = max(consecutiveOpponentChess, opponentChess)
                    consecutiveMyChess = 0
                else:
                    consecutiveMyChess = 0
                    consecutiveOpponentChess = 0
                x = x + 1
                y = y + 1

        return consecutiveMyChess*1000//6

    def newEvaluationFunction(self, board):
        rlt = 0
        rlt1 = 0
        tmpRlt = self.one(board)
        if tmpRlt <0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt>0:
            rlt = max(rlt, tmpRlt)


        tmpRlt = self.two(board)
        if tmpRlt <0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt>0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.three(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.four(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.five(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.six(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.seven(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.eight(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.nine(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.ten(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.eleven(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.twelve(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.thirteen(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        tmpRlt = self.fourteen(board)
        if tmpRlt < 0:
            rlt1 = min(rlt1, tmpRlt)
        elif tmpRlt > 0:
            rlt = max(rlt, tmpRlt)

        #if u can win, ensure you win
        if rlt==10000:
            return rlt
        if rlt1<0:
            return rlt1
        if rlt!=10000:
            return rlt
        return self.evaluationFunction(board)

        # if rlt!=100000:
        #     return rlt
        # else:
        #     return self.evaluationFunction(board)

    def createTree(self, fatherBoard, layer):
        if layer>self.layer:
            return
        if self.newEvaluationFunction(fatherBoard.board)==10000:
            fatherBoard.score = -10000
            return
        if self.newEvaluationFunction(fatherBoard.board)==-10000:
            fatherBoard.score = -10000
            return

        newBoard = Board()
        newBoard.board = fatherBoard.board
        for index1, value1 in enumerate(newBoard.board):
            for index2, value2 in enumerate(value1):
                if value2=='-':
                    if layer%2==0:
                        newBoard.board[index1][index2] = self.symbol
                        newBoard.newX = index1
                        newBoard.newY = index2
                        newBoard.score = self.minScore
                    else:
                        newBoard.board[index1][index2] = self.opponentSymbol
                        newBoard.newX = index1
                        newBoard.newY = index2
                        newBoard.score = self.maxScore
                    if layer == self.layer:
                        newBoard.score = self.newEvaluationFunction(newBoard.board)
                    fatherBoard.next.append(copy.deepcopy(newBoard))
                    self.numberOfBoard = self.numberOfBoard + 1
                    self.CNT = self.CNT + 1
                    self.createTree(fatherBoard.next[-1], layer+1)
                    newBoard.board[index1][index2] = '-'
                    newBoard.newX = 0
                    newBoard.newY = 0

    def test(self, fatherBoard, layer):
        if layer>self.layer:
            return
        if self.evaluationFunction(fatherBoard.board)==100:
            fatherBoard.score = 100
            return
        if self.evaluationFunction(fatherBoard.board)==-100:
            fatherBoard.score = -100
            return


        for index1, value1 in enumerate(fatherBoard.board):
            for index2, value2 in enumerate(value1):
                if value2=='-':
                    if layer%2==0:
                        fatherBoard.board[index1][index2] = self.symbol
                        fatherBoard.newX = index1
                        fatherBoard.newY = index2
                        fatherBoard.score = -101
                    else:
                        fatherBoard.board[index1][index2] = self.opponentSymbol
                        fatherBoard.newX = index1
                        fatherBoard.newY = index2
                        fatherBoard.score = 101
                    if layer == self.layer:
                        fatherBoard.score = self.evaluationFunction(fatherBoard.board)
                    self.numberOfBoard = self.numberOfBoard + 1
                    self.CNT = self.CNT + 1
                    print(self.numberOfBoard)
                    self.test(fatherBoard, layer+1)
                    fatherBoard.board[index1][index2] = '-'
                    fatherBoard.newX = 0
                    fatherBoard.newY = 0

    def printTree(self, board):
        for i in board.next:
            if i.next!=[]:
                self.printTree(i)
            else:
                print(i.board,'\n')

    def searchTree(self, currentBoard, layer):
        if currentBoard.next==[]:
            return [currentBoard.score, [currentBoard.newX, currentBoard.newY]]
        coordinate = []
        currentBoard.score = currentBoard.next[0].score
        for i in currentBoard.next:
            i.socre = self.searchTree(i, layer+1)[0]
            if layer%2==0:
                if i.socre >= currentBoard.score:
                    currentBoard.score = i.socre
                    coordinate = [i.newX, i.newY]
            else:
                if i.socre <= currentBoard.score:
                    currentBoard.score = i.socre
        return [currentBoard.score, coordinate]

    def nextMove(self):
        self.board.score = -101
        self.numberOfBoard = 0
        initialBoard = copy.deepcopy(self.board)
        self.createTree(initialBoard, 0)
        response = self.searchTree(initialBoard, 0)
        nextX = response[1][0]
        nextY = response[1][1]
        return [nextX, nextY]

    def AIMove(self, createAGame, preMove, enemyTeamId=0, enemyGameId=0):
        gameId = '0'
        if createAGame == True and preMove == True:
            rlt = self.createAGame(self.teamId, enemyTeamId)
            if rlt['code'] == 'FAIL':
                print(rlt['message'])
                print('Create a game failed')
                return -1
            else:
                gameId = rlt['gameId']
        elif createAGame == True and preMove == False:
            rlt = self.createAGame(enemyTeamId, self.teamId)
            if rlt['code'] == 'FAIL':
                print(rlt['message'])
                print('Create a game failed')
                return -1
            else:
                gameId = rlt['gameId']
        else:
            gameId = enemyGameId

        print('\nGameId is ', str(gameId), '\n')
        cnt = 0
        lastMoveId = '0'
        # move first
        if preMove == True:
            self.symbol = 'O'
            self.opponentSymbol = 'X'
            while True:
                if cnt == 0:
                    startTime = time.time()
                    move = self.nextMove()
                    responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                    if responseMakeAMove['code'] == 'FAIL':
                        print(responseMakeAMove['message'])
                        return -1
                    self.board.board[move[0]][move[1]] = 'O'
                    endTime = time.time()
                    print('This step running ', endTime-startTime,'ms')
                    print(str(move[0]) + ',' + str(move[1]))
                    print(self.board.board, '\n')

                    if self.checkIfWin(self.board.board)==2:
                        print("You won.")
                        return
                    elif self.checkIfWin(self.board.board)==1:
                        print('Opponent won.')
                        return
                    elif self.checkIfWin(self.board.board)==0:
                        print("Draw.")
                        return

                    lastMoveId = str(responseMakeAMove['moveId'])
                    cnt = cnt + 1
                else:
                    waitTimes = 0
                    while True:
                        responseGetMoves = self.getMoves(str(gameId), '1')
                        if responseGetMoves['code'] == 'FAIL':
                            print(responseGetMoves['message'])
                            return -1
                        tempMoveId = str(responseGetMoves['moves'][0]['moveId'])
                        if tempMoveId == lastMoveId:
                            time.sleep(1)
                            waitTimes = waitTimes + 1
                            if waitTimes > self.waiting:
                                print('You played the last move.')
                                checkWin = self.checkIfWin(self.board.board)
                                if checkWin == 0:
                                    print('Draw!')
                                elif checkWin == 1:
                                    print('Opponent won!')
                                elif checkWin == 2:
                                    print('You won!')
                                return
                            print('Waiting to move...')
                        else:
                            startTime = time.time()
                            moveX = int(responseGetMoves['moves'][0]['moveX'])
                            moveY = int(responseGetMoves['moves'][0]['moveY'])
                            symbol = responseGetMoves['moves'][0]['symbol']
                            self.board.board[moveX][moveY] = symbol
                            move = self.nextMove()
                            responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                            endTime = time.time()
                            print('This step run ', endTime-startTime, 'ms')
                            if responseMakeAMove['code'] == 'FAIL':
                                if len(responseMakeAMove)==1:
                                    print('only response one parameter')
                                    print("Game Over! It's a draw'")
                                    return
                                winSignal = 'Cannot make move - Game is no longer open: '+str(gameId)
                                if responseMakeAMove['message']==winSignal:
                                    print('Game is no longer open.')
                                    checkWin = self.checkIfWin(self.board.board)
                                    if checkWin == 0:
                                        print('Draw!')
                                    elif checkWin == 1:
                                        print('Opponent won!')
                                    elif checkWin == 2:
                                        print('You won!')
                                    return
                                print(responseMakeAMove['message'])
                                return -1
                            lastMoveId = str(responseMakeAMove['moveId'])
                            self.board.board[move[0]][move[1]] = 'O'
                            waitTimes = 0
                            print(str(move[0]) + ',' + str(move[1]))
                            print(self.board.board, '\n')
                            if self.checkIfWin(self.board.board) == 2:
                                print("You won.")
                                return
                            elif self.checkIfWin(self.board.board) == 1:
                                print('Opponent won.')
                                return
                            elif self.checkIfWin(self.board.board) == 0:
                                print("Draw.")
                                return
        # move second
        else:
            self.symbol = 'X'
            self.opponentSymbol = 'O'
            while True:
                cnt = 0
                # test if your opponent make the first move
                while True and cnt <= self.waiting:
                    responseGetMoves = self.getMoves(str(gameId), '1')
                    if responseGetMoves['code'] == 'FAIL':
                        print(responseGetMoves['message'], '! Waiting to move...')
                        cnt = cnt + 1
                        time.sleep(1)
                    else:
                        break

                if cnt > self.waiting:
                    print(r"Game Over! The opponent didn't give the first move!")
                    return -1
                startTime = time.time()
                responseGetMoves = self.getMoves(str(gameId), '1')
                moveX = int(responseGetMoves['moves'][0]['moveX'])
                moveY = int(responseGetMoves['moves'][0]['moveY'])
                symbol = responseGetMoves['moves'][0]['symbol']
                self.board.board[moveX][moveY] = symbol

                move = self.nextMove()
                responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                endTime = time.time()
                print("This step run ", endTime-startTime, 'ms')
                if responseMakeAMove['code'] == 'FAIL':
                    print(responseMakeAMove['message'])
                    return -1
                lastMoveId = str(responseMakeAMove['moveId'])
                self.board.board[move[0]][move[1]] = 'X'
                print(str(move[0]) + ',' + str(move[1]))
                print(self.board.board, '\n')
                if self.checkIfWin(self.board.board) == 2:
                    print("You won.")
                    return
                elif self.checkIfWin(self.board.board) == 1:
                    print('Opponent won.')
                    return
                elif self.checkIfWin(self.board.board) == 0:
                    print("Draw.")
                    return

                # opponent give the first move
                waitingTimes = 0
                while True:
                    responseGetMoves = self.getMoves(str(gameId), '1')
                    if responseGetMoves['code'] == 'FAIL':
                        print(responseGetMoves['message'])
                        return -1
                    tempMoveId = str(responseGetMoves['moves'][0]['moveId'])
                    if tempMoveId == lastMoveId:
                        time.sleep(1)
                        waitingTimes = waitingTimes + 1
                        if waitingTimes > self.waiting:
                            print('You played the last move.')
                            checkWin = self.checkIfWin(self.board.board)
                            if checkWin == 0:
                                print('Draw!')
                            elif checkWin == 1:
                                print('Opponent won!')
                            elif checkWin == 2:
                                print('You won!')
                            return
                        print('Waiting to move...')
                    else:
                        startTime = time.time()
                        moveX = int(responseGetMoves['moves'][0]['moveX'])
                        moveY = int(responseGetMoves['moves'][0]['moveY'])
                        symbol = responseGetMoves['moves'][0]['symbol']
                        self.board.board[moveX][moveY] = symbol
                        move = self.nextMove()
                        responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                        endTime = time.time()
                        print('This step run ', endTime-startTime, 'ms')
                        if responseMakeAMove['code'] == 'FAIL':
                            if len(responseMakeAMove) == 1:
                                print('move the same place.')
                                checkWin = self.checkIfWin(self.board.board)
                                if checkWin == 0:
                                    print('Draw!')
                                elif checkWin == 1:
                                    print('Opponent won!')
                                elif checkWin == 2:
                                    print('You won!')
                                return
                            winSignal = 'Cannot make move - Game is no longer open: ' + str(gameId)
                            if responseMakeAMove['message'] == winSignal:
                                print('Game is not open.')
                                checkWin = self.checkIfWin(self.board.board)
                                if checkWin == 0:
                                    print('Draw!')
                                elif checkWin == 1:
                                    print('Opponent won!')
                                elif checkWin == 2:
                                    print('You won!')
                                return
                            print(responseMakeAMove['message'])
                            return -1
                        lastMoveId = str(responseMakeAMove['moveId'])
                        self.board.board[move[0]][move[1]] = 'X'
                        print(str(move[0]) + ',' + str(move[1]))
                        print(self.board.board, '\n')
                        if self.checkIfWin(self.board.board) == 2:
                            print("You won.")
                            return
                        elif self.checkIfWin(self.board.board) == 1:
                            print('Opponent won.')
                            return
                        elif self.checkIfWin(self.board.board) == 0:
                            print("Draw.")
                            return
                        waitingTimes = 0



player1 = TicTacToe('860', '1212')
player1.AIMove(True, True, '1221')
player1.nextMove()
# player1.test(player1.board, 0)
# a = np.array([
# ['X', 'X', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-'],
# ['X', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['O', 'X', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['X', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']])
# a= player1.fourteen(a)
# print(a)
# # player1.seven(a)