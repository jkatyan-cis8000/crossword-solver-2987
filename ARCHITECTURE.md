# Crossword Puzzle Application Architecture

## Overview
A command-line crossword puzzle game where users fill in words by specifying clue numbers and directions. The application validates letter entries and detects completion when all words are correctly filled.

## Module Structure

### 1. `puzzle_data.py` - Puzzle Configuration
**Responsibility**: Define the crossword puzzle structure including grid layout, clues, and word positions.

**Key Components**:
- `PuzzleConfig` class with:
  - `grid_size` (width, height)
  - `black_squares` set of (row, col) coordinates
  - `words` dict mapping clue_number -> {direction, answer, row, col}
  - `across_clues` dict mapping clue_number -> text
  - `down_clues` dict mapping clue_number -> text

**Interfaces**:
- `get_word_at_position(row, col) -> list of (clue_number, direction)` - find words covering a cell
- `get_clue_text(clue_number, direction) -> str`

### 2. `game_state.py` - Game State Management
**Responsibility**: Track the current state of the puzzle including player inputs.

**Key Components**:
- `GameState` class with:
  - `grid` 2D list of characters (None for empty, 'A'-'Z' for filled)
  - `user_entries` dict mapping (clue_number, direction) -> entered_word
  - `current_position` (row, col) cursor location

**Interfaces**:
- `fill_cell(row, col, char)` - place a single letter
- `get_cell(row, col) -> char or None`
- `is_cell_filled(row, col) -> bool`
- `get_filled_word(clue_number, direction) -> str`
- `is_complete() -> bool` - all words correctly filled

### 3. `validation.py` - Validation Logic
**Responsibility**: Validate user entries against the puzzle solution.

**Key Components**:
- `WordValidator` class

**Interfaces**:
- `validate_word(clue_number, direction, answer) -> bool`
- `validate_cell(row, col) -> bool`
- `get_errors() -> list of (row, col, expected, actual)`
- `validate_full_puzzle() -> (bool, list of errors)`

### 4. `cli.py` - User Interface
**Responsibility**: Handle user input/output and game loop.

**Key Components**:
- `CrosswordCLI` class

**Interfaces**:
- `display_grid()` - render the grid with clue numbers
- `display_clues()` - show across and down clues
- `get_user_input()` - prompt for clue number and direction
- `handle_entry(clue_number, direction, word)` - process user's word entry
- `game_loop()` - main interaction loop

### 5. `main.py` - Application Entry Point
**Responsibility**: Initialize and run the game.

**Key Components**:
- Sample puzzle definition
- Main function to start the game

## Game Flow
1. Initialize puzzle config and game state
2. Display grid and clues
3. User enters clue number (e.g., "1") and direction (e.g., "across")
4. User enters the word
5. Validate each letter
6. Fill in grid or show error
7. Check for completion
8. Repeat until puzzle solved or user quits

## Sample Puzzle Structure
A 5x5 grid with simple words:
- Grid with some black squares
- Simple across/down words (4-6 letters each)
- Overlapping words at intersection points
