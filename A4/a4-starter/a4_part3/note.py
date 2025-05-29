from pathlib import Path

class Note:
    def __init__(self, note_path:Path):
        # create path obj to notes storage file
        if not note_path.exists():
            raise FileNotFoundError("The Note file specified in note_path does not exist.")
        self.note_path = note_path
        self.all_notes = []
        # file exists, so load all notes into the all_notes list
        self._load_notes()

    def _is_int(self, val):
        try:
            int(val)
            return True
        except ValueError:
            return False
    
    def _load_notes(self):
        """
        Load all notes into memory
        """
        f = self.note_path.open()
        self.all_notes = f.readlines()
        f.close()
    
    def _save_notes(self):
        """
        Save all notes in memory to file
        """
        f = self.note_path.open('w')
        for n in self.all_notes:
            f.write(n)
        f.close()

    def save_note(self, note: str):
        """
        adds the value passed to the note parameter to the all_notes list. Saves to file
        """
        # if note is empty, do nothing
        if len(note) == 0:
            return
        
        # add note to list, with new line
        self.all_notes.append(note + '\n')
        # resave all note to file
        self._save_notes()

    def read_notes(self) -> list[str]:
        """
        returns the list of current notes stored in memory
        """
        return self.all_notes

    def remove_note(self, noteid:int) -> str:
        """
        remove a note from the notes file.

        :param noteid: the 0-based index of the note stored in the list returned by read_notes method

        :return: the note removed or empty string if not not found
        """
        removed_note = ""

        # assign note to be removed to return variable and remove it from list
        try:
            removed_note = self.all_notes.pop(noteid)
        except IndexError:
            # handle exception and pass, empty string will be returned
            pass
        else:
            # only save if note removal succeeds
            self._save_notes()

        return removed_note
