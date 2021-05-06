#
# pikachu_oldest.py : Play the game of Pikachu
#
# Suraj Gupta Gudla - surgudla; Tarika sadey - tsadey; Bhargav sai Gogineni - bgoginen
#
# Based on skeleton code by D. Crandall, March 2021
#
import sys
import time
import copy
import heapq
# converts the 2d board in a 1d string format
def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


# gives the successor moves of the pikachu piece
def pikachu_su(board, player, N, direct, pos,kill):
    if player=='w':
        tempboard=copy.deepcopy(board)
        succerlist = []
        if (pos[0] + direct[0] == N or pos[1] +direct[1] == N or pos[0] +direct[0] == -1 or pos[1] +direct[1] == -1):
            return []
        if((pos[0] + 2 * direct[0] == N or pos[1] + 2 * direct[1] == N or pos[0] + 2 * direct[0] == -1 or pos[1] + 2 * direct[1] == -1 )
                and (tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=="b" or tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=="B")):
            return []
        if ((tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=="b" or tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=="B")
                and (tempboard[pos[0]+2 * direct[0]][pos[1]+2 * direct[1]]=='b' or tempboard[pos[0]+2 * direct[0]][pos[1]+2 * direct[1]]=='B')):
            return []
        if (tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=='.'):
            tempboard[pos[0]][pos[1]], tempboard[pos[0] + direct[0]][pos[1] + direct[1]] = tempboard[pos[0] + direct[0]][pos[1] + direct[1]], tempboard[pos[0]][pos[1]]
            pos[0] = pos[0] + direct[0]
            pos[1] = pos[1] + direct[1]
            succerlist.append(tempboard)
            succerlist = succerlist + pikachu_su(tempboard, player, N, direct, pos,kill)
            return succerlist
        elif ((tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=='b' or tempboard[pos[0] + direct[0]][pos[1] + direct[1]]=='B') and tempboard[pos[0] + 2*direct[0]][pos[1] + 2*direct[1]]=='.' and not kill ):
            #have to kill the b after it was crossed by w.
            tempboard[pos[0] + direct[0]][pos[1] + direct[1]] = '.'
            tempboard[pos[0]][pos[1]], tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]] = tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]], tempboard[pos[0]][pos[1]]
            pos[0] = pos[0] + 2 * direct[0]
            pos[1] = pos[1] + 2 * direct[1]
            succerlist.append(tempboard)
            succerlist = succerlist + pikachu_su(tempboard, player, N, direct, pos,True)
            return succerlist
        return []
    elif player=='b':
        tempboard = copy.deepcopy(board)
        succerlist = []
        if (pos[0] + direct[0] == N or pos[1] + direct[1] == N or pos[0] + direct[0] == -1 or pos[1] + direct[1] == -1):
            return []
        if ((pos[0] + 2 * direct[0] == N or pos[1] + 2 * direct[1] == N or pos[0] + 2 * direct[0] == -1 or pos[1] + 2 *
             direct[1] == -1)
                and (tempboard[pos[0] + direct[0]][pos[1] + direct[1]] == "w" or tempboard[pos[0] + direct[0]][pos[1] + direct[1]] == "W")):
            return []
        if ((tempboard[pos[0] + direct[0]][pos[1] + direct[1]] == "w" or tempboard[pos[0] + direct[0]][
            pos[1] + direct[1]] == "W")
                and (tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]] == 'w' or
                     tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]] == 'W')):
            return []
        if (tempboard[pos[0] + direct[0]][pos[1] + direct[1]] == '.'):
            tempboard[pos[0]][pos[1]], tempboard[pos[0] + direct[0]][pos[1] + direct[1]] = \
            tempboard[pos[0] + direct[0]][pos[1] + direct[1]], tempboard[pos[0]][pos[1]]
            pos[0] = pos[0] + direct[0]
            pos[1] = pos[1] + direct[1]
            succerlist.append(tempboard)
            succerlist = succerlist + pikachu_su(tempboard, player, N, direct, pos,kill)
            return succerlist
        elif ((tempboard[pos[0] + direct[0]][pos[1] + direct[1]] == 'w' or tempboard[pos[0] + direct[0]][
            pos[1] + direct[1]] == 'W') and tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]] == '.' and not kill):
            # have to kill the b after it was crossed by w.
            tempboard[pos[0] + direct[0]][pos[1] + direct[1]] = '.'
            tempboard[pos[0]][pos[1]], tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]] = \
            tempboard[pos[0] + 2 * direct[0]][pos[1] + 2 * direct[1]], tempboard[pos[0]][pos[1]]
            pos[0] = pos[0] + 2 * direct[0]
            pos[1] = pos[1] + 2 * direct[1]
            succerlist.append(tempboard)
            succerlist = succerlist + pikachu_su(tempboard, player, N, direct, pos,True)
            return succerlist
        return []

