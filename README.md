# AI Chess Agent

A sophisticated chess game featuring an AI opponent powered by the Minimax algorithm with Alpha-Beta pruning and advanced heuristic evaluation functions. Built with Python and Pygame for an intuitive graphical interface.

## Features

### AI Engine

- **Minimax Algorithm**: Implements the classic Minimax search with configurable depth
- **Alpha-Beta Pruning**: Optimizes search efficiency by eliminating unnecessary branches
- **Multiple Heuristics**: Three levels of evaluation functions ranging from basic material counting to advanced positional analysis
  - **Heuristic 1**: Basic material evaluation (300-500 ELO equivalent)
  - **Heuristic 2**: Material + positional bonuses (600-1000 ELO equivalent)
  - **Heuristic 3**: Advanced evaluation with piece mobility and king safety

### Game Features

- **Complete Chess Rules**: Supports all standard chess rules including:
  - Castling (kingside and queenside)
  - En passant captures
  - Pawn promotion
  - Check and checkmate detection
  - Stalemate recognition
- **Interactive GUI**: User-friendly graphical interface built with Pygame
- **Move Validation**: Ensures all moves follow chess rules
- **Game State Tracking**: Maintains complete move history and game status

### Technical Architecture

- **Modular Design**: Organized into separate modules for AI, game logic, and GUI
- **Object-Oriented**: Clean class-based implementation
- **Extensible**: Easy to add new heuristics or modify existing ones

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-chess-agent.git
   cd ai-chess-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the game from the project root directory:

```bash
python src/gui/display.py
```

### Controls

- **Mouse Click**: Select pieces and make moves
- **Drag and Drop**: Alternative way to move pieces
- The AI will automatically respond after your move

### Configuration

The AI difficulty can be adjusted by modifying the heuristic function and search depth in the `display.py` file. Available heuristics:

- `heuristics_1`: Basic material evaluation
- `heuristics_2`: Material + position
- `heuristics_3`: Advanced evaluation

## Project Structure

```
src/
├── ai/                    # AI algorithms and evaluation
│   ├── minimax.py        # Minimax with Alpha-Beta pruning
│   ├── heuristics.py     # Evaluation functions
│   └── __init__.py
├── game/                  # Chess game logic
│   ├── board.py          # Board representation
│   ├── piece.py          # Piece definitions
│   ├── move.py           # Move validation
│   ├── rules.py          # Game rules and checks
│   └── __init__.py
└── gui/                   # Graphical user interface
    ├── display.py        # Main game loop and rendering
    ├── input_handler.py  # User input processing
    ├── assests.py        # Image loading and assets
    ├── image/            # Chess piece images
    └── __init__.py
```

## Algorithm Details

### Minimax with Alpha-Beta Pruning

The AI uses the Minimax algorithm enhanced with Alpha-Beta pruning to efficiently search through possible game states. The algorithm evaluates positions using heuristic functions that consider:

- **Material Balance**: Point values for different piece types
- **Positional Advantages**: Bonuses for piece placement and development
- **Mobility**: Number of legal moves available
- **King Safety**: Protection and exposure of the king

### Search Optimization

- **Depth-Limited Search**: Configurable search depth to balance performance and strength
- **Move Ordering**: Prioritizes promising moves for better pruning
- **Terminal State Detection**: Immediate evaluation of checkmate, stalemate, and draw positions

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Developed as a team project to demonstrate AI algorithms in game playing
- Built with Python and Pygame for educational purposes
- Chess rules implementation based on standard chess specifications

## Future Enhancements

- [ ] Opening book integration
- [ ] Endgame tablebases
- [ ] Multi-threading for deeper search
- [ ] Neural network evaluation functions
- [ ] Online multiplayer mode
- [ ] Tournament mode with multiple AI strengths
