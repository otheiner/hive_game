# Hive game
_This project is currently work in progress_

This is my Python implementation of [Hive board game](https://en.wikipedia.org/wiki/Hive_(game)). It is a turn-based game that combines simplicity of tic-tac toe and complexity of a chesss. Each player has several pieces which, once placed, can move around the board according to their specific movement patterns. The goal of the game is to surround oponents' queen bee by 6 other pieces (pieces can be of either colour).

I have a several goals in this project:
  - [x] implement the game
  - write different agents which will be able to play the game
    - [x] random agent
    - [ ] minimax
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
This will open the game window and you can play. Have fun!
