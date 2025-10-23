#!/bin/bash
# Dynamic Game Generation Regression Test Suite
# Tests that game requests route correctly to DynamicGameGenerator

echo "=== MC AI DYNAMIC GAME GENERATION - REGRESSION TEST SUITE ==="
echo "Testing game request routing and generation functionality"
echo ""

PASSED=0
FAILED=0

# Test 1: Platformer with specific theme
echo "TEST 1: Platformer Game with Custom Characters"
echo "Request: 'Create a platformer game with ninja turtles'"
RESULT=$(curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a platformer game with ninja turtles", "user_id": "test"}' \
  | python3 -c "import sys, json; d = json.load(sys.stdin); print(d.get('metadata', {}).get('type'))")

if [ "$RESULT" == "game_generation" ]; then
  echo "✅ PASS - Correctly routed to game_generation"
  ((PASSED++))
else
  echo "❌ FAIL - Got: $RESULT (expected: game_generation)"
  ((FAILED++))
fi
echo ""

# Test 2: Racing game with emojis
echo "TEST 2: Racing Game with Emoji Theme"
echo "Request: 'Create a racing game with emoji cars'"
RESULT=$(curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a racing game with emoji cars", "user_id": "test"}' \
  | python3 -c "import sys, json; d = json.load(sys.stdin); print(d.get('metadata', {}).get('type'))")

if [ "$RESULT" == "game_generation" ]; then
  echo "✅ PASS - Correctly routed to game_generation"
  ((PASSED++))
else
  echo "❌ FAIL - Got: $RESULT (expected: game_generation)"
  ((FAILED++))
fi
echo ""

# Test 3: Space shooter
echo "TEST 3: Space Shooter Game"
echo "Request: 'Build a space shooter game'"
RESULT=$(curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Build a space shooter game", "user_id": "test"}' \
  | python3 -c "import sys, json; d = json.load(sys.stdin); print(d.get('metadata', {}).get('type'))")

if [ "$RESULT" == "game_generation" ]; then
  echo "✅ PASS - Correctly routed to game_generation"
  ((PASSED++))
else
  echo "❌ FAIL - Got: $RESULT (expected: game_generation)"
  ((FAILED++))
fi
echo ""

# Test 4: Tic-tac-toe with custom characters (original test case)
echo "TEST 4: Tic-Tac-Toe with Custom Characters"
echo "Request: 'I want to play tic-tac-toe with unicorns vs poop emojis'"
RESULT=$(curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to play tic-tac-toe with unicorns vs poop emojis", "user_id": "test"}' \
  | python3 -c "import sys, json; d = json.load(sys.stdin); print(d.get('metadata', {}).get('type'))")

if [ "$RESULT" == "game_generation" ]; then
  echo "✅ PASS - Correctly routed to game_generation"
  ((PASSED++))
else
  echo "❌ FAIL - Got: $RESULT (expected: game_generation)"
  ((FAILED++))
fi
echo ""

# Summary
echo "=== TEST SUMMARY ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
  echo "✅ ALL TESTS PASSED - Game generation routing working correctly"
  exit 0
else
  echo "❌ SOME TESTS FAILED - Game generation routing needs attention"
  exit 1
fi
