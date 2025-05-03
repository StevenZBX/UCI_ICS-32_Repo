# main module for the Dr.Mario Game
# field module is the module for create field for the game
# faller module is the module for the status of cells and player command
# virus module is the module for creating virus for the game

# Boxuan Zhang
# boxuanz3@uci.edu
# 95535906


import sys
from logic import GameState
from ui import TextUI

def main():
    rows = int(input())
    cols = int(input())
    next_line = sys.stdin.readline().strip()
    game_state = None
    if next_line == 'EMPTY':
        game_state = GameState(rows, cols)
    elif next_line == 'CONTENTS':
        contents = []
        for _ in range(rows):
            line = sys.stdin.readline().strip('\n')
            if len(line) < cols:
                line += ' ' * (cols - len(line))
            contents.append(line[:cols])
        game_state = GameState(rows, cols, contents)
    else:
        print("Invalid input after rows and columns.")
        return

    ui = TextUI(game_state)
    ui.run()

if __name__ == '__main__':
    main()