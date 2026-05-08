"""Command-line interface for crossword puzzle game."""

import re
from validation import WordValidator


class CrosswordCLI:
    """Handles user input/output and game loop for crossword puzzle."""

    def __init__(self, puzzle_config, game_state):
        """Initialize the CLI with puzzle configuration and game state.
        
        Args:
            puzzle_config: PuzzleConfig instance with puzzle data.
            game_state: GameState instance for tracking progress.
        """
        self.puzzle_config = puzzle_config
        self.game_state = game_state
        self.validator = WordValidator(puzzle_config, game_state)
        self.current_clue = None
        self.current_direction = None

    def display_grid(self):
        """Render the grid with row/col coordinates and clue numbers."""
        grid_size = self.puzzle_config.grid_size
        
        print("\n  " + " ".join(f"{col:2d}" for col in range(grid_size[1])))
        
        for row in range(grid_size[0]):
            print(f"{row:2d}", end="")
            for col in range(grid_size[1]):
                cell = self.game_state.get_cell(row, col)
                if (row, col) in self.puzzle_config.black_squares:
                    print(" ██", end="")
                elif cell:
                    print(f" {cell} ", end="")
                else:
                    clue_nums = self._get_clue_number_at(row, col)
                    if clue_nums:
                        print(f" {clue_nums:2d}", end="")
                    else:
                        print(" . ", end="")
            print()
        print()

    def _get_clue_number_at(self, row, col):
        """Get clue number at a position, or empty string if none.
        
        Args:
            row: Row index (0-based).
            col: Column index (0-based).
            
        Returns:
            Clue number string or empty string.
        """
        words_at_pos = self.puzzle_config.get_word_at_position(row, col)
        if words_at_pos:
            return words_at_pos[0][0]
        return ""

    def display_clues(self):
        """Display across and down clues."""
        print("\n=== ACROSS ===")
        for clue_num, clue_text in self.puzzle_config.across_clues.items():
            word_info = self.puzzle_config.words.get(clue_num)
            if word_info:
                filled = self.game_state.get_filled_word(clue_num, 'across')
                print(f"{clue_num:2d}. {clue_text} [{filled}]")
        
        print("\n=== DOWN ===")
        for clue_num, clue_text in self.puzzle_config.down_clues.items():
            word_info = self.puzzle_config.words.get(clue_num)
            if word_info:
                filled = self.game_state.get_filled_word(clue_num, 'down')
                print(f"{clue_num:2d}. {clue_text} [{filled}]")
        print()

    def get_user_input(self):
        """Prompt user for clue number and direction.
        
        Returns:
            Tuple of (clue_number, direction, word) or None if quit.
        """
        print("\nEnter clue (e.g., '1 across' or '1 a'), or 'quit' to exit:")
        print("Format: <number> <direction> then enter word")
        
        line = input("> ").strip()
        
        if not line:
            return None
        
        if line.lower() in ('quit', 'q', 'exit', 'x'):
            print("Thanks for playing!")
            return None
        
        match = re.match(r'^(\d+)\s*(across|a|down|d)\s*$', line, re.IGNORECASE)
        if match:
            clue_num = int(match.group(1))
            direction = 'across' if match.group(2).lower().startswith('a') else 'down'
            
            if clue_num not in self.puzzle_config.words:
                print(f"Error: Clue {clue_num} not found.")
                return None
            
            word_info = self.puzzle_config.words[clue_num]
            if word_info['direction'] != direction:
                print(f"Error: Clue {clue_num} is {word_info['direction']}, not {direction}.")
                return None
            
            self.current_clue = clue_num
            self.current_direction = direction
            
            word = input(f"Enter word for {clue_num} {direction}: ").strip()
            
            if word.lower() in ('quit', 'q', 'exit', 'x'):
                print("Thanks for playing!")
                return None
            
            return (clue_num, direction, word)
        
        print("Invalid format. Use: <number> <direction> (e.g., '1 across' or '1 a')")
        return None

    def handle_entry(self, clue_number, direction, word):
        """Process a user's word entry.
        
        Args:
            clue_number: The clue number entered.
            direction: 'across' or 'down'.
            word: The word entered by user.
            
        Returns:
            True if entry was valid, False otherwise.
        """
        word_info = self.puzzle_config.words.get(clue_number)
        if not word_info:
            print(f"Error: Clue {clue_number} not found.")
            return False
        
        expected_len = len(word_info['answer'])
        if len(word) != expected_len:
            print(f"Error: Word must be {expected_len} letters (got {len(word)}).")
            return False
        
        if not word.isalpha():
            print("Error: Word must contain only letters.")
            return False
        
        row = word_info['row']
        col = word_info['col']
        
        for i, char in enumerate(word.upper()):
            if direction == 'across':
                self.game_state.fill_cell(row, col + i, char)
            else:
                self.game_state.fill_cell(row + i, col, char)
        
        self.game_state.user_entries[(clue_number, direction)] = word.upper()
        
        if self.validator.validate_word(clue_number, direction, word):
            print(f"✓ Correct! Filled in '{word.upper()}'.")
        else:
            print(f"✗ Incorrect. Word '{word.upper()}' doesn't match the answer.")
            self.validator.validate_full_puzzle()
            errors = self.validator.get_errors()
            if errors:
                print("Errors found at:")
                for row, col, expected, actual in errors:
                    print(f"  ({row}, {col}): expected '{expected}', got '{actual}'")
        
        return True

    def game_loop(self):
        """Run the main interaction loop."""
        print("=" * 50)
        print("       CROSSWORD PUZZLE")
        print("=" * 50)
        
        while True:
            self.display_grid()
            self.display_clues()
            
            if self.game_state.is_complete():
                print("\n🎉 CONGRATULATIONS! Puzzle solved!")
                break
            
            result = self.get_user_input()
            if result is None:
                break
            
            clue_num, direction, word = result
            self.handle_entry(clue_num, direction, word)
