from PIL import ImageGrab

#from utils import image_processing


class Game:
    def __init__(self):
        self.status = "Initializing"
        self.players = [{"Player1": 100},
                        {"Player2": 100},
                        {"Player3": 100},
                        {"Player4": 100},
                        {"Player5": 100},
                        {"Player6": 100},
                        {"Player7": 100},
                        {"Player8": 100},
                        ]
        self.health = 100
        self.stage = 1
        self.round = 1
        self.gold = 0
        self.xp = 0
        self.level = 1
        self.xp_thresholds = {
            'level_2': 2,
            'level_3': 6,
            'level_4': 10,
            'level_5': 20,
            'level_6': 36,
            'level_7': 48,
            'level_8': 80,
            'level_9': 84,
            'level_10': 84
        }
        self.shop = []
        self.best_composition = []
        self.opponents = [
            {'name': 'Opponent1', 'level': 6},
            {'name': 'Opponent2', 'level': 7},
            {'name': 'Opponent3', 'level': 5},
            {'name': 'Opponent4', 'level': 7}
        ]
        self.board = [
            {'name': 'Garen', 'is_key': True, 'star': 2, 'cost': 1},
            {'name': 'Darius', 'is_key': False, 'star': 1, 'cost': 1},
            {'name': 'Fiora', 'is_key': True, 'star': 2, 'cost': 1},
            {'name': 'Vayne', 'is_key': True, 'star': 3, 'cost': 3}
        ]
        self.bench = [
            {'name': 'Lucian', 'is_key': True, 'star': 1, 'cost': 2},
            {'name': 'Poppy', 'is_key': False, 'star': 1, 'cost': 1}
        ]
        self.team = self.board + self.bench
        self.units = []
        self.win_streak = 0
        self.lose_streak = 0
        self.items = [
            {'name': 'Tear', 'count': 0},
            {'name': 'Sword', 'count': 0},
        ]

    def update_team(self):
        self.team = self.board + self.bench

    def decide_action(self):
        # Check all possible actions and decide which one to take
        # if self.should_buy_unit() and self.gold >= self.units['cost']:
        #     self.buy_unit()
        # elif self.should_sell_unit() and self.gold + self.units['cost'] >= 2:
        #     self.sell_unit()
        # elif self.should_place_unit_on_board() and len(self.board) < self.level:
        #     self.place_unit_on_board()
        # elif self.should_remove_unit_from_board() and len(self.board) == self.level:
        #     self.remove_unit_from_board()
        # elif self.should_reroll() and self.gold >= 2:
        #     self.reroll()
        # elif self.should_buy_xp() and self.gold >= 4:
        #     self.buy_xp()

        action = self.spend_gold()
        print(action)

    def spend_gold(self):
        action = 'Save gold'

        # Calculate average level of opponents
        avg_level = sum([opponent['level'] for opponent in self.opponents]) / len(self.opponents)

        # Calculate number of key champions in team
        key_champions = [champion for champion in self.team if champion['is_key']]

        # Calculate number of 2-star and 3-star champions in team
        two_star_champions = [champion for champion in self.team if champion['star'] == 2]
        three_star_champions = [champion for champion in self.team if champion['star'] == 3]

        # Calculate number of key champions on bench
        key_champions_bench = [champion for champion in self.bench if champion['is_key']]

        if self.stage in ['1', '2']:
            # Early game strategy
            if self.health > 70 and self.gold > 10:
                action = 'Buy champions'
            elif len(key_champions) < 2 or len(key_champions_bench) > 0:
                action = 'Roll for key champions'
        elif self.stage in ['3', '4']:
            # Mid game strategy
            if self.gold > 50 or (self.gold > 30 and self.health < 50):
                action = 'Level up'
            elif len(key_champions) < 4 or len(two_star_champions) < 3 or len(key_champions_bench) > 0:
                action = 'Roll for key champions'
        else:
            # Late game strategy
            if self.health < 30 or avg_level > self.team['level'] or self.lose_streak > 3:
                action = 'Spend all gold to upgrade champions or level up'
            elif len(key_champions) < len(self.team) or len(three_star_champions) < 2 or len(key_champions_bench) > 0:
                action = 'Roll for key champions'
            elif self.win_streak > 3 and self.gold > 30:
                action = 'Level up'

        return action

    def get_round(self):
        """Gets the current game round"""
        stage = 1
        game_round = 1
        # screen_capture = ImageGrab.grab(bbox=screen_coords.ROUND_POS.get_coords())
        # round_two = screen_capture.crop(screen_coords.ROUND_POS_TWO.get_coords())
        # game_round: str = image_processing.get_text_from_image(image=round_two, whitelist=image_processing.ROUND_WHITELIST)
        # if game_round in game_assets.ROUNDS:
        #     return game_round
        #
        # round_one = screen_capture.crop(screen_coords.ROUND_POS_ONE.get_coords())
        # game_round: str = ocr.get_text_from_image(image=round_one, whitelist=ocr.ROUND_WHITELIST)
        return stage, game_round

    def check_round(self):
        stage, game_round = self.get_round()
        if stage > self.stage:
            self.xp += 2
            self.stage = stage
            self.round = game_round
        if game_round > self.round:
            self.xp += 2



    def should_buy_unit(self):
        # Buy a unit if it fits into the best composition and you have enough gold
        return self.best_composition['units'].contains(self.units) and self.units['cost'] <= self.gold

    def buy_unit(self, unit):
        # Deduct the cost of the unit from your gold
        self.gold -= self.units['cost']
        self.bench.append(unit)
        self.update_team()

    def should_sell_unit(self):
        # Sell a unit if it doesn't fit into the best composition and selling it would provide enough gold for other actions
        return not self.best_composition['units'].contains(self.units) and self.units['cost'] + self.gold >= 2

    def sell_unit(self, unit):
        # Add the selling price of the unit to your gold
        self.gold += self.units['cost']
        self.bench.remove(unit)
        self.update_team()

    def should_place_unit_on_board(self):
        # Place a unit on the board if it fits into the best composition and there's space on the board
        return self.best_composition['units'].contains(self.units) and len(self.board) < self.level

    def place_unit_on_board(self, unit):
        # Add the unit to the board
        self.board.append(unit)
        self.bench.remove(unit)

    def should_remove_unit_from_board(self):
        # Remove a unit from the board if it doesn't fit into the best composition and removing it would make space for a more effective unit
        return not self.best_composition['units'].contains(self.units) and len(self.board) == self.level

    def remove_unit_from_board(self, unit):
        # Remove the unit from the board
        #TODO: can we get a better unit on the board?
        self.board.remove(unit)
        self.bench.append(unit)

    def should_reroll(self):
        # Reroll if you have enough gold and the potential benefits of getting new units in the shop outweigh the cost
        #TODO: rerolling patterns, board strenght
        return self.gold >= 2 and len(self.best_composition['units'] - self.board) > 0

    def reroll(self):
        # Deduct the cost of rerolling from your gold
        self.gold -= 2

    def should_buy_xp(self):
        # Buy XP if you have enough gold and the benefits of reaching the next level outweigh the cost
        #TODO: leveling patterns, gold vs xp benefits
        return self.gold >= 4 and self.level < 9

    def buy_xp(self):
        # Deduct the cost of buying XP from your gold and increase your level
        self.gold -= 4
        self.xp += 4