#returns all the successor states/ next possible moves of a player
def successors(board,player,N):
    successorsList = []
    boardList=copy.deepcopy(board)
    if (player == 'w'):
        for i in range(0, N - 1):  # one pos forward
            for j in range(0, N):
                if boardList[i][j] == 'w':
                    if boardList[i + 1][j] == '.':
                        temp = copy.deepcopy(boardList)
                        if (i + 1 == N - 1):
                            temp[i][j] = '.'
                            temp[i + 1][j] = 'W'
                        else:
                            temp[i][j], temp[i + 1][j] = temp[i + 1][j], temp[i][j]
                        successorsList.append(temp)

        for i in range(0, N):  # one pos right
            for j in range(0, N - 1):
                if boardList[i][j] == 'w':
                    if (boardList[i][j + 1] == '.'):
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j + 1] = temp[i][j + 1], temp[i][j]
                        successorsList.append(temp)

        for i in range(0, N):  # one pos left
            for j in range(N - 1, 0, -1):
                if boardList[i][j] == 'w':
                    if (boardList[i][j - 1] == '.'):
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j - 1] = temp[i][j - 1], temp[i][j]
                        successorsList.append(temp)

        for i in range(0, N):  # one jump right
            for j in range(0, N - 2):
                if boardList[i][j] == 'w':
                    if (boardList[i][j + 2] == '.' and boardList[i][j + 1] == 'b' or boardList[i][j + 1] == 'B'):
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j + 2] = temp[i][j + 2], temp[i][j]
                        temp[i][j + 1] = '.'
                        successorsList.append(temp)

        for i in range(0, N):  # one jump left
            for j in range(N - 1, 1, -1):
                if boardList[i][j] == 'w':
                    if (boardList[i][j - 2] == '.' and boardList[i][j - 1] == 'b' or boardList[i][j - 1] == 'B'):
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j - 2] = temp[i][j - 2], temp[i][j]
                        temp[i][j - 1] = '.'
                        successorsList.append(temp)

        for i in range(0, N - 2):  # one jump forward
            for j in range(0, N):
                if boardList[i][j] == 'w':
                    if boardList[i + 2][j] == '.' and boardList[i + 1][j] == 'b' or boardList[i + 1][j] == 'B':
                        temp = copy.deepcopy(boardList)
                        if (i + 2 == N - 1):
                            temp[i][j] = '.'
                            temp[i + 2][j] = 'W'
                            temp[i + 1][j] = '.'
                        else:
                            temp[i][j], temp[i + 2][j] = temp[i + 2][j], temp[i][j]
                            temp[i + 1][j] = '.'
                        successorsList.append(temp)

        for i in range(0, N):  # W pikachu
            for j in range(0, N):
                if (boardList[i][j] == 'W'):
                    pikachuBoard = pikachu_su(boardList, player, N, [1, 0], [i, j],False)
                    successorsList = successorsList + pikachuBoard
                    pikachuBoard = pikachu_su(boardList, player, N, [0, 1], [i, j],False)
                    successorsList = successorsList + pikachuBoard
                    pikachuBoard = pikachu_su(boardList, player, N, [-1, 0], [i, j],False)
                    successorsList = successorsList + pikachuBoard
                    pikachuBoard = pikachu_su(boardList, player, N, [0, -1], [i, j],False)
                    successorsList = successorsList + pikachuBoard
    else:
        for i in range(N - 1, -1, -1):  # B pikachu
            for j in range(N - 1, -1, -1):
                if (boardList[i][j] == 'B'):
                    pikachuBoard = pikachu_su(boardList, player, N, [1, 0], [i, j],False)
                    successorsList = successorsList + pikachuBoard
                    pikachuBoard = pikachu_su(boardList, player, N, [0, 1], [i, j],False)
                    successorsList = successorsList + pikachuBoard
                    pikachuBoard = pikachu_su(boardList, player, N, [-1, 0], [i, j],False)
                    successorsList = successorsList + pikachuBoard
                    pikachuBoard = pikachu_su(boardList, player, N, [0, -1], [i, j],False)
                    successorsList = successorsList + pikachuBoard

        for i in range(N - 1, 0, -1):  # one pos forward
            for j in range(0, N):
                if boardList[i][j] == 'b':
                    if boardList[i - 1][j] == '.':
                        temp = copy.deepcopy(boardList)
                        if i - 1 == 0:
                            temp[i][j] = '.'
                            temp[i - 1][j] = 'B'
                        else:
                            temp[i][j], temp[i - 1][j] = temp[i - 1][j], temp[i][j]
                        successorsList.append(temp)

        for i in range(0, N - 1):  # one pos right
            for j in range(0, N - 1):
                if boardList[i][j] == 'b':
                    if boardList[i][j + 1] == '.':
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j + 1] = temp[i][j + 1], temp[i][j]
                        successorsList.append(temp)

        for i in range(0, N - 1):  # one pos left
            for j in range(N - 2, -1, -1):
                if boardList[i][j] == 'b':
                    if boardList[i][j - 1] == '.':
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j - 1] = temp[i][j - 1], temp[i][j]
                        successorsList.append(temp)

        for i in range(N - 1, 1, -1):  # one jump forward
            for j in range(0, N):
                if boardList[i][j] == 'b':
                    if boardList[i - 2][j] == '.' and boardList[i - 1][j] == 'w' or boardList[i - 1][j] == 'W':
                        temp = copy.deepcopy(boardList)
                        if (i - 2 == 0):
                            temp[i][j] = '.'
                            temp[i - 2][j] = 'B'
                            temp[i - 1][j] = '.'
                        else:
                            temp[i][j], temp[i - 2][j] = temp[i - 2][j], temp[i][j]
                            temp[i - 1][j] = '.'
                        successorsList.append(temp)

        for i in range(0, N - 1):  # one jump right
            for j in range(0, N - 2):
                if boardList[i][j] == 'b':
                    if boardList[i][j + 2] == '.' and boardList[i][j + 1] == 'w' or boardList[i][j + 1] == 'W':
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j + 2] = temp[i][j + 2], temp[i][j]
                        temp[i][j + 1] = '.'
                        successorsList.append(temp)

        for i in range(0, N - 1):  # one jump left
            for j in range(N - 3, -1, -1):
                if boardList[i][j] == 'b':
                    if boardList[i][j - 2] == '.' and boardList[i][j - 1] == 'w' or boardList[i][j - 1] == 'W':
                        temp = copy.deepcopy(boardList)
                        temp[i][j], temp[i][j - 2] = temp[i][j - 2], temp[i][j]
                        temp[i][j - 1] = '.'
                        successorsList.append(temp)
    return successorsList

