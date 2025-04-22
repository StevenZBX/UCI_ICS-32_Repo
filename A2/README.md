This assignment is part of a two-part assignment in which you will build a video game. In this assignment, you will implement the model of the game. We want you to implement the fundamental logic in the game and build a text-based user interface that allows a user to play the game, albeit in a rather cumbersome fashion. In a future assignment, we will build a user-friendly GUI.


What is Dr. Mario?
Dr. Mario is a falling block puzzle game (think Tetris) that was released in 1990 for the Nintendo Entertainment System (and the Gameboy, but since we want to think of the matching in terms of color, let’s only focus on the NES version). If you don’t know of the original puzzle game featuring Dr. Mario, you may know the character from the Super Smash Bros. series. The objective of the game (or a single level rather), is to remove a group of viruses occupying a grid using colorful vitamin capsules. Here you can watch a bit of the gameplay:


Additionally, here is the official game manualLinks to an external site. for Dr. Mario as it was included with the game cartridge. You may find this document useful (or interesting).

Game Components
Based on the gameplay, Dr. Mario consists of core components we discuss in the following.

Field
The field is a grid of cells, each of which is occupied by part (one half) of a vitamin capsule, a virus, or empty space.

Vitamin Capsule
A vitamin capsule is made up of two connected segments, each possessing its color (red, yellow, or blue). A capsule can be two-color or one-color. It can be (at any time), horizontal or vertical.



Virus
A virus, like the Vitamin Capsules, can be red, yellow, or blue. Unlike Vitamin Capsules, viruses are single-celled (no pun intended).



Faller

A faller is the current vitamin capsule that is descending downward in our field until it lands either on an occupied cell or the bottommost row of the field. Note, a faller lands if either of its segments (if it is horizontal), is on top of an occupied cell.

It can be rotated either clockwise 🔁 or counterclockwise 🔄. This changes the orientation of the faller. Fallers freeze when they land; after this point, they can no longer be moved left or right or rotated. Rotation is a fairly complex mechanism in our program, so it might be good to expand on it a bit more here. Firstly, let's highlight this graphic from the official manual linked above.

capsule-rotation.png
There are two sequences of rotation, one clockwise and the other counterclockwise. Each A or B command rotates the faller 90 degrees clockwise or counterclockwise, respectively. This graphic, while useful, is a little deceptive in that it appears to show that rotating a faller would move it down a level. This is not actually the case. It would be helpful to consider the fallers as 2 x 2 grids, in which the bottom left cell is always occupied.

Here is a representation of clockwise rotation and counterclockwise rotation, respectively:

rotation.png
Note that the bottom left cell always remains occupied. Therefore, upon rotation, the faller should not move down a level. It may be helpful to think of a faller as occupying this four-cell grid at all times and making moves centering around this bottom left cell. 

Wall Kick: At this point, you may have noticed something interesting about rotation that I have not yet mentioned. When rotating a vertical faller either clockwise or counterclockwise, it will become a horizontal faller. But what if the bottom right cell in the 2 x 2 grid is occupied? Well, then we encounter something called a wall kick. 

wall-kick.png
Note that the cell with the gray X is filled (vitamin capsule segment, virus, or the wall of the field).

In a wall kick of this kind, we should move the faller one cell to the left. Thus, it is possible for an A or B command to have two effects: rotating the faller and moving it to the left (like a < command). Fortunately, we do not have to worry about any other types of wall kicks for our program (though other versions of the game do account for other types of wall kicks). Also note that if we encounter a wall kick, but the cell to the left of the faller is also occupied (a left move is not possible), then the rotation should not occur. 

