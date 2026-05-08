"""Validation logic for crossword puzzle entries.

This module defines the WordValidator class which validates
user entries against the puzzle solution and reports errors.
"""

from typing import Dict, List, Tuple

from puzzle_data import PuzzleConfig
from game_state import GameState


class WordValidator:
    """Validates crossword puzzle entries.

    Provides methods to validate individual words, cells,
    and the full puzzle against the expected solution.
    """

    def __init__(self, puzzle_config: PuzzleConfig, game_state: GameState) -> None:
        """Initialize validator with puzzle and game state.

        Args:
            puzzle_config: The PuzzleConfig containing the solution.
            game_state: The GameState containing user entries.
        """
        self.puzzle_config = puzzle_config
        self.game_state = game_state
        self._errors: List[Tuple[int, int, str, str]] = []

    def validate_word(self, clue_number: int, direction: str, answer: str) -> bool:
        """Validate a word entry against the solution.

        Args:
            clue_number: The clue number to validate.
            direction: Either 'across' or 'down'.
            answer: The user's word entry.

        Returns:
            True if the word is correct, False otherwise.
        """
        expected_info = self.puzzle_config.words[clue_number]
        expected_direction = expected_info['direction']
        expected_answer = expected_info['answer']

        if direction != expected_direction:
            return False

        row = expected_info['row']
        col = expected_info['col']

        self._errors = []

        if len(answer) != len(expected_answer):
            self._collect_errors(clue_number, direction, answer, expected_answer)
            return False

        for i in range(len(answer)):
            if direction == 'across':
                cell_row, cell_col = row, col + i
            else:
                cell_row, cell_col = row + i, col

            expected_char = expected_answer[i]
            actual_char = answer[i].upper() if i < len(answer) else ''

            if actual_char != expected_char:
                self._errors.append((cell_row, cell_col, expected_char, actual_char))

        return len(self._errors) == 0

    def validate_cell(self, row: int, col: int) -> bool:
        """Validate a single cell.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            True if the cell is correctly filled, False otherwise.
        """
        if self.game_state.is_black_square(row, col):
            return True

        cell_value = self.game_state.get_cell(row, col)
        if cell_value is None:
            return False

        expected_char = self._get_expected_char_at(row, col)
        return cell_value.upper() == expected_char.upper()

    def get_errors(self) -> List[Tuple[int, int, str, str]]:
        """Get list of validation errors.

        Returns:
            List of (row, col, expected, actual) tuples for each error.
        """
        return self._errors.copy()

    def validate_full_puzzle(self) -> Tuple[bool, List[Tuple[int, int, str, str]]]:
        """Validate the entire puzzle.

        Returns:
            Tuple of (is_valid, list of all errors).
        """
        all_errors: List[Tuple[int, int, str, str]] = []

        for clue_number, word_info in self.puzzle_config.words.items():
            direction = word_info['direction']
            answer = word_info['answer']
            row = word_info['row']
            col = word_info['col']

            for i in range(len(answer)):
                if direction == 'across':
                    cell_row, cell_col = row, col + i
                else:
                    cell_row, cell_col = row + i, col

                expected_char = answer[i]
                actual_char = self.game_state.get_cell(cell_row, cell_col)

                if actual_char is None or actual_char.upper() != expected_char.upper():
                    all_errors.append((cell_row, cell_col, expected_char, actual_char or ''))

        return len(all_errors) == 0, all_errors

    def _get_expected_char_at(self, row: int, col: int) -> str:
        """Get the expected character at a cell.

        Args:
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            The expected character at the cell.
        """
        words_at_pos = self.puzzle_config.get_word_at_position(row, col)
        if not words_at_pos:
            return ''

        clue_number, direction = words_at_pos[0]
        word_info = self.puzzle_config.words[clue_number]
        start_row = word_info['row']
        start_col = word_info['col']
        answer = word_info['answer']

        if direction == 'across':
            index = col - start_col
        else:
            index = row - start_row

        return answer[index]

    def _collect_errors(
        self,
        clue_number: int,
        direction: str,
        user_answer: str,
        expected_answer: str,
    ) -> None:
        """Collect all error positions for a word.

        Args:
            clue_number: The clue number.
            direction: Either 'across' or 'down'.
            user_answer: The user's word entry.
            expected_answer: The correct word.
        """
        word_info = self.puzzle_config.words[clue_number]
        row = word_info['row']
        col = word_info['col']

        for i in range(max(len(user_answer), len(expected_answer))):
            if direction == 'across':
                cell_row, cell_col = row, col + i
            else:
                cell_row, cell_col = row + i, col

            expected_char = expected_answer[i] if i < len(expected_answer) else ''
            actual_char = user_answer[i].upper() if i < len(user_answer) else ''

            if expected_char != actual_char:
                self._errors.append((cell_row, cell_col, expected_char, actual_char))
