# Main module for the Dr.Mario Game
# The logical.py is the module for the game logic
# The ui.py is the module for displaying the game field


# Name Boxuan Zhang
# Email boxuanz3@uci.edu
# Student ID 95535906


from logic import GameState
from ui import TextUI


def get_game_state() -> GameState or None:
    """Get game state from user input."""
    try:
        rows: int = int(input())
        cols: int = int(input())
        status: str = input().strip()
        if rows >= 4 and cols >= 3:
            if status == 'EMPTY':    
                return GameState(rows, cols)
            elif status == 'CONTENTS':
                contents: list[str] = []
                for _ in range(rows):
                    content: str = input().strip('\n')
                    if len(content) < cols:
                        content += ' ' * (cols - len(content))
                    contents.append(content[:cols])
                return GameState(rows, cols, contents)
            else:
                print("ERROR")
                return None
        else:
            pass
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
    