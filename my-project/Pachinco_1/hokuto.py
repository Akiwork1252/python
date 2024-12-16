import random
# CR北斗の拳:
# (通常時の大当り確率): 1/349, (初当たり出玉): +300(80%) or +1500(20%),
# (確率変動突入率): 100%, (確率変動時の大当り確率): 当たり:1/25, 転落:1/180,
# (確率変動時の出玉振り分け): +300(25%) or +1500(75%), (大当り継続率): 88%


# 抽選（通常時）
def h_lottery():
    probability_of_winning = 349  # 大当り確率
    n = random.randint(1, probability_of_winning)  # パチンコ台の乱数
    user = random.randint(1, probability_of_winning)  # ユーザーの乱数
    # ユーザー乱数＝パチンコ台乱数 >> 大当り
    if user == n:
        # 20%でビッグボーナス (+1500玉）
        if user <= (probability_of_winning * 0.2):
            big_bonus = 1500
            print('***BIG BONUS(+1500玉)ゲット*** >>> 確率変動突入!')
            return big_bonus
        else:
            bonus = 300
            print('***BONUS(+300玉)ゲット*** >>> 確率変動突入!')
            return bonus
    else:
        print('-', end='')
        return None


# 抽選（確率変動時） 大当り(1/25)転落(1/180)どちらか引くまで確率変動ループ
def h_lottery_bonus():
    winning = 25  # 大当り確率
    losing = 180  # 転落確率
    machine_winning = random.randint(1, winning)  # パチンコ台の当たり乱数
    user_winning = random.randint(1, winning)  # ユーザーの当たり乱数
    machine_losing = random.randint(1, losing)  # パチンコ台の転落乱数
    user_losing = random.randint(1, losing)  # ユーザーの転落乱数
    # ユーザー乱数＝パチンコ台当たり乱数 >> 大当り
    if user_winning == machine_winning:
        # 75%がビッグボーナス
        if user_winning <= (winning * 0.75):
            big_bonus = 1500
            input('*BIG BONUS(+1500玉)* を引きました。>>> 確率変動継続! Enterキーを押してください。')
            return big_bonus
        else:
            bonus = 300
            input('*BONUS(+300玉)* を引きました。>>> 確率変動継続! Enterキーを押してください。')
            return bonus
    # ユーザー乱数＝パチンコ台転落乱数 >> 通常に転落
    elif user_losing == machine_losing:
        print(f'転落を引きました。確率変動を終了します。')
        return 'end'
    else:
        print('-', end='')
        return None
