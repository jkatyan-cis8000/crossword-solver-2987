"""Game state management for crossword puzzle.

This module defines the GameState class which tracks the current
state of the puzzle including player inputs and cursor position.
"""

from typing import Dict, List, Optional, Tuple

from puzzle_data import PuzzleConfig


class GameState:
    """Tracks the current state of a crossword puzzle game.

    Manages the grid state, user entries, and provides methods
    to fill cells and check puzzle completion.
    """

    def __init__(self, puzzle_config: PuzzleConfig) -> None:
        """Initialize game state from puzzle configuration.

        Args:
            puzzle_config: The PuzzleConfig containing the puzzle structure.
        """
        self.puzzle_config = puzzle_config
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(puzzle_config.grid_size[1])]
            for _ in range(puzzle_config.grid_size[0])
        ]
        self.user_entries: Dict[Tuple[int, str], str] = {}
        self.current_position: Tuple[int, int] = (0, 0)

    def fill_cell(self, row: int, col: int, char: str) -> bool:
        """Place a single letter in a cell.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).
            char: The character to place (A-Z).

        Returns:
            True if the cell was successfully filled, False if invalid.
        """
        if self._is_valid_cell(row, col):
            self.grid[row][col] = char.upper()
            return True
        return False

    def get_cell(self, row: int, col: int) -> Optional[str]:
        """Get the character in a cell.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            The character at the cell, or None if empty.
        """
        if self._is_valid_cell(row, col):
            return self.grid[row][col]
        return None

    def is_cell_filled(self, row: int, col: int) -> bool:
        """Check if a cell has been filled.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            True if the cell contains a letter.
        """
        return self.grid[row][col] is not None

    def is_black_square(self, row: int, col: int) -> bool:
        """Check if a cell is a black square.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            True if the cell is a black square.
        """
        return self.puzzle_config.is_black_square(row, col)

    def get_filled_word(self, clue_number: int, direction: str) -> str:
        """Get the currently filled word for a clue.

        Args:
            clue_number: The clue number.
            direction: Either 'across' or 'down'.

        Returns:
            String with filled letters or underscores for empty cells.
        """
        word_info = self.puzzle_config.words[clue_number]
        answer = word_info['answer']
        row = word_info['row']
        col = word_info['col']

        filled = []
        for i in range(len(answer)):
            if direction == 'across':
                cell_char = self.get_cell(row, col + i)
            else:
                cell_char = self.get_cell(row + i, col)
            filled.append(cell_char if cell_char is not None else '_')

        return ''.join(filled)

    def is_complete(self) -> bool:
        """Check if all words in the puzzle are correctly filled.

        Returns:
            True if all words are correctly filled, False otherwise.
        """
        for clue_number, word_info in self.puzzle_config.words.items():
            direction = word_info['direction']
            answer = word_info['answer']

            if not self._word_matches(clue_number, direction, answer):
                return False

        return True

    def _is_valid_cell(self, row: int, col: int) -> bool:
        """Check if a cell position is valid.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            True if the cell is within grid bounds and not a black square.
        """
        if row < 0 or row >= self.puzzle_config.grid_size[0]:
            return False
        if col < 0 or col >= self.puzzle_config.grid_size[1]:
            return False
        if self.puzzle_config.is_black_square(row, col):
            return False
        return True

    def _word_matches(self, clue_number: int, direction: str, answer: str) -> bool:
        """Check if a word matches the filled grid.

        Args:
            clue_number: The clue number.
            direction: Either 'across' or 'down'.
            answer: The expected answer string.

        Returns:
            True if the filled word matches the answer.
        """
        word_info = self.puzzle_config.words[clue_number]
        row = word_info['row']
        col = word_info['col']

        for i in range(len(answer)):
            if direction == 'across':
                cell_char = self.get_cell(row, col + i)
            else:
                cell_char = self.get_cell(row + i, col)

            if cell_char is None or cell_char != answer[i]:
                return False

        return True

    def get_word_cells(self, clue_number: int, direction: str) -> List[Tuple[int, int]]:
        """Get all cell coordinates for a word.

        Args:
            clue_number: The clue number.
            direction: Either 'across' or 'down'.

        Returns:
            List of (row, col) tuples for the word's cells.
        """
        word_info = self.puzzle_config.words[clue_number]
        answer = word_info['answer']
        row = word_info['row']
        col = word_info['col']

        cells = []
        for i in range(len(answer)):
            if direction == 'across':
                cells.append((row, col + i))
            else:
                cells.append((row + i, col))

        return cells
