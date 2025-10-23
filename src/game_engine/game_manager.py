"""
Game Manager - Central hub for all games in MC AI V4
Handles save/load, statistics, leaderboards
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import pickle

# Import all games
from src.game_engine.chess import ChessGame
from src.game_engine.risk import RiskGame
from src.game_engine.tic_tac_toe_advanced import TicTacToeAdvanced
from src.game_engine.minesweeper import Minesweeper
from src.game_engine.game_2048 import Game2048
from src.game_engine.blackjack import Blackjack
from src.game_engine.crossword import CrosswordPuzzle

class GameManager:
    """
    Central game management system
    """
    
    def __init__(self):
        self.save_path = "/mnt/user-data/game_saves"
        self.stats_path = "/mnt/user-data/game_stats"
        os.makedirs(self.save_path, exist_ok=True)
        os.makedirs(self.stats_path, exist_ok=True)
        
        self.current_game = None
        self.current_game_type = None
        
        # Available games
        self.available_games = {
            'chess': {
                'name': 'Chess',
                'description': 'Classic strategy board game',
                'class': ChessGame,
                'emoji': '♟️'
            },
            'risk': {
                'name': 'Risk',
                'description': 'World domination strategy',
                'class': RiskGame,
                'emoji': '🌍'
            },
            'tictactoe': {
                'name': 'Tic-Tac-Toe',
                'description': 'Classic X and O game with variants',
                'class': TicTacToeAdvanced,
                'emoji': '⭕'
            },
            'minesweeper': {
                'name': 'Minesweeper',
                'description': 'Mine-sweeping puzzle',
                'class': Minesweeper,
                'emoji': '💣'
            },
            '2048': {
                'name': '2048',
                'description': 'Tile-merging number puzzle',
                'class': Game2048,
                'emoji': '🔢'
            },
            'blackjack': {
                'name': 'Blackjack',
                'description': 'Casino card game (21)',
                'class': Blackjack,
                'emoji': '🃏'
            },
            'crossword': {
                'name': 'Crossword',
                'description': 'Word puzzle with clues',
                'class': CrosswordPuzzle,
                'emoji': '📰'
            }
        }
        
        # Load statistics
        self.stats = self._load_stats()
    
    def list_games(self) -> str:
        """List all available games"""
        output = []
        output.append("\n🎮 AVAILABLE GAMES 🎮\n")
        
        for game_id, game_info in self.available_games.items():
            output.append(f"{game_info['emoji']} {game_info['name']} ({game_id})")
            output.append(f"   {game_info['description']}")
            
            # Show stats if available
            if game_id in self.stats:
                stats = self.stats[game_id]
                output.append(f"   Games played: {stats.get('games_played', 0)} | "
                            f"Wins: {stats.get('wins', 0)}")
            output.append("")
        
        output.append("Use: start_game <game_id> to begin playing")
        
        return '\n'.join(output)
    
    def start_game(self, game_type: str, **kwargs) -> Dict:
        """
        Start a new game
        
        Args:
            game_type: Game identifier
            **kwargs: Game-specific parameters
        
        Returns:
            Dict with game instance and info
        """
        if game_type not in self.available_games:
            return {
                'success': False,
                'error': f'Unknown game: {game_type}',
                'available_games': list(self.available_games.keys())
            }
        
        game_class = self.available_games[game_type]['class']
        
        try:
            # Create game instance
            self.current_game = game_class(**kwargs)
            self.current_game_type = game_type
            
            # Update stats
            self._update_stat(game_type, 'games_played', 1)
            
            return {
                'success': True,
                'game_type': game_type,
                'game_name': self.available_games[game_type]['name'],
                'game': self.current_game,
                'display': self.current_game.display() if hasattr(self.current_game, 'display') else ''
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to start game: {str(e)}'
            }
    
    def save_game(self, slot_name: str = 'autosave') -> Dict:
        """Save current game"""
        if not self.current_game:
            return {'success': False, 'error': 'No active game'}
        
        save_data = {
            'game_type': self.current_game_type,
            'timestamp': datetime.now().isoformat(),
            'state': self.current_game.get_state() if hasattr(self.current_game, 'get_state') else {}
        }
        
        filepath = f"{self.save_path}/{slot_name}_{self.current_game_type}.json"
        
        try:
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return {
                'success': True,
                'filepath': filepath,
                'slot_name': slot_name
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to save: {str(e)}'
            }
    
    def load_game(self, slot_name: str = 'autosave', game_type: str = None) -> Dict:
        """Load saved game"""
        if not game_type and not self.current_game_type:
            return {'success': False, 'error': 'Specify game type'}
        
        game_type = game_type or self.current_game_type
        filepath = f"{self.save_path}/{slot_name}_{game_type}.json"
        
        if not os.path.exists(filepath):
            return {'success': False, 'error': 'Save file not found'}
        
        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            # Create game instance and restore state
            result = self.start_game(save_data['game_type'])
            
            if result['success'] and 'state' in save_data:
                # Restore state (implementation depends on each game)
                # For now, just indicate successful load
                pass
            
            return {
                'success': True,
                'game_type': save_data['game_type'],
                'timestamp': save_data['timestamp'],
                'display': self.current_game.display() if hasattr(self.current_game, 'display') else ''
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to load: {str(e)}'
            }
    
    def list_saves(self) -> List[Dict]:
        """List all saved games"""
        saves = []
        
        for filename in os.listdir(self.save_path):
            if filename.endswith('.json'):
                filepath = f"{self.save_path}/{filename}"
                try:
                    with open(filepath, 'r') as f:
                        save_data = json.load(f)
                    
                    saves.append({
                        'filename': filename,
                        'slot_name': filename.replace('.json', ''),
                        'game_type': save_data.get('game_type'),
                        'timestamp': save_data.get('timestamp')
                    })
                except:
                    pass
        
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)
    
    def record_win(self, game_type: str = None):
        """Record a win"""
        game_type = game_type or self.current_game_type
        if game_type:
            self._update_stat(game_type, 'wins', 1)
    
    def record_loss(self, game_type: str = None):
        """Record a loss"""
        game_type = game_type or self.current_game_type
        if game_type:
            self._update_stat(game_type, 'losses', 1)
    
    def get_statistics(self, game_type: str = None) -> Dict:
        """Get game statistics"""
        if game_type:
            return self.stats.get(game_type, {})
        else:
            return self.stats
    
    def get_leaderboard(self, game_type: str, metric: str = 'wins') -> List[Dict]:
        """Get leaderboard for specific game"""
        # Simplified - in production would track per-user stats
        stats = self.stats.get(game_type, {})
        
        return [{
            'player': 'You',
            'metric': metric,
            'value': stats.get(metric, 0)
        }]
    
    def _update_stat(self, game_type: str, stat_name: str, increment: int = 1):
        """Update a statistic"""
        if game_type not in self.stats:
            self.stats[game_type] = {}
        
        if stat_name not in self.stats[game_type]:
            self.stats[game_type][stat_name] = 0
        
        self.stats[game_type][stat_name] += increment
        
        self._save_stats()
    
    def _load_stats(self) -> Dict:
        """Load statistics from file"""
        stats_file = f"{self.stats_path}/statistics.json"
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {}
    
    def _save_stats(self):
        """Save statistics to file"""
        stats_file = f"{self.stats_path}/statistics.json"
        
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Failed to save stats: {e}")
    
    def get_game_help(self, game_type: str = None) -> str:
        """Get help for a game"""
        game_type = game_type or self.current_game_type
        
        if not game_type:
            return "No game specified. Use list_games to see available games."
        
        help_text = {
            'chess': """
