import random
# CR魔法少女まどかマギカ:
# (通常時の大当り確率): 1/199, (初当たり出玉): +450(90%) or +1500(10%),
# (確率変動突入率): 50%, (確率変動時の大当り確率): 1/70 回転数:80回転, (確率変動<上位>時の確率): 1/60: 回転数:120回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率):68% or 86%, (補足)確率変動中の当たり1/4で確率変動<上位>に突入


# 抽選（通常）
def m_lottery():
    probability_of_winning = 199  # 大当り確率
    n = random.randint(1, probability_of_winning)  # パチンコ台の乱数
    user = random.randint(1, probability_of_winning)  # ユーザーの乱数
    # ユーザー乱数＝パチンコ台乱数 >> 大当り
    if user == n:
        # 50%で確率変動突入
        if user <= (probability_of_winning * 0.5):
            # 初回大当りのうちの10%がビッグボーナス (+1500玉)
            if user <= ((probability_of_winning * 0.5) * 0.1):
                big_bonus = 1500
                print('***BIG BONUS(+1500玉)ゲット*** >>> 確率変動突入!(80回転)')
                return big_bonus
            else:
                bonus = 450
                print('***BONUS(+450玉)ゲット*** >>> 確率変動突入!(80回転)')
                return bonus
        else:
            bonus = 450
            print('***BONUS(+450玉)ゲット*** >>> 通常に戻ります。')
            return float(bonus)
    else:
        print('-', end='')
        return None


# 抽選（確率変動） 大当り(1/70: 80回)、当たりの内1/4で上位突入
def m_lottery_bonus():
    winning = 70
    n_winning = random.randint(1, winning)
    user = random.randint(1, winning)
    if user == n_winning:
        big_bonus = 1500
        lucky = random.randint(0, 3)
        if lucky == 0:
            print('!!!<Lucky>!!!', end='')
            input('*BIG BONUS(+1500玉)* を引きました。>>> 確率変動<上位>突入!(120回転) Enterキーを押してください。')
            return float(big_bonus)
        else:
            input('*BIG BONUS(+1500玉)* を引きました。>>> 確率変動継続!(80回転) Enterキーを押してください。')
            return big_bonus
    else:
        print('-', end='')
        return None


# 抽選（確率変動<上位>） 大当り(1/60: 120回)
def m_lottery_bonus_plus():
    winning = 60
    n_winning = random.randint(1, winning)
    user = random.randint(1, winning)
    if user == n_winning:
        big_bonus = 1500
        input('*BIG BONUS(+1500玉)* を引きました。>>> 確率変動<上位>継続!(120回転) Enterキーを押してください。')
        return big_bonus
    else:
        print('-', end='')
        return None
