# Running Tests for Terraria Clone

## Prerequisites

1. Install test dependencies:
```bash
pip install pytest pytest-cov
```

## Running All Tests

From the project root directory:
```bash
pytest src/test_*.py -v
```

## Running Individual Test Files

1. Test game mechanics:
```bash
pytest src/test_game.py -v
```

2. Test world generation:
```bash
pytest src/test_world.py -v
```

3. Test player mechanics:
```bash
pytest src/test_player.py -v
```

## Running Tests with Coverage

To see test coverage:
```bash
pytest --cov=src src/test_*.py
```

## Test Output

The -v flag shows detailed test output:
- ✓ indicates a passing test
- F indicates a failing test
- E indicates an error during test
- . indicates a passing test (without -v)