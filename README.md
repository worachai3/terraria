# Terraria Clone

A simple 2D sandbox game inspired by Terraria, implemented in Python using Pygame.

## Features

- Procedurally generated 2D world
- Basic terrain with dirt, stone, and grass blocks
- Player character with physics
- Block breaking and placing
- Smooth camera following player
- Block interaction with range limiting
- Basic collision detection

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python src/game.py
```

## Controls

### Movement
- A: Move left
- D: Move right
- SPACE: Jump

### Block Interaction
- Left Mouse Button: Break block
- Right Mouse Button: Place dirt block
- Mouse Position: Target block (within range)

### Other
- ESC: Quit game

## Game Features

### Physics System
- Gravity and jumping
- Collision detection with blocks
- Smooth movement with acceleration
- Ground friction

### World Features
- Procedurally generated terrain
- Different block types
- Block interaction system
- Visual block targeting

## Testing

Run tests using pytest:
```bash
pytest src/test_*.py
```

## Development Status
- [x] Basic game loop
- [x] Window creation
- [x] Input handling
- [x] World generation
- [x] Basic terrain
- [x] Camera movement
- [x] Player movement
- [x] Basic physics
- [x] Block interaction
- [ ] Inventory system
- [ ] Different tools
- [ ] More block types

## Project Structure
```
├── src/
│   ├── game.py         # Main game class and loop
│   ├── world.py        # World generation and block management
│   ├── player.py       # Player class and physics
│   ├── test_game.py    # Game tests
│   ├── test_world.py   # World system tests
│   └── test_player.py  # Player and physics tests
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Technical Details

### Game Parameters
- Block size: 32x32 pixels
- World size: 100x100 blocks
- Resolution: 800x600 pixels
- Target FPS: 60
- Player size: 20x40 pixels
- Block interaction range: 5 blocks

### Physics Parameters
- Gravity: 0.5 pixels/frame²
- Jump strength: -10 pixels/frame
- Max speed: 5 pixels/frame
- Acceleration: 0.5 pixels/frame²
- Ground friction: 0.8

## Next Steps
1. Add inventory system
2. Implement different tools
3. Add more block types
4. Add crafting system
5. Implement resource collection
6. Add basic enemies

## Contributing

Feel free to submit issues and enhancement requests!

## Tips
- Break blocks to create paths
- Place blocks to build structures
- Use terrain to your advantage
- Stay within block interaction range (5 blocks)