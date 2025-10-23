"""
Complete Chess Implementation for MC AI V4
Full rules, move validation, AI with minimax + alpha-beta pruning
"""

from typing import Dict, List, Optional, Tuple, Set
import copy

class ChessGame:
    """
    Complete chess implementation with AI
    """
    
    def __init__(self):
        self.board = self._initialize_board()
        self.current_player = 'white'
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.game_over = False
        self.winner = None
        
        # Game state tracking
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.en_passant_target = None
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1
        
        # Check/checkmate status
        self.in_check = False
        self.checkmate = False
        self.stalemate = False
    
    def _initialize_board(self) -> List[List[Optional[Dict]]]:
        """Create starting chess board"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Piece notation: type, color
        # Pawns
        for col in range(8):
            board[1][col] = {'type': 'pawn', 'color': 'black'}
            board[6][col] = {'type': 'pawn', 'color': 'white'}
        
        # Other pieces
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        
        for col, piece_type in enumerate(back_row):
            board[0][col] = {'type': piece_type, 'color': 'black'}
            board[7][col] = {'type': piece_type, 'color': 'white'}
        
        return board
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                  promotion: str = 'queen') -> Dict:
        """
        Make a move
        
        Args:
            from_pos: (row, col) starting position
            to_pos: (row, col) ending position
            promotion: Piece type for pawn promotion
        
        Returns:
            Dict with move result
        """
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Validate positions
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and
                0 <= to_row < 8 and 0 <= to_col < 8):
            return {'success': False, 'error': 'Invalid position'}
        
        piece = self.board[from_row][from_col]
        
        # Check if piece exists and belongs to current player
        if not piece or piece['color'] != self.current_player:
            return {'success': False, 'error': 'Invalid piece selection'}
        
        # Get valid moves for this piece
        valid_moves = self.get_valid_moves(from_pos)
        
        if to_pos not in valid_moves:
            return {'success': False, 'error': 'Invalid move'}
        
        # Make the move
        captured = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Handle special moves
        move_type = 'normal'
        
        # Castling
        if piece['type'] == 'king' and abs(to_col - from_col) == 2:
            move_type = 'castling'
            # Move rook
            if to_col > from_col:  # Kingside
                self.board[to_row][5] = self.board[to_row][7]
                self.board[to_row][7] = None
            else:  # Queenside
                self.board[to_row][3] = self.board[to_row][0]
                self.board[to_row][0] = None
        
        # En passant
        if piece['type'] == 'pawn' and to_pos == self.en_passant_target:
            move_type = 'en_passant'
            # Capture the pawn
            capture_row = from_row
            self.board[capture_row][to_col] = None
            captured = {'type': 'pawn', 'color': 'black' if self.current_player == 'white' else 'white'}
        
        # Pawn promotion
        if piece['type'] == 'pawn' and (to_row == 0 or to_row == 7):
            move_type = 'promotion'
            self.board[to_row][to_col] = {'type': promotion, 'color': self.current_player}
        
        # Update en passant target
        self.en_passant_target = None
        if piece['type'] == 'pawn' and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        
        # Update castling rights
        if piece['type'] == 'king':
            self.castling_rights[self.current_player]['kingside'] = False
            self.castling_rights[self.current_player]['queenside'] = False
        elif piece['type'] == 'rook':
            if from_col == 0:
                self.castling_rights[self.current_player]['queenside'] = False
            elif from_col == 7:
                self.castling_rights[self.current_player]['kingside'] = False
        
        # Track captured pieces
        if captured:
            self.captured_pieces[self.current_player].append(captured['type'])
        
        # Update move counters
        if piece['type'] == 'pawn' or captured:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        # Record move
        move_notation = self._get_algebraic_notation(from_pos, to_pos, piece, captured, move_type)
        self.move_history.append({
            'from': from_pos,
            'to': to_pos,
            'piece': piece['type'],
            'captured': captured['type'] if captured else None,
            'notation': move_notation,
            'move_type': move_type
        })
        
        # Switch players
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'
            self.fullmove_number += 1
        
        # Check game end conditions
        self._update_game_status()
        
        result = {
            'success': True,
            'move_notation': move_notation,
            'captured': captured['type'] if captured else None,
            'in_check': self.in_check,
            'checkmate': self.checkmate,
            'stalemate': self.stalemate,
            'game_over': self.game_over
        }
        
        if self.game_over:
            result['winner'] = self.winner
        
        return result
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get all valid moves for piece at position"""
        row, col = pos
        piece = self.board[row][col]
        
        if not piece:
            return []
        
        # Get pseudo-legal moves (not considering check)
        if piece['type'] == 'pawn':
            moves = self._get_pawn_moves(pos)
        elif piece['type'] == 'knight':
            moves = self._get_knight_moves(pos)
        elif piece['type'] == 'bishop':
            moves = self._get_bishop_moves(pos)
        elif piece['type'] == 'rook':
            moves = self._get_rook_moves(pos)
        elif piece['type'] == 'queen':
            moves = self._get_queen_moves(pos)
        elif piece['type'] == 'king':
            moves = self._get_king_moves(pos)
        else:
            moves = []
        
        # Filter out moves that would leave king in check
        legal_moves = []
        for move in moves:
            if self._is_legal_move(pos, move):
                legal_moves.append(move)
        
        return legal_moves
    
    def _get_pawn_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get pawn moves"""
        row, col = pos
        piece = self.board[row][col]
        moves = []
        
        direction = -1 if piece['color'] == 'white' else 1
        start_row = 6 if piece['color'] == 'white' else 1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 8 and not self.board[new_row][col]:
            moves.append((new_row, col))
            
            # Double move from starting position
            if row == start_row:
                new_row2 = row + 2 * direction
                if not self.board[new_row2][col]:
                    moves.append((new_row2, col))
        
        # Captures
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_col < 8:
                new_row = row + direction
                if 0 <= new_row < 8:
                    target = self.board[new_row][new_col]
                    if target and target['color'] != piece['color']:
                        moves.append((new_row, new_col))
                    
                    # En passant
                    if (new_row, new_col) == self.en_passant_target:
                        moves.append((new_row, new_col))
        
        return moves
    
    def _get_knight_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get knight moves"""
        row, col = pos
        piece = self.board[row][col]
        moves = []
        
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if not target or target['color'] != piece['color']:
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_bishop_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get bishop moves"""
        return self._get_sliding_moves(pos, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
    
    def _get_rook_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get rook moves"""
        return self._get_sliding_moves(pos, [(-1, 0), (1, 0), (0, -1), (0, 1)])
    
    def _get_queen_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get queen moves"""
        return self._get_sliding_moves(pos, [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ])
    
    def _get_sliding_moves(self, pos: Tuple[int, int], 
                          directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Get moves for sliding pieces (bishop, rook, queen)"""
        row, col = pos
        piece = self.board[row][col]
        moves = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                
                if not target:
                    moves.append((new_row, new_col))
                elif target['color'] != piece['color']:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                
                new_row += dr
                new_col += dc
        
        return moves
    
    def _get_king_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get king moves including castling"""
        row, col = pos
        piece = self.board[row][col]
        moves = []
        
        # Normal king moves
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if not target or target['color'] != piece['color']:
                        moves.append((new_row, new_col))
        
        # Castling
        if not self._is_square_attacked(pos, piece['color']):
            # Kingside
            if self.castling_rights[piece['color']]['kingside']:
                if (not self.board[row][5] and not self.board[row][6] and
                    not self._is_square_attacked((row, 5), piece['color']) and
                    not self._is_square_attacked((row, 6), piece['color'])):
                    moves.append((row, 6))
            
            # Queenside
            if self.castling_rights[piece['color']]['queenside']:
                if (not self.board[row][1] and not self.board[row][2] and 
                    not self.board[row][3] and
                    not self._is_square_attacked((row, 2), piece['color']) and
                    not self._is_square_attacked((row, 3), piece['color'])):
                    moves.append((row, 2))
        
        return moves
    
    def _is_legal_move(self, from_pos: Tuple[int, int], 
                      to_pos: Tuple[int, int]) -> bool:
        """Check if move is legal (doesn't leave king in check)"""
        # Make temporary move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Find king position
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p['type'] == 'king' and p['color'] == piece['color']:
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        
        # Check if king is in check
        in_check = self._is_square_attacked(king_pos, piece['color'])
        
        # Undo move
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured
        
        return not in_check
    
    def _is_square_attacked(self, pos: Tuple[int, int], color: str) -> bool:
        """Check if square is attacked by opponent"""
        row, col = pos
        opponent = 'black' if color == 'white' else 'white'
        
        # Check all opponent pieces
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece['color'] == opponent:
                    # Get moves for this piece (without legal move checking to avoid recursion)
                    if piece['type'] == 'pawn':
                        moves = self._get_pawn_attack_squares((r, c))
                    elif piece['type'] == 'knight':
                        moves = self._get_knight_moves((r, c))
                    elif piece['type'] == 'bishop':
                        moves = self._get_bishop_moves((r, c))
                    elif piece['type'] == 'rook':
                        moves = self._get_rook_moves((r, c))
                    elif piece['type'] == 'queen':
                        moves = self._get_queen_moves((r, c))
                    elif piece['type'] == 'king':
                        moves = self._get_king_attack_squares((r, c))
                    else:
                        moves = []
                    
                    if pos in moves:
                        return True
        
        return False
    
    def _get_pawn_attack_squares(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get squares attacked by pawn"""
        row, col = pos
        piece = self.board[row][col]
        squares = []
        
        direction = -1 if piece['color'] == 'white' else 1
        
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                squares.append((new_row, new_col))
        
        return squares
    
    def _get_king_attack_squares(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get squares attacked by king"""
        row, col = pos
        squares = []
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    squares.append((new_row, new_col))
        
        return squares
    
    def _update_game_status(self):
        """Update check, checkmate, stalemate status"""
        # Find king
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece['type'] == 'king' and piece['color'] == self.current_player:
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        
        # Check if in check
        self.in_check = self._is_square_attacked(king_pos, self.current_player)
        
        # Check if any legal moves available
        has_legal_moves = False
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece['color'] == self.current_player:
                    if self.get_valid_moves((r, c)):
                        has_legal_moves = True
                        break
            if has_legal_moves:
                break
        
        if not has_legal_moves:
            if self.in_check:
                self.checkmate = True
                self.game_over = True
                self.winner = 'black' if self.current_player == 'white' else 'white'
            else:
                self.stalemate = True
                self.game_over = True
                self.winner = 'draw'
        
        # Check 50-move rule
        if self.halfmove_clock >= 100:  # 50 moves per player
            self.game_over = True
            self.winner = 'draw'
    
    def _get_algebraic_notation(self, from_pos: Tuple[int, int], 
                               to_pos: Tuple[int, int],
                               piece: Dict, captured: Optional[Dict],
                               move_type: str) -> str:
        """Convert move to algebraic notation"""
        files = 'abcdefgh'
        ranks = '87654321'
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        notation = ''
        
        # Castling
        if move_type == 'castling':
            return 'O-O' if to_col > from_col else 'O-O-O'
        
        # Piece prefix
        if piece['type'] != 'pawn':
            notation += piece['type'][0].upper()
        elif captured:
            notation += files[from_col]
        
        # Capture
        if captured:
            notation += 'x'
        
        # Destination
        notation += files[to_col] + ranks[to_row]
        
        # Promotion
        if move_type == 'promotion':
            notation += '=Q'  # Simplified - always queen
        
        return notation
    
    def get_ai_move(self, difficulty: str = 'medium', 
                   max_depth: int = 3) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get AI move using minimax with alpha-beta pruning
        
        Args:
            difficulty: 'easy', 'medium', 'hard'
            max_depth: Search depth (higher = stronger but slower)
        
        Returns:
            (from_pos, to_pos) or None
        """
        if difficulty == 'easy':
            depth = 1
        elif difficulty == 'medium':
            depth = 2
        else:
            depth = max_depth
        
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Get all possible moves
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece['color'] == self.current_player:
                    valid_moves = self.get_valid_moves((r, c))
                    
                    for to_pos in valid_moves:
                        # Make move
                        from_pos = (r, c)
                        captured = self.board[to_pos[0]][to_pos[1]]
                        self.board[to_pos[0]][to_pos[1]] = piece
                        self.board[r][c] = None
                        
                        # Evaluate
                        value = self._minimax(depth - 1, alpha, beta, False)
                        
                        # Undo move
                        self.board[r][c] = piece
                        self.board[to_pos[0]][to_pos[1]] = captured
                        
                        if value > best_value:
                            best_value = value
                            best_move = (from_pos, to_pos)
                        
                        alpha = max(alpha, value)
        
        return best_move
    
    def _minimax(self, depth: int, alpha: float, beta: float, 
                maximizing: bool) -> float:
        """Minimax with alpha-beta pruning"""
        if depth == 0:
            return self._evaluate_board()
        
        player = self.current_player if maximizing else ('black' if self.current_player == 'white' else 'white')
        
        if maximizing:
            max_eval = float('-inf')
            
            for r in range(8):
                for c in range(8):
                    piece = self.board[r][c]
                    if piece and piece['color'] == player:
                        valid_moves = self.get_valid_moves((r, c))
                        
                        for to_pos in valid_moves:
                            # Make move
                            captured = self.board[to_pos[0]][to_pos[1]]
                            self.board[to_pos[0]][to_pos[1]] = piece
                            self.board[r][c] = None
                            
                            # Recurse
                            eval = self._minimax(depth - 1, alpha, beta, False)
                            
                            # Undo
                            self.board[r][c] = piece
                            self.board[to_pos[0]][to_pos[1]] = captured
                            
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            
                            if beta <= alpha:
                                break
            
            return max_eval
        else:
            min_eval = float('inf')
            
            for r in range(8):
                for c in range(8):
                    piece = self.board[r][c]
                    if piece and piece['color'] == player:
                        valid_moves = self.get_valid_moves((r, c))
                        
                        for to_pos in valid_moves:
                            # Make move
                            captured = self.board[to_pos[0]][to_pos[1]]
                            self.board[to_pos[0]][to_pos[1]] = piece
                            self.board[r][c] = None
                            
                            # Recurse
                            eval = self._minimax(depth - 1, alpha, beta, True)
                            
                            # Undo
                            self.board[r][c] = piece
                            self.board[to_pos[0]][to_pos[1]] = captured
                            
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            
                            if beta <= alpha:
                                break
            
            return min_eval
    
    def _evaluate_board(self) -> float:
        """Evaluate board position"""
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0
        }
        
        score = 0
        
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece:
                    value = piece_values[piece['type']]
                    
                    # Position bonuses
                    if piece['type'] == 'pawn':
                        # Pawns more valuable as they advance
                        if piece['color'] == 'white':
                            value += (6 - r) * 0.1
                        else:
                            value += (r - 1) * 0.1
                    
                    elif piece['type'] == 'knight' or piece['type'] == 'bishop':
                        # Knights and bishops better in center
                        center_distance = abs(r - 3.5) + abs(c - 3.5)
                        value += (7 - center_distance) * 0.1
                    
                    if piece['color'] == self.current_player:
                        score += value
                    else:
                        score -= value
        
        return score
    
    def display(self) -> str:
        """Display board"""
        piece_symbols = {
            ('pawn', 'white'): '♙', ('pawn', 'black'): '♟',
            ('knight', 'white'): '♘', ('knight', 'black'): '♞',
            ('bishop', 'white'): '♗', ('bishop', 'black'): '♝',
            ('rook', 'white'): '♖', ('rook', 'black'): '♜',
            ('queen', 'white'): '♕', ('queen', 'black'): '♛',
            ('king', 'white'): '♔', ('king', 'black'): '♚'
        }
        
        output = []
        output.append("\n  a b c d e f g h")
        output.append(" ┌─────────────────┐")
        
        for row in range(8):
            line = f"{8-row}│"
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    symbol = piece_symbols[(piece['type'], piece['color'])]
                else:
                    symbol = '·' if (row + col) % 2 == 0 else ' '
                line += f" {symbol}"
            line += f" │{8-row}"
            output.append(line)
        
        output.append(" └─────────────────┘")
        output.append("  a b c d e f g h")
        
        # Game info
        output.append(f"\nCurrent player: {self.current_player.capitalize()}")
        if self.in_check:
            output.append("CHECK!")
        if self.checkmate:
            output.append(f"CHECKMATE! {self.winner.capitalize()} wins!")
        if self.stalemate:
            output.append("STALEMATE!")
        
        # Captured pieces
        if self.captured_pieces['white']:
            output.append(f"White captured: {', '.join(self.captured_pieces['white'])}")
        if self.captured_pieces['black']:
            output.append(f"Black captured: {', '.join(self.captured_pieces['black'])}")
        
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'in_check': self.in_check,
            'checkmate': self.checkmate,
            'stalemate': self.stalemate,
            'game_over': self.game_over,
            'winner': self.winner,
            'move_history': self.move_history,
            'captured_pieces': self.captured_pieces
        }
