# Python_Chess_Game

This is a **complex chess game** developed using **Pygame**, complete with visuals and sound effects. The project was a challenging and rewarding experience that significantly stretched my skills as a developer. The game includes all the necessary resources such as **images** and **sound files**, providing an immersive experience for players.

## Features
- Full chess board implementation
- Drag-and-drop functionality for moving pieces
- Sound effects for moves and actions
- Highlights valid moves and captures
- Clean and minimalistic UI
- Modular code structure for ease of development and future upgrades

## Project Structure
The project consists of several Python modules that handle different parts of the game logic:

- `board.py`: Manages the chessboard and its state
- `color.py`: Handles color configurations for pieces and board squares
- `config.py`: Configuration settings for the game
- `const.py`: Constants used throughout the game (e.g., screen size, piece sizes)
- `dragger.py`: Manages piece dragging and dropping functionality
- `game.py`: Core game logic, handling turns, rules, and win conditions
- `main.py`: The main entry point to launch the game
- `move.py`: Defines and validates legal moves
- `piece.py`: Manages individual chess pieces and their behavior
- `sound.py`: Handles the game’s sound effects
- `square.py`: Manages the squares on the chessboard
- `theme.py`: Manages the visual appearance of the game

## Future Development
I plan to add **AI** functionality using **minimax algorithm** for single-player mode in the future. If you’re interested, feel free to contribute by adding AI or other features to improve the game.

## How to Run the Game
1. Install the required dependencies (make sure you have Python and Pygame installed):
   ```bash
   pip install pygame
   ```
2. Clone this repository and navigate to the project directory:
   
3. Run the game:
   ```bash
   python main.py
   ```

## Contributing
Contributions are welcome! If you'd like to enhance the game, feel free to fork the project and submit a pull request.
