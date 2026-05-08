"""Puzzle configuration for crossword puzzle.

This module defines the PuzzleConfig class which holds the structure
of the crossword puzzle including grid layout, clues, and word positions.
"""

from typing import Dict, List, Set, Tuple, Optional


class PuzzleConfig:
    """Configuration for a crossword puzzle.

    Manages the grid layout, black squares, word definitions,
    and clue texts for both across and down directions.
    """

    def __init__(
        self,
        grid_size: Tuple[int, int],
        black_squares: Set[Tuple[int, int]],
        words: Dict[int, Dict[str, any]],
        across_clues: Dict[int, str],
        down_clues: Dict[int, str],
    ) -> None:
        """Initialize puzzle configuration.

        Args:
            grid_size: Tuple of (width, height) for the grid dimensions.
            black_squares: Set of (row, col) coordinates that are black/solid cells.
            words: Dict mapping clue_number -> {direction, answer, row, col}
                where direction is 'across' or 'down'.
            across_clues: Dict mapping clue_number -> clue text for across words.
            down_clues: Dict mapping clue_number -> clue text for down words.
        """
        self.grid_size = grid_size
        self.black_squares = black_squares
        self.words = words
        self.across_clues = across_clues
        self.down_clues = down_clues

    def get_word_at_position(self, row: int, col: int) -> List[Tuple[int, str]]:
        """Find all words that cover the given cell.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            List of (clue_number, direction) tuples for words covering this cell.
        """
        words_at_position = []
        for clue_number, word_info in self.words.items():
            direction = word_info['direction']
            start_row = word_info['row']
            start_col = word_info['col']
            answer = word_info['answer']

            if direction == 'across':
                if row == start_row and start_col <= col < start_col + len(answer):
                    words_at_position.append((clue_number, direction))
            elif direction == 'down':
                if col == start_col and start_row <= row < start_row + len(answer):
                    words_at_position.append((clue_number, direction))

        return words_at_position

    def get_clue_text(self, clue_number: int, direction: str) -> str:
        """Get the text for a specific clue.

        Args:
            clue_number: The clue number.
            direction: Either 'across' or 'down'.

        Returns:
            The clue text string.

        Raises:
            KeyError: If the clue doesn't exist.
        """
        if direction == 'across':
            return self.across_clues[clue_number]
        elif direction == 'down':
            return self.down_clues[clue_number]
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def is_black_square(self, row: int, col: int) -> bool:
        """Check if a cell is a black square.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            True if the cell is a black square.
        """
        return (row, col) in self.black_squares

    def get_word_info(self, clue_number: int) -> Dict[str, any]:
        """Get information about a specific word.

        Args:
            clue_number: The clue number.

        Returns:
            Dict with direction, answer, row, col keys.

        Raises:
            KeyError: If the word doesn't exist.
        """
        return self.words[clue_number]


def create_sample_puzzle() -> PuzzleConfig:
    """Create a sample 5x5 crossword puzzle.

    Grid layout (5x5):
        0   1   2   3   4
      +---+---+---+---+---+
    0 | A | L | P | H | A |
      +---+---+---+---+---+
    1 | B | # | E | # | # |
      +---+---+---+---+---+
    2 | C | B | G | L | E |
      +---+---+---+---+---+
    3 | U | A | # | L | # |
      +---+---+---+---+---+
    4 | T | R | U | E | # |
      +---+---+---+---+---+

    Words:
    - 1ACROSS: ALPHA (row 0, cols 0-4)
    - 3ACROSS: CBGLE (row 2, cols 0-4)
    - 1DOWN: ABCUT (col 0, rows 0-4)
    - 2DOWN: LBA (col 1, rows 0-2)
    - 4DOWN: AEGLE (col 3, rows 0-4)
    - 5DOWN: BENT (col 4, rows 2-5)

    Returns:
        PuzzleConfig with the sample puzzle data.
    """
    grid_size = (5, 5)
    black_squares = {
        (1, 1),  # row 1, col 1
        (1, 3),  # row 1, col 3
        (1, 4),  # row 1, col 4
        (3, 2),  # row 3, col 2
        (3, 4),  # row 3, col 4
        (4, 4),  # row 4, col 4
    }

    words = {
        1: {'direction': 'across', 'answer': 'ALPHA', 'row': 0, 'col': 0},
        3: {'direction': 'across', 'answer': 'CBGLE', 'row': 2, 'col': 0},
        6: {'direction': 'down', 'answer': 'ABCUT', 'row': 0, 'col': 0},
        2: {'direction': 'down', 'answer': 'LBA', 'row': 0, 'col': 1},
        4: {'direction': 'down', 'answer': 'AEGLE', 'row': 0, 'col': 3},
        5: {'direction': 'down', 'answer': 'BENT', 'row': 2, 'col': 4},
    }

    across_clues = {
        1: "Greek letter at the start of the alphabet",
        3: "Anagram of 'belge' - a historical region",
    }

    down_clues = {
        6: "First five letters of the alphabet series",
        2: "Reverse of 'AB' + 'E'",
        4: "A group of five similar things",
        5: "To leave or go away",
    }

    return PuzzleConfig(grid_size, black_squares, words, across_clues, down_clues)