#computes the utility function value to a state
def evaluate(board,N,player):
    #difference in pichus and pikachus
    p1=p2=pk1=pk2=0
    for i in range(N):
        for j in range(N):
            if(board[i][j]=="b"):
                p1+=1
            if(board[i][j]=="B"):
                pk1+=1
            if(board[i][j]=="w"):
                p2+=1
            if(board[i][j]=="W"):
                pk2+=1
    if (player=="w"):
        if(p1+pk1==0):
            return 1000000
        else:
            return (p2-p1)+3*(pk2-pk1)
    else:
        if(p2+pk2==0):
            return 1000000
        else:
            return -1*((p2-p1)+3*(pk2-pk1))

#checks whether a state is a terminal sttae or not
def isTerminalState(successor,N):
    blacks=0
    whites=0
    for i in range(N):
        for j in range(N):
            if(successor[i][j]=="b" or successor[i][j]=="B" ):
                blacks+=1
            if(successor[i][j]=="w" or successor[i][j]=="W"):
                whites+=1
    if(blacks==0 or whites==0):
        return True
    else:
        return False


#computes the minimum value among the successors of a given state
def minvalue(successor, alpha, beta, depth, player, depthlimit,N):
    depth += 1
    if time.time() >= endtime - 1:
        sys.exit(0)
    if depth == depthlimit or isTerminalState(successor,N):
        return evaluate(successor, N,player)
    else:
        if (player=="w"):
            oppositeplayer="b"
        else:
            oppositeplayer="w"
        maxsuccessors = successors(successor, oppositeplayer,N)
        for maxsucc in maxsuccessors:
            beta = min(beta, maxvalue(maxsucc, alpha, beta, depth, player, depthlimit,N))
            if alpha >= beta:
                return beta
        return beta

#computes the maximum value among the successors of a given state
def maxvalue(successor, alpha, beta, depth, player, depthlimit,N):
    depth += 1
    if time.time() >= endtime - 1:
        sys.exit(0)
    if depth == depthlimit or isTerminalState(successor, N):
        return evaluate(successor, N,player)
    else:
        minsuccessors = successors(successor, player,N)
        for minsucc in minsuccessors:
            alpha = max(alpha, minvalue(minsucc, alpha, beta, depth, player, depthlimit,N))
            if alpha >= beta:
                return alpha
        return alpha

def min_max(board,player,N,depth):
    succ=successors(board,player,N)
    defaultBetaValue = 100000000
    defaultAlphaValue = -10000000
    betavaluemaxheap = []
    for minsucc in succ:
        heapq.heappush(betavaluemaxheap, (minvalue(minsucc, defaultAlphaValue, defaultBetaValue, 0, player, depth,N)*-1, minsucc))
    return heapq.heappop(betavaluemaxheap)[1]

starttime = time.time()
endtime = time.time() 

# finds the best possible move
def find_best_move(board, N, player, timelimit):
    boardList=[]
    i=0
    while i<N*N:
        li = []
        for j in range(N):
            li.append(board[i])
            i+=1
        boardList.append(li)
    global endtime
    endtime = time.time() + float(timelimit)
    depth=2

    while True:
        result= min_max(boardList, player, N,depth)
        str1 = ""
        for i in range(len(result)):
            for j in range(len(result[0])):
                str1 = str1 + str(result[i][j])
        print("\n")
        yield str1
        depth+=1

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")
    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")
    if len(board) != N * N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")
    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
