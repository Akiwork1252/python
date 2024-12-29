import random
from Pachinko_store.game.pachinko_func import Pachinko
# CRエヴァンゲリオン
# (通常時の大当り確率): 1/319, (初当たり出玉): +450(75%) or +1500(25%),
# (初当たり振り分け): 確率変動:70%, チャンスタイム(100回転:大当り確率1/170):30%, (確率変動時の大当り確率): 当選:1/90 回転数:170回転,
# (確率変動時の出玉振り分け): ALL+1500, (大当り継続率): 85%


class Eva(Pachinko):
    min_amount = 500  # 遊技が可能な金額
    big_bonus = 1500  # 確変突入
    bonus_plus = 450  # 確変突入
    bonus = float(bonus_plus)  # チャンスタイム突入
    bonus_time = 170  # 確変回転数
    chance_time = 100  # チャンスタイム回転数
    lose = False

# =========== 抽選関数 ============
    # 抽選(通常)
    @staticmethod
    def _lottery(probability=1 / 319, rush_entry_potential=0.7, big_bonus_potential=0.25):
        user = random.random()  # ユーザー乱数
        rush_probability = probability * rush_entry_potential  # 確率変動突入確率
        big_bonus_potential = rush_probability * big_bonus_potential
        # 当選
        if user <= probability:
            # Rush獲得
            if user <= rush_probability:
                # Big Bonus
                if user <= big_bonus_potential:
                    print(f'**BigBonus(+{Eva.big_bonus})GET** >>> 確率変動突入')
                    return Eva.big_bonus
                else:
                    print(f'**Bonus(+{int(Eva.bonus_plus)})GET** >>> 確率変動突入')
                    return Eva.bonus_plus
            # チャンスタイム獲得
            else:
                print(f'**Bonus(+{Eva.bonus})GET** >>> チャンスタイム突入')
                return Eva.bonus
        else:
            print('-', end='')
            return Eva.lose

    # 抽選(チャンスタイム(100回転:大当り確率1/170))
    @staticmethod
    def _chance_lottery(probability=1 / 170):
        user = random.random()  # ユーザー乱数取得
        # 当選(Big Bonus確定)
        if user <= probability:
            print(f'**BigBonus(+{Eva.big_bonus})GET** >>> 確率変動突入')
            return Eva.big_bonus
        else:
            print('-', end='')
            return Eva.lose

    # 抽選(確変)
    @staticmethod
    def _rush_lottery(probability=1 / 90):
        user = random.random()
        if user <= probability:
            print('**BigBonus(+1500)GET** >>> 確率変動継続')
            return Eva.big_bonus
        else:
            print('-', end='')
            return Eva.lose

# =========== エヴァンゲリオンのループ処理 ============
    # 通常時の抽選フロー
    def lottery_flow(self, jackpot=None):
        # 遊戯玉がなくなるまでループ
        while ((Pachinko.replay == 0) and (self.balls > 0)) or ((Pachinko.replay != 0) and (Pachinko.balls_for_replay > 0)):
            goes_in = Pachinko.ball_goes_in(self)
            # 入賞判定
            if goes_in is False:
                continue
            else:
                jackpot = Eva._lottery()  # jackpot(False:ハズレ、int:当選、float:チャンスタイム)
                # 当たり判定
                if jackpot is False:
                    continue
                # 当選(確変orチャンスタイム)
                else:
                    break
        return jackpot

    # チェンスタイム中の抽選フロー
    def chance_mode_lottery_flow(self, jackpot=None):
        Pachinko.num_of_rotations = 0  # 回転数初期化
        print(f'チャンスタイム({Eva.chance_time}回転)に突入します!! 大当たりを引くと確率変動に突入します。')
        Pachinko.firing_balls(self)
        # 100回転
        while Pachinko.num_of_rotations < Eva.chance_time:
            goes_in = Pachinko.ball_goes_in_rush(self)
            # 入賞判定
            if goes_in is False:
                continue
            else:
                jackpot = Eva._chance_lottery()  # jackpot(False:ハズレ、int:確変当選)
                if jackpot is False:
                    continue
                # 当選(確変突入)
                else:
                    break
        return jackpot

    # 確変中の抽選フロー
    def _rush_mode_lottery_flow(self, jackpot=None):
        # 170回転
        while Pachinko.num_of_rotations < Eva.bonus_time_flow:
            goes_in = Pachinko.ball_goes_in_rush(self)  # 入賞判定
            if goes_in is False:
                continue
            # 入賞
            else:
                jackpot = Eva._rush_lottery()  # 抽選  jackpot(False:ハズレ、int:当選)
                if jackpot is False:
                    continue
                # 当選
                else:
                    break
        return jackpot

    # 確率変動
    def bonus_time_flow(self):
        Pachinko.num_of_rotations = 0  # 回転数初期化
        print(f'確率変動({Eva.bonus_time}回転)に突入します!! 変動中に大当たりを引くと確率継続します。')
        # jackpotがNoneを返すまでループ
        while True:
            print(f'\n< 確率変動: {Pachinko.total_bonus-1}回目 >')
            Pachinko.firing_balls(self)
            jackpot = Eva._rush_mode_lottery_flow(self)
            # 当選
            if type(jackpot) is int:
                Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                Pachinko.display_rotational_count_hyper(self, jackpot)  # 情報表示(大当たり回数など)、csv保存
                Pachinko.num_of_rotations = 0  # 回転数初期化
                continue
            else:
                print(f'\n確率変動{Eva.bonus_time}回転中に大当たりを引くことができませんでした。通常モードに戻ります。')
                Pachinko.result(self)
                Pachinko.do_after_losing()
                break

    # 確変突入後(通常から突入、チャンスタイムから突入)
    def until_after_rush(self, jackpot):
        Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
        print(f'{Pachinko.num_of_rotations}回転目で大当りを引きました。おめでとうございます\n')
        Eva.bonus_time_flow(self)  # 確変ループ
        replay = Pachinko.check_for_replay_first(self)  # 持ち玉を使用して遊技を継続するか確認
        Pachinko.num_of_rotations = 0  # 回転数初期化
        return replay

