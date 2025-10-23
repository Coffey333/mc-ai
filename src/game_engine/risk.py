"""
Risk - World Domination Strategy Game for MC AI V4
Complete implementation with AI opponents
"""

import random
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import json

class RiskGame:
    """
    Risk board game implementation
    """
    
    def __init__(self, num_players: int = 3, variant: str = 'classic'):
        """
        Args:
            num_players: 2-6 players
            variant: 'classic', 'quick', or 'world'
        """
        self.num_players = min(6, max(2, num_players))
        self.variant = variant
        
        # Initialize map
        self.territories = self._create_map(variant)
        self.continents = self._define_continents(variant)
        
        # Game state
        self.players = [f'Player{i+1}' for i in range(num_players)]
        self.current_player_idx = 0
        self.phase = 'setup'  # setup, reinforce, attack, fortify
        self.round_number = 0
        
        # Territory ownership and armies
        self.territory_owner = {}
        self.territory_armies = {}
        
        # Cards
        self.cards = []
        self.player_cards = {player: [] for player in self.players}
        self.card_turn_in_count = 0
        
        # Game log
        self.game_log = []
        
        # Initialize game
        self._setup_game()
    
    def _create_map(self, variant: str) -> Dict:
        """Create territory map with connections"""
        if variant == 'classic' or variant == 'world':
            # Simplified world map
            territories = {
                # North America
                'Alaska': ['Northwest Territory', 'Alberta', 'Kamchatka'],
                'Northwest Territory': ['Alaska', 'Alberta', 'Ontario', 'Greenland'],
                'Alberta': ['Alaska', 'Northwest Territory', 'Ontario', 'Western US'],
                'Ontario': ['Northwest Territory', 'Alberta', 'Western US', 'Eastern US', 'Quebec', 'Greenland'],
                'Greenland': ['Northwest Territory', 'Ontario', 'Quebec', 'Iceland'],
                'Quebec': ['Ontario', 'Eastern US', 'Greenland'],
                'Western US': ['Alberta', 'Ontario', 'Eastern US', 'Central America'],
                'Eastern US': ['Ontario', 'Quebec', 'Western US', 'Central America'],
                'Central America': ['Western US', 'Eastern US', 'Venezuela'],
                
                # South America
                'Venezuela': ['Central America', 'Peru', 'Brazil'],
                'Peru': ['Venezuela', 'Brazil', 'Argentina'],
                'Brazil': ['Venezuela', 'Peru', 'Argentina', 'North Africa'],
                'Argentina': ['Peru', 'Brazil'],
                
                # Europe
                'Iceland': ['Greenland', 'Great Britain', 'Scandinavia'],
                'Great Britain': ['Iceland', 'Scandinavia', 'Northern Europe', 'Western Europe'],
                'Scandinavia': ['Iceland', 'Great Britain', 'Northern Europe', 'Ukraine'],
                'Northern Europe': ['Great Britain', 'Scandinavia', 'Ukraine', 'Southern Europe', 'Western Europe'],
                'Western Europe': ['Great Britain', 'Northern Europe', 'Southern Europe', 'North Africa'],
                'Southern Europe': ['Northern Europe', 'Ukraine', 'Western Europe', 'North Africa', 'Egypt', 'Middle East'],
                'Ukraine': ['Scandinavia', 'Northern Europe', 'Southern Europe', 'Middle East', 'Afghanistan', 'Ural'],
                
                # Africa
                'North Africa': ['Brazil', 'Western Europe', 'Southern Europe', 'Egypt', 'East Africa', 'Congo'],
                'Egypt': ['Southern Europe', 'North Africa', 'East Africa', 'Middle East'],
                'East Africa': ['North Africa', 'Egypt', 'Middle East', 'Congo', 'South Africa', 'Madagascar'],
                'Congo': ['North Africa', 'East Africa', 'South Africa'],
                'South Africa': ['Congo', 'East Africa', 'Madagascar'],
                'Madagascar': ['East Africa', 'South Africa'],
                
                # Asia
                'Middle East': ['Southern Europe', 'Ukraine', 'Egypt', 'East Africa', 'Afghanistan', 'India'],
                'Afghanistan': ['Ukraine', 'Middle East', 'India', 'China', 'Ural'],
                'Ural': ['Ukraine', 'Afghanistan', 'China', 'Siberia'],
                'Siberia': ['Ural', 'China', 'Mongolia', 'Irkutsk', 'Yakutsk'],
                'Yakutsk': ['Siberia', 'Irkutsk', 'Kamchatka'],
                'Irkutsk': ['Siberia', 'Yakutsk', 'Kamchatka', 'Mongolia'],
                'Kamchatka': ['Alaska', 'Yakutsk', 'Irkutsk', 'Mongolia', 'Japan'],
                'Mongolia': ['Siberia', 'Irkutsk', 'Kamchatka', 'China', 'Japan'],
                'Japan': ['Kamchatka', 'Mongolia'],
                'China': ['Afghanistan', 'Ural', 'Siberia', 'Mongolia', 'India', 'Siam'],
                'India': ['Middle East', 'Afghanistan', 'China', 'Siam'],
                'Siam': ['China', 'India', 'Indonesia'],
                
                # Australia
                'Indonesia': ['Siam', 'New Guinea', 'Western Australia'],
                'New Guinea': ['Indonesia', 'Western Australia', 'Eastern Australia'],
                'Western Australia': ['Indonesia', 'New Guinea', 'Eastern Australia'],
                'Eastern Australia': ['New Guinea', 'Western Australia']
            }
        else:  # quick variant
            # Smaller map for faster games
            territories = {
                'A1': ['A2', 'B1'],
                'A2': ['A1', 'A3', 'B2'],
                'A3': ['A2', 'B3'],
                'B1': ['A1', 'B2', 'C1'],
                'B2': ['A2', 'B1', 'B3', 'C2'],
                'B3': ['A3', 'B2', 'C3'],
                'C1': ['B1', 'C2'],
                'C2': ['B2', 'C1', 'C3'],
                'C3': ['B3', 'C2']
            }
        
        return territories
    
    def _define_continents(self, variant: str) -> Dict:
        """Define continent groupings and bonuses"""
        if variant == 'classic' or variant == 'world':
            return {
                'North America': {
                    'territories': ['Alaska', 'Northwest Territory', 'Alberta', 'Ontario', 
                                  'Greenland', 'Quebec', 'Western US', 'Eastern US', 'Central America'],
                    'bonus': 5
                },
                'South America': {
                    'territories': ['Venezuela', 'Peru', 'Brazil', 'Argentina'],
                    'bonus': 2
                },
                'Europe': {
                    'territories': ['Iceland', 'Great Britain', 'Scandinavia', 'Northern Europe',
                                  'Western Europe', 'Southern Europe', 'Ukraine'],
                    'bonus': 5
                },
                'Africa': {
                    'territories': ['North Africa', 'Egypt', 'East Africa', 'Congo', 'South Africa', 'Madagascar'],
                    'bonus': 3
                },
                'Asia': {
                    'territories': ['Middle East', 'Afghanistan', 'Ural', 'Siberia', 'Yakutsk',
                                  'Irkutsk', 'Kamchatka', 'Mongolia', 'Japan', 'China', 'India', 'Siam'],
                    'bonus': 7
                },
                'Australia': {
                    'territories': ['Indonesia', 'New Guinea', 'Western Australia', 'Eastern Australia'],
                    'bonus': 2
                }
            }
        else:  # quick
            return {
                'Top': {'territories': ['A1', 'A2', 'A3'], 'bonus': 2},
                'Middle': {'territories': ['B1', 'B2', 'B3'], 'bonus': 2},
                'Bottom': {'territories': ['C1', 'C2', 'C3'], 'bonus': 2}
            }
    
    def _setup_game(self):
        """Initialize game setup"""
        # Distribute territories randomly
        all_territories = list(self.territories.keys())
        random.shuffle(all_territories)
        
        for i, territory in enumerate(all_territories):
            owner = self.players[i % self.num_players]
            self.territory_owner[territory] = owner
            self.territory_armies[territory] = 1  # Start with 1 army
        
        # Give initial reinforcements
        initial_armies = {
            2: 40, 3: 35, 4: 30, 5: 25, 6: 20
        }
        
        armies_per_player = initial_armies[self.num_players] - len(all_territories) // self.num_players
        
        # Players place remaining armies (simplified - auto-distribute)
        for player in self.players:
            player_territories = [t for t, owner in self.territory_owner.items() if owner == player]
            for _ in range(armies_per_player):
                territory = random.choice(player_territories)
                self.territory_armies[territory] += 1
        
        # Create cards
        card_types = ['Infantry', 'Cavalry', 'Artillery']
        for territory in all_territories:
            self.cards.append({
                'territory': territory,
                'type': random.choice(card_types)
            })
        
        self.phase = 'reinforce'
        self._log("Game started!")
    
    def get_reinforcements(self, player: str) -> int:
        """Calculate reinforcements for player"""
        # Base: territories / 3 (minimum 3)
        player_territories = [t for t, owner in self.territory_owner.items() if owner == player]
        base = max(3, len(player_territories) // 3)
        
        # Continent bonuses
        bonus = 0
        for continent, data in self.continents.items():
            if all(self.territory_owner.get(t) == player for t in data['territories']):
                bonus += data['bonus']
        
        return base + bonus
    
    def place_armies(self, territory: str, count: int) -> Dict:
        """Place reinforcement armies"""
        current_player = self.players[self.current_player_idx]
        
        if self.territory_owner.get(territory) != current_player:
            return {'success': False, 'error': 'Not your territory'}
        
        self.territory_armies[territory] += count
        self._log(f"{current_player} placed {count} armies in {territory}")
        
        return {'success': True}
    
    def attack(self, from_territory: str, to_territory: str, 
              num_dice: int = 3) -> Dict:
        """
        Attack from one territory to another
        
        Args:
            from_territory: Attacking territory
            to_territory: Defending territory
            num_dice: Number of dice (1-3)
        
        Returns:
            Dict with battle results
        """
        current_player = self.players[self.current_player_idx]
        
        # Validate attack
        if self.territory_owner.get(from_territory) != current_player:
            return {'success': False, 'error': 'Not your territory'}
        
        if to_territory not in self.territories[from_territory]:
            return {'success': False, 'error': 'Territories not adjacent'}
        
        if self.territory_owner.get(to_territory) == current_player:
            return {'success': False, 'error': 'Cannot attack your own territory'}
        
        if self.territory_armies[from_territory] <= 1:
            return {'success': False, 'error': 'Need at least 2 armies to attack'}
        
        # Limit attacking dice
        max_attack_dice = min(3, self.territory_armies[from_territory] - 1)
        num_dice = min(num_dice, max_attack_dice)
        
        # Defender rolls
        defender = self.territory_owner[to_territory]
        def_dice = min(2, self.territory_armies[to_territory])
        
        # Roll dice
        attack_rolls = sorted([random.randint(1, 6) for _ in range(num_dice)], reverse=True)
        defend_rolls = sorted([random.randint(1, 6) for _ in range(def_dice)], reverse=True)
        
        # Compare dice
        attacker_losses = 0
        defender_losses = 0
        
        for i in range(min(len(attack_rolls), len(defend_rolls))):
            if attack_rolls[i] > defend_rolls[i]:
                defender_losses += 1
            else:
                attacker_losses += 1
        
        # Apply losses
        self.territory_armies[from_territory] -= attacker_losses
        self.territory_armies[to_territory] -= defender_losses
        
        # Check if territory conquered
        conquered = False
        if self.territory_armies[to_territory] <= 0:
            conquered = True
            self.territory_owner[to_territory] = current_player
            
            # Move armies
            move_armies = num_dice
            self.territory_armies[from_territory] -= move_armies
            self.territory_armies[to_territory] = move_armies
            
            self._log(f"{current_player} conquered {to_territory}!")
            
            # Check if player eliminated
            if not any(owner == defender for owner in self.territory_owner.values()):
                self._log(f"{defender} has been eliminated!")
        
        self._log(f"Battle: {from_territory} -> {to_territory}. "
                 f"Attacker rolls: {attack_rolls}, Defender rolls: {defend_rolls}. "
                 f"Attacker lost {attacker_losses}, Defender lost {defender_losses}")
        
        return {
            'success': True,
            'attack_rolls': attack_rolls,
            'defend_rolls': defend_rolls,
            'attacker_losses': attacker_losses,
            'defender_losses': defender_losses,
            'conquered': conquered
        }
    
    def fortify(self, from_territory: str, to_territory: str, count: int) -> Dict:
        """Move armies between adjacent territories"""
        current_player = self.players[self.current_player_idx]
        
        # Validate
        if self.territory_owner.get(from_territory) != current_player:
            return {'success': False, 'error': 'Not your territory'}
        
        if self.territory_owner.get(to_territory) != current_player:
            return {'success': False, 'error': 'Target not your territory'}
        
        if to_territory not in self.territories[from_territory]:
            return {'success': False, 'error': 'Territories not adjacent'}
        
        if count >= self.territory_armies[from_territory]:
            return {'success': False, 'error': 'Must leave at least 1 army'}
        
        # Move armies
        self.territory_armies[from_territory] -= count
        self.territory_armies[to_territory] += count
        
        self._log(f"{current_player} moved {count} armies from {from_territory} to {to_territory}")
        
        return {'success': True}
    
    def end_turn(self) -> Dict:
        """End current player's turn"""
        current_player = self.players[self.current_player_idx]
        
        # Award card if conquered territory this turn
        # (simplified - always award for now)
        if self.cards:
            card = self.cards.pop(0)
            self.player_cards[current_player].append(card)
            self._log(f"{current_player} received a card")
        
        # Next player
        self.current_player_idx = (self.current_player_idx + 1) % self.num_players
        
        if self.current_player_idx == 0:
            self.round_number += 1
        
        self.phase = 'reinforce'
        
        # Check win condition
        winner = self._check_winner()
        if winner:
            return {
                'success': True,
                'game_over': True,
                'winner': winner
            }
        
        return {'success': True, 'next_player': self.players[self.current_player_idx]}
    
    def get_ai_move(self, difficulty: str = 'medium') -> Dict:
        """
        Get AI move for current player
        
        Args:
            difficulty: 'easy', 'medium', 'hard'
        
        Returns:
            Dict with recommended action
        """
        current_player = self.players[self.current_player_idx]
        player_territories = [t for t, owner in self.territory_owner.items() 
                             if owner == current_player]
        
        if self.phase == 'reinforce':
            # Place armies on weakest border
            reinforcements = self.get_reinforcements(current_player)
            
            border_territories = []
            for territory in player_territories:
                for neighbor in self.territories[territory]:
                    if self.territory_owner[neighbor] != current_player:
                        border_territories.append(territory)
                        break
            
            if border_territories:
                weakest = min(border_territories, key=lambda t: self.territory_armies[t])
                return {
                    'action': 'place_armies',
                    'territory': weakest,
                    'count': reinforcements
                }
        
        elif self.phase == 'attack':
            # Find best attack opportunity
            best_attack = None
            best_ratio = 0
            
            for territory in player_territories:
                if self.territory_armies[territory] > 1:
                    for neighbor in self.territories[territory]:
                        if self.territory_owner[neighbor] != current_player:
                            ratio = self.territory_armies[territory] / self.territory_armies[neighbor]
                            
                            if ratio > best_ratio and ratio >= 1.5:  # Only attack if advantage
                                best_ratio = ratio
                                best_attack = (territory, neighbor)
            
            if best_attack and (difficulty == 'hard' or random.random() < 0.7):
                return {
                    'action': 'attack',
                    'from': best_attack[0],
                    'to': best_attack[1],
                    'dice': 3
                }
            else:
                return {'action': 'end_attack'}
        
        elif self.phase == 'fortify':
            # Fortify weakest border from strongest interior
            border_territories = []
            interior_territories = []
            
            for territory in player_territories:
                has_enemy_neighbor = any(
                    self.territory_owner[n] != current_player 
                    for n in self.territories[territory]
                )
                
                if has_enemy_neighbor:
                    border_territories.append(territory)
                else:
                    interior_territories.append(territory)
            
            if interior_territories and border_territories:
                strongest_interior = max(interior_territories, 
                                       key=lambda t: self.territory_armies[t])
                weakest_border = min(border_territories,
                                   key=lambda t: self.territory_armies[t])
                
                # Check if adjacent
                if weakest_border in self.territories[strongest_interior]:
                    move_count = self.territory_armies[strongest_interior] - 1
                    if move_count > 0:
                        return {
                            'action': 'fortify',
                            'from': strongest_interior,
                            'to': weakest_border,
                            'count': move_count
                        }
            
            return {'action': 'end_turn'}
        
        return {'action': 'end_turn'}
    
    def _check_winner(self) -> Optional[str]:
        """Check if someone has won"""
        owners = set(self.territory_owner.values())
        if len(owners) == 1:
            return list(owners)[0]
        return None
    
    def _log(self, message: str):
        """Add to game log"""
        self.game_log.append(f"Round {self.round_number}: {message}")
    
    def display_map(self) -> str:
        """Display game state"""
        output = []
        output.append(f"\n=== RISK - Round {self.round_number} ===")
        output.append(f"Current Player: {self.players[self.current_player_idx]}")
        output.append(f"Phase: {self.phase}")
        output.append("\nTerritories:")
        
        for continent, data in self.continents.items():
            output.append(f"\n{continent} (Bonus: {data['bonus']}):")
            for territory in data['territories']:
                owner = self.territory_owner.get(territory, 'Unknown')
                armies = self.territory_armies.get(territory, 0)
                output.append(f"  {territory}: {owner} ({armies} armies)")
        
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'players': self.players,
            'current_player': self.players[self.current_player_idx],
            'phase': self.phase,
            'round': self.round_number,
            'territories': self.territories,
            'territory_owner': self.territory_owner,
            'territory_armies': self.territory_armies,
            'continents': self.continents,
            'game_log': self.game_log[-10:]  # Last 10 entries
        }
