# main module for the Dr.Mario Game
# The logical.py is the module for the game logic
# The ui.py is the module for displaying the game field


# Name Boxuan Zhang
# Email boxuanz3@uci.edu
# Student ID 95535906


import shlex
from logic import GameState
from ui import TextUI


def get_game_state() -> GameState or None:
    """Get game state from user input."""
    try:
        rows: int = int(input())
        cols: int = int(input())
        next_line: str = input().strip()
        
        if next_line == 'EMPTY':    
            return GameState(rows, cols)
        elif next_line == 'CONTENTS':
            contents: list[str] = []
            for _ in range(rows):
                line: str = input().strip('\n')
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


def main() -> None:
    game_state: GameState | None = get_game_state()
    if game_state is None:
        return
        
    ui: TextUI = TextUI(game_state)
    ui.run()


if __name__ == '__main__':
    main()
    