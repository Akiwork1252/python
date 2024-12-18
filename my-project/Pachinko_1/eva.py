import random
# CRエヴァンゲリオン:
# (通常時の大当り確率): 1/319, (初当たり出玉): +450(75%) or +1500(25%),
# (初当たり振り分け): 確率変動:70%, チャンスタイム(100回転:大当り確率1/170):30%, (確率変動時の大当り確率): 当選:1/90 回転数:170回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率): 85%


# 抽選（通常時）
def e_lottery():
    probability_of_winning = 319  # 大当り確率
    n = random.randint(1, probability_of_winning)  # パチンコ台の乱数
    user = random.randint(1, probability_of_winning)  # ユーザーの乱数
    # ユーザー乱数＝パチンコ台乱数 >> 大当り
    if user == n:
        # 70%で確率変動突入
        if user <= (probability_of_winning * 0.7):
            # 初回大当りのうちの25%がビッグボーナス (+1500玉)
            if user <= ((probability_of_winning * 0.7) * 0.25):
                big_bonus = 1500
                print('***BIG BONUS(+1500玉)ゲット*** >>> 確率変動突入!(170回転)')
                return big_bonus
            else:
                bonus = 450
                print('***BONUS(+450玉)ゲット*** >>> 確率変動突入!(170回転)')
                return bonus
        else:
            bonus = 450
            print('***BONUS(+450玉)ゲット*** >>> チャンスタイム突入!(100回転)')
            return float(bonus)  # チャンスタイムであればfloat型で返す
    else:
        print('-', end='')
        return None


# 抽選（チャンスタイム）
def e_lottery_chance():
    probability_of_winning = 170
    n = random.randint(1, probability_of_winning)  # パチンコ台の乱数
    user = random.randint(1, probability_of_winning)  # ユーザーの乱数
    # ユーザー乱数＝パチンコ台乱数 >> 大当り+確率変動突入
    if user == n:
        big_bonus = 1500
        print('***BIG BONUS(+1500玉)ゲット*** >>> 確率変動突入!(170回転)')
        return big_bonus
    else:
        print('-', end='')
        return None


# 抽選（確率変動時） 大当り(1/90)
def e_lottery_bonus():
    winning = 90  # 大当り確率
    n_winning = random.randint(1, winning)  # パチンコ台の大当り乱数
    user = random.randint(1, winning)  # ユーザーの乱数
    # ユーザー乱数＝パチンコ台当たり乱数 >> 大当り(+1500玉)
    if user == n_winning:
        big_bonus = 1500
        input('*BIG BONUS(+1500玉)* を引きました。>>> 確率変動継続!(170回転) Enterキーを押してください。')
        return big_bonus
    else:
        print('-', end='')
        return None
