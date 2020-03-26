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
        if response.json()['code']=='OK':
            print('teamId = ', response.json()['gameId'])
        else:
            print(response.json()['message'])
        return response.json()

    def makeAMove(self, move, gameId):
        # use API to make a move
        url = "https://www.notexponential.com/aip2pgaming/api/index.php"

        payload = {'teamId': '1212',
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
        #print(response.text.encode('utf8'))
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
        #print(response.json())
        #print(response.json()['moves'][0]['moveId'])
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

        #print(response.text.encode('utf8'))
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

        #print(response.text.encode('utf8'))
        return response.json()

    def evaluationFunction(self, board):
        maxConsecutiveO = 0
        maxConsecutiveX = 0
        # check row
        for i in board:
            consecutiveO = 0
            consecutiveX = 0
            for j in i:
                if j=='O':
                    consecutiveO = consecutiveO+1
                    maxConsecutiveO = max(consecutiveO, maxConsecutiveO)
                    consecutiveX = 0
                elif j=='X':
                    consecutiveX = consecutiveO + 1
                    maxConsecutiveX = max(consecutiveX, maxConsecutiveX)
                    consecutiveO = 0
                else:
                    consecutiveO = 0
                    consecutiveX = 0

        # check column
        for i in range(len(board)):
            consecutiveO = 0
            consecutiveX = 0
            for column in board[:,i]:
                if column == 'O':
                    consecutiveO = consecutiveO + 1
                    maxConsecutiveO = max(consecutiveO, maxConsecutiveO)
                    consecutiveX = 0
                elif column == 'X':
                    consecutiveX = consecutiveO + 1
                    maxConsecutiveX = max(consecutiveX, maxConsecutiveX)
                    consecutiveO = 0
                else:
                    consecutiveO = 0
                    consecutiveX = 0

        # diagonal
        ScoreO = maxConsecutiveO*100//6
        ScoreX = maxConsecutiveX*100//6
        # print('maxConsecutiveO = ', ScoreO)
        # print('maxConsecutiveX = ', ScoreX)
        # print(board,'\n')
        if ScoreX==100:
            return -100
        return (maxConsecutiveO*100//6)


    def createTree(self, fatherBoard, layer):
        if layer>1:
            return
        if self.evaluationFunction(fatherBoard.board)==100:
            fatherBoard.score = 100
            return
        if self.evaluationFunction(fatherBoard.board)==-100:
            fatherBoard.score = -100
            return

        newBoard = Board()
        newBoard.board = fatherBoard.board
        for index1, value1 in enumerate(newBoard.board):
            for index2, value2 in enumerate(value1):
                if value2=='-':
                    if layer%2==0:
                        newBoard.board[index1][index2] = 'O'
                        newBoard.newX = index1
                        newBoard.newY = index2
                        newBoard.score = -101
                    else:
                        newBoard.board[index1][index2] = 'X'
                        newBoard.newX = index1
                        newBoard.newY = index2
                        newBoard.score = 101
                    if layer == 1:
                        newBoard.score = self.evaluationFunction(newBoard.board)
                    fatherBoard.next.append(copy.deepcopy(newBoard))
                    # print(newBoard.board)
                    # print('')
                    self.CNT = self.CNT + 1
                    self.createTree(fatherBoard.next[-1], layer+1)
                    newBoard.board[index1][index2] = '-'
                    newBoard.newX = 0
                    newBoard.newY = 0
                    # for i in fatherBoard.next:
                    #     print(i.board)
                    # print('')

    def printTree(self, board):
        for i in board.next:
            if i.next!=[]:
                self.printTree(i)
            else:
                print(i.board,'\n')

    def searchTree(self, currentBoard, layer):
        # set values of states
        if currentBoard.next==[]:
            # print(currentBoard.board)
            # print('')
            b = currentBoard.score
            return [currentBoard.score, currentBoard.newX, currentBoard.newY]
        coordinate = []
        c = currentBoard.score
        currentBoard.score = currentBoard.next[0].score
        for i in currentBoard.next:
            i.socre = self.searchTree(i, layer+1)[0]
            a = i.socre
            if layer%2==0:
                if i.socre >= currentBoard.score:
                    currentBoard.score = i.socre
                    coordinate = [i.newX, i.newY]
            else:
                if i.socre <= currentBoard.score:
                    currentBoard.score = i.socre
        return [currentBoard.score, coordinate]
        # for i in currentBoard.next:
        #     res = self.searchTree(i, layer + 1)
        #     a = currentBoard.score
        #     if layer%2==0:
        #         if res[0] >= currentBoard.score:
        #             currentBoard.score  = res[0]
        #             coordinate = [res[1], res[2]]
        #         #currentBoard.score = max(self.searchTree(i, layer + 1)[0], currentBoard.score)
        #     else:
        #         if res[0] <= currentBoard.score:
        #             currentBoard.score = res[0]
        #             coordinate = [res[1], res[2]]
        #         #currentBoard.score = min(self.searchTree(i, layer+1)[0], currentBoard.score)
        # return  [currentBoard.score, coordinate[0], coordinate[1]]



    def nextMove(self):
        self.board.score = -101
        # self.board.board[0][0] = 'O'
        initialBoard = copy.deepcopy(self.board)
        self.createTree(initialBoard, 0)
        # print('test')
        # self.printTree(initialBoard)
        # print('test')
        response = self.searchTree(initialBoard, 0)
        nextX = response[1][0]
        nextY = response[1][1]
        # self.board.board[nextX][nextY] = 'O'
        # print(str(nextX)+','+str(nextY))
        # print(self.board.board, '\n')
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
            while True:
                if cnt == 0:
                    move = self.nextMove()
                    responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                    if responseMakeAMove['code'] == 'FAIL':
                        print(responseMakeAMove['message'])
                        return -1
                    self.board.board[move[0]][move[1]] = 'O'
                    print(str(move[0]) + ',' + str(move[1]))
                    print(self.board.board, '\n')
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
                            if waitTimes > 30:
                                print('Game Over!')
                                return
                            print('Waiting to move...')
                        else:
                            # print('tempMoveId= ', tempMoveId)
                            # print('lastMoveId= ', lastMoveId)
                            moveX = int(responseGetMoves['moves'][0]['moveX'])
                            moveY = int(responseGetMoves['moves'][0]['moveY'])
                            symbol = responseGetMoves['moves'][0]['symbol']
                            self.board.board[moveX][moveY] = symbol

                            move = self.nextMove()
                            responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                            if responseMakeAMove['code'] == 'FAIL':
                                print(responseMakeAMove)
                                print(responseMakeAMove['message'])
                                return -1
                            lastMoveId = str(responseMakeAMove['moveId'])
                            self.board.board[move[0]][move[1]] = 'O'
                            print(str(move[0]) + ',' + str(move[1]))
                            print(self.board.board, '\n')
        # move second
        else:
            while True:
                cnt = 0
                # test if your opponent make the first move
                while True and cnt <= 30:
                    responseGetMoves = self.getMoves(str(gameId), '1')
                    if responseGetMoves['code'] == 'FAIL':
                        print(responseGetMoves['message'], '! Wating to move...')
                        cnt = cnt + 1
                        time.sleep(1)
                    else:
                        break

                if cnt > 30:
                    print(r"Game Over! The opponent didn't give the first move!")
                    return -1
                responseGetMoves = self.getMoves(str(gameId), '1')
                moveX = int(responseGetMoves['moves'][0]['moveX'])
                moveY = int(responseGetMoves['moves'][0]['moveY'])
                symbol = responseGetMoves['moves'][0]['symbol']
                self.board.board[moveX][moveY] = symbol

                move = self.nextMove()
                responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                if responseMakeAMove['code'] == 'FAIL':
                    print(responseMakeAMove['message'])
                    return -1
                lastMoveId = str(responseMakeAMove['moveId'])
                self.board.board[move[0]][move[1]] = 'X'
                print(str(move[0]) + ',' + str(move[1]))
                print(self.board.board, '\n')

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
                        if waitingTimes > 30:
                            print('Game Over!')
                            return
                        print('Waiting to move...')
                    else:
                        moveX = int(responseGetMoves['moves'][0]['moveX'])
                        moveY = int(responseGetMoves['moves'][0]['moveY'])
                        symbol = responseGetMoves['moves'][0]['symbol']
                        self.board.board[moveX][moveY] = symbol

                        move = self.nextMove()
                        responseMakeAMove = self.makeAMove(str(move[0]) + ',' + str(move[1]), gameId)
                        if responseMakeAMove['code'] == 'FAIL':
                            print(responseMakeAMove['message'])
                            return -1
                        lastMoveId = str(responseMakeAMove['moveId'])
                        self.board.board[move[0]][move[1]] = 'X'
                        print(str(move[0]) + ',' + str(move[1]))
                        print(self.board.board, '\n')








player1 = TicTacToe('860', '1212')
player1.AIMove(True, False, '1221')
# player1.nextMove()
