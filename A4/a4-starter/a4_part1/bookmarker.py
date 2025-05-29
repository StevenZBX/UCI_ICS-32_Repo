from pathlib import Path
from note import Note
import webbrowser

class Bookmarker(Note):

    def __init__(self, note_path: Path):
        super().__init__(note_path)

    def add(self, url: str):
        """
        add a url to bookmark

        :param url: a valid url, must begin with http

        :raises ValueError: raised if url parameter does not start with http
        """
        # perform some lightweight validation checking.
        # Note, this is quite simplistic, but reinforces why inheritance
        # can be useful. We are reusing the save_note code, while introducing
        # custom operations that meet the needs of our program.
        if url.startswith("http"):
            self.save_note(url)
        else:
            raise ValueError(
                       "The value assigned to the url parameter is not valid.")

    def remove_by_url(self, url:str):
        """
        attempt to remove a url from bookmarks.
        If bookmark is not found, operation is ignored

        :param url: a valid url, must begin with http
        """
        id = -1

        # attempt to remove by index, if exception, ignore.
        # ignore here is a design decision, but is it the right one?
        # Perhaps a raised ValueError would be more useful,
        # but that would require the calling code to handle the exception.
        # What would you do?
        try:
            id = self.all_notes.index(url)
        except ValueError:
            pass
        else:
            self.remove_note(id)

    def remove_by_id(self, url_id:str):
        """
        removes the url in all_notes associated with to the url_id parameter
        in the local system's default browser

        :param url_id: the index of the url to open
        """

        if self._is_int(url_id):
            id = int(url_id)
            self.remove_note(id)

    def find(self, keyword:str) -> list[str]:
        """
        given a search parameter, attempts to find a list of matching urls.

        :param keyword: the word or words to use for search

        :returns list: a list of url's that contain the words
        assigned to the keyword param
        """
        results = [x for x in self.all_notes if keyword in x]
        return results

    def open(self, url_id:str):
        """
        opens the url in all_notes associated with to the url_id parameter
        in the local system's default browser

        :param url_id: the index of the url to open
        """
        if self._is_int(url_id):
            id = int(url_id)
            url = self.all_notes[id]
            webbrowser.open(url)
        else:
            raise ValueError("The url_id does not match a valid bookmark")
