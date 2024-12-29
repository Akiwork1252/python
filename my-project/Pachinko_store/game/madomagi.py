import random
from Pachinko_store.game.pachinko_func import Pachinko

# CR魔法少女まどかマギカ:
# (通常時の大当り確率): 1/199, (初当たり出玉): +450(90%) or +1500(10%),
# (確率変動突入率): 50%, (確率変動時の大当り確率): 1/70 回転数:80回転, (確率変動<上位>時の確率): 1/60: 回転数:120回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率):68% or 86%, (補足)確率変動中の当たり1/4で確率変動<上位>に突入


class MadoMagi(Pachinko):
    min_amount = 500  # 遊技が可能な金額
    big_bonus = 1500
    big_bonus_plus = float(big_bonus)  # 上位確率変動突入 <<< 確変中の当たりで発生
    bonus = 450
    bonus_n = float(bonus)  # 通常
    bonus_time = 80
    top_bonus_time = 120
    promotion_potential = 0.25  # 上位確変突入確率
    lose = False

# =========== 抽選関数 ============
    # 抽選(通常)
    @staticmethod
    def _lottery(probability=1 / 199, rush_entry_potential=0.5, big_bonus_potential=0.1):
        user = random.random()
        rush_probability = probability * rush_entry_potential
        big_bonus_probability = rush_probability * big_bonus_potential
        # 当選
        if user <= probability:
            # 確変獲得
            if user <= rush_probability:
                # Big Bonus獲得
                if user <= big_bonus_probability:
                    print(f'**BigBonus(+{MadoMagi.big_bonus})GET** >>> 確率変動突入')
                    return MadoMagi.big_bonus
                else:
                    print(f'**Bonus(+{MadoMagi.bonus})GET** >>> 確率変動突入')
                    return MadoMagi.bonus
            else:
                print(f'**Bonus(+{int(MadoMagi.bonus_n)})GET** >>> 通常')
                return MadoMagi.bonus_n
        else:
            print('-', end='')
            return MadoMagi.lose

    # 抽選(確変)
    @staticmethod
    def _rush_lottery(probability=1 / 70):
        user = random.random()
        promotion_probability = probability * MadoMagi.promotion_potential  # 上位確率変動突入確率
        # 当選
        if user <= probability:
            # 上位突入
            if user <= promotion_probability:
                print(f'**<Lucky!!>BigBonus(+{int(MadoMagi.big_bonus_plus)})GET** >>> 確率変動<上位>突入')
                return MadoMagi.big_bonus_plus
            else:
                print(f'**BigBonus(+{MadoMagi.big_bonus})GET** >>> 確率変動継続')
                return MadoMagi.big_bonus
        else:
            print('-', end='')
            return MadoMagi.lose

    # 抽選(上位確変)
    @staticmethod
    def _top_rush_lottery(probability=1 / 60):
        user = random.random()
        # 当選
        if user <= probability:
            print(f'**BigBonus(+{MadoMagi.big_bonus})GET** >>> 確率変動継続')
            return MadoMagi.big_bonus
        else:
            print('-', end='')
            return MadoMagi.lose