♟️ CHESS HELP

Commands:
- make_move(from_pos, to_pos): Move piece
  Example: make_move((6, 4), (4, 4))  # Move e2 to e4
- get_valid_moves(pos): See valid moves for piece
- get_ai_move(difficulty): Get AI suggestion
  Difficulties: 'easy', 'medium', 'hard'

Notation: Positions are (row, col) where (0,0) is top-left (a8)
""",
            'risk': """
🌍 RISK HELP

Commands:
- place_armies(territory, count): Place reinforcements
- attack(from_territory, to_territory, dice): Attack
- fortify(from_territory, to_territory, count): Move armies
- end_turn(): End your turn
- get_ai_move(difficulty): Get AI suggestion

Phases: reinforce → attack → fortify
""",
            'tictactoe': """
⭕ TIC-TAC-TOE HELP

Commands:
- make_move(row, col): Place your mark
- get_ai_move(difficulty): Get AI suggestion
  Difficulties: 'easy', 'medium', 'hard'

Variants:
- 'classic': 3x3 grid
- 'ultimate': 9 small 3x3 boards
- '5x5': 5x5 grid
""",
            'minesweeper': """
💣 MINESWEEPER HELP

Commands:
- reveal(row, col): Reveal a cell
- toggle_flag(row, col): Flag/unflag a cell
- chord(row, col): Auto-reveal adjacent cells
- get_hint(): Get a safe cell

Difficulties: 'beginner', 'intermediate', 'expert'
""",
            '2048': """
🔢 2048 HELP

Commands:
- move(direction): Move tiles
  Directions: 'up', 'down', 'left', 'right'
- undo(): Undo last move
- get_ai_move(): Get AI suggestion

Goal: Create a 2048 tile by merging!
""",
            'blackjack': """
🃏 BLACKJACK HELP

Commands:
- start_round(bet): Start new round with bet
- hit(): Take another card
- stand(): End turn, dealer plays
- double_down(): Double bet, take one card, stand
- get_strategy_hint(): Get basic strategy advice

Goal: Get closer to 21 than dealer without busting!
""",
            'crossword': """
📰 CROSSWORD HELP

Commands:
- fill_cell(row, col, letter): Fill in a letter
- clear_cell(row, col): Clear a cell
- get_hint(): Reveal a random letter
- reveal_word(clue_num, direction): Reveal entire word

Directions: 'across' or 'down'
"""
        }
        
        return help_text.get(game_type, "No help available for this game.")
    
    def display_current_game(self) -> str:
        """Display current game state"""
        if not self.current_game:
            return "No active game. Use start_game to begin!"
        
        if hasattr(self.current_game, 'display'):
            return self.current_game.display()
        else:
            return f"Current game: {self.current_game_type}"
