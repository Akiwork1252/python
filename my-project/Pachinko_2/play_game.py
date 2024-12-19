from pachinko import Pachinko
from game_info import GameData


class GameCommonalities(Pachinko):
    def __init__(self, name, age, money):
        super().__init__(name, age, money)

    def


class GameMain(GameCommonalities):
    def __init__(self, name, age, money):
        super().__init__(name, age, money)

    # 北斗の拳
    def fist_of_the_north_star(self, model='CR北斗の拳'):
        self.model_played = model
        print('-'*20)
        print(f'{model}で遊びます。')
        GameData.add_data(self.rotational_count, self.balls)  # (回転数:0/玉推移:0)

    # エヴァンゲリオン
    def neon_genesis_evangelion(self, model='CRエヴァンゲリオン'):
        self.model_played = model
        print('-'*20)
        print(f'{model}で遊びます。')
        GameData.add_data(self.rotational_count, self.balls)  # (回転数:0/玉推移:0)

    # 魔法少女まどかマギカ
    def puella_magi_madoka_magika(self, model='魔法少女まどかマギカ'):
        self.model_played = model
        print('-'*20)
        print(f'{model}で遊びます。')
        GameData.add_data(self.rotational_count, self.balls)  # (回転数:0/玉推移:0)
