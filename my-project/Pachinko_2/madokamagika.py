import random
# CR魔法少女まどかマギカ:
# (通常時の大当り確率): 1/199, (初当たり出玉): +450(90%) or +1500(10%),
# (確率変動突入率): 50%, (確率変動時の大当り確率): 1/70 回転数:80回転, (確率変動<上位>時の確率): 1/60: 回転数:120回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率):68% or 86%, (補足)確率変動中の当たり1/4で確率変動<上位>に突入


class MadokaMagika:
    big_bonus = 1500
    big_bonus_plus = 1500.0  # float:上位確変突入
    bonus_plus = 450  # int:確変突入
    bonus = 450.0  # float:通常
    lose = None

    # 抽選(通常)
    @staticmethod
    def m_lottery(jackpot_probability=1/199, rush=0.5, big_bonus=0.1):
        user_num = random.random()
        # 当選判定(50%で確変突入、そのうち10%がBigBonus)
        if user_num <= jackpot_probability:
            rush_probability = jackpot_probability * rush
            # Rush判定
            if user_num <= rush_probability:
                big_bonus_probability = rush_probability * big_bonus
                # BigBonus判定
                if user_num <= big_bonus_probability:
                    print('**BigBonus(+1500)GET** >>> 確率変動突入')
                    return MadokaMagika.big_bonus
                else:
                    print('**Bonus(+450)GET** >>> 確率変動突入')
                    return MadokaMagika.bonus_plus
            else:
                print('**Bonus(+450)GET** >>> 確率変動を引けませんでした。通常に戻ります。')
                return MadokaMagika.bonus
        else:
            print('-', end='')
            return MadokaMagika.lose

    # 抽選(確変)
    @staticmethod
    def m_lottery_plus(jackpot_probability=1/70, rush_plus=0.25):
        user_num = random.random()
        # 当選判定(25%で上位確率変動に突入)
        if user_num <= jackpot_probability:
            rush_plus_probability = jackpot_probability * rush_plus
            # 上位突入判定
            if user_num <= rush_plus_probability:
                print('** <LUCKY> BigBonus(+1500)GET** >>> 確率変動<上位>突入')
                return MadokaMagika.big_bonus_plus
            else:
                print('**BigBonus(+1500)GET** >>> 確率変動継続')
                return MadokaMagika.big_bonus
        else:
            print('-', end='')
            return MadokaMagika.lose
