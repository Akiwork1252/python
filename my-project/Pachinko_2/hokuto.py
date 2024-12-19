import random
# CR北斗の拳:
# (通常時の大当り確率): 1/349, (初当たり出玉): +300(80%) or +1500(20%),
# (確率変動突入率): 100%, (確率変動時の大当り確率): 当たり:1/25, 転落:1/180,
# (確率変動時の出玉振り分け): +300(20%) or +1500(80%), (大当り継続率): 88%


class FistOfTheNorthStar:
    big_bonus = 1500
    bonus = 300
    losing = 'END'
    lose = False

    # 抽選(通常)
    @staticmethod
    def h_lottery(jackpot_probability=1/349, big_bonus=0.2):
        user_num = random.random()
        # 当選判定(20%がBigBonus)
        if user_num <= jackpot_probability:
            big_bonus_probability = jackpot_probability * big_bonus
            if user_num < big_bonus_probability:
                print('**BigBonus(+1500)GET** >>> 確率変動突入')
                return FistOfTheNorthStar.big_bonus
            else:
                print('**Bonus(+300)GET** >>> 確率変動突入')
                return FistOfTheNorthStar.bonus
        else:
            print('-', end='')
            return FistOfTheNorthStar.lose

    # 抽選(確変)
    @staticmethod
    def h_lottery_plus(jackpot_probability=1/25, probability_of_losing=1/180, big_bonus=0.8):
        user_num = random.random()
        # 当選判定(80%がBigBonus)
        if user_num <= jackpot_probability:
            big_bonus_probability = jackpot_probability * big_bonus
            if user_num <= big_bonus_probability:
                print('**BigBonus(+1500)GET** >>> 確率変動継続')
                return FistOfTheNorthStar.big_bonus
            else:
                print('**Bonus(+300)GET** >>> 確率変動継続')
                return FistOfTheNorthStar.bonus
        # 転落
        elif user_num <= probability_of_losing:
            print('転落を引きました。 >>> 通常モードに戻ります。')
            return FistOfTheNorthStar.losing
        else:
            print('-', end='')
            return FistOfTheNorthStar.lose
