"""Main application entry point for crossword puzzle game."""

from puzzle_data import PuzzleConfig, create_sample_puzzle
from game_state import GameState
from cli import CrosswordCLI


def main():
    """Initialize and run the crossword puzzle game."""
    print("Loading crossword puzzle...")
    
    puzzle_config = create_sample_puzzle()
    game_state = GameState(puzzle_config)
    
    cli = CrosswordCLI(puzzle_config, game_state)
    
    cli.game_loop()


if __name__ == "__main__":
    main()
