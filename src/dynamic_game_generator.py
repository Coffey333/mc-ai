"""
Dynamic Game Generator - AI-Powered Game Creation
Generates custom HTML5 games based on user descriptions using GPT-4o
Supports multiple game types and full customization (characters, themes, colors)
"""

import logging
from typing import Dict, Optional, List
import json

logger = logging.getLogger(__name__)

class GameType:
    """Supported game types with complexity levels"""
    BOARD = "board"  # Tic-tac-toe, checkers, chess
    ARCADE = "arcade"  # Snake, breakout, whack-a-mole
    PLATFORMER = "platformer"  # Mario-style games
    PUZZLE = "puzzle"  # Memory match, sliding puzzles
    RACING = "racing"  # Top-down or side-view racing
    SHOOTER = "shooter"  # Space invaders, shoot-em-ups
    CARD = "card"  # Solitaire, matching games

class DynamicGameGenerator:
    """
    AI-Powered Dynamic Game Generator
    
    Takes user description and generates playable HTML5 games
    Integrates with Canvas System for build → test → deliver workflow
    """
    
    def __init__(self):
        # Use MC AI's LLM for AI-powered game generation
        from src.knowledge_engine import LLMClient
        self.llm = LLMClient()
        
        self.game_templates = {
            GameType.BOARD: self._get_board_game_template,
            GameType.ARCADE: self._get_arcade_game_template,
            GameType.PLATFORMER: self._get_platformer_template,
            GameType.PUZZLE: self._get_puzzle_template,
            GameType.RACING: self._get_racing_template,
            GameType.SHOOTER: self._get_shooter_template,
            GameType.CARD: self._get_card_game_template
        }
        
        logger.info("🎮 Dynamic Game Generator initialized")
    
    def generate_game(
        self, 
        user_request: str,
        game_type: Optional[str] = None,
        customization: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a custom game from user description
        
        Args:
            user_request: Natural language game request
            game_type: Optional game type hint
            customization: Optional custom characters/themes
            
        Returns:
            Dict with HTML code, game_type, title, description
        """
        try:
            # Analyze request to determine game type and extract customization
            analysis = self._analyze_game_request(user_request)
            
            # Use provided type or analyzed type
            final_game_type = game_type or analysis['game_type']
            final_customization = {**(customization or {}), **analysis['customization']}
            
            # Generate game code using GPT-4o
            game_code = self._generate_game_code(
                game_type=final_game_type,
                request=user_request,
                customization=final_customization,
                complexity=analysis.get('complexity', 'medium')
            )
            
            logger.info(f"🎮 Generated {final_game_type} game: {analysis['title']}")
            
            return {
                'success': True,
                'html': game_code,
                'game_type': final_game_type,
                'title': analysis['title'],
                'description': analysis['description'],
                'customization': final_customization
            }
            
        except Exception as e:
            logger.error(f"Game generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_html': self._get_error_game(str(e))
            }
    
    def _analyze_game_request(self, request: str) -> Dict:
        """Use LLM to analyze game request and extract details"""
        
        system_prompt = """You are a game design analyzer. Extract details from user game requests.

Analyze the request and return JSON with:
- game_type: board/arcade/platformer/puzzle/racing/shooter/card
- title: Creative game title
- description: Brief game description
- complexity: simple/medium/advanced
- customization: {player_character, opponent_character, theme, colors, special_features}

Examples:
"tic-tac-toe with unicorns vs poop emojis" →
{
  "game_type": "board",
  "title": "Unicorn vs Poop Tic-Tac-Toe",
  "description": "Classic tic-tac-toe with magical unicorns battling poop emojis",
  "complexity": "simple",
  "customization": {
    "player_character": "🦄 unicorn",
    "opponent_character": "💩 poop emoji",
    "theme": "fun and silly",
    "colors": ["#ff69b4", "#8b4513"]
  }
}

"mario-style platformer with cats" →
{
  "game_type": "platformer",
  "title": "Cat Quest Adventure",
  "description": "Side-scrolling platformer starring a brave cat",
  "complexity": "advanced",
  "customization": {
    "player_character": "🐱 cat",
    "theme": "adventure platformer",
    "special_features": ["jumping", "enemies", "coins", "levels"]
  }
}
"""
        
        try:
            response = self.llm.complete(
                system_prompt=system_prompt,
                messages=[{"role": "user", "content": f"Analyze this game request: {request}"}],
                max_tokens=500
            )
            
            # Parse JSON from response
            text = response['text'].strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(text)
            return analysis
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {
                'game_type': 'arcade',
                'title': 'Custom Game',
                'description': request,
                'complexity': 'medium',
                'customization': {}
            }
    
    def _generate_game_code(
        self,
        game_type: str,
        request: str,
        customization: Dict,
        complexity: str
    ) -> str:
        """Generate complete HTML5 game code using GPT-4o"""
        
        # Get base template for this game type
        template_func = self.game_templates.get(game_type, self._get_arcade_game_template)
        base_template = template_func()
        
        system_prompt = f"""You are an expert HTML5 game developer. Generate complete, self-contained games.

REQUIREMENTS:
- Single HTML file with embedded CSS and JavaScript
- No external dependencies or libraries
- Mobile-friendly and responsive
- Beautiful, polished UI with animations
- Complete game logic (win/lose conditions, scoring, restart)
- Smooth 60fps performance
- Touch and keyboard controls

GAME TYPE: {game_type}
COMPLEXITY: {complexity}

CUSTOMIZATION:
{self._format_customization(customization)}

BASE TEMPLATE STRUCTURE:
{base_template}

Generate a complete, playable game that matches the user's request EXACTLY.
Make it fun, beautiful, and addictive!"""

        try:
            response = self.llm.complete(
                system_prompt=system_prompt,
                messages=[{"role": "user", "content": f"Create this game: {request}"}],
                max_tokens=4000
            )
            
            game_code = response['text']
            
            # Clean up markdown code blocks if present
            if '```html' in game_code:
                game_code = game_code.split('```html')[1].split('```')[0].strip()
            elif '```' in game_code:
                game_code = game_code.split('```')[1].split('```')[0].strip()
            
            return game_code
            
        except Exception as e:
            logger.error(f"Code generation error: {str(e)}")
            return self._get_fallback_game(request, customization)
    
    def _format_customization(self, customization: Dict) -> str:
        """Format customization dict for prompt"""
        if not customization:
            return "No specific customization requested"
        
        lines = []
        for key, value in customization.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
    def _get_board_game_template(self) -> str:
        """Template structure for board games"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Board Game</title>
    <style>
        /* Dark theme, centered layout */
        body { background: #1a1a2e; color: #eee; font-family: Arial; }
        #game-board { display: grid; max-width: 500px; margin: 20px auto; }
        .cell { aspect-ratio: 1; border: 2px solid #16c79a; cursor: pointer; }
        .cell:hover { background: rgba(22, 199, 154, 0.2); }
    </style>
</head>
<body>
    <div id="game-container">
        <h1 id="title"></h1>
        <div id="game-board"></div>
        <div id="status"></div>
        <button id="restart">Play Again</button>
    </div>
    <script>
        // Game logic here
        // Grid-based game mechanics
        // Win condition checking
        // Touch and click handlers
    </script>
</body>
</html>
"""
    
    def _get_arcade_game_template(self) -> str:
        """Template for arcade-style games"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcade Game</title>
    <style>
        body { background: #1a1a2e; margin: 0; overflow: hidden; }
        canvas { display: block; margin: 20px auto; border: 3px solid #16c79a; }
        #score { text-align: center; color: #16c79a; font-size: 24px; }
    </style>
</head>
<body>
    <div id="score">Score: 0</div>
    <canvas id="game"></canvas>
    <script>
        const canvas = document.getElementById('game');
        const ctx = canvas.getContext('2d');
        // Canvas-based game with animation loop
        // Collision detection
        // Score tracking
        // Game over conditions
    </script>
</body>
</html>
"""
    
    def _get_platformer_template(self) -> str:
        """Template for platformer games (Mario-style)"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Platformer Game</title>
    <style>
        body { background: #87CEEB; margin: 0; overflow: hidden; }
        canvas { display: block; margin: 0 auto; }
    </style>
</head>
<body>
    <canvas id="game"></canvas>
    <script>
        // Platformer physics (gravity, jumping)
        // Level design with platforms
        // Enemy AI
        // Collectibles and power-ups
        // Multiple lives system
    </script>
</body>
</html>
"""
    
    def _get_puzzle_template(self) -> str:
        """Template for puzzle games"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle Game</title>
    <style>
        body { background: #1a1a2e; color: #eee; font-family: Arial; }
        .puzzle-grid { display: grid; max-width: 600px; margin: 20px auto; }
        .puzzle-piece { border: 2px solid #16c79a; cursor: pointer; transition: all 0.3s; }
    </style>
</head>
<body>
    <div id="game-container">
        <h1 id="title"></h1>
        <div id="puzzle-grid"></div>
        <button id="restart">New Puzzle</button>
    </div>
    <script>
        // Puzzle logic (matching, sliding, memory)
        // Shuffle algorithm
        // Match detection
        // Timer and moves counter
    </script>
</body>
</html>
"""
    
    def _get_racing_template(self) -> str:
        """Template for racing games"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Racing Game</title>
    <style>
        body { background: #1a1a2e; margin: 0; overflow: hidden; }
        canvas { display: block; margin: 0 auto; }
        #ui { position: absolute; top: 20px; left: 20px; color: #16c79a; }
    </style>
</head>
<body>
    <div id="ui">
        <div id="speed">Speed: 0</div>
        <div id="lap">Lap: 1/3</div>
    </div>
    <canvas id="game"></canvas>
    <script>
        // Top-down or side-view racing
        // Vehicle physics
        // Track rendering
        // Opponent AI
        // Lap timing
    </script>
</body>
</html>
"""
    
    def _get_shooter_template(self) -> str:
        """Template for shooter games"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shooter Game</title>
    <style>
        body { background: #000; margin: 0; overflow: hidden; }
        canvas { display: block; margin: 0 auto; }
        #hud { position: absolute; top: 10px; width: 100%; text-align: center; color: #0f0; }
    </style>
</head>
<body>
    <div id="hud">
        <span id="score">Score: 0</span>
        <span id="lives">Lives: 3</span>
    </div>
    <canvas id="game"></canvas>
    <script>
        // Shooter mechanics
        // Enemy waves
        // Bullet physics
        // Power-ups
        // Boss battles
    </script>
</body>
</html>
"""
    
    def _get_card_game_template(self) -> str:
        """Template for card games"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Game</title>
    <style>
        body { background: #1a1a2e; color: #eee; font-family: Arial; }
        .card { width: 100px; height: 140px; border: 2px solid #16c79a; border-radius: 8px; }
        .card:hover { transform: translateY(-10px); }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="deck"></div>
        <div id="play-area"></div>
        <button id="deal">Deal Cards</button>
    </div>
    <script>
        // Card game logic
        // Deck shuffling
        // Card dealing and matching
        // Score tracking
    </script>
</body>
</html>
"""
    
    def _get_fallback_game(self, request: str, customization: Dict) -> str:
        """Simple fallback game if AI generation fails"""
        player = customization.get('player_character', '😊')
        opponent = customization.get('opponent_character', '🤖')
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic-Tac-Toe</title>
    <style>
        body {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        #game {{
            text-align: center;
            background: rgba(255,255,255,0.05);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        h1 {{ color: #16c79a; margin-bottom: 20px; }}
        #board {{
            display: grid;
            grid-template-columns: repeat(3, 100px);
            gap: 10px;
            margin: 20px auto;
        }}
        .cell {{
            width: 100px;
            height: 100px;
            background: rgba(22, 199, 154, 0.1);
            border: 3px solid #16c79a;
            border-radius: 10px;
            font-size: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }}
        .cell:hover {{ background: rgba(22, 199, 154, 0.3); transform: scale(1.05); }}
        #status {{ font-size: 20px; margin: 20px 0; color: #16c79a; }}
        button {{
            background: #16c79a;
            color: #1a1a2e;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        button:hover {{ background: #0fa; transform: scale(1.05); }}
    </style>
</head>
<body>
    <div id="game">
        <h1>{request}</h1>
        <div id="status">Your turn! You're {player}</div>
        <div id="board"></div>
        <button onclick="resetGame()">Play Again</button>
    </div>
    <script>
        const board = Array(9).fill('');
        const player = '{player}';
        const ai = '{opponent}';
        let currentPlayer = player;
        let gameOver = false;

        function createBoard() {{
            const boardEl = document.getElementById('board');
            boardEl.innerHTML = '';
            for (let i = 0; i < 9; i++) {{
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.onclick = () => makeMove(i);
                boardEl.appendChild(cell);
            }}
            updateBoard();
        }}

        function updateBoard() {{
            const cells = document.querySelectorAll('.cell');
            cells.forEach((cell, i) => {{
                cell.textContent = board[i];
            }});
        }}

        function makeMove(i) {{
            if (gameOver || board[i]) return;
            
            board[i] = currentPlayer;
            updateBoard();
            
            if (checkWin()) {{
                document.getElementById('status').textContent = `${{currentPlayer}} wins! 🎉`;
                gameOver = true;
                return;
            }}
            
            if (board.every(cell => cell)) {{
                document.getElementById('status').textContent = "It's a tie!";
                gameOver = true;
                return;
            }}
            
            currentPlayer = currentPlayer === player ? ai : player;
            document.getElementById('status').textContent = `${{currentPlayer}}'s turn`;
            
            if (currentPlayer === ai) {{
                setTimeout(aiMove, 500);
            }}
        }}

        function aiMove() {{
            const empty = board.map((v, i) => v === '' ? i : null).filter(v => v !== null);
            if (empty.length > 0) {{
                const move = empty[Math.floor(Math.random() * empty.length)];
                makeMove(move);
            }}
        }}

        function checkWin() {{
            const wins = [
                [0,1,2], [3,4,5], [6,7,8],
                [0,3,6], [1,4,7], [2,5,8],
                [0,4,8], [2,4,6]
            ];
            return wins.some(w => 
                board[w[0]] && board[w[0]] === board[w[1]] && board[w[0]] === board[w[2]]
            );
        }}

        function resetGame() {{
            board.fill('');
            currentPlayer = player;
            gameOver = false;
            document.getElementById('status').textContent = `Your turn! You're ${{player}}`;
            updateBoard();
        }}

        createBoard();
    </script>
</body>
</html>"""
    
    def _get_error_game(self, error: str) -> str:
        """Error message as playable button game"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oops!</title>
    <style>
        body {{
            background: #1a1a2e;
            color: #eee;
            font-family: Arial;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            text-align: center;
        }}
        h1 {{ color: #ff6b6b; }}
        button {{
            background: #16c79a;
            color: #1a1a2e;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            margin: 10px;
        }}
        button:hover {{ background: #0fa; }}
    </style>
</head>
<body>
    <div>
        <h1>😅 Oops! Game generation hiccup</h1>
        <p>Error: {error}</p>
        <button onclick="alert('Let me try again! Can you describe the game differently?')">Try Again</button>
    </div>
</body>
</html>"""


# Global instance
_game_generator: Optional[DynamicGameGenerator] = None

def get_game_generator() -> DynamicGameGenerator:
    """Get or create game generator instance"""
    global _game_generator
    if _game_generator is None:
        _game_generator = DynamicGameGenerator()
    return _game_generator
