"""
Minesweeper for MC AI V4
Classic mine-sweeping puzzle game with hints
"""

import random
from typing import Dict, List, Tuple, Set

class Minesweeper:
    """
    Complete Minesweeper implementation
    """
    
    def __init__(self, difficulty: str = 'beginner'):
        """
        Args:
            difficulty: 'beginner', 'intermediate', 'expert', 'custom'
        """
        self.difficulty = difficulty
        
        # Set board parameters
        if difficulty == 'beginner':
            self.rows, self.cols, self.num_mines = 9, 9, 10
        elif difficulty == 'intermediate':
            self.rows, self.cols, self.num_mines = 16, 16, 40
        elif difficulty == 'expert':
            self.rows, self.cols, self.num_mines = 16, 30, 99
        else:  # custom
            self.rows, self.cols, self.num_mines = 10, 10, 15
        
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.mines = set()
        self.game_over = False
        self.won = False
        self.first_click = True
        self.cells_revealed = 0
        self.flags_placed = 0
        self.move_history = []
    
    def _place_mines(self, safe_row: int, safe_col: int):
        """Place mines ensuring first click is safe"""
        # Safe zone: first click and adjacent cells
        safe_cells = {(safe_row, safe_col)}
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = safe_row + dr, safe_col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    safe_cells.add((r, c))
        
        # Place mines
        placed = 0
        while placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            if (row, col) not in safe_cells and (row, col) not in self.mines:
                self.mines.add((row, col))
                self.board[row][col] = -1  # -1 represents mine
                placed += 1
        
        # Calculate numbers
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            r, c = row + dr, col + dc
                            if 0 <= r < self.rows and 0 <= c < self.cols:
                                if self.board[r][c] == -1:
                                    count += 1
                    self.board[row][col] = count
    
    def reveal(self, row: int, col: int) -> Dict:
        """
        Reveal a cell
        
        Args:
            row, col: Cell position
        
        Returns:
            Dict with result
        """
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return {'success': False, 'error': 'Invalid position'}
        
        if self.revealed[row][col]:
            return {'success': False, 'error': 'Already revealed'}
        
        if self.flagged[row][col]:
            return {'success': False, 'error': 'Cell is flagged'}
        
        # First click - place mines
        if self.first_click:
            self._place_mines(row, col)
            self.first_click = False
        
        # Hit mine
        if self.board[row][col] == -1:
            self.revealed[row][col] = True
            self.game_over = True
            self._reveal_all_mines()
            self.move_history.append({'action': 'reveal', 'pos': (row, col), 'result': 'mine'})
            return {
                'success': True,
                'mine': True,
                'game_over': True,
                'won': False
            }
        
        # Reveal cell(s)
        self._reveal_cell(row, col)
        self.move_history.append({'action': 'reveal', 'pos': (row, col), 'result': 'safe'})
        
        # Check win
        total_cells = self.rows * self.cols
        if self.cells_revealed == total_cells - self.num_mines:
            self.game_over = True
            self.won = True
            return {
                'success': True,
                'mine': False,
                'game_over': True,
                'won': True
            }
        
        return {
            'success': True,
            'mine': False,
            'game_over': False,
            'cells_revealed': self.cells_revealed
        }
    
    def _reveal_cell(self, row: int, col: int):
        """Recursively reveal cells"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        
        if self.revealed[row][col] or self.flagged[row][col]:
            return
        
        self.revealed[row][col] = True
        self.cells_revealed += 1
        
        # If cell has no adjacent mines, reveal neighbors
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self._reveal_cell(row + dr, col + dc)
    
    def toggle_flag(self, row: int, col: int) -> Dict:
        """Toggle flag on cell"""
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return {'success': False, 'error': 'Invalid position'}
        
        if self.revealed[row][col]:
            return {'success': False, 'error': 'Cannot flag revealed cell'}
        
        self.flagged[row][col] = not self.flagged[row][col]
        
        if self.flagged[row][col]:
            self.flags_placed += 1
        else:
            self.flags_placed -= 1
        
        self.move_history.append({
            'action': 'flag' if self.flagged[row][col] else 'unflag',
            'pos': (row, col)
        })
        
        return {
            'success': True,
            'flagged': self.flagged[row][col],
            'flags_remaining': self.num_mines - self.flags_placed
        }
    
    def chord(self, row: int, col: int) -> Dict:
        """
        Chord - reveal all adjacent cells if flags match number
        
        Args:
            row, col: Center cell
        
        Returns:
            Dict with result
        """
        if not self.revealed[row][col]:
            return {'success': False, 'error': 'Cell not revealed'}
        
        if self.board[row][col] == 0:
            return {'success': False, 'error': 'No adjacent mines'}
        
        # Count adjacent flags
        flag_count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.flagged[r][c]:
                        flag_count += 1
        
        # Flags must match number
        if flag_count != self.board[row][col]:
            return {'success': False, 'error': 'Flags do not match number'}
        
        # Reveal all unflagged adjacent cells
        revealed_cells = []
        hit_mine = False
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if not self.revealed[r][c] and not self.flagged[r][c]:
                        if self.board[r][c] == -1:
                            hit_mine = True
                            self.game_over = True
                            self._reveal_all_mines()
                        else:
                            self._reveal_cell(r, c)
                        revealed_cells.append((r, c))
        
        return {
            'success': True,
            'revealed_cells': revealed_cells,
            'mine': hit_mine,
            'game_over': hit_mine
        }
    
    def get_hint(self) -> Dict:
        """Get a safe cell to reveal"""
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        # Find a safe unrevealed cell
        safe_cells = []
        
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col] and not self.flagged[row][col]:
                    if self.board[row][col] != -1:
                        # Prioritize cells adjacent to revealed cells
                        adjacent_to_revealed = False
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                r, c = row + dr, col + dc
                                if 0 <= r < self.rows and 0 <= c < self.cols:
                                    if self.revealed[r][c]:
                                        adjacent_to_revealed = True
                                        break
                            if adjacent_to_revealed:
                                break
                        
                        if adjacent_to_revealed:
                            safe_cells.append((row, col))
        
        if not safe_cells:
            # Fall back to any safe cell
            for row in range(self.rows):
                for col in range(self.cols):
                    if not self.revealed[row][col] and self.board[row][col] != -1:
                        safe_cells.append((row, col))
        
        if safe_cells:
            hint = random.choice(safe_cells)
            return {
                'success': True,
                'hint': hint,
                'message': f"Try cell ({hint[0]}, {hint[1]})"
            }
        
        return {'success': False, 'error': 'No hints available'}
    
    def _reveal_all_mines(self):
        """Reveal all mines (game over)"""
        for row, col in self.mines:
            self.revealed[row][col] = True
    
    def display(self) -> str:
        """Display board"""
        output = []
        
        # Header
        output.append(f"\nMinesweeper - {self.difficulty.capitalize()}")
        output.append(f"Mines: {self.num_mines} | Flags: {self.flags_placed} | "
                     f"Remaining: {self.num_mines - self.flags_placed}")
        
        # Column numbers
        col_header = "   " + " ".join(f"{i:2}" for i in range(self.cols))
        output.append(col_header)
        
        # Board
        for row in range(self.rows):
            line = f"{row:2} "
            for col in range(self.cols):
                if self.flagged[row][col]:
                    line += " 🚩"
                elif not self.revealed[row][col]:
                    line += " ◻️"
                elif self.board[row][col] == -1:
                    line += " 💣"
                elif self.board[row][col] == 0:
                    line += "  "
                else:
                    # Number with color coding
                    num = self.board[row][col]
                    colors = ['', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
                    line += f" {colors[num] if num < len(colors) else str(num)}"
            output.append(line)
        
        # Game status
        if self.game_over:
            if self.won:
                output.append("\n🎉 YOU WIN! 🎉")
            else:
                output.append("\n💥 GAME OVER 💥")
        
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'difficulty': self.difficulty,
            'rows': self.rows,
            'cols': self.cols,
            'num_mines': self.num_mines,
            'board': self.board,
            'revealed': self.revealed,
            'flagged': self.flagged,
            'game_over': self.game_over,
            'won': self.won,
            'cells_revealed': self.cells_revealed,
            'flags_placed': self.flags_placed,
            'move_history': self.move_history
        }