# =========== 魔法少女まどかマギカのループ処理 ============
    # 通常時の抽選フロー
    def lottery_flow(self, jackpot=None):
        # 遊戯玉がなくなるまでループ
        while ((Pachinko.replay == 0) and (self.balls > 0)) or ((Pachinko.replay != 0) and (Pachinko.balls_for_replay > 0)):
            goes_in = Pachinko.ball_goes_in(self)
            # 入賞判定
            if goes_in is False:
                continue
            else:
                jackpot = MadoMagi._lottery()  # jackpot(False:ハズレ、int:当選、float:通常)
                # 当たり判定
                if jackpot is False:
                    continue
                # 当選(確変orチャンスタイム)
                else:
                    break
        return jackpot

    # 確変中の抽選フロー
    def _rush_mode_lottery_flow(self, jackpot=None):
        # 80回転
        while Pachinko.num_of_rotations < MadoMagi.bonus_time:
            goes_in = Pachinko.ball_goes_in_rush(self)  # 入賞判定
            if goes_in is False:
                continue
            # 入賞
            else:
                jackpot = MadoMagi._rush_lottery()  # 抽選  jackpot(False:ハズレ、int:当選, float:上位突入)
                if jackpot is False:
                    continue
                # 当選
                else:
                    break
        return jackpot

    # 上位確変中の抽選フロー
    def _top_rush_mode_lottery_flow(self, jackpot=None):
        # 120回転
        while Pachinko.num_of_rotations < MadoMagi.top_bonus_time:
            goes_in = Pachinko.ball_goes_in_rush(self)  # 入賞判定
            if goes_in is False:
                continue
            # 入賞
            else:
                jackpot = MadoMagi._top_rush_lottery()  # 抽選  jackpot(False:ハズレ、int:当選, float:上位突入)
                if jackpot is False:
                    continue
                # 当選
                else:
                    break
        return jackpot

    # 確率変動
    def bonus_time_flow(self):
        top_rush_probability = MadoMagi.promotion_potential * 100
        Pachinko.num_of_rotations = 0  # 回転数初期化
        print(f'確率変動({MadoMagi.bonus_time}回転)に突入します!!')
        print(f'変動中に大当たりを引くと確率継続します。また、{int(top_rush_probability)}%の確率で上位確率変動に突入します。')
        # jackpotがNoneを返すまでループ
        while True:
            print(f'\n< 確率変動: {Pachinko.total_bonus}回目 >')
            Pachinko.firing_balls(self)
            jackpot = MadoMagi._rush_mode_lottery_flow(self)
            # 当選
            if type(jackpot) is int:
                Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                Pachinko.display_rotational_count_hyper(self, jackpot)  # 情報表示(大当たり回数など)、csv保存
                Pachinko.num_of_rotations = 0  # 回転数初期化
                continue
            # 当選＋上位突入
            elif isinstance(jackpot, float):
                return jackpot
            else:
                print(f'\n確率変動{MadoMagi.bonus_time}回転中に大当たりを引くことができませんでした。通常モードに戻ります。')
                Pachinko.result(self)
                Pachinko.do_after_losing()
                break

    # 確率変動<上位>
    def top_bonus_time_flow(self, count=1):
        Pachinko.num_of_rotations = 0  # 回転数初期化
        print(f'確率変動<上位>({MadoMagi.top_bonus_time}回転)に突入します!! 変動中に大当たりを引くと確率継続します。')
        # jackpotがNoneを返すまでループ
        while True:
            print(f'\n< 確率変動<上位>: {count}回目 >')
            Pachinko.firing_balls(self)
            jackpot = MadoMagi._top_rush_mode_lottery_flow(self)
            # 当選
            if type(jackpot) is int:
                Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                Pachinko.display_rotational_count_hyper(self, jackpot)  # 情報表示(大当たり回数など)、csv保存
                Pachinko.num_of_rotations = 0  # 回転数初期化
                continue
            else:
                print(f'\n確率変動{MadoMagi.top_bonus_time}回転中に大当たりを引くことができませんでした。通常モードに戻ります。')
                Pachinko.result(self)
                Pachinko.do_after_losing()
                break

# =========== メイン ============
    def main(self):
        Pachinko.seated_flow(self)
        # 所持金500円未満/持ち玉０玉/遊技終了を選択/ までループ
        while (self.money >= MadoMagi.min_amount) or (self.balls > 0):
            playing = Pachinko.lend_flow(self)  # 遊戯玉取得(現金->遊戯玉 or 貯玉->遊戯玉)
            # 遊技を終了する
            if playing is False:
                Pachinko.end_of_game(self)
                return False
            else:
                Pachinko.firing_balls(self)
                jackpot = MadoMagi.lottery_flow(self)  # 通常時の抽選(当選したらループを抜ける)
                if isinstance(jackpot, bool):
                    Pachinko.display_rotational_count()  # '遊技玉が無くなりました'
                    # 再プレイ中に持ち玉を使い切った場合にループを抜ける
                    if (Pachinko.replay != 0) and (self.balls == 0):
                        break
                    continue
                elif isinstance(jackpot, float):
                    Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                    print(f'{Pachinko.num_of_rotations}回転目で小当りを引きました。おめでとうございます')
                    Pachinko.result(self)
                    Pachinko.num_of_rotations = 0  # 回転数初期化
                    Pachinko.replay += 1
                    continue
                else:
                    Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                    print(f'{Pachinko.num_of_rotations}回転目で大当りを引きました。おめでとうございます\n')
                    top_mode = MadoMagi.bonus_time_flow(self)  # 確変ループ
                    if isinstance(top_mode, float):
                        MadoMagi.top_bonus_time_flow(self)  # 上位確変ループ
                    replay = Pachinko.check_for_replay_first(self)  # 持ち玉を使用して遊技を継続するか確認
                    Pachinko.num_of_rotations = 0  # 回転数初期化
                    # 持ち玉を使用して再プレイする
                    if replay is True:
                        Pachinko.replay += 1
                        return MadoMagi.main(self)
                    # 結果を表示後にStoreメニューに戻る
                    else:
                        print('遊戯を終了します。')
                        Pachinko.end_of_game(self)  # 遊戯台の初期化、換金 >>> 収支表示 >>> 遊戯履歴保存 >>> 出玉推移グラフ表示
                        return False
        # 所持金を使い切った場合
        if self.money < MadoMagi.min_money:
            return Pachinko.continue_or_not(self)  # 戻り値('*':退店、それ以外:メニューに戻る)
        # 持ち玉を使い切った場合
        elif (self.money >= MadoMagi.min_money) and (self.balls == 0):
            choice = Pachinko.continue_or_not_for_replay(self)  # 戻り値('=':所持金で再遊技、'#':storeメニュー、'*':退店、)
            if choice == '=':
                Pachinko.replay = 0
                return MadoMagi.main(self)
            else:
                return choice
