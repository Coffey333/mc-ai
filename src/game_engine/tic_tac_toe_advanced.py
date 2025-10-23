"""
Advanced Tic-Tac-Toe Suite for MC AI V4
- Classic 3x3 with perfect AI
- Ultimate Tic-Tac-Toe
- 5x5 variant
"""

import copy
from typing import Dict, List, Optional, Tuple
import random

class TicTacToeAdvanced:
    """
    Multiple Tic-Tac-Toe variants with AI
    """
    
    def __init__(self, variant: str = 'classic'):
        """
        Args:
            variant: 'classic', 'ultimate', or '5x5'
        """
        self.variant = variant
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        if self.variant == 'classic':
            self.board = [[' ' for _ in range(3)] for _ in range(3)]
            self.size = 3
        elif self.variant == '5x5':
            self.board = [[' ' for _ in range(5)] for _ in range(5)]
            self.size = 5
        elif self.variant == 'ultimate':
            # 9 small boards
            self.board = [
                [[' ' for _ in range(3)] for _ in range(3)]
                for _ in range(9)
            ]
            self.meta_board = [[' ' for _ in range(3)] for _ in range(3)]
            self.active_board = None  # None means any board
        
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def make_move(self, row: int, col: int, board_idx: int = None) -> Dict:
        """
        Make a move
        
        Args:
            row, col: Position
            board_idx: For ultimate variant (0-8)
        
        Returns:
            Dict with move result
        """
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        if self.variant == 'ultimate':
            return self._make_ultimate_move(row, col, board_idx)
        else:
            return self._make_classic_move(row, col)
    
    def _make_classic_move(self, row: int, col: int) -> Dict:
        """Make move in classic or 5x5 variant"""
        # Validate move
        if not (0 <= row < self.size and 0 <= col < self.size):
            return {'success': False, 'error': 'Invalid position'}
        
        if self.board[row][col] != ' ':
            return {'success': False, 'error': 'Position occupied'}
        
        # Make move
        self.board[row][col] = self.current_player
        self.move_history.append((row, col, self.current_player))
        
        # Check win
        if self._check_win(self.board, self.current_player):
            self.game_over = True
            self.winner = self.current_player
            return {
                'success': True,
                'game_over': True,
                'winner': self.winner,
                'winning_line': self._get_winning_line(self.board)
            }
        
        # Check draw
        if self._is_board_full(self.board):
            self.game_over = True
            return {
                'success': True,
                'game_over': True,
                'winner': 'Draw'
            }
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return {'success': True, 'game_over': False}
    
    def _make_ultimate_move(self, row: int, col: int, board_idx: int) -> Dict:
        """Make move in ultimate tic-tac-toe"""
        # Validate board selection
        if self.active_board is not None and board_idx != self.active_board:
            return {'success': False, 'error': f'Must play in board {self.active_board}'}
        
        # Check if selected board is already won
        board_row = board_idx // 3
        board_col = board_idx % 3
        if self.meta_board[board_row][board_col] != ' ':
            return {'success': False, 'error': 'Board already won'}
        
        # Validate position
        if not (0 <= row < 3 and 0 <= col < 3):
            return {'success': False, 'error': 'Invalid position'}
        
        if self.board[board_idx][row][col] != ' ':
            return {'success': False, 'error': 'Position occupied'}
        
        # Make move
        self.board[board_idx][row][col] = self.current_player
        self.move_history.append((board_idx, row, col, self.current_player))
        
        # Check if small board is won
        if self._check_win(self.board[board_idx], self.current_player):
            self.meta_board[board_row][board_col] = self.current_player
            
            # Check if meta board is won
            if self._check_win(self.meta_board, self.current_player):
                self.game_over = True
                self.winner = self.current_player
                return {
                    'success': True,
                    'game_over': True,
                    'winner': self.winner
                }
        
        # Set next active board
        next_board_idx = row * 3 + col
        next_board_row = next_board_idx // 3
        next_board_col = next_board_idx % 3
        
        # If next board is won or full, allow any board
        if (self.meta_board[next_board_row][next_board_col] != ' ' or
            self._is_board_full(self.board[next_board_idx])):
            self.active_board = None
        else:
            self.active_board = next_board_idx
        
        # Check meta board draw
        if all(self.meta_board[i][j] != ' ' for i in range(3) for j in range(3)):
            self.game_over = True
            return {
                'success': True,
                'game_over': True,
                'winner': 'Draw'
            }
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return {
            'success': True,
            'game_over': False,
            'next_board': self.active_board
        }
    
    def get_ai_move(self, difficulty: str = 'hard') -> Tuple[int, int, Optional[int]]:
        """
        Get AI move
        
        Args:
            difficulty: 'easy', 'medium', 'hard'
        
        Returns:
            (row, col) for classic/5x5, (board_idx, row, col) for ultimate
        """
        if self.variant == 'ultimate':
            return self._get_ultimate_ai_move(difficulty)
        else:
            return self._get_classic_ai_move(difficulty)
    
    def _get_classic_ai_move(self, difficulty: str) -> Tuple[int, int]:
        """Get AI move for classic/5x5"""
        if difficulty == 'easy':
            # Random move
            empty = [(i, j) for i in range(self.size) 
                    for j in range(self.size) 
                    if self.board[i][j] == ' ']
            return random.choice(empty) if empty else (0, 0)
        
        elif difficulty == 'medium':
            # 50% perfect, 50% random
            if random.random() < 0.5:
                return self._get_classic_ai_move('hard')
            else:
                return self._get_classic_ai_move('easy')
        
        else:  # hard
            # Minimax algorithm
            best_score = float('-inf')
            best_move = None
            
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == ' ':
                        # Try move
                        self.board[i][j] = self.current_player
                        score = self._minimax(self.board, 0, False)
                        self.board[i][j] = ' '
                        
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            
            return best_move if best_move else (0, 0)
    
    def _get_ultimate_ai_move(self, difficulty: str) -> Tuple[int, int, int]:
        """Get AI move for ultimate tic-tac-toe"""
        # Simplified AI for ultimate variant
        if self.active_board is not None:
            # Must play in specific board
            available_boards = [self.active_board]
        else:
            # Can play in any unwon board
            available_boards = []
            for idx in range(9):
                board_row = idx // 3
                board_col = idx % 3
                if self.meta_board[board_row][board_col] == ' ':
                    available_boards.append(idx)
        
        # Find best move across available boards
        best_score = float('-inf')
        best_move = None
        
        for board_idx in available_boards:
            for i in range(3):
                for j in range(3):
                    if self.board[board_idx][i][j] == ' ':
                        # Simple scoring
                        score = self._score_ultimate_move(board_idx, i, j)
                        
                        if score > best_score:
                            best_score = score
                            best_move = (board_idx, i, j)
        
        return best_move if best_move else (available_boards[0], 0, 0)
    
    def _minimax(self, board: List[List[str]], depth: int, 
                is_maximizing: bool) -> int:
        """Minimax algorithm for perfect AI"""
        # Check terminal states
        if self._check_win(board, self.current_player):
            return 10 - depth
        if self._check_win(board, 'X' if self.current_player == 'O' else 'O'):
            return depth - 10
        if self._is_board_full(board):
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == ' ':
                        board[i][j] = self.current_player
                        score = self._minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            opponent = 'X' if self.current_player == 'O' else 'O'
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == ' ':
                        board[i][j] = opponent
                        score = self._minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score
    
    def _score_ultimate_move(self, board_idx: int, row: int, col: int) -> int:
        """Score a move in ultimate tic-tac-toe"""
        score = 0
        
        # Prioritize winning small board
        temp_board = copy.deepcopy(self.board[board_idx])
        temp_board[row][col] = self.current_player
        if self._check_win(temp_board, self.current_player):
            score += 100
        
        # Prioritize center
        if row == 1 and col == 1:
            score += 10
        
        # Prioritize corners
        if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            score += 5
        
        return score
    
    def _check_win(self, board: List[List[str]], player: str) -> bool:
        """Check if player has won on given board"""
        size = len(board)
        
        # Check rows and columns
        for i in range(size):
            if all(board[i][j] == player for j in range(size)):
                return True
            if all(board[j][i] == player for j in range(size)):
                return True
        
        # Check diagonals
        if all(board[i][i] == player for i in range(size)):
            return True
        if all(board[i][size-1-i] == player for i in range(size)):
            return True
        
        return False
    
    def _is_board_full(self, board: List[List[str]]) -> bool:
        """Check if board is full"""
        return all(board[i][j] != ' ' 
                  for i in range(len(board)) 
                  for j in range(len(board[0])))
    
    def _get_winning_line(self, board: List[List[str]]) -> Optional[List[Tuple[int, int]]]:
        """Get coordinates of winning line"""
        size = len(board)
        player = self.winner
        
        # Check rows
        for i in range(size):
            if all(board[i][j] == player for j in range(size)):
                return [(i, j) for j in range(size)]
        
        # Check columns
        for j in range(size):
            if all(board[i][j] == player for i in range(size)):
                return [(i, j) for i in range(size)]
        
        # Check diagonals
        if all(board[i][i] == player for i in range(size)):
            return [(i, i) for i in range(size)]
        
        if all(board[i][size-1-i] == player for i in range(size)):
            return [(i, size-1-i) for i in range(size)]
        
        return None
    
    def display(self) -> str:
        """Display board as string"""
        if self.variant == 'ultimate':
            return self._display_ultimate()
        else:
            return self._display_classic()
    
    def _display_classic(self) -> str:
        """Display classic/5x5 board"""
        output = []
        
        for i, row in enumerate(self.board):
            output.append(' | '.join(row))
            if i < self.size - 1:
                output.append('-' * (self.size * 4 - 1))
        
        return '\n'.join(output)
    
    def _display_ultimate(self) -> str:
        """Display ultimate tic-tac-toe"""
        output = []
        output.append("Ultimate Tic-Tac-Toe:")
        output.append("\nMeta Board:")
        output.append(self._display_classic_board(self.meta_board))
        
        output.append("\nSmall Boards:")
        for i in range(3):
            row_boards = []
            for j in range(3):
                board_idx = i * 3 + j
                board_str = self._display_classic_board(self.board[board_idx])
                row_boards.append(board_str.split('\n'))
            
            # Combine horizontally
            for line_idx in range(len(row_boards[0])):
                line_parts = [row_boards[j][line_idx] for j in range(3)]
                output.append('  ||  '.join(line_parts))
            
            if i < 2:
                output.append('=' * 40)
        
        if self.active_board is not None:
            output.append(f"\n► Next move must be in board {self.active_board}")
        
        return '\n'.join(output)
    
    def _display_classic_board(self, board: List[List[str]]) -> str:
        """Helper to display a single 3x3 board"""
        output = []
        for i, row in enumerate(board):
            output.append(' | '.join(row))
            if i < 2:
                output.append('-' * 9)
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'variant': self.variant,
            'board': self.board,
            'meta_board': self.meta_board if self.variant == 'ultimate' else None,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'active_board': self.active_board if self.variant == 'ultimate' else None,
            'move_history': self.move_history
        }
