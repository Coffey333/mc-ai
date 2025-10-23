"""
Interactive Game Generation for MC AI V4
Creates playable HTML5 games based on user requests
Integrates with comprehensive game engine
"""

import random
from typing import Dict, Optional

class GameGenerator:
    """
    Generates interactive games as HTML5 artifacts
    Users can play directly in the interface
    Supports both simple HTML5 games and advanced game engine games
    """
    
    def __init__(self):
        self.game_templates = {
            'puzzle': self._generate_puzzle,
            'memory': self._generate_memory_game,
            'rhythm': self._generate_rhythm_game,
            'meditation': self._generate_meditation_game,
            'reflex': self._generate_reflex_game,
            'chess': self._generate_chess,
            'tictactoe': self._generate_tictactoe,
            'minesweeper': self._generate_minesweeper,
            '2048': self._generate_2048,
            'crossword': self._generate_crossword,
            'risk': self._generate_risk
        }
        
        self.game_manager = None
    
    def generate_game(self, game_type: str, emotion: str = "neutral", difficulty: str = "medium") -> Dict:
        """
        Generate interactive game
        
        Args:
            game_type: Type of game (puzzle, memory, rhythm, etc.)
            emotion: User's emotional state (affects game design)
            difficulty: easy, medium, hard
        
        Returns:
            Dict with HTML code, game_type, instructions
        """
        if game_type not in self.game_templates:
            game_type = self._suggest_game_for_emotion(emotion)
        
        game_html = self.game_templates[game_type](emotion, difficulty)
        
        return {
            'success': True,
            'game_type': game_type,
            'html': game_html,
            'emotion_optimized': emotion,
            'difficulty': difficulty
        }
    
    def _suggest_game_for_emotion(self, emotion: str) -> str:
        """Suggest game type based on emotional state"""
        game_map = {
            'anxiety': 'meditation',  # Calming game
            'calm': 'puzzle',  # Maintain flow
            'focus': 'reflex',  # Challenge focus
            'stress': 'rhythm',  # Rhythmic relaxation
            'curiosity': 'memory',  # Exploration
            'neutral': 'puzzle'  # General engagement
        }
        return game_map.get(emotion, 'puzzle')
    
    def _get_emotion_colors(self, emotion: str) -> list:
        """Get color scheme for emotion"""
        color_map = {
            'anxiety': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            'calm': ['#A8E6CF', '#DCEDC1', '#FFD3B6', '#FFAAA5'],
            'focus': ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
            'stress': ['#89f7fe', '#66a6ff', '#f5576c', '#feda75'],
            'love': ['#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
            'meditation': ['#9D84B7', '#C6A9E0', '#E8D9F5', '#F5E6FF'],
            'transcendence': ['#667eea', '#764ba2', '#f5af19', '#f12711'],
            'curiosity': ['#4facfe', '#00f2fe', '#43e97b', '#38f9d7'],
            'neutral': ['#667eea', '#764ba2', '#45B7D1', '#96CEB4']
        }
        return color_map.get(emotion, color_map['neutral'])
    
    def _generate_puzzle(self, emotion: str, difficulty: str) -> str:
        """Generate sliding tile puzzle game"""
        colors = self._get_emotion_colors(emotion)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]});
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        .game-container {{
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        .puzzle-grid {{
            display: grid;
            grid-template-columns: repeat(3, 100px);
            gap: 5px;
            margin: 20px auto;
        }}
        .tile {{
            width: 100px;
            height: 100px;
            background: {colors[2]};
            border: 2px solid {colors[3]};
            border-radius: 10px;
            font-size: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .tile:hover {{
            transform: scale(1.05);
        }}
        .empty {{
            background: transparent;
            border: 2px dashed #ccc;
        }}
        button {{
            background: {colors[0]};
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h2>🧩 Sliding Puzzle</h2>
        <p>Click tiles to slide them into the empty space</p>
        <div id="moves">Moves: 0</div>
        <div class="puzzle-grid" id="puzzle"></div>
        <button onclick="resetPuzzle()">New Game</button>
    </div>
    <script>
        let tiles = [1,2,3,4,5,6,7,8,0];
        let moves = 0;
        
        function shuffle() {{
            for (let i = 0; i < 100; i++) {{
                const validMoves = getValidMoves();
                const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
                swapTiles(tiles.indexOf(0), randomMove);
            }}
        }}
        
        function getValidMoves() {{
            const emptyIndex = tiles.indexOf(0);
            const row = Math.floor(emptyIndex / 3);
            const col = emptyIndex % 3;
            const valid = [];
            
            if (row > 0) valid.push(emptyIndex - 3);
            if (row < 2) valid.push(emptyIndex + 3);
            if (col > 0) valid.push(emptyIndex - 1);
            if (col < 2) valid.push(emptyIndex + 1);
            
            return valid;
        }}
        
        function swapTiles(i1, i2) {{
            [tiles[i1], tiles[i2]] = [tiles[i2], tiles[i1]];
        }}
        
        function renderPuzzle() {{
            const puzzle = document.getElementById('puzzle');
            puzzle.innerHTML = tiles.map((num, idx) => 
                `<div class="tile ${{num === 0 ? 'empty' : ''}}" onclick="moveTile(${{idx}})">${{num || ''}}</div>`
            ).join('');
            document.getElementById('moves').textContent = `Moves: ${{moves}}`;
        }}
        
        function moveTile(index) {{
            if (tiles[index] === 0) return;
            const emptyIndex = tiles.indexOf(0);
            if (getValidMoves().includes(index)) {{
                swapTiles(index, emptyIndex);
                moves++;
                renderPuzzle();
                checkWin();
            }}
        }}
        
        function checkWin() {{
            if (tiles.join('') === '123456780') {{
                setTimeout(() => alert(`🎉 You won in ${{moves}} moves!`), 100);
            }}
        }}
        
        function resetPuzzle() {{
            tiles = [1,2,3,4,5,6,7,8,0];
            shuffle();
            moves = 0;
            renderPuzzle();
        }}
        
        resetPuzzle();
    </script>
</body>
</html>
        """
    
    def _generate_memory_game(self, emotion: str, difficulty: str) -> str:
        """Generate memory card matching game"""
        colors = self._get_emotion_colors(emotion)
        
        pairs = 6 if difficulty == 'easy' else 8 if difficulty == 'medium' else 12
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]});
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        .game-container {{
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        .memory-grid {{
            display: grid;
            grid-template-columns: repeat(4, 80px);
            gap: 10px;
            margin: 20px auto;
        }}
        .card {{
            width: 80px;
            height: 80px;
            background: {colors[2]};
            border: 3px solid {colors[3]};
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .card.flipped {{
            background: white;
        }}
        .card.matched {{
            background: {colors[0]};
            opacity: 0.6;
        }}
        button {{
            background: {colors[0]};
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h2>🎴 Memory Match</h2>
        <p>Find all matching pairs</p>
        <div id="score">Pairs: 0/{pairs}</div>
        <div class="memory-grid" id="game"></div>
        <button onclick="resetGame()">New Game</button>
    </div>
    <script>
        const symbols = ['🌟', '🎨', '🎵', '🌈', '🔥', '💎', '🌺', '🦋', '🍀', '🎭', '🎪', '🎯'];
        let cards = [];
        let flipped = [];
        let matched = 0;
        
        function initGame() {{
            const gameSymbols = symbols.slice(0, {pairs});
            cards = [...gameSymbols, ...gameSymbols].sort(() => Math.random() - 0.5);
            flipped = [];
            matched = 0;
            renderGame();
        }}
        
        function renderGame() {{
            const game = document.getElementById('game');
            game.innerHTML = cards.map((symbol, idx) => 
                `<div class="card" id="card-${{idx}}" onclick="flipCard(${{idx}})">?</div>`
            ).join('');
            document.getElementById('score').textContent = `Pairs: ${{matched}}/{pairs}`;
        }}
        
        function flipCard(index) {{
            if (flipped.length >= 2 || flipped.includes(index)) return;
            
            const card = document.getElementById(`card-${{index}}`);
            card.textContent = cards[index];
            card.classList.add('flipped');
            flipped.push(index);
            
            if (flipped.length === 2) {{
                setTimeout(checkMatch, 800);
            }}
        }}
        
        function checkMatch() {{
            const [i1, i2] = flipped;
            const card1 = document.getElementById(`card-${{i1}}`);
            const card2 = document.getElementById(`card-${{i2}}`);
            
            if (cards[i1] === cards[i2]) {{
                card1.classList.add('matched');
                card2.classList.add('matched');
                matched++;
                document.getElementById('score').textContent = `Pairs: ${{matched}}/{pairs}`;
                
                if (matched === {pairs}) {{
                    setTimeout(() => alert('🎉 You won!'), 100);
                }}
            }} else {{
                card1.textContent = '?';
                card2.textContent = '?';
                card1.classList.remove('flipped');
                card2.classList.remove('flipped');
            }}
            
            flipped = [];
        }}
        
        function resetGame() {{
            initGame();
        }}
        
        initGame();
    </script>
</body>
</html>
        """
    
    def _generate_rhythm_game(self, emotion: str, difficulty: str) -> str:
        """Generate rhythm/timing game"""
        colors = self._get_emotion_colors(emotion)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]});
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        .game-container {{
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        #game-area {{
            width: 400px;
            height: 300px;
            background: #f0f0f0;
            position: relative;
            margin: 20px auto;
            border-radius: 10px;
            overflow: hidden;
        }}
        .note {{
            position: absolute;
            width: 60px;
            height: 60px;
            background: {colors[2]};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            animation: fall linear;
        }}
        @keyframes fall {{
            from {{ top: -60px; }}
            to {{ top: 300px; }}
        }}
        #target {{
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 80px;
            border: 4px solid {colors[3]};
            border-radius: 50%;
        }}
        button {{
            background: {colors[0]};
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h2>🎵 Rhythm Game</h2>
        <p>Press SPACE when notes reach the circle!</p>
        <div id="score">Score: 0</div>
        <div id="game-area">
            <div id="target"></div>
        </div>
        <button onclick="startGame()">Start Game</button>
    </div>
    <script>
        let score = 0;
        let gameRunning = false;
        let noteInterval;
        
        function startGame() {{
            score = 0;
            gameRunning = true;
            document.getElementById('score').textContent = 'Score: 0';
            
            noteInterval = setInterval(() => {{
                if (gameRunning) createNote();
            }}, 1500);
            
            setTimeout(() => {{
                gameRunning = false;
                clearInterval(noteInterval);
                alert(`Game Over! Score: ${{score}}`);
            }}, 30000);
        }}
        
        function createNote() {{
            const gameArea = document.getElementById('game-area');
            const note = document.createElement('div');
            note.className = 'note';
            note.textContent = '♪';
            note.style.left = Math.random() * 340 + 'px';
            note.style.animationDuration = '2s';
            gameArea.appendChild(note);
            
            setTimeout(() => note.remove(), 2000);
        }}
        
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space' && gameRunning) {{
                const notes = document.querySelectorAll('.note');
                notes.forEach(note => {{
                    const rect = note.getBoundingClientRect();
                    const targetRect = document.getElementById('target').getBoundingClientRect();
                    
                    if (Math.abs(rect.top - targetRect.top) < 40) {{
                        score += 10;
                        document.getElementById('score').textContent = `Score: ${{score}}`;
                        note.remove();
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
        """
    
    def _generate_meditation_game(self, emotion: str, difficulty: str) -> str:
        """Generate breathing/meditation exercise"""
        colors = self._get_emotion_colors(emotion)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]});
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        .meditation-container {{
            text-align: center;
            color: white;
        }}
        #breathing-circle {{
            width: 200px;
            height: 200px;
            background: rgba(255,255,255,0.3);
            border-radius: 50%;
            margin: 40px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            transition: all 4s ease-in-out;
        }}
        #breathing-circle.inhale {{
            transform: scale(1.5);
            background: rgba(255,255,255,0.5);
        }}
        #breathing-circle.exhale {{
            transform: scale(1);
            background: rgba(255,255,255,0.3);
        }}
        button {{
            background: white;
            color: {colors[0]};
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px;
        }}
    </style>
</head>
<body>
    <div class="meditation-container">
        <h1>🧘 Breathing Exercise</h1>
        <p id="instruction">Click Start to begin</p>
        <div id="breathing-circle">
            <span id="breath-text">Ready</span>
        </div>
        <button onclick="toggleMeditation()">Start</button>
    </div>
    <script>
        let meditating = false;
        let breathInterval;
        
        function toggleMeditation() {{
            meditating = !meditating;
            const button = document.querySelector('button');
            
            if (meditating) {{
                button.textContent = 'Stop';
                startBreathing();
            }} else {{
                button.textContent = 'Start';
                stopBreathing();
            }}
        }}
        
        function startBreathing() {{
            let isInhale = true;
            const circle = document.getElementById('breathing-circle');
            const text = document.getElementById('breath-text');
            const instruction = document.getElementById('instruction');
            
            function breathe() {{
                if (isInhale) {{
                    circle.className = 'inhale';
                    text.textContent = 'Breathe In';
                    instruction.textContent = 'Inhale slowly through your nose';
                }} else {{
                    circle.className = 'exhale';
                    text.textContent = 'Breathe Out';
                    instruction.textContent = 'Exhale slowly through your mouth';
                }}
                isInhale = !isInhale;
            }}
            
            breathe();
            breathInterval = setInterval(breathe, 4000);
        }}
        
        function stopBreathing() {{
            clearInterval(breathInterval);
            const circle = document.getElementById('breathing-circle');
            const text = document.getElementById('breath-text');
            const instruction = document.getElementById('instruction');
            
            circle.className = '';
            text.textContent = 'Ready';
            instruction.textContent = 'Click Start to begin';
        }}
    </script>
</body>
</html>
        """
    
    def _generate_reflex_game(self, emotion: str, difficulty: str) -> str:
        """Generate reflex/reaction time game"""
        colors = self._get_emotion_colors(emotion)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]});
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        .game-container {{
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            width: 400px;
        }}
        #game-box {{
            width: 100%;
            height: 200px;
            background: #f0f0f0;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
            cursor: pointer;
            font-size: 24px;
            transition: all 0.3s;
        }}
        #game-box.waiting {{
            background: #ff6b6b;
        }}
        #game-box.ready {{
            background: #4ecdc4;
        }}
        button {{
            background: {colors[0]};
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h2>⚡ Reflex Test</h2>
        <p id="instruction">Click Start to test your reaction time!</p>
        <div id="game-box" onclick="checkReaction()">
            Click to Start
        </div>
        <div id="result"></div>
        <button onclick="startTest()">Start Test</button>
    </div>
    <script>
        let startTime;
        let timeout;
        let waiting = false;
        
        function startTest() {{
            const box = document.getElementById('game-box');
            const instruction = document.getElementById('instruction');
            const result = document.getElementById('result');
            
            box.className = 'waiting';
            box.textContent = 'Wait for GREEN...';
            instruction.textContent = 'Click when the box turns green!';
            result.textContent = '';
            waiting = true;
            
            timeout = setTimeout(() => {{
                box.className = 'ready';
                box.textContent = 'CLICK NOW!';
                startTime = Date.now();
            }}, Math.random() * 3000 + 1000);
        }}
        
        function checkReaction() {{
            const box = document.getElementById('game-box');
            const result = document.getElementById('result');
            
            if (!waiting) return;
            
            if (box.className === 'waiting') {{
                clearTimeout(timeout);
                box.className = '';
                box.textContent = 'Too early! Try again.';
                result.textContent = '❌ Clicked too soon!';
                waiting = false;
            }} else if (box.className === 'ready') {{
                const reactionTime = Date.now() - startTime;
                box.className = '';
                box.textContent = `${{reactionTime}}ms`;
                
                let rating = reactionTime < 200 ? 'Excellent! 🌟' : 
                            reactionTime < 300 ? 'Good! 👍' : 
                            reactionTime < 400 ? 'Not bad! 👌' : 'Keep practicing!';
                
                result.textContent = `⚡ ${{reactionTime}}ms - ${{rating}}`;
                waiting = false;
            }}
        }}
    </script>
</body>
</html>
        """
    
    def _generate_chess(self, emotion: str, difficulty: str) -> str:
        """Generate chess game (uses game engine)"""
        return self._generate_engine_game_message('Chess', 'chess', '♟️')
    
    def _generate_tictactoe(self, emotion: str, difficulty: str) -> str:
        """Generate tic-tac-toe game (uses game engine)"""
        return self._generate_engine_game_message('Tic-Tac-Toe', 'tictactoe', '⭕')
    
    def _generate_minesweeper(self, emotion: str, difficulty: str) -> str:
        """Generate minesweeper game (uses game engine)"""
        return self._generate_engine_game_message('Minesweeper', 'minesweeper', '💣')
    
    def _generate_2048(self, emotion: str, difficulty: str) -> str:
        """Generate 2048 game (uses game engine)"""
        return self._generate_engine_game_message('2048', '2048', '🔢')
    
    def _generate_crossword(self, emotion: str, difficulty: str) -> str:
        """Generate crossword game (uses game engine)"""
        return self._generate_engine_game_message('Crossword', 'crossword', '📰')
    
    def _generate_risk(self, emotion: str, difficulty: str) -> str:
        """Generate Risk world domination game with interactive visual map"""
        colors = self._get_emotion_colors(emotion)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]});
            font-family: Arial, sans-serif;
            padding: 20px;
            min-height: 100vh;
        }}
        .game-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        h1 {{ text-align: center; color: #333; margin-bottom: 10px; }}
        #status {{
            text-align: center;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .player-turn {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            margin: 0 5px;
        }}
        .map-container {{
            position: relative;
            background: #e3f2fd;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            min-height: 500px;
        }}
        .continent {{
            position: absolute;
            border: 3px solid #1976d2;
            border-radius: 10px;
            background: rgba(255,255,255,0.3);
        }}
        .territory {{
            position: absolute;
            width: 80px;
            height: 60px;
            border: 2px solid #333;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 11px;
            text-align: center;
            padding: 5px;
        }}
        .territory:hover {{
            transform: scale(1.1);
            z-index: 100;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }}
        .territory.selected {{
            box-shadow: 0 0 20px #ffeb3b;
            border-color: #ffeb3b;
            border-width: 3px;
        }}
        .territory.player1 {{
            background: {colors[0]};
            color: white;
        }}
        .territory.player2 {{
            background: {colors[2]};
            color: white;
        }}
        .territory.player3 {{
            background: {colors[3]};
            color: white;
        }}
        .armies {{
            font-size: 16px;
            font-weight: bold;
            margin-top: 3px;
        }}
        .controls {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 20px 0;
        }}
        button {{
            background: {colors[0]};
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .legend {{
            padding: 15px;
            background: #f9f9f9;
            border-radius: 10px;
            margin-top: 20px;
        }}
        .legend h3 {{ margin-bottom: 10px; }}
        .legend ul {{ padding-left: 20px; }}
        .legend li {{ margin: 5px 0; }}
        .connection {{
            position: absolute;
            height: 2px;
            background: rgba(0,0,0,0.2);
            transform-origin: left center;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🌍 RISK - World Domination</h1>
        <div id="status">
            <div>
                <span class="player-turn" id="p1" style="background: {colors[0]};">Player 1</span>
                <span class="player-turn" id="p2" style="background: {colors[2]};">Player 2</span>
                <span class="player-turn" id="p3" style="background: {colors[3]};">Player 3</span>
            </div>
            <div style="margin-top: 10px;">
                <strong>Phase:</strong> <span id="phase">Setup</span> | 
                <strong>Reinforcements:</strong> <span id="reinforcements">5</span>
            </div>
        </div>
        
        <div class="map-container" id="map">
            <!-- North America Continent -->
            <div class="continent" style="left: 10px; top: 50px; width: 300px; height: 280px;"></div>
            <div class="territory player1" id="alaska" style="left: 20px; top: 60px;">Alaska<div class="armies">1</div></div>
            <div class="territory player2" id="nw-terr" style="left: 120px; top: 60px;">NW Terr<div class="armies">1</div></div>
            <div class="territory player3" id="alberta" style="left: 120px; top: 140px;">Alberta<div class="armies">1</div></div>
            <div class="territory player1" id="ontario" style="left: 220px; top: 140px;">Ontario<div class="armies">1</div></div>
            <div class="territory player2" id="greenland" style="left: 320px; top: 60px;">Greenland<div class="armies">1</div></div>
            <div class="territory player3" id="quebec" style="left: 320px; top: 140px;">Quebec<div class="armies">1</div></div>
            <div class="territory player1" id="w-us" style="left: 120px; top: 220px;">W US<div class="armies">1</div></div>
            <div class="territory player2" id="e-us" style="left: 220px; top: 220px;">E US<div class="armies">1</div></div>
            <div class="territory player3" id="c-america" style="left: 170px; top: 290px;">C America<div class="armies">1</div></div>
            
            <!-- Europe Continent -->
            <div class="continent" style="left: 420px; top: 50px; width: 280px; height: 200px;"></div>
            <div class="territory player1" id="iceland" style="left: 430px; top: 60px;">Iceland<div class="armies">1</div></div>
            <div class="territory player2" id="britain" style="left: 430px; top: 140px;">Britain<div class="armies">1</div></div>
            <div class="territory player3" id="scandinavia" style="left: 530px; top: 60px;">Scandinavia<div class="armies">1</div></div>
            <div class="territory player1" id="n-europe" style="left: 530px; top: 140px;">N Europe<div class="armies">1</div></div>
            <div class="territory player2" id="w-europe" style="left: 430px; top: 210px;">W Europe<div class="armies">1</div></div>
            <div class="territory player3" id="s-europe" style="left: 530px; top: 210px;">S Europe<div class="armies">1</div></div>
            <div class="territory player1" id="ukraine" style="left: 630px; top: 110px;">Ukraine<div class="armies">1</div></div>
            
            <!-- Asia Continent -->
            <div class="continent" style="left: 740px; top: 50px; width: 420px; height: 280px;"></div>
            <div class="territory player2" id="ural" style="left: 750px; top: 60px;">Ural<div class="armies">1</div></div>
            <div class="territory player3" id="siberia" style="left: 850px; top: 60px;">Siberia<div class="armies">1</div></div>
            <div class="territory player1" id="yakutsk" style="left: 950px; top: 60px;">Yakutsk<div class="armies">1</div></div>
            <div class="territory player2" id="kamchatka" style="left: 1050px; top: 60px;">Kamchatka<div class="armies">1</div></div>
            <div class="territory player3" id="afghanistan" style="left: 750px; top: 140px;">Afghanistan<div class="armies">1</div></div>
            <div class="territory player1" id="china" style="left: 850px; top: 140px;">China<div class="armies">1</div></div>
            <div class="territory player2" id="mongolia" style="left: 950px; top: 140px;">Mongolia<div class="armies">1</div></div>
            <div class="territory player3" id="japan" style="left: 1050px; top: 140px;">Japan<div class="armies">1</div></div>
            <div class="territory player1" id="middle-east" style="left: 680px; top: 220px;">M East<div class="armies">1</div></div>
            <div class="territory player2" id="india" style="left: 780px; top: 220px;">India<div class="armies">1</div></div>
            <div class="territory player3" id="siam" style="left: 880px; top: 220px;">Siam<div class="armies">1</div></div>
            
            <!-- Africa Continent -->
            <div class="continent" style="left: 420px; top: 270px; width: 260px; height: 200px;"></div>
            <div class="territory player1" id="n-africa" style="left: 430px; top: 280px;">N Africa<div class="armies">1</div></div>
            <div class="territory player2" id="egypt" style="left: 530px; top: 280px;">Egypt<div class="armies">1</div></div>
            <div class="territory player3" id="e-africa" style="left: 630px; top: 300px;">E Africa<div class="armies">1</div></div>
            <div class="territory player1" id="congo" style="left: 480px; top: 360px;">Congo<div class="armies">1</div></div>
            <div class="territory player2" id="s-africa" style="left: 550px; top: 420px;">S Africa<div class="armies">1</div></div>
            
            <!-- South America Continent -->
            <div class="continent" style="left: 220px; top: 370px; width: 180px; height: 150px;"></div>
            <div class="territory player3" id="venezuela" style="left: 230px; top: 380px;">Venezuela<div class="armies">1</div></div>
            <div class="territory player1" id="brazil" style="left: 280px; top: 440px;">Brazil<div class="armies">1</div></div>
            <div class="territory player2" id="peru" style="left: 230px; top: 470px;">Peru<div class="armies">1</div></div>
            <div class="territory player3" id="argentina" style="left: 280px; top: 500px;">Argentina<div class="armies">1</div></div>
            
            <!-- Australia Continent -->
            <div class="continent" style="left: 900px; top: 350px; width: 220px; height: 150px;"></div>
            <div class="territory player1" id="indonesia" style="left: 910px; top: 360px;">Indonesia<div class="armies">1</div></div>
            <div class="territory player2" id="new-guinea" style="left: 1010px; top: 360px;">N Guinea<div class="armies">1</div></div>
            <div class="territory player3" id="w-australia" style="left: 910px; top: 440px;">W Australia<div class="armies">1</div></div>
            <div class="territory player1" id="e-australia" style="left: 1010px; top: 440px;">E Australia<div class="armies">1</div></div>
        </div>
        
        <div class="controls">
            <button onclick="placeArmy()" id="place-btn">Place Army</button>
            <button onclick="attack()" id="attack-btn" disabled>Attack</button>
            <button onclick="fortify()" id="fortify-btn" disabled>Fortify</button>
            <button onclick="endTurn()">End Turn</button>
            <button onclick="newGame()">New Game</button>
        </div>
        
        <div class="legend">
            <h3>How to Play:</h3>
            <ul>
                <li><strong>Setup:</strong> Click your territories to place starting armies</li>
                <li><strong>Reinforce:</strong> Place your bonus armies (3-10 per turn based on territories)</li>
                <li><strong>Attack:</strong> Click your territory, then click enemy territory to attack</li>
                <li><strong>Fortify:</strong> Move armies between your connected territories</li>
                <li><strong>Win:</strong> Conquer all territories! Control continents for bonus armies</li>
            </ul>
        </div>
    </div>
    
    <script>
        const territories = {{
            'alaska': {{owner: 1, armies: 1, connects: ['nw-terr', 'alberta', 'kamchatka']}},
            'nw-terr': {{owner: 2, armies: 1, connects: ['alaska', 'alberta', 'ontario', 'greenland']}},
            'alberta': {{owner: 3, armies: 1, connects: ['alaska', 'nw-terr', 'ontario', 'w-us']}},
            'ontario': {{owner: 1, armies: 1, connects: ['nw-terr', 'alberta', 'quebec', 'w-us', 'e-us', 'greenland']}},
            'greenland': {{owner: 2, armies: 1, connects: ['nw-terr', 'ontario', 'quebec', 'iceland']}},
            'quebec': {{owner: 3, armies: 1, connects: ['ontario', 'greenland', 'e-us']}},
            'w-us': {{owner: 1, armies: 1, connects: ['alberta', 'ontario', 'e-us', 'c-america']}},
            'e-us': {{owner: 2, armies: 1, connects: ['ontario', 'quebec', 'w-us', 'c-america']}},
            'c-america': {{owner: 3, armies: 1, connects: ['w-us', 'e-us', 'venezuela']}},
            'venezuela': {{owner: 3, armies: 1, connects: ['c-america', 'brazil', 'peru']}},
            'brazil': {{owner: 1, armies: 1, connects: ['venezuela', 'peru', 'argentina', 'n-africa']}},
            'peru': {{owner: 2, armies: 1, connects: ['venezuela', 'brazil', 'argentina']}},
            'argentina': {{owner: 3, armies: 1, connects: ['brazil', 'peru']}},
            'n-africa': {{owner: 1, armies: 1, connects: ['brazil', 'w-europe', 's-europe', 'egypt', 'e-africa', 'congo']}},
            'egypt': {{owner: 2, armies: 1, connects: ['n-africa', 's-europe', 'e-africa', 'middle-east']}},
            'e-africa': {{owner: 3, armies: 1, connects: ['n-africa', 'egypt', 'congo', 's-africa', 'middle-east']}},
            'congo': {{owner: 1, armies: 1, connects: ['n-africa', 'e-africa', 's-africa']}},
            's-africa': {{owner: 2, armies: 1, connects: ['congo', 'e-africa']}},
            'iceland': {{owner: 1, armies: 1, connects: ['greenland', 'britain', 'scandinavia']}},
            'britain': {{owner: 2, armies: 1, connects: ['iceland', 'scandinavia', 'n-europe', 'w-europe']}},
            'scandinavia': {{owner: 3, armies: 1, connects: ['iceland', 'britain', 'n-europe', 'ukraine']}},
            'n-europe': {{owner: 1, armies: 1, connects: ['britain', 'scandinavia', 'ukraine', 's-europe', 'w-europe']}},
            'w-europe': {{owner: 2, armies: 1, connects: ['britain', 'n-europe', 's-europe', 'n-africa']}},
            's-europe': {{owner: 3, armies: 1, connects: ['n-europe', 'ukraine', 'w-europe', 'n-africa', 'egypt', 'middle-east']}},
            'ukraine': {{owner: 1, armies: 1, connects: ['scandinavia', 'n-europe', 's-europe', 'middle-east', 'afghanistan', 'ural']}},
            'ural': {{owner: 2, armies: 1, connects: ['ukraine', 'afghanistan', 'china', 'siberia']}},
            'siberia': {{owner: 3, armies: 1, connects: ['ural', 'china', 'mongolia', 'yakutsk']}},
            'yakutsk': {{owner: 1, armies: 1, connects: ['siberia', 'kamchatka', 'mongolia']}},
            'kamchatka': {{owner: 2, armies: 1, connects: ['alaska', 'yakutsk', 'mongolia', 'japan']}},
            'afghanistan': {{owner: 3, armies: 1, connects: ['ukraine', 'ural', 'china', 'india', 'middle-east']}},
            'china': {{owner: 1, armies: 1, connects: ['ural', 'siberia', 'mongolia', 'afghanistan', 'india', 'siam']}},
            'mongolia': {{owner: 2, armies: 1, connects: ['siberia', 'yakutsk', 'kamchatka', 'china', 'japan']}},
            'japan': {{owner: 3, armies: 1, connects: ['kamchatka', 'mongolia']}},
            'middle-east': {{owner: 1, armies: 1, connects: ['s-europe', 'ukraine', 'egypt', 'e-africa', 'afghanistan', 'india']}},
            'india': {{owner: 2, armies: 1, connects: ['middle-east', 'afghanistan', 'china', 'siam']}},
            'siam': {{owner: 3, armies: 1, connects: ['china', 'india', 'indonesia']}},
            'indonesia': {{owner: 1, armies: 1, connects: ['siam', 'new-guinea', 'w-australia']}},
            'new-guinea': {{owner: 2, armies: 1, connects: ['indonesia', 'w-australia', 'e-australia']}},
            'w-australia': {{owner: 3, armies: 1, connects: ['indonesia', 'new-guinea', 'e-australia']}},
            'e-australia': {{owner: 1, armies: 1, connects: ['new-guinea', 'w-australia']}}
        }};
        
        let currentPlayer = 1;
        let phase = 'setup';
        let reinforcements = 5;
        let selectedTerritory = null;
        
        function updateDisplay() {{
            document.getElementById('phase').textContent = phase.charAt(0).toUpperCase() + phase.slice(1);
            document.getElementById('reinforcements').textContent = reinforcements;
            
            document.getElementById('p1').style.opacity = currentPlayer === 1 ? '1' : '0.4';
            document.getElementById('p2').style.opacity = currentPlayer === 2 ? '1' : '0.4';
            document.getElementById('p3').style.opacity = currentPlayer === 3 ? '1' : '0.4';
            
            document.getElementById('place-btn').disabled = phase !== 'reinforce' && phase !== 'setup';
            document.getElementById('attack-btn').disabled = phase !== 'attack';
            document.getElementById('fortify-btn').disabled = phase !== 'fortify';
            
            for (let id in territories) {{
                const elem = document.getElementById(id);
                if (elem) {{
                    elem.className = `territory player${{territories[id].owner}}`;
                    if (selectedTerritory === id) elem.classList.add('selected');
                    elem.querySelector('.armies').textContent = territories[id].armies;
                }}
            }}
        }}
        
        document.getElementById('map').addEventListener('click', (e) => {{
            const terr = e.target.closest('.territory');
            if (!terr) return;
            
            const id = terr.id;
            if (selectedTerritory) {{
                document.getElementById(selectedTerritory).classList.remove('selected');
            }}
            selectedTerritory = id;
            terr.classList.add('selected');
        }});
        
        function placeArmy() {{
            if (!selectedTerritory || reinforcements === 0) return;
            if (territories[selectedTerritory].owner !== currentPlayer) {{
                alert('Select your own territory!');
                return;
            }}
            
            territories[selectedTerritory].armies++;
            reinforcements--;
            
            if (phase === 'setup' && reinforcements === 0) {{
                phase = 'reinforce';
                reinforcements = 3;
            }} else if (phase === 'reinforce' && reinforcements === 0) {{
                phase = 'attack';
            }}
            
            updateDisplay();
        }}
        
        function attack() {{
            if (!selectedTerritory || phase !== 'attack') return;
            
            const from = territories[selectedTerritory];
            if (from.owner !== currentPlayer) {{
                alert('Select your own territory to attack from!');
                return;
            }}
            if (from.armies <= 1) {{
                alert('Need at least 2 armies to attack!');
                return;
            }}
            
            const targets = from.connects.filter(id => territories[id].owner !== currentPlayer);
            if (targets.length === 0) {{
                alert('No enemy territories to attack!');
                return;
            }}
            
            const targetId = targets[Math.floor(Math.random() * targets.length)];
            const target = territories[targetId];
            
            const attackRoll = Math.floor(Math.random() * 6) + 1;
            const defendRoll = Math.floor(Math.random() * 6) + 1;
            
            if (attackRoll > defendRoll) {{
                target.armies--;
                if (target.armies === 0) {{
                    target.owner = currentPlayer;
                    target.armies = from.armies - 1;
                    from.armies = 1;
                    alert(`Conquered ${{targetId}}! (⚔️ ${{attackRoll}} vs 🛡️ ${{defendRoll}})`);
                }} else {{
                    alert(`Hit! (⚔️ ${{attackRoll}} vs 🛡️ ${{defendRoll}})`);
                }}
            }} else {{
                from.armies--;
                alert(`Defended! (⚔️ ${{attackRoll}} vs 🛡️ ${{defendRoll}})`);
            }}
            
            updateDisplay();
        }}
        
        function fortify() {{
            if (!selectedTerritory || phase !== 'fortify') return;
            
            const from = territories[selectedTerritory];
            if (from.owner !== currentPlayer || from.armies <= 1) return;
            
            const owned = from.connects.filter(id => territories[id].owner === currentPlayer);
            if (owned.length > 0) {{
                from.armies--;
                territories[owned[0]].armies++;
                alert(`Moved 1 army to ${{owned[0]}}`);
            }}
            
            phase = 'reinforce';
            updateDisplay();
        }}
        
        function endTurn() {{
            currentPlayer = (currentPlayer % 3) + 1;
            phase = 'reinforce';
            
            const owned = Object.values(territories).filter(t => t.owner === currentPlayer).length;
            reinforcements = Math.max(3, Math.floor(owned / 3));
            
            selectedTerritory = null;
            updateDisplay();
        }}
        
        function newGame() {{
            if (confirm('Start new game?')) {{
                location.reload();
            }}
        }}
        
        updateDisplay();
    </script>
</body>
</html>
        """
    
    def _generate_engine_game_message(self, game_name: str, game_id: str, emoji: str) -> str:
        """Generate HTML message for game engine games"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        .message-container {{
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            max-width: 500px;
        }}
        .game-icon {{
            font-size: 80px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #333;
            margin-bottom: 20px;
        }}
        p {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .features {{
            text-align: left;
            margin: 20px 0;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
        }}
        .features li {{
            margin: 10px 0;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="message-container">
        <div class="game-icon">{emoji}</div>
        <h2>{game_name} Game Available!</h2>
        <p>The comprehensive {game_name} game is available through MC AI's game engine.</p>
        <div class="features">
            <strong>To play {game_name}:</strong>
            <ul>
                <li>Ask: "I want to play {game_name.lower()}"</li>
                <li>Or: "Start a game of {game_name.lower()}"</li>
                <li>Or: "Let's play {game_name.lower()}"</li>
            </ul>
        </div>
        <p>The game engine provides full gameplay, AI opponents, save/load, statistics, and more!</p>
    </div>
</body>
</html>
        """