Matching: After a faller lands, matching may occur. Matching happens when at least four (though it's pretty difficult to get a match of more than six cells in the real game) vertically or horizontally adjacent cells are occupied by the same color, whether it be a virus cell or a vitamin capsule cell. When cells are matched, the virus and capsule cells occupying them vanish. This is how we erase viruses.

Gravity: After matching concludes, gravity does its thing. Any singular capsule pieces with empty space below them should be subject to gravity; that is, they should fall downward. Any horizontal two-segment capsules with empty cells beneath both ends should also feel the effect of gravity. A vertical two-segment capsule with empty cells below the bottom segment should also feel the effect of gravity. Viruses, unlike vitamin capsules, are not affected by gravity. More information about the intricacies of gravity can be seen in the examples below.

Level
A level is complete when all viruses are erased from the field.


There are a few things about the gameplay that you can disregard for this assignment (but you may choose to consider for the next assignment):

The score. If you look to the top left section of the screen, there are two numbers: the high school on the top and the current player score on the bottom. While the score is a cornerstone of an arcade game like this, we really want you to focus on the fundamentals of the game for this assignment.
The next vitamin capsule. In the top right section of the screen, we have our titular character tossing capsules onto the playing field. While the current capsule has not yet landed, the player can glimpse what is to come by looking at the capsule Dr. Mario is holding.
Again, while these are certainly core components of the playing experience of this game, they are not essential for completing this assignment.

Building the Game
For this assignment, you will build a shell program that takes user input representing basic actions in our game and print output that will display the current state of the game. This assignment will be auto-graded. Therefore, you must conform to a strict set of allowable inputs and an even stricter output format. You must follow the examples down to the individual characters.

Initializing the Game
Upon running your program, it needs to know the size of the playing field. You can assume it should always be a rectangle, but the number of rows and columns can vary.

First, your program reads a line of input specifying the number of rows in the field. You can assume this will be at least 4.

Next, your program reads a line of input specifying the number of columns in the field. You can assume this will be at least 3.

At any given time, the field will consist of (B)lue, (R)ed, and/or (Y)ellow vitamin capsules and (b)lue, (r)ed, and/or (y)ellow viruses.

The characters R, B, and Y denote a cell is occupied by a vitamin capsule 💊 of the corresponding color.
The characters r, b, and y denote a cell occupied by a virus 🦠 of the corresponding color.
The capitalization is very important here.
Your program needs to take in a specific configuration of the field to begin the game. There are two possible situations: starting with an empty field, or with a field containing some vitamin capsule cells or virus cells.

If we want to start with an empty field, the word EMPTY should be entered alone on the next input line.

If we want to start our game with a specific field configuration, the word CONTENTS should be entered alone on the next input line. After that, assuming we have entered r rows and c columns, there should be r additional lines of input expected, and each line should contain exactly c characters; these characters represent the contents of each of the field’s cells at the outset of our game.

For a cell with a virus, a lowercase letter should be used (r,y,b).
For a cell with a portion of a vitamin capsule, an uppercase letter should be used (R, B, Y)
A space should be used for an empty cell.
Note that every cell should be represented in this input. Every empty cell should be represented by its own space character.
Notably, we defined a vitamin capsule above as being made up of “two connecting segments.” Though I have not yet gone into detail about how we will represent each cell in our grid, you may be wondering how we would capture the connection between two cells as they may be part of the same vitamin capsule. For simplicity, you can assume that any cell in the initial configuration supplied this way is just a portion of a vitamin capsule. These kinds of cells are possible, as you may have noticed in the gameplay video and would normally come about as a result of matching (as described in more detail below)
Playing the Game
At this point, the game can begin. Now, we will continuously display the field and then ask for a command from the user.

Field Representation
The field will be represented by r + 1 (or conditionally, r + 2) lines of output. For the each of the r rows, a|character should be printed at the beginning, followed by 3 characters for each cell, then followed by another |. Each cell will be represented by a group of 3 characters.

Three spaces if the cell is empty
A space, then an uppercase letter (R, B, Y), then another space, if the cell contains a single portion of a capsule.
A space, then an uppercase letter (R, B, Y), then a - if the cell is occupied by the left portion of a capsule.
A -, then an uppercase letter (R, B, Y), then a space, if the cell is occupied by the right portion of a capsule.
Note, a cell that is a portion of a two-segment capsule should contain a - if it is either the left or right end of a horizontal capsule. For a vertical capsule, we will represent it as two separate single-segment capsules, just as those created by matching. You should however, be able to easily transition between these two representations for a falling capsule upon rotation.
A [, then an uppercase letter, then another ] for any cell that is part of a vertical faller.
A [, then an uppercase letter, then a - if the cell is occupied by the left end of a horizontal faller.
A -, then an uppercase letter, then a ] if the cell is occupied by the right end of a horizontal faller.
A |, then an uppercase letter, then another | for any cell that is part of a currently landed vertical faller that has not yet frozen.
A |, then an uppercase letter, then a - if the cell is occupied by the left end of a landed horizontal faller that has not yet frozen.
A -, then an uppercase letter, then a|if the cell is occupied by the right end of a landed horizontal faller that has not yet frozen.
A space, then a lowercase letter (r, y, b), then another space, if the cell is occupied by a virus.
A *, then an uppercase OR lowercase letter, then another * for any cell that is recognized as part of a match. Note, this is the only case for matching, regardless of whether or not the cell is part of any capsule (horizontal or vertical) or a virus.
After the last row of the field, there should be 3c - characters, followed by another space. This represents the bottom of the field.
For potential r + 2th row, you would print LEVEL CLEARED if the field contains no virus cells in its current state. This does not terminate the program.
Supported Commands
Your program should be able to read the following commands:

A blank line (entered simply by pressing the ENTER key). This command represents the passage of time in our game. (In the next assignment, this update would occur simply as a result of a timed event rather than any user input).
If there is a faller currently on the field, it falls down one cell. If there is a faller that has currently landed, it freezes. If there are capsule cells with empty cells below them, then gravity should be applied one cell at a time and the capsule cells should move downward.
F, followed by two uppercase letters (R, B, or Y) each separated by whitespace (any amount of whitespace is acceptable, consider using shlex as in assignment 1). This command will create a faller with the first uppercase letter after F representing the left end of a horizontal faller and the second letter after F representing the right end of a horizontal faller. F R Y, would create a faller with a red left segment, and a yellow right segment.
All fallers should be created horizontally with their left end occupying the middle cell of the second row of our field. You may be wondering: why the second row? Well, it is probably not visible in the gameplay above, but the top cell of the field in the original game is actually not blocked by any sort of barrier. That is, a vitamin capsule can overlap the glass covering the top of the field. Whether or not this is an error in the original game’s code, I am not sure. But it does make some of the game logic a bit simpler to grapple with. I attached an image of the effect below if you're interested.
If c (the number of columns) is odd, there will be one middle cell, located at the column numbered 
 (in a 0-based index system as we use in Python). If c is even, there will be two middle cells, occupying the columns 
 and 
. 
A alone on a line, which rotates the faller clockwise (rotation is described in depth below as it is a bit more complex than the other operations).
B alone on a line, which rotates the faller counterclockwise. You may be wondering why A and B were chosen to represent rotation instead of something that makes more sense mnemonically. We chose A and B because those are the buttons that you would press on a Gameboy or NES controller to achieve this rotation. Note, if there is no faller currently on the field, these two commands have no effect. Rotation is, however, possible for a faller that has landed but not yet frozen.
< alone a line, which moves the faller (if there is one), to the left. If there is no faller, or the faller cannot be moved to the left, then this command has no effect. Note, a landed faller that has not yet frozen can in fact, be moved to the left, and in some cases, this can make it so a landed faller is no longer in a landed state (if the faller is moved to a position with no occupied cells below either of its segments (or the bottom one, if it is vertical). 
> alone a line, which moves the faller (if there is one), to the right. If there is no faller, or the faller cannot be moved to the left, then this command has no effect. Note, a landed faller that has not yet frozen can in fact, be moved to the left, and in some cases, this can make it so a landed faller is no longer in a landed state (if the faller is moved to a position with no occupied cells below either of its segments (or the bottom one, if it is vertical).
V, followed by two integers, representing a row, and a column (respectively), followed by a lowercase letter (r, b, y). This command creates a virus cell in the specified row and cow of the field. For example, V 1 2 r  would create a red virus cell in the 2nd column of the 1st row. As with the F command, the arguments can be separated by any amount of whitespace
Q alone on a line, to quit the program.
Ending the Game
There are 2 ways for the program to end:

If the user inputs the Q command. No additional output should be printed.
If a faller is created while the middle cell(s) of the top row are occupied by capsule segments. In this case, the player has lost, the game should end, and your program should print GAME OVER before terminating.
Notably, in our program, since we allow you to begin with an empty field, a cleared level is not a terminating condition. In the next assignment, you will have freedom over how you want to allow the user to continue playing, but it’s not important here. Unlike a game like Tetris, Dr. Mario is level-based, and does not continue endlessly, thus it will be up to you to decide how you want the GUI version of the game to continue after a level is cleared. (Actually, the NES version of Tetris does have a final level that had never been reached until as recently as December 2023, some 34 years after the game’s release).
Two Complete Examples
Below, we provide two examples of the program’s execution which we hope is useful as you attempt to build your program’s functionality. Input is indicated by black text and output is represented by blue text. Blank lines of input are intentionally blank, as they represent the empty input command. Additional commentary is also provided as comments in green (# this is a comment).

 

4
4
EMPTY
|            |
|            |
|            |
|            |
 ------------
LEVEL CLEARED   # "LEVEL CLEARED" since there are no virus cells in the field
F R Y           # create a faller with RED left end and YELLOW right end
|   [R--Y]   |
|            |
|            |
|            |
 ------------ 
LEVEL CLEARED
                # This is a blank line
|            |
|   [R--Y]   |
|            |
|            |
 ------------ 
LEVEL CLEARED

|            |
|            |
|   [R--Y]   |
|            |
 ------------ 
LEVEL CLEARED

|            |
|            |
|            |
|   |R--Y|   |  # the faller has landed
 ------------ 
LEVEL CLEARED

|            |
|            |
|            |
|    R--Y    |  # the faller has frozen
 ------------ 
LEVEL CLEARED

F Y B           # create another faller (this time yellow and blue)
|            |
|   [Y--B]   |
|            |
|    R--Y    |
 ------------ 
LEVEL CLEARED

|            |
|            |
|   |Y--B|   |
|    R--Y    |
 ------------ 
LEVEL CLEARED
A               #rotate faller clockwise 
|            |
|   |B|      |
|   |Y|      |
|    R--Y    |
 ------------ 
LEVEL CLEARED
>
|            |
|      |B|   |
|      |Y|   |
|    R--Y    |
 ------------ 
LEVEL CLEARED

|            |
|       B    |
|       Y    |
|    R--Y    |
 ------------ 
LEVEL CLEARED
V 2 1 R         #create a virus cell 
|            |
|       B    |
|    r  Y    |
|    R--Y    |
 ------------ 
V 1 1 R         # "LEVEL CLEARED" is not printed here since there is a virus cell
|            |
|    r  B    |
|    r  Y    |
|    R--Y    |
 ------------ 
V 0 1 R         # For illustrative purposes, there's a virus in the top cell. This doesn't happen in the official game.
|   *r*      |  # matching ensues immediately as soon as a match is detected
|   *r* B    | 
|   *r* Y    |
|   *R*-Y    |
 ------------ 

|            |  # matched cells vanish after matching
|       B    |  # notice also, that the yellow cell in the bottom row is no longer connected to another cell
|       Y    |
|       Y    |
 ------------ 
LEVEL CLEARED   # once again printed as all virus cells are eliminated                
F Y Y
|            |
|    [Y--Y]  |  
|       Y    |
|       Y    |
 ------------ 
GAME OVER       # GAME OVER because a horizontal faller was added to an occupied cell
#NOTHING PRINTED HERE. note again, that fallers are always added horizontally to the middle of the second row 
##END OF EXAMPLE ONE
A second example with initial contents and more gravity
4
4
CONTENTS
    
R  r 
    
YyYy
|            |
| R        r |  
|            |
|*Y**y**Y**y*|  # matching begins immediately 
 ------------ 

|            |  # gravity is now applied to the vitamin cell, but not the virus cell
|          r |  
| R          |
|            |
 ------------ 

|            |
|          r |
|            |  
| R          |
 ------------ 
F R Y
|            |
|   [R--Y] r |
|            |  
| R          |
 ------------ 
<
|            |
|[R--Y]    r |
|            |  
| R          |
 ------------ 
<
|            |  # < has no effect since the faller reached the wall
|[R--Y]    r |
|            |  
| R          |
 ------------ 

|            |
|          r |
|[R--Y]      |  
| R          |
 ------------ 

|            |
|          r |
||R--Y|      |  
| R          |
 ------------ 

|            |
|          r |
| R--Y       |  
| R          |
 ------------ 

|            |
|          r |
| R--Y       |  
| R          |
 ------------   # This update had no effect. Note the yellow capsule cell does not have gravity applied to it.
F R R
|            |
|   [R--R] r |
| R--Y       |  
| R          |
 ------------ 
A
|   [R]      |
|   [R]    r |
| R--Y       |  
| R          |
 ------------ 
<
|[R]         |
|[R]       r |
| R--Y       |  
| R          |
 ------------ 

||R|         |
||R|       r |
| R--Y       |  
| R          |
 ------------ 

|*R*         |  # matching occurs as soon as the faller freezes
|*R*       r |
|*R*-Y       |  
|*R*         |
 ------------ 

|            |  # the yellow cell is detached from the now vanished capsule segment
|          r |
|    Y       |  
|            |
 ------------ 

|            |  # gravity is applied to the now singular yellow cell
|          r |
|            |  
|    Y       |
 ------------
F B Y
|            | 
|   [B--Y] r |
|            |  
|    Y       |
 ------------
B               # rotate counterclockwise
|   [Y]      | 
|   [B]    r |
|            |  
|    Y       |
 ------------
Q
# END OF EXAMPLE TWO
Program Requirements
As with the previous assignments, you have flexibility with how you choose to break up your code, but the following is required:

a2.py: This module will be the entry point of your program, and it must be executable (should contain the if __name__ == '__main__' block. 
You are also required to decouple your code into at least two modules, one that handles the user interface, and another that handles the logic of your game. Your code must also contain at least one class that represents the current state of your game (you may even want additional classes). It’s up to you to decide how exactly you want to design this class, but here are a few methods you might want to have:

A method to get the number of rows/columns in your field
A method to create a faller
A method to rotate a faller
A method to determine if the field contains any viruses
This is by no means a comprehensive list of methods you may want to have in your code, but it should get you to start thinking about the kind of things that a method should do/represent.  