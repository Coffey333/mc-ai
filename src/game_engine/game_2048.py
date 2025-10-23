"""
2048 Game for MC AI V4
Addictive tile-merging puzzle game
"""

import random
from typing import Dict, List, Optional, Tuple

class Game2048:
    """
    Complete 2048 implementation
    """
    
    def __init__(self, size: int = 4):
        """
        Args:
            size: Board size (typically 4x4)
        """
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.best_score = 0
        self.game_over = False
        self.won = False
        self.move_history = []
        
        # Add initial tiles
        self._add_random_tile()
        self._add_random_tile()
    
    def _add_random_tile(self):
        """Add a random 2 or 4 tile to empty cell"""
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    empty_cells.append((row, col))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            # 90% chance of 2, 10% chance of 4
            self.board[row][col] = 2 if random.random() < 0.9 else 4
    
    def move(self, direction: str) -> Dict:
        """
        Move tiles in direction
        
        Args:
            direction: 'up', 'down', 'left', 'right'
        
        Returns:
            Dict with move result
        """
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        # Save board state
        old_board = [row[:] for row in self.board]
        old_score = self.score
        
        # Make move
        moved = False
        if direction == 'left':
            moved = self._move_left()
        elif direction == 'right':
            moved = self._move_right()
        elif direction == 'up':
            moved = self._move_up()
        elif direction == 'down':
            moved = self._move_down()
        else:
            return {'success': False, 'error': 'Invalid direction'}
        
        if not moved:
            return {'success': False, 'error': 'Cannot move in that direction'}
        
        # Add new tile
        self._add_random_tile()
        
        # Record move
        self.move_history.append({
            'direction': direction,
            'board': old_board,
            'score': old_score
        })
        
        # Check win condition
        if not self.won and self._check_win():
            self.won = True
        
        # Check game over
        if self._check_game_over():
            self.game_over = True
        
        # Update best score
        self.best_score = max(self.best_score, self.score)
        
        return {
            'success': True,
            'score': self.score,
            'best_score': self.best_score,
            'won': self.won,
            'game_over': self.game_over
        }
    
    def _move_left(self) -> bool:
        """Move all tiles left"""
        moved = False
        
        for row in range(self.size):
            # Compact tiles
            tiles = [self.board[row][col] for col in range(self.size) if self.board[row][col] != 0]
            
            # Merge tiles
            merged = []
            skip = False
            for i in range(len(tiles)):
                if skip:
                    skip = False
                    continue
                
                if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                    merged.append(tiles[i] * 2)
                    self.score += tiles[i] * 2
                    skip = True
                else:
                    merged.append(tiles[i])
            
            # Fill row
            new_row = merged + [0] * (self.size - len(merged))
            
            # Check if changed
            if new_row != self.board[row]:
                moved = True
                self.board[row] = new_row
        
        return moved
    
    def _move_right(self) -> bool:
        """Move all tiles right"""
        moved = False
        
        for row in range(self.size):
            # Compact tiles (reversed)
            tiles = [self.board[row][col] for col in range(self.size - 1, -1, -1) if self.board[row][col] != 0]
            
            # Merge tiles
            merged = []
            skip = False
            for i in range(len(tiles)):
                if skip:
                    skip = False
                    continue
                
                if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                    merged.append(tiles[i] * 2)
                    self.score += tiles[i] * 2
                    skip = True
                else:
                    merged.append(tiles[i])
            
            # Fill row (reversed)
            new_row = [0] * (self.size - len(merged)) + merged
            
            # Check if changed
            if new_row != self.board[row]:
                moved = True
                self.board[row] = new_row
        
        return moved
    
    def _move_up(self) -> bool:
        """Move all tiles up"""
        moved = False
        
        for col in range(self.size):
            # Compact tiles
            tiles = [self.board[row][col] for row in range(self.size) if self.board[row][col] != 0]
            
            # Merge tiles
            merged = []
            skip = False
            for i in range(len(tiles)):
                if skip:
                    skip = False
                    continue
                
                if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                    merged.append(tiles[i] * 2)
                    self.score += tiles[i] * 2
                    skip = True
                else:
                    merged.append(tiles[i])
            
            # Fill column
            new_col = merged + [0] * (self.size - len(merged))
            
            # Check if changed
            old_col = [self.board[row][col] for row in range(self.size)]
            if new_col != old_col:
                moved = True
                for row in range(self.size):
                    self.board[row][col] = new_col[row]
        
        return moved
    
    def _move_down(self) -> bool:
        """Move all tiles down"""
        moved = False
        
        for col in range(self.size):
            # Compact tiles (reversed)
            tiles = [self.board[row][col] for row in range(self.size - 1, -1, -1) if self.board[row][col] != 0]
            
            # Merge tiles
            merged = []
            skip = False
            for i in range(len(tiles)):
                if skip:
                    skip = False
                    continue
                
                if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                    merged.append(tiles[i] * 2)
                    self.score += tiles[i] * 2
                    skip = True
                else:
                    merged.append(tiles[i])
            
            # Fill column (reversed)
            new_col = [0] * (self.size - len(merged)) + merged
            
            # Check if changed
            old_col = [self.board[row][col] for row in range(self.size)]
            if new_col != old_col:
                moved = True
                for row in range(self.size):
                    self.board[row][col] = new_col[row]
        
        return moved
    
    def _check_win(self) -> bool:
        """Check if 2048 tile reached"""
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] >= 2048:
                    return True
        return False
    
    def _check_game_over(self) -> bool:
        """Check if no moves available"""
        # Check for empty cells
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return False
        
        # Check for possible merges
        for row in range(self.size):
            for col in range(self.size):
                current = self.board[row][col]
                
                # Check right
                if col + 1 < self.size and self.board[row][col + 1] == current:
                    return False
                
                # Check down
                if row + 1 < self.size and self.board[row + 1][col] == current:
                    return False
        
        return True
    
    def undo(self) -> Dict:
        """Undo last move"""
        if not self.move_history:
            return {'success': False, 'error': 'No moves to undo'}
        
        last_move = self.move_history.pop()
        self.board = last_move['board']
        self.score = last_move['score']
        self.game_over = False
        
        return {'success': True}
    
    def get_ai_move(self) -> str:
        """Get AI-suggested move (simple heuristic)"""
        # Try each direction and score the resulting board
        best_direction = None
        best_score = -1
        
        for direction in ['left', 'right', 'up', 'down']:
            # Simulate move
            temp_board = [row[:] for row in self.board]
            temp_game = Game2048(self.size)
            temp_game.board = temp_board
            temp_game.score = self.score
            
            result = temp_game.move(direction)
            
            if result['success']:
                # Score based on: empty cells, max tile position, monotonicity
                score = self._score_board(temp_game.board)
                
                if score > best_score:
                    best_score = score
                    best_direction = direction
        
        return best_direction if best_direction else 'left'
    
    def _score_board(self, board: List[List[int]]) -> float:
        """Score board state for AI"""
        score = 0
        
        # Empty cells (more is better)
        empty_cells = sum(1 for row in board for cell in row if cell == 0)
        score += empty_cells * 100
        
        # Max tile in corner (better)
        max_tile = max(max(row) for row in board)
        if board[0][0] == max_tile or board[0][self.size-1] == max_tile or \
           board[self.size-1][0] == max_tile or board[self.size-1][self.size-1] == max_tile:
            score += 1000
        
        # Monotonicity (tiles should be ordered)
        for row in board:
            for i in range(len(row) - 1):
                if row[i] >= row[i + 1]:
                    score += 10
        
        return score
    
    def display(self) -> str:
        """Display board"""
        output = []
        
        output.append(f"\n2048 Game")
        output.append(f"Score: {self.score} | Best: {self.best_score}")
        output.append("─" * (self.size * 7 + 1))
        
        for row in self.board:
            line = "│"
            for cell in row:
                if cell == 0:
                    line += "      │"
                else:
                    line += f" {cell:4} │"
            output.append(line)
            output.append("─" * (self.size * 7 + 1))
        
        if self.won:
            output.append("\n🎉 YOU REACHED 2048! 🎉")
        
        if self.game_over:
            output.append("\n💥 GAME OVER 💥")
        
        output.append("\nControls: up, down, left, right")
        
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'board': self.board,
            'score': self.score,
            'best_score': self.best_score,
            'game_over': self.game_over,
            'won': self.won,
            'size': self.size,
            'move_history': len(self.move_history)
        }
