from flask import session


def winner(turn, board):
    #list turn coordinates
    position = list()
    for col in range(6):
        for row in range(6):
            if board[col][row] == turn:
                position.append((col, row))
    
                
    #check horizontal win
    for i in range(6):
        columns = [j for j in position if j[0] == i]
        if len(columns) >= 3:
            counter = 0
            for each in range(len(columns)):
                try:
                    if columns[each + 1][1] - columns[each][1] == 1:
                        counter += 1
                    else:
                        counter = 0
                except:
                    break                    
        else:
            continue
        if counter >= 3:
            return turn
        else:
            continue

    #check vertical wins
    for i in range(6):
        rows = [j for j in position if j[1] == i]
        if len(rows) >= 3:
            counter = 0
            for each in range(len(rows)):
                try:
                    if rows[each + 1][0] - rows[each][0] == 1:
                        counter += 1
                    else:
                        counter = 0
                except:
                    break
        else:
            continue
        if counter >= 3:
            return turn
        else:
            continue


    #check left-right diagonal wins
    for cord in position:
        gen_cords = []
        for _ in range(4):
            gen_cords.append(cord)
            cord = (cord[0]+1, cord[1]+1)
        counter = 0
        for cords in gen_cords:
            try:
                if board[cords[0]][cords[1]] == turn:
                    counter += 1
                else:
                    break
            except:
                continue
        if counter >= 4:
            return turn
        else:
            continue


    #check right-left diagonal wins
    for cord in position:
        gen_cords = []
        for _ in range(4):
            gen_cords.append(cord)
            cord = (cord[0]+1, cord[1]-1)
        counter = 0
        for cords in gen_cords:
            try:
                if board[cords[0]][cords[1]] == turn:
                    counter += 1
                else:
                    break
            except:
                continue
        if counter >= 4:
            return turn
        else:
            continue

    #check for draw
    #session['draw'] = 0
    for coords in session['board']:
        for coord in coords:
            if coord == None:
                session['draw']  += 1
                break
    if session['draw']  == 0:
        session['draw']  = True
    else:
        draw = False
    return None


def minimax(board):

    from random import choice

    #copy board to session
    session['temp_board'] = list()
    for i in board:
        session['temp_board'].append(i)

    #list all empty coordinates
    position = list()
    for col in range(6):
        for row in range(6):
            if session['temp_board'][col][row] == None:
                position.append((col, row))


    #defend against users moves
    for pos in position:
        session['temp_board'][pos[0]][pos[1]] = "X"
        result = winner("X", session['temp_board'])
        if result == "X":
            session['temp_board'][pos[0]][pos[1]] = None
            return (pos[0], pos[1])
        for next_pos in position:
            session['temp_board'][next_pos[0]][next_pos[1]] = "X"
            next_result = winner("X", session['temp_board'])    
            if next_result == "X":
                session['temp_board'][next_pos[0]][next_pos[1]] = None
                return (pos[0], pos[1])
            session['temp_board'][next_pos[0]][next_pos[1]] = None
        session['temp_board'][pos[0]][pos[1]] = None


    #make first random move
    check = 0
    for line in session['temp_board']:
        if "O" in line:
            check += 1
    if check == 0:
        return choice(position)

    #make intelligent move
    for pos in position:
        session['temp_board'][pos[0]][pos[1]] = "O"
        result = winner("O", session['temp_board'])
        if result == "O":
            session['temp_board'][pos[0]][pos[1]] = None
            print("first move")
            return (pos[0], pos[1])
        for next_pos in position:
            session['temp_board'][next_pos[0]][next_pos[1]] = "O"
            next_result = winner("O", session['temp_board'])
            if next_result == "O":
                session['temp_board'][next_pos[0]][next_pos[1]] = None
                print("second move")
                return (next_pos[0], next_pos[1])
            for next_next_pos in position:
                session['temp_board'][next_next_pos[0]][next_next_pos[1]] = "O"
                next_next_result = winner("O", session['temp_board'])
                if next_next_result == "O":
                    session['temp_board'][next_next_pos[0]][next_next_pos[1]] = None
                    print("third move")
                    return (next_next_pos[0], next_next_pos[1])
                session['temp_board'][next_next_pos[0]][next_next_pos[1]] = None
            session['temp_board'][next_pos[0]][next_pos[1]] = None
        session['temp_board'][pos[0]][pos[1]] = None
        return choice(position)