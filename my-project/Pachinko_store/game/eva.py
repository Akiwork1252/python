import random
from Pachinko_store.game.pachinko_func import Pachinko

# CRエヴァンゲリオン
# (通常時の大当り確率): 1/319, (初当たり出玉): +450(75%) or +1500(25%),
# (初当たり振り分け): 確率変動:70%, チャンスタイム(100回転:大当り確率1/170):30%, (確率変動時の大当り確率): 当選:1/90 回転数:170回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率): 85%


class Eva(Pachinko):
    big_bonus = 1500
    bonus = 450
    lose = False

# =========== 抽選関数 ============
    # 抽選(通常)
    @staticmethod
    def lottery():
        pass

    # 抽選(チャンスタイム)
    @staticmethod
    def lottery_chance():
        pass

    # 抽選(確変)
    @staticmethod
    def lottery_rush():
        pass

# =========== メイン ============
    def main(self):
        pass