# main module for the Dr.Mario Game
# field module is the module for create field for the game
# faller module is the module for the status of cells and player command
# virus module is the module for creating virus for the game

# Boxuan Zhang
# boxuanz3@uci.edu
# 95535906

import shlex
from logic import GameState
from ui import TextUI

def get_game_state():
    """Get game state from user input."""
    try:
        rows = int(input())
        cols = int(input())
        next_line = input().strip()
        
        if next_line == 'EMPTY':
            return GameState(rows, cols)
        elif next_line == 'CONTENTS':
            contents = []
            for _ in range(rows):
                line = input().strip('\n')
                if len(line) < cols:
                    line += ' ' * (cols - len(line))
                contents.append(line[:cols])
            return GameState(rows, cols, contents)
        else:
            print("ERROR")
            return None
    except (ValueError, EOFError):
        print("ERROR")
        return None

def main():
    game_state = get_game_state()
    if game_state is None:
        return
        
    ui = TextUI(game_state)
    ui.run()

if __name__ == '__main__':
    main()
    