# The module for displaying the game field

# Name Boxuan Zhang
# Email boxuanz3@uci.edu
# Student ID 95535906


import shlex
from logic import GameState


class TextUI:
    def __init__(self, game_state: GameState) -> None:
        """
        Initialize the text with game state (True or False).
        Prepares the game field for user to interact and display.
        """
        self.game_state = game_state


    def run(self) -> None:
        """
        Main game loop for user.
        Processing input, output, and updating the game status.
        """
        # check whether the cells in the field are matched
        self.game_state.current_matches = self.find_matches()
        while True:
            self.display_field()
            if self.game_state.game_over:
                print("GAME OVER")
                break
            if not self.game_state.has_viruses():
                print("LEVEL CLEARED")
            try:
                user = input().strip()
                if user == 'Q':
                    break
                self.process_command(user)
            except EOFError:
                break


    def find_matches(self) -> set[tuple[int, int]]:
        """
        Find all 4 matches in the current field.
        Returns a set of positions of mached elements.
        """
        matches = set()
        # Check horizontal matches
        for r in range(self.game_state.rows):
            for c in range(self.game_state.cols - 3):
                color = self.game_state.field.get_cell(r, c).color
                if color is None:
                    continue
                if all(self.game_state.field.get_cell(r, c+i).color and 
                      self.game_state.field.get_cell(r, c+i).color.upper() == color.upper() 
                      for i in range(4)):
                    matches.update((r, c+i) for i in range(4))
        # Check vertical matches
        for r in range(self.game_state.rows - 3):
            for c in range(self.game_state.cols):
                color = self.game_state.field.get_cell(r, c).color
                if color is None:
                    continue
                if all(self.game_state.field.get_cell(r+i, c).color and 
                      self.game_state.field.get_cell(r+i, c).color.upper() == color.upper() 
                      for i in range(4)):
                    matches.update((r+i, c) for i in range(4))
        return matches


    def display_field(self) -> None:
        """
        Print the current game field with capsules and viruses
        """
        matches = self.game_state.current_matches
        for r in range(self.game_state.rows):
            row = ['|']
            for c in range(self.game_state.cols):
                cell = self.game_state.field.get_cell(r, c)
                faller = self.game_state.faller
                faller_positions = faller.get_positions() if faller is not None else []
                if (r, c) in faller_positions:
                    if self.game_state.can_move_down():
                        # Falling state: use [color]
                        if faller.orientation == 'horizontal':
                            if c == faller.col:
                                color = faller.colors[0]
                                row.append(f'[{color}-')
                            else:
                                color = faller.colors[1]
                                row.append(f'-{color}]')
                        else:
                            if r == faller.row:
                                color = faller.colors[0]
                            else:
                                color = faller.colors[1]
                            row.append(f'[{color}]')
                    else:  # Landed state: use |color|
                        if faller.orientation == 'horizontal':
                            if c == faller.col:
                                color = faller.colors[0]
                                row.append(f'|{color}-')
                            else:
                                color = faller.colors[1]
                                row.append(f'-{color}|')
                        else:
                            if r == faller.row:
                                color = faller.colors[0]
                            else:
                                color = faller.colors[1]
                            row.append(f'|{color}|')
                else:
                    if (r, c) in matches: # if matches, the status will become *color* and wait for the user stress enter
                        color = cell.color.lower() if cell.content == 'virus' else cell.color
                        row.append(f'*{color}*')
                    elif cell.content == 'empty':
                        row.append('   ')
                    elif cell.content == 'virus': # virus display the color with lower letter
                        row.append(f' {cell.color.lower()} ')
                    elif cell.content == 'capsule':
                        if cell.capsule_type == 'left':
                            row.append(f' {cell.color}-')
                        elif cell.capsule_type == 'right':
                            row.append(f'-{cell.color} ')
                        elif cell.capsule_type in ['top', 'bottom']:
                            row.append(f' {cell.color} ')
                        else:
                            row.append(f' {cell.color} ')
            row.append('|')
            print(''.join(row))
        print(f" {'-' * (3 * self.game_state.cols)} ")


    def process_command(self, user: str) -> None:
        """
        Process a user command string.
        Conducting faller creation, movement, rotation, and virus addition.
        """
        user_input = shlex.split(user)
        valid_command = ['F', 'A', 'B', 'V', '<', '>']
        valid_colors = ['R', 'B', 'Y']
        if not user_input:
            self.game_state.time_step()
            return
        if user_input[0] in valid_command:
            if user_input[0] == 'F':
                if len(user_input) != 3:
                    return
                color1, color2 = user_input[1], user_input[2]
                if color1 not in valid_colors or color2 not in valid_colors:
                    return
                self.game_state.create_faller(color1, color2)
                top_middle = self.game_state.get_middle_cols(0)
                for c in top_middle:
                    cell = self.game_state.field.get_cell(0, c)
                    if cell.content == 'capsule':
                        self.game_state.game_over = True
            elif user_input[0] in ['A', 'B', '<', '>']:
                self.game_state.command(user_input[0])
            elif user_input[0] == 'V':
                if len(user_input) < 4:
                    return
                try:
                    row: int = int(user_input[1])
                    col: int = int(user_input[2])
                    color: str = user_input[3]
                    if color not in valid_colors:
                        return
                    # create the virus obejct
                    self.game_state.field.add_virus(row, col, color)
                    # add virus and check matches
                    self.game_state.current_matches = self.find_matches()
                except (ValueError, IndexError):
                    pass
        else:
            return
