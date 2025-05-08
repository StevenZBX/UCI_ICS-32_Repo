# Dr. Mario Game Implementation

## Overview
This is part one of a two-part assignment where you'll build a video game. In this part, you'll implement the game's core logic and a text-based interface. The GUI version will be built in a future assignment.

## Game Description
Dr. Mario is a puzzle game similar to Tetris, originally released in 1990 for the Nintendo Entertainment System. The goal is to clear viruses from a grid using colorful vitamin capsules.

## Game Components

### 1. Field
- A grid where the game takes place
- Each cell can contain:
  - Part of a vitamin capsule
  - A virus
  - Empty space

### 2. Vitamin Capsules
- Made of two connected segments
- Each segment has a color (Red, Yellow, or Blue)
- Can be:
  - Two different colors
  - Same color
  - Horizontal or vertical orientation

### 3. Viruses
- Single-celled elements
- Come in three colors: red, yellow, or blue

### 4. Faller
- The current vitamin capsule moving down the field
- Lands when it hits:
  - An occupied cell
  - The bottom of the field
- Can be:
  - Rotated (clockwise or counterclockwise)
  - Moved left or right
  - Frozen when landed

## Game Rules

### Rotation
- Fallers can rotate clockwise (A) or counterclockwise (B)
- Rotation happens around the bottom-left cell
- Wall kicks occur when rotation is blocked:
  - If blocked, faller moves left
  - If left move is impossible, rotation fails

### Matching
- Matches occur when 4+ adjacent cells have the same color
- Matches can be horizontal or vertical
- Matched cells (viruses and capsules) disappear

### Gravity
- Affects capsule pieces, not viruses
- Makes pieces fall when there's empty space below
- Applies to:
  - Single capsule pieces
  - Horizontal capsules with empty space below both ends
  - Vertical capsules with empty space below bottom segment

### Level Completion
- A level is complete when all viruses are removed
- Game continues after level completion

## Game Setup

### Field Size
1. Enter number of rows (minimum 4)
2. Enter number of columns (minimum 3)

### Initial Field State
Two options:
1. Empty field: Enter "EMPTY"
2. Custom field: Enter "CONTENTS" followed by field configuration
   - Use uppercase letters (R,B,Y) for capsule segments
   - Use lowercase letters (r,b,y) for viruses
   - Use spaces for empty cells

## Game Commands

### Basic Commands
- `ENTER` (blank line): Advance time
- `F [color1] [color2]`: Create new faller
- `A`: Rotate clockwise
- `B`: Rotate counterclockwise
- `<`: Move left
- `>`: Move right
- `V [row] [col] [color]`: Create virus
- `Q`: Quit game

### Game End Conditions
1. Player quits (Q command)
2. Game over when new faller can't be created (top row blocked)

## Implementation Requirements

### File Structure
- `a2.py`: Main program entry point
- At least two modules:
  - User interface module
  - Game logic module
- At least one class for game state

### Required Methods
- Get field dimensions
- Create faller
- Rotate faller
- Check for viruses
- (Additional methods as needed)

## Field Display Format
Each cell is represented by 3 characters:
- Empty: `   ` (three spaces)
- Single capsule: ` R ` (space, letter, space)
- Left capsule end: ` R-` (space, letter, dash)
- Right capsule end: `-R ` (dash, letter, space)
- Vertical faller: `[R]`
- Horizontal faller left: `[R-`
- Horizontal faller right: `-R]`
- Virus: ` r ` (space, lowercase letter, space)
- Matched cell: `*R*` or `*r*`