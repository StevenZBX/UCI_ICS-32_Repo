import shlex

class TextUI:
    def __init__(self, game_state):
        self.game_state = game_state

    def run(self):
        while True:
            self.display_field()
            if self.game_state.game_over:
                print("GAME OVER")
                break
            if not self.game_state.has_viruses():
                print("LEVEL CLEARED")
            try:
                line = input()
                command = line.strip()
                if command == 'Q':
                    break
                self.process_command(command)
            except EOFError:
                break

    def display_field(self):
        for r in range(self.game_state.rows):
            row = ['|']
            for c in range(self.game_state.cols):
                cell = self.game_state.field.get_cell(r, c)
                faller = self.game_state.faller
                is_faller = False
                faller_positions = []
                if faller is not None:
                    faller_positions = faller.get_positions()
                if (r, c) in faller_positions:
                    is_faller = True
                    if faller.state == 'falling':
                        if faller.orientation == 'horizontal':
                            if c == faller.col:
                                row.append(f'[{cell.color}-')
                            else:
                                row.append(f'-{cell.color}]')
                        else:
                            row.append(f'[{cell.color}]')
                    else:
                        if faller.orientation == 'horizontal':
                            if c == faller.col:
                                row.append(f'|{cell.color}-')
                            else:
                                row.append(f'-{cell.color}|')
                        else:
                            row.append(f'|{cell.color}|')
                else:
                    if cell.content == 'empty':
                        row.append('   ')
                    elif cell.content == 'virus':
                        row.append(f' {cell.color} ')
                    elif cell.content == 'capsule':
                        row.append(f' {cell.color} ')
            row.append('|')
            print(''.join(row))
        print(f' {"-" * (3 * self.game_state.cols)} ')

    def process_command(self, command_str):
        parts = shlex.split(command_str)
        if not parts:
            self.game_state.time_step()
            return
        cmd = parts[0]
        if cmd == 'F':
            if len(parts) != 3:
                return
            color1, color2 = parts[1], parts[2]
            self.game_state.create_faller(color1, color2)
            top_middle = self.game_state.get_middle_cols(0)
            for c in top_middle:
                cell = self.game_state.field.get_cell(0, c)
                if cell.content == 'capsule':
                    self.game_state.game_over = True
        elif cmd in ['A', 'B', '<', '>']:
            self.game_state.process_command(cmd)
        elif cmd == 'V':
            if len(parts) < 4:
                return
            try:
                row = int(parts[1])
                col = int(parts[2])
                color = parts[3]
                self.game_state.field.add_virus(row, col, color)
            except:
                pass