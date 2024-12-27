import random
from Pachinko_store.game.pachinko_func import Pachinko

# CR魔法少女まどかマギカ:
# (通常時の大当り確率): 1/199, (初当たり出玉): +450(90%) or +1500(10%),
# (確率変動突入率): 50%, (確率変動時の大当り確率): 1/70 回転数:80回転, (確率変動<上位>時の確率): 1/60: 回転数:120回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率):68% or 86%, (補足)確率変動中の当たり1/4で確率変動<上位>に突入


class MadoMagi(Pachinko):
    big_bonus = 1500
    bonus = 450
    lose = False

# =========== 抽選関数 ============
    # 抽選(通常)
    @staticmethod
    def lottery():
        pass

    # 抽選(確変)
    @staticmethod
    def lottery_rush():
        pass

    # 抽選(上位確変)
    @staticmethod
    def lottery_rush_plus():
        pass

# =========== メイン ============
    def main(self):
        pass