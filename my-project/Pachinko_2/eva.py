import random
# CRエヴァンゲリオン:
# (通常時の大当り確率): 1/319, (初当たり出玉): +450(75%) or +1500(25%),
# (初当たり振り分け): 確率変動:70%, チャンスタイム(100回転:大当り確率1/170):30%, (確率変動時の大当り確率): 当選:1/90 回転数:170回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率): 85%


class Eva:
    big_bonus = 1500
    bonus_plus = 450  # int:確変突入
    bonus = 450.0  # float:チャンスタイム突入
    lose = None

    # 抽選(通常)
    @staticmethod
    def e_lottery(jackpot_probability=1/319, rush=0.7, big_bonus=0.2):
        user_num = random.random()
        # 当選判定(70%で確変突入、そのうち20%がBigBonus)
        if user_num <= jackpot_probability:
            rush_probability = jackpot_probability * rush  # 確変突入確率
            # Rush判定
            if user_num <= rush_probability:
                big_bonus_probability = rush_probability * big_bonus  # BigBonus確率
                # BigBonus判定
                if user_num <= big_bonus_probability:
                    print('**BigBonus(+1500)GET** >>> 確率変動突入')
                    return Eva.big_bonus
                else:
                    print('**Bonus(+450)GET** >>> 確率変動突入')
                    return Eva.bonus_plus
            else:
                print('**Bonus(+450)**GET >>> チャンスタイム突入(100回転)')
                return Eva.bonus
        else:
            print('-', end='')
            return Eva.lose

    # 抽選(チャンスタイム)
    @staticmethod
    def e_lottery_chance(jackpot_probability=1/170):
        user_num = random.random()
        if user_num <= jackpot_probability:
            print('**BigBonus(+1500)GET** >>> 確率変動突入')
            return Eva.big_bonus
        else:
            print('-', end='')
            return Eva.lose

    # 抽選(確変)
    @staticmethod
    def e_lottery_plus(jackpot_probability=1/90):
        user_num = random.random()
        if user_num <= jackpot_probability:
            print('**BigBonus(+1500)GET** >>> 確率変動継続')
            return Eva.big_bonus
        else:
            print('-', end='')
            return Eva.lose
