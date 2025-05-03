class GameState:
    def __init__(self, rows, cols, contents=None):
        self.rows = rows
        self.cols = cols
        self.field = Field(rows, cols, contents)
        self.faller = None
        self.game_over = False
        self.level_cleared = False

    def create_faller(self, color1, color2):
        if self.faller is not None:
            return
        top_middle_cols = self.get_middle_cols(0)
        for c in top_middle_cols:
            cell = self.field.get_cell(0, c)
            if cell.content == 'capsule':
                self.game_over = True
                return
        middle_cols = self.get_middle_cols(1)
        positions = [(1, c) for c in middle_cols]
        if len(positions) == 1:
            positions = [(1, middle_cols[0]), (1, middle_cols[0]+1)]
        available = all(self.field.get_cell(r, c).content == 'empty' for (r, c) in positions)
        if available:
            self.faller = Faller('horizontal', (color1, color2), 1, middle_cols[0])

    def get_middle_cols(self, row):
        if self.cols % 2 == 1:
            mid = self.cols // 2
            return [mid]
        else:
            mid = self.cols // 2 - 1
            return [mid, mid + 1]

    def process_command(self, command):
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
            row = int(parts[1])
            col = int(parts[2])
            color = parts[3]
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.field.add_virus(row, col, color)

    def rotate_clockwise(self):
        if self.faller is None or self.faller.state != 'falling':
            return
        new_faller = self.faller.rotate_clockwise()
        if self.positions_available(new_faller.get_positions()):
            self.faller = new_faller
        else:
            new_faller.wall_kick_left()
            if self.positions_available(new_faller.get_positions()):
                self.faller = new_faller

    def rotate_counter_clockwise(self):
        if self.faller is None or self.faller.state != 'falling':
            return
        new_faller = self.faller.rotate_counter_clockwise()
        if self.positions_available(new_faller.get_positions()):
            self.faller = new_faller
        else:
            new_faller.wall_kick_left()
            if self.positions_available(new_faller.get_positions()):
                self.faller = new_faller

    def positions_available(self, positions):
        for (r, c) in positions:
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                return False
            cell = self.field.get_cell(r, c)
            if cell.content not in ['empty', 'faller']:
                return False
        return True

    def move_left(self):
        if self.faller is None or self.faller.state != 'falling':
            return
        new_col = self.faller.col - 1
        if new_col < 0:
            return
        positions = self.faller.get_positions_at_col(new_col)
        if self.positions_available(positions):
            self.faller.col = new_col

    def move_right(self):
        if self.faller is None or self.faller.state != 'falling':
            return
        new_col = self.faller.col + 1
        if new_col + (self.faller.orientation == 'horizontal') >= self.cols:
            return
        positions = self.faller.get_positions_at_col(new_col)
        if self.positions_available(positions):
            self.faller.col = new_col

    def time_step(self):
        if self.game_over:
            return
        if self.faller is not None:
            if self.faller.state == 'falling':
                if self.can_move_down():
                    self.faller.row += 1
                else:
                    self.faller.state = 'landed'
            elif self.faller.state == 'landed':
                self.freeze_faller()
                self.handle_matches_and_gravity()
                if self.faller is not None and self.faller.state == 'frozen':
                    self.faller = None
        else:
            self.handle_matches_and_gravity()

    def can_move_down(self):
        positions = self.faller.get_positions_below()
        return self.positions_available(positions)

    def freeze_faller(self):
        positions = self.faller.get_positions()
        for (r, c) in positions:
            cell = self.field.get_cell(r, c)
            cell.content = 'capsule'
            cell.color = self.faller.colors[0] if (r == self.faller.row and c == self.faller.col) else self.faller.colors[1]
            cell.capsule_type = 'single'
        self.faller = None

    def handle_matches_and_gravity(self):
        changed = True
        while changed:
            changed = self.field.apply_gravity()
            matches = self.field.find_matches()
            if matches:
                self.field.remove_matches(matches)
                changed = True

    def has_viruses(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.field.get_cell(r, c).content == 'virus':
                    return True
        return False

class Field:
    def __init__(self, rows, cols, contents=None):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        if contents is not None:
            for r in range(rows):
                line = contents[r]
                for c in range(cols):
                    char = line[c]
                    if char == ' ':
                        self.grid[r][c].content = 'empty'
                    elif char.islower():
                        self.grid[r][c].content = 'virus'
                        self.grid[r][c].color = char
                    else:
                        self.grid[r][c].content = 'capsule'
                        self.grid[r][c].color = char
                        self.grid[r][c].capsule_type = 'single'

    def get_cell(self, row, col):
        return self.grid[row][col]

    def add_virus(self, row, col, color):
        cell = self.grid[row][col]
        if cell.content == 'empty':
            cell.content = 'virus'
            cell.color = color

    def apply_gravity(self):
        changed = False
        for r in reversed(range(self.rows - 1)):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.content == 'capsule' and cell.capsule_type == 'single':
                    below = self.grid[r+1][c]
                    if below.content == 'empty':
                        self.grid[r+1][c], self.grid[r][c] = self.grid[r][c], self.grid[r+1][c]
                        changed = True
        return changed

    def find_matches(self):
        matches = set()
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.grid[r][c].color
                if color is None:
                    continue
                horizontal = set()
                vertical = set()
                for i in range(c, self.cols):
                    if self.grid[r][i].color == color and self.grid[r][i].content in ['capsule', 'virus']:
                        horizontal.add((r, i))
                    else:
                        break
                for i in range(r, self.rows):
                    if self.grid[i][c].color == color and self.grid[i][c].content in ['capsule', 'virus']:
                        vertical.add((i, c))
                    else:
                        break
                if len(horizontal) >= 4:
                    matches.update(horizontal)
                if len(vertical) >= 4:
                    matches.update(vertical)
        return matches

    def remove_matches(self, matches):
        for (r, c) in matches:
            self.grid[r][c].content = 'empty'
            self.grid[r][c].color = None
            self.grid[r][c].capsule_type = None

class Cell:
    def __init__(self):
        self.content = 'empty'
        self.color = None
        self.capsule_type = None

class Faller:
    def __init__(self, orientation, colors, row, col):
        self.orientation = orientation
        self.colors = colors
        self.row = row
        self.col = col
        self.state = 'falling'

    def rotate_clockwise(self):
        if self.orientation == 'horizontal':
            new_orientation = 'vertical'
            new_colors = (self.colors[0], self.colors[1])
            return Faller(new_orientation, new_colors, self.row, self.col)
        else:
            new_orientation = 'horizontal'
            new_colors = (self.colors[0], self.colors[1])
            return Faller(new_orientation, new_colors, self.row, self.col)

    def rotate_counter_clockwise(self):
        if self.orientation == 'horizontal':
            new_orientation = 'vertical'
            new_colors = (self.colors[1], self.colors[0])
            return Faller(new_orientation, new_colors, self.row, self.col)
        else:
            new_orientation = 'horizontal'
            new_colors = (self.colors[1], self.colors[0])
            return Faller(new_orientation, new_colors, self.row, self.col)

    def wall_kick_left(self):
        self.col -= 1

    def get_positions(self):
        if self.orientation == 'horizontal':
            return [(self.row, self.col), (self.row, self.col + 1)]
        else:
            return [(self.row, self.col), (self.row - 1, self.col)]

    def get_positions_below(self):
        positions = self.get_positions()
        return [(r + 1, c) for (r, c) in positions]

    def get_positions_at_col(self, new_col):
        if self.orientation == 'horizontal':
            return [(self.row, new_col), (self.row, new_col + 1)]
        else:
            return [(self.row, new_col), (self.row - 1, new_col)]
