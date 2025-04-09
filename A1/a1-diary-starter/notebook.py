# ICS 32
# Assignment #1: Diary
#
# Author: Aaron Imani
#
# v0.1.0

# You should review this code to identify what features you need to support
# in your program for assignment 1.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE 
# RIGHT NOW, though can you certainly take a look at it if you are curious since we 
# already covered a bit of the JSON format in class.

import json, time
from pathlib import Path
from typing import Union

class NotebookFileError(Exception):
    """
    NotebookFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Notebook objects to file the system.
    """
    pass

class IncorrectNotebookError(Exception):
    """
    NotebookError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a notebook file to a Notebook object.
    """
    pass


class Diary(dict):
    """ 

    The Diary class is responsible for working with individual user diaries. It currently 
    supports two features: A timestamp property that is set upon instantiation and 
    when the entry object is set and an entry property that stores the diary message.

    """
    def __init__(self, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Diary properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and 
    time values. When the value for entry is changed, or set, the timestamp field is 
    updated to the current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)
    
    
class Notebook:
    """Notebook is a class that can be used to manage a diary notebook."""

    def __init__(self, username: str, password: str, bio: str):
        """Creates a new Notebook object. 
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            bio (str): The bio of the user.
        """
        self.username = username 
        self.password = password 
        self.bio = bio 
        self._diaries = []
    

    def add_diary(self, diary: Diary) -> None:
        """Accepts a Diary object as parameter and appends it to the diary list. Diaries 
        are stored in a list object in the order they are added. So if multiple Diary objects 
        are created, but added to the Profile in a different order, it is possible for the 
        list to not be sorted by the Diary.timestamp property. So take caution as to how you 
        implement your add_diary code.

        """
        self._diaries.append(diary)


    def del_diary(self, index: int) -> bool:
        """
        Removes a Diary at a given index and returns `True` if successful and `False` if an invalid index was supplied. 

        To determine which diary to delete you must implement your own search operation on 
        the diary returned from the get_diaries function to find the correct index.

        """
        try:
            del self._diaries[index]
            return True
        except IndexError:
            return False
        
    def get_diaries(self) -> list[Diary]:
        """Returns the list object containing all diaries that have been added to the Notebook object"""
        return self._diaries

    def save(self, path: Union[str, Path]) -> None:
        """
        Accepts a path to create and store a notebook file. 

        Arguments:
          path: The full path to create the notebook file. The path must include `.json` in the end.

        Example usage:
        
        ```
        notebook = Notebook('jo)
        notebook.save('/path/to/file.json')
        ```

        Raises NotebookFileError, IncorrectNotebookError
        """
        if isinstance(path, Path):
            p = path
        else:
            p = Path(path)

        if p.parent.exists() and p.suffix == '.json':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f, indent=4)
                f.close()
            except Exception as ex:
                raise NotebookFileError("Error while attempting to process the notebook file.", ex)
        else:
            raise NotebookFileError("Invalid notebook file path or type")

    def load(self, path: str) -> None:
        """
        Populates the current instance of Notebook with data stored in a notebook file.

        Example usage: 

        ```
        notebook = Notebook()
        notebook.load('/path/to/file.json')
        ```

        Raises NotebookFileError, IncorrectNotebookError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.json':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.bio = obj['bio']
                for diary_obj in obj['_diaries']:
                    diary = Diary(diary_obj['entry'], diary_obj['timestamp'])
                    self._diaries.append(diary)
                f.close()
            except Exception as ex:
                raise IncorrectNotebookError(ex)
        else:
            raise NotebookFileError()
