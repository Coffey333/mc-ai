"""
Crossword Puzzle Generator for MC AI V4
Auto-generates puzzles with clues
"""

import random
from typing import Dict, List, Optional, Tuple, Set

class CrosswordPuzzle:
    """
    Crossword puzzle generator and player
    """
    
    def __init__(self, size: int = 15, difficulty: str = 'medium'):
        """
        Args:
            size: Grid size (NxN)
            difficulty: 'easy', 'medium', 'hard'
        """
        self.size = size
        self.difficulty = difficulty
        
        # Grid: None = black square, letter = white square
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.player_grid = [['' for _ in range(size)] for _ in range(size)]
        
        self.words = []  # List of placed words
        self.clues = {'across': {}, 'down': {}}
        self.clue_numbers = {}  # (row, col) -> number
        
        # Word database
        self.word_database = self._load_word_database(difficulty)
        
        # Generate puzzle
        self._generate_puzzle()
    
    def _load_word_database(self, difficulty: str) -> Dict[int, List[Tuple[str, str]]]:
        """Load word database by length with clues"""
        # Simplified word database - in production, load from file
        database = {
            3: [
                ('CAT', 'Feline pet'),
                ('DOG', 'Canine pet'),
                ('SUN', 'Star at center of solar system'),
                ('RUN', 'Move quickly on foot'),
                ('BAT', 'Flying mammal'),
                ('HAT', 'Head covering'),
                ('CAR', 'Motor vehicle'),
                ('BUS', 'Large passenger vehicle'),
                ('TEA', 'Hot beverage'),
                ('ICE', 'Frozen water'),
            ],
            4: [
                ('CODE', 'Programming instructions'),
                ('DATA', 'Information'),
                ('BYTE', 'Eight bits'),
                ('DISK', 'Storage device'),
                ('FILE', 'Computer document'),
                ('MOON', 'Earth satellite'),
                ('STAR', 'Celestial body'),
                ('TREE', 'Woody plant'),
                ('BIRD', 'Feathered animal'),
                ('FISH', 'Aquatic animal'),
            ],
            5: [
                ('MOUSE', 'Computer input device'),
                ('CLOUD', 'Data storage service'),
                ('PHONE', 'Communication device'),
                ('ROBOT', 'Automated machine'),
                ('SPACE', 'Outer ___'),
                ('OCEAN', 'Large body of water'),
                ('RIVER', 'Flowing water'),
                ('PLANT', 'Living organism'),
                ('MUSIC', 'Organized sound'),
                ('DANCE', 'Rhythmic movement'),
            ],
            6: [
                ('PYTHON', 'Programming language'),
                ('SERVER', 'Network computer'),
                ('ROUTER', 'Network device'),
                ('LAPTOP', 'Portable computer'),
                ('TABLET', 'Touch screen device'),
                ('PLANET', 'Celestial body orbiting star'),
                ('GALAXY', 'Star system'),
                ('FOREST', 'Dense woodland'),
                ('ANIMAL', 'Living creature'),
                ('GARDEN', 'Cultivated plants'),
            ],
            7: [
                ('COMPUTER', 'Electronic device'),
                ('NETWORK', 'Connected systems'),
                ('PROGRAM', 'Software application'),
                ('DISPLAY', 'Screen output'),
                ('JUPITER', 'Largest planet'),
                ('MERCURY', 'Closest planet to sun'),
                ('RAINBOW', 'Colorful arc'),
                ('WEATHER', 'Atmospheric conditions'),
                ('SCIENCE', 'Systematic study'),
                ('HISTORY', 'Past events'),
            ],
            8: [
                ('KEYBOARD', 'Typing input device'),
                ('DATABASE', 'Organized data'),
                ('SOFTWARE', 'Computer programs'),
                ('HARDWARE', 'Physical computer parts'),
                ('INTERNET', 'Global network'),
                ('MOUNTAIN', 'Large landform'),
                ('WATERFALL', 'Cascading water'),
                ('UNIVERSE', 'All of space'),
                ('DINOSAUR', 'Extinct reptile'),
                ('ELEPHANT', 'Large mammal'),
            ]
        }
        
        # Filter by difficulty
        if difficulty == 'easy':
            return {k: v for k, v in database.items() if k <= 5}
        elif difficulty == 'hard':
            return database
        else:  # medium
            return {k: v for k, v in database.items() if k <= 7}
    
    def _generate_puzzle(self):
        """Generate crossword puzzle"""
        # Start with a random seed word in the center
        center = self.size // 2
        
        # Get starting word
        word_length = random.choice([5, 6, 7])
        if word_length in self.word_database:
            word, clue = random.choice(self.word_database[word_length])
            
            # Place horizontal word in center
            start_col = center - len(word) // 2
            self._place_word(word, clue, center, start_col, 'across')
        
        # Try to add more words
        max_words = 20 if self.difficulty == 'easy' else 30 if self.difficulty == 'medium' else 40
        attempts = 0
        max_attempts = 1000
        
        while len(self.words) < max_words and attempts < max_attempts:
            attempts += 1
            
            # Try to place a word
            if random.random() < 0.5:
                # Try across
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 8)
                direction = 'across'
            else:
                # Try down
                row = random.randint(0, self.size - 8)
                col = random.randint(0, self.size - 1)
                direction = 'down'
            
            # Find word that fits
            word_length = random.randint(3, 8)
            if word_length in self.word_database:
                word, clue = random.choice(self.word_database[word_length])
                
                if self._can_place_word(word, row, col, direction):
                    self._place_word(word, clue, row, col, direction)
        
        # Number the clues
        self._number_clues()
    
    def _can_place_word(self, word: str, row: int, col: int, direction: str) -> bool:
        """Check if word can be placed at position"""
        if direction == 'across':
            if col + len(word) > self.size:
                return False
            
            # Check if space is available
            for i, letter in enumerate(word):
                r, c = row, col + i
                
                if self.grid[r][c] is not None:
                    # Cell occupied - must match
                    if self.grid[r][c] != letter:
                        return False
                else:
                    # Check perpendicular conflicts
                    # Check above
                    if r > 0 and self.grid[r-1][c] is not None:
                        return False
                    # Check below
                    if r < self.size - 1 and self.grid[r+1][c] is not None:
                        return False
            
            # Check ends
            if col > 0 and self.grid[row][col-1] is not None:
                return False
            if col + len(word) < self.size and self.grid[row][col+len(word)] is not None:
                return False
        
        else:  # down
            if row + len(word) > self.size:
                return False
            
            # Check if space is available
            for i, letter in enumerate(word):
                r, c = row + i, col
                
                if self.grid[r][c] is not None:
                    # Cell occupied - must match
                    if self.grid[r][c] != letter:
                        return False
                else:
                    # Check perpendicular conflicts
                    # Check left
                    if c > 0 and self.grid[r][c-1] is not None:
                        return False
                    # Check right
                    if c < self.size - 1 and self.grid[r][c+1] is not None:
                        return False
            
            # Check ends
            if row > 0 and self.grid[row-1][col] is not None:
                return False
            if row + len(word) < self.size and self.grid[row+len(word)][col] is not None:
                return False
        
        return True
    
    def _place_word(self, word: str, clue: str, row: int, col: int, direction: str):
        """Place word on grid"""
        self.words.append({
            'word': word,
            'clue': clue,
            'row': row,
            'col': col,
            'direction': direction
        })
        
        # Place letters
        for i, letter in enumerate(word):
            if direction == 'across':
                self.grid[row][col + i] = letter
            else:
                self.grid[row + i][col] = letter
    
    def _number_clues(self):
        """Number clues sequentially"""
        clue_num = 1
        
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is not None:
                    # Check if start of across word
                    is_across_start = (col == 0 or self.grid[row][col-1] is None) and \
                                     (col < self.size - 1 and self.grid[row][col+1] is not None)
                    
                    # Check if start of down word
                    is_down_start = (row == 0 or self.grid[row-1][col] is None) and \
                                   (row < self.size - 1 and self.grid[row+1][col] is not None)
                    
                    if is_across_start or is_down_start:
                        self.clue_numbers[(row, col)] = clue_num
                        
                        # Add clues
                        if is_across_start:
                            # Find the word
                            for word_data in self.words:
                                if (word_data['row'] == row and 
                                    word_data['col'] == col and 
                                    word_data['direction'] == 'across'):
                                    self.clues['across'][clue_num] = word_data['clue']
                                    break
                        
                        if is_down_start:
                            # Find the word
                            for word_data in self.words:
                                if (word_data['row'] == row and 
                                    word_data['col'] == col and 
                                    word_data['direction'] == 'down'):
                                    self.clues['down'][clue_num] = word_data['clue']
                                    break
                        
                        clue_num += 1
    
    def fill_cell(self, row: int, col: int, letter: str) -> Dict:
        """Fill a cell with a letter"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return {'success': False, 'error': 'Invalid position'}
        
        if self.grid[row][col] is None:
            return {'success': False, 'error': 'Black square'}
        
        letter = letter.upper()
        if len(letter) != 1 or not letter.isalpha():
            return {'success': False, 'error': 'Invalid letter'}
        
        self.player_grid[row][col] = letter
        
        # Check if correct
        correct = (letter == self.grid[row][col])
        
        # Check if puzzle complete
        complete = self.check_complete()
        
        return {
            'success': True,
            'correct': correct,
            'complete': complete
        }
    
    def clear_cell(self, row: int, col: int) -> Dict:
        """Clear a cell"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return {'success': False, 'error': 'Invalid position'}
        
        self.player_grid[row][col] = ''
        
        return {'success': True}
    
    def get_hint(self) -> Dict:
        """Get a hint - reveal a random empty cell"""
        # Find empty cells
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is not None and self.player_grid[row][col] == '':
                    empty_cells.append((row, col))
        
        if not empty_cells:
            return {'success': False, 'error': 'No empty cells'}
        
        row, col = random.choice(empty_cells)
        self.player_grid[row][col] = self.grid[row][col]
        
        return {
            'success': True,
            'position': (row, col),
            'letter': self.grid[row][col]
        }
    
    def check_word(self, word_data: Dict) -> bool:
        """Check if a word is correct"""
        row = word_data['row']
        col = word_data['col']
        word = word_data['word']
        direction = word_data['direction']
        
        for i, letter in enumerate(word):
            if direction == 'across':
                if self.player_grid[row][col + i] != letter:
                    return False
            else:
                if self.player_grid[row + i][col] != letter:
                    return False
        
        return True
    
    def check_complete(self) -> bool:
        """Check if puzzle is complete and correct"""
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is not None:
                    if self.player_grid[row][col] != self.grid[row][col]:
                        return False
        return True
    
    def reveal_word(self, clue_num: int, direction: str) -> Dict:
        """Reveal a word"""
        # Find word
        for word_data in self.words:
            if word_data['direction'] == direction:
                row, col = word_data['row'], word_data['col']
                if self.clue_numbers.get((row, col)) == clue_num:
                    # Reveal it
                    word = word_data['word']
                    for i, letter in enumerate(word):
                        if direction == 'across':
                            self.player_grid[row][col + i] = letter
                        else:
                            self.player_grid[row + i][col] = letter
                    
                    return {'success': True, 'word': word}
        
        return {'success': False, 'error': 'Word not found'}
    
    def display(self) -> str:
        """Display crossword"""
        output = []
        
        output.append("\n📰 CROSSWORD PUZZLE 📰")
        output.append(f"Difficulty: {self.difficulty.capitalize()}")
        output.append(f"Words placed: {len(self.words)}")
        output.append("\nGrid:")
        
        # Display grid
        for row in range(self.size):
            line = ""
            for col in range(self.size):
                if self.grid[row][col] is None:
                    line += "███"
                else:
                    # Show clue number if present
                    clue_num = self.clue_numbers.get((row, col))
                    player_letter = self.player_grid[row][col]
                    
                    if clue_num and not player_letter:
                        line += f"{clue_num:2} "
                    elif player_letter:
                        line += f" {player_letter} "
                    else:
                        line += " _ "
            output.append(line)
        
        # Display clues
        if self.clues['across']:
            output.append("\n📍 ACROSS:")
            for num in sorted(self.clues['across'].keys()):
                output.append(f"  {num}. {self.clues['across'][num]}")
        
        if self.clues['down']:
            output.append("\n📍 DOWN:")
            for num in sorted(self.clues['down'].keys()):
                output.append(f"  {num}. {self.clues['down'][num]}")
        
        # Check completion
        if self.check_complete():
            output.append("\n🎉 PUZZLE COMPLETE! 🎉")
        
        return '\n'.join(output)
    
    def get_state(self) -> Dict:
        """Get complete game state"""
        return {
            'size': self.size,
            'difficulty': self.difficulty,
            'grid': self.grid,
            'player_grid': self.player_grid,
            'words': self.words,
            'clues': self.clues,
            'clue_numbers': {f"{k[0]},{k[1]}": v for k, v in self.clue_numbers.items()},
            'complete': self.check_complete()
        }
