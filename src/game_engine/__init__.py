"""
MC AI V4 Game Engine
Complete game library with multiple games and AI opponents
"""

from src.game_engine.chess import ChessGame
from src.game_engine.risk import RiskGame
from src.game_engine.tic_tac_toe_advanced import TicTacToeAdvanced
from src.game_engine.minesweeper import Minesweeper
from src.game_engine.game_2048 import Game2048
from src.game_engine.blackjack import Blackjack
from src.game_engine.crossword import CrosswordPuzzle
from src.game_engine.game_manager import GameManager

__all__ = [
    'ChessGame',
    'RiskGame',
    'TicTacToeAdvanced',
    'Minesweeper',
    'Game2048',
    'Blackjack',
    'CrosswordPuzzle',
    'GameManager'
]
