# The module for the game logic

# Name Boxuan Zhang
# Email boxuanz3@uci.edu
# Student ID 95535906


class GameState:
    def __init__(self, rows: int, cols: int, contents: list[str] = None) -> None:
        """
        Initialize the game state with the given rows, columns and contents.
        """
        self.rows = rows
        self.cols = cols
        self.field = Field(rows, cols, contents)
        self.faller = None
        self.game_over = False  # check the game status
        self.level_cleared = False  # check whether there is any viruses
        self.current_matches = set()  # track current matches


    def create_faller(self, color1: str, color2: str) -> None:
        """
        Create a new faller in the center of the second row.
        If the posititon is occupied, overlap and game over.
        """
        if self.faller is not None:
            return

        # Get middle column for the second row
        middle_cols = self.get_middle_cols(1)
        positions = [(1, c) for c in middle_cols]
        if len(positions) == 1:
            positions = [(1, middle_cols[0]), (1, middle_cols[0]+1)]

        if all(self.field.get_cell(r, c).content == 'empty' for (r, c) in positions):
            self.faller = Faller('horizontal', (color1, color2), 1, middle_cols[0])
        else:
            # overlap the faller, then the game over
            self.faller = Faller('horizontal', (color1, color2), 1, middle_cols[0])
            for idx, (r, c) in enumerate(positions):
                cell = self.field.get_cell(r, c)
                cell.content = 'capsule'
                cell.color = (color1, color2)[idx]
                cell.capsule_type = 'left' if idx == 0 else 'right'
            self.game_over = True


    def get_middle_cols(self, row: int) -> list[int]:
        """
        Return the middle column for a given row.
        """
        if self.cols % 2 == 1:
            return [self.cols // 2]
        return [self.cols // 2 - 1, self.cols // 2]


    def command(self, command: str) -> None:
        """
        Process a single game command for change the capsules status.
        A: Rotating clockwise
        B: Rotating counter clockwise
        <: Moving left
        >: Moving right
        """
        if command == 'A':
            self.rotate_clockwise()
        elif command == 'B':
            self.rotate_counter_clockwise()
        elif command == '<':
            self.move_left()
        elif command == '>':
            self.move_right()
        elif command.startswith('V'):
            parts = command.split()
            if len(parts) < 4:
                return
            try:
                row = int(parts[1])
                col = int(parts[2])
                color = parts[3]
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.field.add_virus(row, col, color)
            except (ValueError, IndexError):
                pass


    def rotate_clockwise(self) -> None:
        """
        Rotate the current faller clockwise.
        """
        if self.faller is None or self.faller.state != 'falling':
            return
        new_faller = self.faller.rotate_clockwise()
        if self.positions_available(new_faller.get_positions()):
            self.faller = new_faller
        else:
            new_faller.wall_kick_left()
            if self.positions_available(new_faller.get_positions()):
                self.faller = new_faller


    def rotate_counter_clockwise(self) -> None:
        """
        Rotate the current faller counter-clockwise.
        """
        if self.faller is None or self.faller.state != 'falling':
            return
        new_faller = self.faller.rotate_counter_clockwise()
        if self.positions_available(new_faller.get_positions()):
            self.faller = new_faller
        else:
            new_faller.wall_kick_left()
            if self.positions_available(new_faller.get_positions()):
                self.faller = new_faller


    def positions_available(self, positions: list[tuple[int, int]]) -> bool:
        """
        Check if all given positions are available for movement.
        """
        return all(
            0 <= r < self.rows and 0 <= c < self.cols and
            self.field.get_cell(r, c).content in ['empty', 'faller']
            for (r, c) in positions
        )


    def move_left(self) -> None:
        """
        Move the faller one column to the left if possible.
        """
        if self.faller is None or self.faller.state != 'falling':
            return
        new_col = self.faller.col - 1
        if new_col < 0:
            return
        positions = self.faller.get_positions_at_col(new_col)
        if self.positions_available(positions):
            self.faller.col = new_col


    def move_right(self) -> None:
        """
        Move the faller one column to the right if possible.
        """
        if self.faller is None or self.faller.state != 'falling':
            return
        new_col = self.faller.col + 1
        if new_col + (self.faller.orientation == 'horizontal') >= self.cols:
            return
        positions = self.faller.get_positions_at_col(new_col)
        if self.positions_available(positions):
            self.faller.col = new_col


    def time_step(self) -> None:
        """
        When user stress enter, the program will conduct time function
        The function time_step is modeling for the time passing
        """
        if self.game_over:
            return
        if self.faller is not None:
            if self.can_move_down():
                self.faller.row += 1
                self.faller.state = 'falling'
            else:
                self.faller.state = 'landed'
                self.freeze_faller()
                self.handle_matches_and_gravity()
        else:
            # Check if any capsule can fall
            gravity_needed = False
            for r in range(self.rows - 1):
                for c in range(self.cols):
                    cell = self.field.get_cell(r, c)
                    if cell.content == 'capsule':
                        # Check single capsule
                        if cell.capsule_type == 'single':
                            if self.field.get_cell(r + 1, c).content == 'empty':
                                gravity_needed = True
                        # Check vertical capsule
                        elif cell.capsule_type == 'bottom':
                            if r > 0:
                                top_cell = self.field.get_cell(r - 1, c)
                                if (top_cell.content == 'capsule' and top_cell.capsule_type == 'top' and
                                    self.field.get_cell(r + 1, c).content == 'empty'):
                                    gravity_needed = True
                        # Check horizontal capsule
                        elif cell.capsule_type == 'left' and c < self.cols - 1:
                            right_cell = self.field.get_cell(r, c + 1)
                            if (right_cell.content == 'capsule' and right_cell.capsule_type == 'right' and
                                self.field.get_cell(r + 1, c).content == 'empty' and 
                                self.field.get_cell(r + 1, c + 1).content == 'empty'):
                                gravity_needed = True
            
            if gravity_needed:
                self.field.apply_gravity()
            self.handle_matches_and_gravity()


    def can_move_down(self) -> bool:
        """
        Check if the current faller can move down by one row.
        """
        if self.faller is None:
            return False
        positions = self.faller.get_positions_below()
        return self.positions_available(positions)


    def freeze_faller(self) -> None:
        """
        Convert the current faller into fixed capsules in the field.
        """
        if self.faller is None:
            return
        positions = self.faller.get_positions()
        if self.faller.orientation == 'horizontal':
            left_pos, right_pos = positions
            left_cell = self.field.get_cell(*left_pos)
            right_cell = self.field.get_cell(*right_pos)
            left_cell.content = right_cell.content = 'capsule'
            left_cell.color, right_cell.color = self.faller.colors
            left_cell.capsule_type, right_cell.capsule_type = 'left', 'right'
        else:
            # For vertical orientation, positions[0] is bottom, positions[1] is top
            bottom_pos, top_pos = positions
            bottom_cell = self.field.get_cell(*bottom_pos)
            top_cell = self.field.get_cell(*top_pos)
            bottom_cell.content = top_cell.content = 'capsule'
            bottom_cell.color = self.faller.colors[0]  # bottom color
            top_cell.color = self.faller.colors[1]  # top color
            # Make both capsules independent
            bottom_cell.capsule_type = 'single'
            top_cell.capsule_type = 'single'
        self.faller = None


    def single_capsule_fall(self) -> None:
        """
        For single capsule fall automatically if the user stress time_step
        """
        for r in reversed(range(self.rows - 1)):
            for c in range(self.cols):
                cell = self.field.get_cell(r, c)
                if cell.content == 'capsule' and cell.capsule_type == 'single':
                    below = self.field.get_cell(r + 1, c)
                    if below.content == 'empty':
                        self.field.grid[r + 1][c], self.field.grid[r][c] = self.field.grid[r][c], self.field.grid[r + 1][c]


    def handle_matches_and_gravity(self) -> None:
        """
        1. check single capsule and let them fall once
        2. check whether there exists matches
        3. if matches, use *color*
        4. if *color*, remove all matches
        5. if any whole capsule can fall, apply gravity
        """
        matches = self.field.matches()
        if matches:
            if not self.current_matches:  # if new
                self.current_matches = matches  # save
            else:  # if old
                self.field.remove_matches(self.current_matches)  # remove
                self.current_matches = set()  # clear matches
        else:
            if not self.current_matches:
                pass


    def has_viruses(self) -> bool:
        """
        Check the stauts of the field
        """
        return any(
            self.field.get_cell(r, c).content == 'virus'
            for r in range(self.rows)
            for c in range(self.cols)
        )


class Field:
    def __init__(self, rows: int, cols: int, contents: list[str] = None) -> None:
        """
        Initialize the field grid rows, columns and contents
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        if contents is not None:
            self.initialize_from_contents(contents)


    def initialize_from_contents(self, contents: list[str]) -> None:
        """
        If the status is contents
        Initialize the field with the contents from user inputing
        """
        for r in range(self.rows):
            line = contents[r]
            for c in range(self.cols):
                char = line[c]
                cell = self.grid[r][c]
                if char == ' ':
                    cell.content = 'empty'
                elif char.islower():
                    cell.content = 'virus'
                    cell.color = char
                else:
                    cell.content = 'capsule'
                    cell.color = char
                    cell.capsule_type = 'single'


    def get_cell(self, row: int, col: int) -> 'Cell':
        """
        Return the Cell object at the specified row and column.
        """
        return self.grid[row][col]


    def add_virus(self, row: int, col: int, color: str) -> None:
        """
        Add a virus of the given color at the specified position.
        """
        cell = self.grid[row][col]
        if cell.content == 'empty':
            cell.content = 'virus'
            cell.color = color


    def can_capsule_fall(self, r: int, c: int, visited: set = None) -> bool:
        """
        Check if a capsule at the given position can fall.
        A capsule can fall if:
        1. The space below is empty
        2. The capsule below can fall
        3. The capsule below can merge with this capsule
        
        r: row position
        c: column position
        visited: set of visited positions to prevent infinite recursion
        """
        if visited is None:
            visited = set()
            
        if (r, c) in visited:
            return True  # prevent infinite recursion
            
        visited.add((r, c))
        
        if r + 1 >= self.rows:
            return False
            
        cell = self.grid[r][c]
        below = self.grid[r+1][c]
        
        if below.content == 'empty':
            return True
            
        if below.content == 'capsule':
            # For horizontal capsules, check both parts
            if below.capsule_type == 'left':
                if c + 1 >= self.cols:
                    return False
                right_below = self.grid[r+1][c+1]
                if right_below.content != 'capsule' or right_below.capsule_type != 'right':
                    return False
                # Both parts of horizontal capsule must be able to fall
                return (self.can_capsule_fall(r+1, c, visited) and 
                       self.can_capsule_fall(r+1, c+1, visited))
            elif below.capsule_type == 'right':
                if c - 1 < 0:
                    return False
                left_below = self.grid[r+1][c-1]
                if left_below.content != 'capsule' or left_below.capsule_type != 'left':
                    return False
                return (self.can_capsule_fall(r+1, c, visited) and 
                       self.can_capsule_fall(r+1, c-1, visited))
            # For vertical capsules, check the bottom part
            elif below.capsule_type == 'bottom':
                if r + 2 >= self.rows:
                    return False
                return self.can_capsule_fall(r+2, c, visited)
            # For single capsules or top parts, check recursively
            else:
                return self.can_capsule_fall(r+1, c, visited)
                
        return False


    def apply_gravity(self) -> bool:
        """
        Apply gravity to the field.
        Check horizontal, vertical and single capsules recursively.
        """
        changed = False
        # Process from bottom to top, right to left
        for r in reversed(range(self.rows - 1)):
            for c in reversed(range(self.cols)):
                cell = self.grid[r][c]
                if cell.content == 'capsule':
                    # Handle horizontal capsules
                    if cell.capsule_type == 'left':
                        if c + 1 < self.cols:
                            right_cell = self.grid[r][c+1]
                            if (right_cell.content == 'capsule' and right_cell.capsule_type == 'right' and
                                self.can_capsule_fall(r, c) and self.can_capsule_fall(r, c+1)):
                                self.grid[r+1][c] = cell
                                self.grid[r+1][c+1] = right_cell
                                self.grid[r][c] = Cell()
                                self.grid[r][c+1] = Cell()
                                changed = True
                    # Handle vertical capsules
                    elif cell.capsule_type == 'top':
                        if r + 1 < self.rows:
                            bottom_cell = self.grid[r+1][c]
                            if (bottom_cell.content == 'capsule' and bottom_cell.capsule_type == 'bottom' and
                                self.can_capsule_fall(r, c) and self.can_capsule_fall(r+1, c)):
                                self.grid[r+2][c] = bottom_cell
                                self.grid[r+1][c] = cell
                                self.grid[r][c] = Cell()
                                changed = True
                    # Handle single capsules
                    elif cell.capsule_type == 'single':
                        if self.can_capsule_fall(r, c):
                            self.grid[r+1][c] = cell
                            self.grid[r][c] = Cell()
                            changed = True
        return changed


    def matches(self) -> set[tuple[int, int]]:
        """
        Find all matches.
        Returns a set of matched cell positions.
        """
        matches = set()
        # horizontal match
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                start = c
                color = self.grid[r][c].color
                if color is None or self.grid[r][c].content not in ['capsule', 'virus']:
                    c += 1
                    continue
                # find continuous same color
                while (c < self.cols and
                       self.grid[r][c].color is not None and
                       self.grid[r][c].color.lower() == color.lower() and
                       self.grid[r][c].content in ['capsule', 'virus']):
                    c += 1
                length = c - start
                if length >= 4:
                    can_match = True
                    for i in range(start, c):
                        cell = self.grid[r][i]
                        if cell.content == 'capsule':
                            if cell.capsule_type == 'left' and i+1 < self.cols: # check left side
                                right_cell = self.grid[r][i+1]
                                if right_cell.content == 'capsule' and right_cell.capsule_type == 'right':
                                    if self.can_capsule_fall(r, i) and self.can_capsule_fall(r, i+1):
                                        can_match = False
                                        break
                            elif cell.capsule_type == 'right' and i-1 >= 0: # check right side
                                left_cell = self.grid[r][i-1]
                                if left_cell.content == 'capsule' and left_cell.capsule_type == 'left':
                                    if self.can_capsule_fall(r, i) and self.can_capsule_fall(r, i-1):
                                        can_match = False
                                        break
                            elif cell.capsule_type == 'single':
                                # check single
                                if self.can_capsule_fall(r, i):
                                    can_match = False
                                    break
                            elif cell.capsule_type != 'right':
                                if self.can_capsule_fall(r, i):
                                    can_match = False
                                    break
                    if can_match:
                        matches.update((r, i) for i in range(start, c))
        # vertical match
        for c in range(self.cols):
            r = 0
            while r < self.rows:
                start = r
                color = self.grid[r][c].color
                if color is None or self.grid[r][c].content not in ['capsule', 'virus']:
                    r += 1
                    continue
                while (r < self.rows and
                       self.grid[r][c].color is not None and
                       self.grid[r][c].color.lower() == color.lower() and
                       self.grid[r][c].content in ['capsule', 'virus']):
                    r += 1
                length = r - start
                if length >= 4:
                    matches.update((i, c) for i in range(start, r))
        return matches


    def remove_matches(self, matches: set[tuple[int, int]]) -> None:
        """
        Remove all matched cells from the field and update capsule types.
        """
        for (r, c) in matches:
            cell = self.grid[r][c]
            if cell.content == 'capsule':
                # Check if this is part of a horizontal capsule
                if cell.capsule_type == 'left':
                    # Check if right part is not matched
                    if c + 1 < self.cols and (r, c + 1) not in matches:
                        right_cell = self.grid[r][c + 1]
                        if right_cell.capsule_type == 'right':
                            # Convert right part to single capsule
                            right_cell.capsule_type = 'single'
                elif cell.capsule_type == 'right':
                    # Check if left part is not matched
                    if c - 1 >= 0 and (r, c - 1) not in matches:
                        left_cell = self.grid[r][c - 1]
                        if left_cell.capsule_type == 'left':
                            # Convert left part to single capsule
                            left_cell.capsule_type = 'single'
                elif cell.capsule_type == 'top':
                    # Check if bottom part is not matched
                    if r + 1 < self.rows and (r + 1, c) not in matches:
                        bottom_cell = self.grid[r + 1][c]
                        if bottom_cell.capsule_type == 'bottom':
                            # Convert bottom part to single capsule
                            bottom_cell.capsule_type = 'single'
                elif cell.capsule_type == 'bottom':
                    # Check if top part is not matched
                    if r - 1 >= 0 and (r - 1, c) not in matches:
                        top_cell = self.grid[r - 1][c]
                        if top_cell.capsule_type == 'top':
                            # Convert top part to single capsule
                            top_cell.capsule_type = 'single'
            # Clear the matched cell
            cell.content = 'empty'
            cell.color = None
            cell.capsule_type = None


class Cell:
    def __init__(self) -> None:
        """
        Initialize a cell as empty with no color or capsule type.
        Used for all field grid positions.
        """
        self.content = 'empty'
        self.color = None
        self.capsule_type = None
        self.state = 'empty'


class Faller:
    def __init__(self, orientation: str, colors: tuple[str, str], row: int, col: int) -> None:
        """
        Initialize a new faller with orientation, colors, and position.
        Used for falling capsule logic.
        """
        self.orientation = orientation
        self.colors = colors
        self.row = row
        self.col = col
        self.state = 'falling'


    def rotate_counter_clockwise(self) -> 'Faller':
        """
        Return a new Faller rotated counter-clockwise from the current orientation.
        """
        if self.orientation == 'horizontal':
            return Faller('vertical', (self.colors[0], self.colors[1]), self.row, self.col)
        else:
            return Faller('horizontal', (self.colors[1], self.colors[0]), self.row, self.col)


    def rotate_clockwise(self) -> 'Faller':
        """
        Return a new Faller rotated clockwise from the current orientation.
        """
        if self.orientation == 'horizontal':
            return Faller('vertical', (self.colors[1], self.colors[0]), self.row, self.col)
        else:
            return Faller('horizontal', (self.colors[0], self.colors[1]), self.row, self.col)


    def wall_kick_left(self) -> None:
        """
        Move the faller one column to the left for wall kick during rotation.
        """
        self.col -= 1


    def get_positions(self) -> list[tuple[int, int]]:
        """
        Return a list of positions occupied by the faller.
        Depends on orientation and current position.
        """
        if self.orientation == 'horizontal':
            return [(self.row, self.col), (self.row, self.col + 1)]
        # For vertical orientation, return positions in order: bottom, top
        return [(self.row, self.col), (self.row - 1, self.col)]


    def get_positions_below(self) -> list[tuple[int, int]]:
        """
        Return a list of positions directly below the faller.
        Used to check if the faller can move down.
        """
        positions = self.get_positions()
        # For vertical orientation, only check the bottom position
        if self.orientation == 'vertical':
            return [(positions[0][0] + 1, positions[0][1])]
        return [(r + 1, c) for (r, c) in positions]


    def get_positions_at_col(self, new_col: int) -> list[tuple[int, int]]:
        """
        Return a list of positions the faller would occupy at a new column.
        """
        if self.orientation == 'horizontal':
            return [(self.row, new_col), (self.row, new_col + 1)]
        # For vertical orientation, maintain the same order as get_positions
        return [(self.row, new_col), (self.row - 1, new_col)]
    