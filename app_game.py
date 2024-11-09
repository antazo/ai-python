#!/usr/bin/env python3
# app_game.py

import random
from flask import Blueprint, render_template, request

app_game_bp = Blueprint('game', __name__)

@app_game_bp.route('/game')
def game():
    class GameRockPaperScissors:
        def __init__(self):
            self.player = None
            self.enemy = None
            self.switcher = {
                "rock": 0,
                "paper": 1,
                "scissors": 2,
                "lizard": 3,
                "spock": 4
            }
            self.rules = [
                [0, -1, 1, 1, -1],
                [1, 0, -1, -1, 1],
                [-1, 1, 0, 1, -1],
                [-1, 1, -1, 0, 1],
                [1, -1, 1, -1, 0]
            ]

        def toNumericalChoice(self, choice):
            return self.switcher[choice]

        def play(self):

            player_num = self.toNumericalChoice(self.player)
            enemy_num = self.toNumericalChoice(self.enemy)

            if self.rules[player_num][enemy_num] == 1:
                return "You WIN!"
            elif self.rules[player_num][enemy_num] == -1:
                return "You lose!"
            else:
                return "It's a tie!"

    game = GameRockPaperScissors()
    
    choices = list(game.switcher.keys())

    choicePlayer = request.args.get('choice').lower() if request.args.get('choice') in list(game.switcher.keys()) else None
    choiceEnemy = random.choice(choices)
    
    result = None
    if choicePlayer:
        game.player = choicePlayer
        game.enemy = choiceEnemy
        result = game.play()
    return render_template(
        'rockpaperscissors.html',
        choices=choices,
        choicePlayer=choicePlayer,
        choiceEnemy=choiceEnemy,
        result=result
    )