# =========== メイン ============
    def main(self):
        Pachinko.seated_flow(self)
        # 所持金500円未満/持ち玉０玉/遊技終了を選択/ までループ
        while (self.money >= Eva.min_amount) or (self.balls > 0):
            playing = Pachinko.lend_flow(self)  # 遊戯玉取得(現金->遊戯玉 or 貯玉->遊戯玉)
            # 遊技を終了する
            if playing is False:
                Pachinko.end_of_game(self)
                return False
            else:
                Pachinko.firing_balls(self)
                jackpot = Eva.lottery_flow(self)  # 通常時の抽選(当選したらループを抜ける)
                if isinstance(jackpot, bool):
                    Pachinko.display_rotational_count()  # '遊技玉が無くなりました'
                    # 再プレイ中に持ち玉を使い切った場合にループを抜ける
                    if (Pachinko.replay != 0) and (self.balls == 0):
                        break
                    continue
                # チャンスタイム突入
                elif isinstance(jackpot, float):
                    Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                    print(f'{Pachinko.num_of_rotations}回転目で小当りを引きました。おめでとうございます')
                    jackpot = Eva.chance_mode_lottery_flow(self)
                    # チャンスタイム終了 >>> 通常に戻る
                    if jackpot is False:
                        print('\nチャンスタイム100回転中に大当たりを引くことができませんでした。通常モードに戻ります。')
                        Pachinko.result(self)
                        Pachinko.num_of_rotations = 0  # 回転数初期化
                        Pachinko.replay += 1
                        continue
                    # 確率変動突入
                    else:
                        replay = Eva.until_after_rush(self, jackpot)  # 獲得後処理、確変ループ、リプレイ確認、回転数初期化まで
                        # 持ち玉を使用して再プレイする
                        if replay is True:
                            Pachinko.replay += 1
                            return Eva.main(self)
                        # 結果を表示後にStoreメニューに戻る
                        else:
                            print('遊戯を終了します。')
                            Pachinko.end_of_game(self)  # 遊戯台の初期化、換金 >>> 収支表示 >>> 遊戯履歴保存 >>> 出玉推移グラフ表示
                            return False
                # 確率変動突入
                elif isinstance(jackpot, int):
                    replay = Eva.until_after_rush(self, jackpot)  # 獲得後処理、確変ループ、リプレイ確認、回転数初期化まで
                    # 持ち玉を使用して再プレイする
                    if replay is True:
                        Pachinko.replay += 1
                        return Eva.main(self)
                    # 結果を表示後にStoreメニューに戻る
                    else:
                        print('遊戯を終了します。')
                        Pachinko.end_of_game(self)  # 遊戯台の初期化、換金 >>> 収支表示 >>> 遊戯履歴保存 >>> 出玉推移グラフ表示
                        return False

        # 所持金を使い切った場合
        if self.money < Eva.min_money:
            return Pachinko.continue_or_not(self)  # 戻り値('*':退店、それ以外:メニューに戻る)
        # 持ち玉を使い切った場合
        elif (self.money >= Eva.min_money) and (self.balls == 0):
            choice = Pachinko.continue_or_not_for_replay(self)  # 戻り値('=':所持金で再遊技、'#':storeメニュー、'*':退店、)
            if choice == '=':
                Pachinko.replay = 0
                return Eva.main(self)
            else:
                return choice
