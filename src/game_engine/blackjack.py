"""
Blackjack (21) for MC AI V4
Casino card game with betting and strategy hints
"""

import random
from typing import Dict, List, Optional, Tuple

class Blackjack:
    """
    Complete Blackjack implementation
    """
    
    def __init__(self, initial_balance: int = 1000):
        """
        Args:
            initial_balance: Starting chips
        """
        self.balance = initial_balance
        self.bet = 0
        
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        
        self.game_active = False
        self.player_stood = False
        self.round_history = []
        
        self._create_deck()
    
    def _create_deck(self):
        """Create and shuffle standard deck"""
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append({'rank': rank, 'suit': suit})
        
        random.shuffle(self.deck)
    
    def _card_value(self, card: Dict) -> int:
        """Get numeric value of card"""
        rank = card['rank']
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11  # Will adjust for soft/hard later
        else:
            return int(rank)
    
    def _hand_value(self, hand: List[Dict]) -> Tuple[int, bool]:
        """
        Calculate hand value
        
        Returns:
            (value, is_soft) - is_soft means contains usable Ace
        """
        value = sum(self._card_value(card) for card in hand)
        aces = sum(1 for card in hand if card['rank'] == 'A')
        
        # Adjust for Aces if busted
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        is_soft = aces > 0 and value <= 21
        
        return value, is_soft
    
    def start_round(self, bet: int) -> Dict:
        """
        Start new round with bet
        
        Args:
            bet: Amount to bet
        
        Returns:
            Dict with initial hands
        """
        if bet <= 0:
            return {'success': False, 'error': 'Bet must be positive'}
        
        if bet > self.balance:
            return {'success': False, 'error': 'Insufficient balance'}
        
        # Reset for new round
        self.bet = bet
        self.balance -= bet
        self.player_hand = []
        self.dealer_hand = []
        self.player_stood = False
        self.game_active = True
        
        # Shuffle if deck is low
        if len(self.deck) < 20:
            self._create_deck()
        
        # Deal initial cards
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        
        # Check for player blackjack
        player_value, _ = self._hand_value(self.player_hand)
        
        if player_value == 21:
            return self._end_round('blackjack')
        
        return {
            'success': True,
            'player_hand': self.player_hand,
            'dealer_hand': [self.dealer_hand[0]],  # Only show one card
            'player_value': player_value,
            'balance': self.balance,
            'bet': self.bet
        }
    
    def hit(self) -> Dict:
        """Player takes another card"""
        if not self.game_active:
            return {'success': False, 'error': 'No active game'}
        
        if self.player_stood:
            return {'success': False, 'error': 'Already stood'}
        
        # Deal card
        self.player_hand.append(self.deck.pop())
        player_value, is_soft = self._hand_value(self.player_hand)
        
        # Check bust
        if player_value > 21:
            return self._end_round('bust')
        
        return {
            'success': True,
            'player_hand': self.player_hand,
            'player_value': player_value,
            'is_soft': is_soft,
            'busted': False
        }
    
    def stand(self) -> Dict:
        """Player stands - dealer plays"""
        if not self.game_active:
            return {'success': False, 'error': 'No active game'}
        
        self.player_stood = True
        
        # Dealer plays (hits until 17+)
        dealer_value, _ = self._hand_value(self.dealer_hand)
        
        while dealer_value < 17:
            self.dealer_hand.append(self.deck.pop())
            dealer_value, _ = self._hand_value(self.dealer_hand)
        
        # Determine winner
        player_value, _ = self._hand_value(self.player_hand)
        
        if dealer_value > 21:
            return self._end_round('dealer_bust')
        elif player_value > dealer_value:
            return self._end_round('win')
        elif player_value < dealer_value:
            return self._end_round('lose')
        else:
            return self._end_round('push')
    
    def double_down(self) -> Dict:
        """Double bet, take one card, then stand"""
        if not self.game_active:
            return {'success': False, 'error': 'No active game'}
        
        if len(self.player_hand) != 2:
            return {'success': False, 'error': 'Can only double on first turn'}
        
        if self.bet > self.balance:
            return {'success': False, 'error': 'Insufficient balance'}
        
        # Double bet
        self.balance -= self.bet
        self.bet *= 2
        
        # Take one card
        self.player_hand.append(self.deck.pop())
        player_value, _ = self._hand_value(self.player_hand)
        
        # Check bust
        if player_value > 21:
            return self._end_round('bust')
        
        # Automatically stand
        return self.stand()
    
    def split(self) -> Dict:
        """Split pair into two hands (simplified - not fully implemented)"""
        if not self.game_active:
            return {'success': False, 'error': 'No active game'}
        
        if len(self.player_hand) != 2:
            return {'success': False, 'error': 'Can only split initial hand'}
        
        if self._card_value(self.player_hand[0]) != self._card_value(self.player_hand[1]):
            return {'success': False, 'error': 'Can only split pairs'}
        
        return {'success': False, 'error': 'Split not yet implemented'}
    
    def _end_round(self, result: str) -> Dict:
        """End round and calculate payouts"""
        self.game_active = False
        
        player_value, _ = self._hand_value(self.player_hand)
        dealer_value, _ = self._hand_value(self.dealer_hand)
        
        payout = 0
        message = ''
        
        if result == 'blackjack':
            payout = int(self.bet * 2.5)  # 3:2 payout
            message = '🎉 BLACKJACK! 🎉'
        elif result == 'bust':
            payout = 0
            message = '💥 BUST! Dealer wins.'
        elif result == 'dealer_bust':
            payout = self.bet * 2
            message = '🎊 Dealer busts! You win!'
        elif result == 'win':
            payout = self.bet * 2
            message = '✨ You win!'
        elif result == 'lose':
            payout = 0
            message = '😞 Dealer wins.'
        elif result == 'push':
            payout = self.bet
            message = '🤝 Push - tie game.'
        
        self.balance += payout
        winnings = payout - self.bet
        
        # Record round
        self.round_history.append({
            'result': result,
            'player_hand': self.player_hand[:],
            'dealer_hand': self.dealer_hand[:],
            'player_value': player_value,
            'dealer_value': dealer_value,
            'bet': self.bet,
            'winnings': winnings
        })
        
        return {
            'success': True,
            'result': result,
            'message': message,
            'player_hand': self.player_hand,
            'dealer_hand': self.dealer_hand,
            'player_value': player_value,
            'dealer_value': dealer_value,
            'winnings': winnings,
            'balance': self.balance
        }
    
    def get_strategy_hint(self) -> str:
        """Get basic strategy recommendation"""
        if not self.game_active:
            return "No active game"
        
        player_value, is_soft = self._hand_value(self.player_hand)
        dealer_up_card = self._card_value(self.dealer_hand[0])
        
        # Simplified basic strategy
        if len(self.player_hand) == 2:
            # Check for pair
            if self._card_value(self.player_hand[0]) == self._card_value(self.player_hand[1]):
                pair_value = self._card_value(self.player_hand[0])
                if pair_value in [8, 11]:  # Always split 8s and Aces
                    return "💡 Strategy: SPLIT"
        
        if is_soft:
            # Soft hand strategy
            if player_value <= 17:
                return "💡 Strategy: HIT"
            elif player_value == 18:
                if dealer_up_card >= 9:
                    return "💡 Strategy: HIT"
                else:
                    return "💡 Strategy: STAND"
            else:
                return "💡 Strategy: STAND"
        else:
            # Hard hand strategy
            if player_value <= 11:
                return "💡 Strategy: HIT (can't bust)"
            elif player_value == 12:
                if 4 <= dealer_up_card <= 6:
                    return "💡 Strategy: STAND"
                else:
                    return "💡 Strategy: HIT"
            elif 13 <= player_value <= 16:
                if dealer_up_card <= 6:
                    return "💡 Strategy: STAND"
                else:
                    return "💡 Strategy: HIT"
            else:  # 17+
                return "💡 Strategy: STAND"
    
    def display(self) -> str:
        """Display game state"""
        output = []
        
        output.append(f"\n♠♥ BLACKJACK ♦♣")
        output.append(f"Balance: ${self.balance}")
        
        if self.game_active:
            output.append(f"Current Bet: ${self.bet}")
            output.append("\nDealer's Hand:")
            
            if self.player_stood:
                # Show all dealer cards
                dealer_cards = " ".join(f"{c['rank']}{c['suit']}" for c in self.dealer_hand)
                dealer_value, _ = self._hand_value(self.dealer_hand)
                output.append(f"  {dealer_cards} (Value: {dealer_value})")
            else:
                # Show one card
                first_card = self.dealer_hand[0]
                output.append(f"  {first_card['rank']}{first_card['suit']} ?? (One card hidden)")
            
            output.append("\nYour Hand:")
            player_cards = " ".join(f"{c['rank']}{c['suit']}" for c in self.player_hand)
            player_value, is_soft = self._hand_value(self.player_hand)
            soft_text = " (soft)" if is_soft else ""
            output.append(f"  {player_cards} (Value: {player_value}{soft_text})")
            
            # Strategy hint
            output.append(f"\n{self.get_strategy_hint()}")
            
            # Available actions
            if not self.player_stood:
                output.append("\nActions: hit, stand, double_down")
        else:
            output.append("\nNo active game. Place a bet to start!")
        
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'balance': self.balance,
            'bet': self.bet,
            'player_hand': self.player_hand,
            'dealer_hand': self.dealer_hand,
            'game_active': self.game_active,
            'player_stood': self.player_stood,
            'round_history': self.round_history
        }
