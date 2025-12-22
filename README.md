# Hive game 🍯🐝
_Disclaimer: This project is currently work in progress, so not everything works perfectly yet._

This is my Python implementation of [Hive board game](https://en.wikipedia.org/wiki/Hive_(game)). It is a turn-based game that combines simplicity of tic-tac toe and complexity of a chesss. Each player has several pieces which, once placed, can move around the board according to their specific movement patterns. The goal of the game is to surround oponents' queen bee by 6 other pieces (pieces can be of either colour).

I have a several goals in this project:
  - implement the game
    - [x] implement the game logic
    - [x] write GUI
    - [x] implement all types of pieces (pillbug will be added later)
  - write different agents which will be able to play the game
    - [x] random agent
    - [x] minimax
    - [ ] alpha-beta pruning
    - [ ] explore suitable NN architecture(s)
  - learn something new from machine learning
    - [ ] reinforcement learning

The screenshot of a current simple game display is shown below.

<img src="https://github.com/otheiner/hive_game/blob/main/assets/game_screenshot_1.png" width="750">

## How to run the game?
Just clone this repository to your local machine and from inside the main folder where ```hive_game.py``` is located run:
```
python3 hive_game.py
```
This will open the game window and you can play. If you play vs. computer, you are by default white and you start the game. Colour selection will be added to the game menu later. Have fun!

The game shouldn't use any unusual packages, except ```pygame```, which you might need to install.
