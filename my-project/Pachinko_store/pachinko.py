class PachinkoGame:
    def __init__(self):
        self.balls = 0  # 遊技で使用
        self.num_of_rotations = 0  # 遊技台回転数
        self.total_num_of_balls = 0  # 遊戯台の出玉数(出玉推移グラフ用)
        self.total_num_of_rotations = 0  # 遊戯台の総回転数(出玉推移グラフで使用)
        self.total_get_balls = 0  # 確率変動中の総獲得出玉(リザルト画面で使用)
        self.num_of_big_bonuses_earned = 0  # 確率変動中に獲得したBigBonus数(リザルト画面で使用)
        self.num_of_bonuses_earned = 0  # 確率変動中に獲得したBonus数(リザルト画面で使用)

