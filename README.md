# Tetris
# Author: Kevin Yang
# Since: Sept 2022

A Tetris game clone using Python and Pygame with local user data system.
The LeaderBoard.txt MUST be in the same folder as the .py file to ensure the local user data system is working properly.

The game features the typical Trtris functionalities including:
    different shaped, different colored blocks
    moving (a, s, d keys) and rotating (left, right arrow keys) the blocks
    score tracking system
    bonus score for multiple row cancellation
    increasing speed scaling with scores
    implementation of local leaderboard system

The LeaderBoard.txt keeps track of the username entered and the score they got upon reaching the end of a game.
It follows on each line the format of:
    [username],[score]

exe folder contains the Executable files for this game, with the application shortcut (tetris--Kevin - Shortcut) directly visible in the folder.
    It serves the same functionalities as the .py file with leaderboard function also implemented (LeaderBoard.txt included).