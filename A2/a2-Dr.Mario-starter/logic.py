class GameState:
    def __init__(self, rows: int, cols: int, contents: list[str] = None) -> None:
        self.rows = rows
        self.cols = cols
        self.field = Field(rows, cols, contents)
        self.faller = None
        self.game_over = False  # check the game status
        self.level_cleared = False  # check whether there is any viruses
        self.current_matches = set()  # track current matches


    def create_faller(self, color1: str, color2: str) -> None:
        """Create a new faller if possible."""
        if self.faller is not None:
            return

        # Get middle column for the second row
        middle_cols = self.get_middle_cols(1)
        positions = [(1, c) for c in middle_cols]
        if len(positions) == 1:
            positions = [(1, middle_cols[0]), (1, middle_cols[0]+1)]

        # Check if middle positions are available
        if all(self.field.get_cell(r, c).content == 'empty' for (r, c) in positions):
            self.faller = Faller('horizontal', (color1, color2), 1, middle_cols[0])
        else:
            # If middle positions are not available, game over
            self.game_over = True


    def get_middle_cols(self, row: int) -> list[int]:
        """Get the middle column(s) for a given row."""
        if self.cols % 2 == 1:
            return [self.cols // 2]
        return [self.cols // 2 - 1, self.cols // 2]


    def command(self, command: str) -> None:
        """Process a game command."""
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
        """Rotate the faller clockwise."""
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
        """Rotate the faller counter-clockwise."""
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
        """Check if all positions are available."""
        return all(
            0 <= r < self.rows and 0 <= c < self.cols and
            self.field.get_cell(r, c).content in ['empty', 'faller']
            for (r, c) in positions
        )


    def move_left(self) -> None:
        """Move the faller left."""
        if self.faller is None or self.faller.state != 'falling':
            return
        new_col = self.faller.col - 1
        if new_col < 0:
            return
        positions = self.faller.get_positions_at_col(new_col)
        if self.positions_available(positions):
            self.faller.col = new_col


    def move_right(self) -> None:
        """Move the faller right."""
        if self.faller is None or self.faller.state != 'falling':
            return
        new_col = self.faller.col + 1
        if new_col + (self.faller.orientation == 'horizontal') >= self.cols:
            return
        positions = self.faller.get_positions_at_col(new_col)
        if self.positions_available(positions):
            self.faller.col = new_col


    def time_step(self) -> None:
        """Advance the game by one time step."""
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
            self.handle_matches_and_gravity()


    def can_move_down(self) -> bool:
        """Check if the faller can move down."""
        if self.faller is None:
            return False
        positions = self.faller.get_positions_below()
        return self.positions_available(positions)


    def freeze_faller(self) -> None:
        """Freeze the faller in place."""
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
            bottom_cell.color = self.faller.colors[0]  # Bottom color
            top_cell.color = self.faller.colors[1]  # Top color
            bottom_cell.capsule_type = 'bottom'
            top_cell.capsule_type = 'top'
        self.faller = None


    def handle_matches_and_gravity(self) -> None:
        """Handle matches and apply gravity."""
        matches = self.field.find_matches()
        if matches:
            if not self.current_matches:  # if new matches
                self.current_matches = matches  # save
            else:  # if show matches
                self.field.remove_matches(self.current_matches)  # remove previous
                self.current_matches = set()  # remove the matches element
        else:
            if not self.current_matches:  # if not matches
                self.field.apply_gravity()  # only gravity


    def has_viruses(self) -> bool:
        """Check if there are any viruses remaining."""
        return any(
            self.field.get_cell(r, c).content == 'virus'
            for r in range(self.rows)
            for c in range(self.cols)
        )


class Field:
    def __init__(self, rows: int, cols: int, contents: list[str] = None) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        if contents is not None:
            self.initialize_from_contents(contents)


    def initialize_from_contents(self, contents: list[str]) -> None:
        """Initialize the field from contents."""
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
        """Get the cell at the specified position."""
        return self.grid[row][col]


    def add_virus(self, row: int, col: int, color: str) -> None:
        """Add a virus at the specified position."""
        cell = self.grid[row][col]
        if cell.content == 'empty':
            cell.content = 'virus'
            cell.color = color


    def apply_gravity(self) -> bool:
        """Apply gravity to the field."""
        changed = False
        for r in reversed(range(self.rows - 1)):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.content == 'capsule':
                    if cell.capsule_type == 'single':
                        # Move single capsule down if possible
                        if self.grid[r+1][c].content == 'empty':
                            self.grid[r+1][c], self.grid[r][c] = self.grid[r][c], self.grid[r+1][c]
                            changed = True
                    elif cell.capsule_type == 'bottom':
                        # Move bottom part down if possible
                        if r + 1 < self.rows and self.grid[r+1][c].content == 'empty':
                            # Find the top part
                            if r > 0 and self.grid[r-1][c].content == 'capsule' and self.grid[r-1][c].capsule_type == 'top':
                                # Move both parts down
                                self.grid[r+1][c] = cell  # Move bottom part down
                                self.grid[r][c] = self.grid[r-1][c]  # Move top part down
                                self.grid[r-1][c] = Cell()  # Clear old top position
                                changed = True
                            else:  # If no top part found, treat as single
                                self.grid[r+1][c], self.grid[r][c] = self.grid[r][c], self.grid[r+1][c]
                                changed = True
                    elif cell.capsule_type == 'top':
                        # Check if both parts can move down
                        if r + 1 < self.rows and self.grid[r+1][c].content == 'capsule' and self.grid[r+1][c].capsule_type == 'bottom':
                            if r + 2 < self.rows and self.grid[r+2][c].content == 'empty':
                                # Move both parts down
                                self.grid[r+2][c] = self.grid[r+1][c]  # Move bottom part down
                                self.grid[r+1][c] = cell  # Move top part down
                                self.grid[r][c] = Cell()  # Clear old top position
                                changed = True
        return changed


    def find_matches(self) -> set[tuple[int, int]]:
        """Find all matches in the field."""
        matches = set()
        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                color = self.grid[r][c].color
                if color is None or self.grid[r][c].content not in ['capsule', 'virus']:
                    continue
                if all(self.grid[r][c+i].color is not None and
                       self.grid[r][c+i].color.lower() == color.lower() and
                       self.grid[r][c+i].content in ['capsule', 'virus']
                       for i in range(4)):
                    matches.update((r, c+i) for i in range(4))
        # Vertical
        for r in range(self.rows - 3):
            for c in range(self.cols):
                color = self.grid[r][c].color
                if color is None or self.grid[r][c].content not in ['capsule', 'virus']:
                    continue
                if all(self.grid[r+i][c].color is not None and
                       self.grid[r+i][c].color.lower() == color.lower() and
                       self.grid[r+i][c].content in ['capsule', 'virus']
                       for i in range(4)):
                    matches.update((r+i, c) for i in range(4))
        return matches


    def remove_matches(self, matches: set[tuple[int, int]]) -> None:
        """Remove all matched cells and handle remaining capsule parts."""
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
        self.content = 'empty'
        self.color = None
        self.capsule_type = None


class Faller:
    def __init__(self, orientation: str, colors: tuple[str, str], row: int, col: int) -> None:
        self.orientation = orientation
        self.colors = colors
        self.row = row
        self.col = col
        self.state = 'falling'


    def rotate_clockwise(self) -> 'Faller':
        """Rotate the faller clockwise."""
        if self.orientation == 'horizontal':
            return Faller('vertical', self.colors, self.row, self.col)
        return Faller('horizontal', self.colors, self.row, self.col)


    def rotate_counter_clockwise(self) -> 'Faller':
        """Rotate the faller counter clockwise."""
        if self.orientation == 'horizontal':
            return Faller('vertical', (self.colors[1], self.colors[0]), self.row, self.col)
        return Faller('horizontal', (self.colors[1], self.colors[0]), self.row, self.col)


    def wall_kick_left(self) -> None:
        """If the faller is close to the wall, move left automatically to conduct rotate"""
        self.col -= 1


    def get_positions(self) -> list[tuple[int, int]]:
        """Get the positions occupied by the faller"""
        if self.orientation == 'horizontal':
            return [(self.row, self.col), (self.row, self.col + 1)]
        # For vertical orientation, return positions in order: bottom, top
        return [(self.row, self.col), (self.row - 1, self.col)]


    def get_positions_below(self) -> list[tuple[int, int]]:
        """Get the positions below the faller"""
        positions = self.get_positions()
        # For vertical orientation, only check the bottom position
        if self.orientation == 'vertical':
            return [(positions[0][0] + 1, positions[0][1])]
        return [(r + 1, c) for (r, c) in positions]


    def get_positions_at_col(self, new_col: int) -> list[tuple[int, int]]:
        """Get the positions at a new column"""
        if self.orientation == 'horizontal':
            return [(self.row, new_col), (self.row, new_col + 1)]
        # For vertical orientation, maintain the same order as get_positions
        return [(self.row, new_col), (self.row - 1, new_col)]
    