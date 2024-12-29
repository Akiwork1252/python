import random
from Pachinko_store.game.pachinko_func import Pachinko
# CR北斗の拳:
# (通常時の大当り確率): 1/349, (初当たり出玉): +300(80%) or +1500(20%),
# (確率変動突入率): 100%, (確率変動時の大当り確率): 当たり:1/30, 転落:1/180,
# (確率変動時の出玉振り分け): +300(20%) or +1500(80%), (大当り継続率): 88%


class Hokuto(Pachinko):
    min_amount = 500  # 遊技が可能な金額
    big_bonus = 1500
    bonus = 300
    bonus_end = 'END'
    lose = False

# =========== 抽選関数 ============
    # 抽選(通常)
    @staticmethod
    def _lottery(probability=1 / 349, big_bonus_probability=0.2):
        user = random.random()  # ユーザー乱数
        # 当選
        if user <= probability:
            # Big Bonus
            if user <= (probability * big_bonus_probability):
                print(f'**BigBonus(+{Hokuto.big_bonus})GET** >>> 確率変動突入')
                return Hokuto.big_bonus
            else:
                print(f'**Bonus(+{Hokuto.bonus})GET** >>> 確率変動突入')
                return Hokuto.bonus
        else:
            print('-', end='')
            return Hokuto.lose

    # 抽選(確変)
    @staticmethod
    def _rush_lottery(probability_of_winning=1 / 30, probability_of_losing=1 / 180, big_bonus_probability=0.8):
        user = random.random()
        # 当選
        if user <= probability_of_winning:
            if user <= (probability_of_winning * big_bonus_probability):
                print(f'**BigBonus(+{Hokuto.big_bonus})GET** >>> 確率変動継続')
                return Hokuto.big_bonus
            else:
                print(f'**Bonus(+{Hokuto.bonus})GET** >>> 確率変動継続')
                return Hokuto.bonus
        # 転落
        elif user >= (1-probability_of_losing):
            print('転落を引きました。 >>> 通常モードに戻ります。')
            return Hokuto.bonus_end
        else:
            print('-', end='')
            return Hokuto.lose

# =========== 北斗の拳のループ処理 ============
    # 通常時の抽選フロー
    def lottery_flow(self, jackpot=None):
        # 遊戯玉がなくなるまでループ
        while ((Pachinko.replay == 0) and (self.balls > 0)) or ((Pachinko.replay != 0) and (Pachinko.balls_for_replay > 0)):
            goes_in = Pachinko.ball_goes_in(self)
            # 入賞判定
            if goes_in is False:
                continue
            else:
                jackpot = Hokuto._lottery()  # jackpot(False:ハズレ、int:当選、)
                # 当たり判定
                if jackpot is False:
                    continue
                # 当選
                else:
                    break
        return jackpot

    # 確変時の抽選フロー <<< bonus_time()で実行
    def _rush_mode_lottery_flow(self, jackpot=None):
        # 転落か当選を引くまでループ
        while True:
            goes_in = Pachinko.ball_goes_in_rush(self)
            if goes_in is False:
                continue
            else:
                jackpot = Hokuto._rush_lottery()  # jackpot(False:ハズレ、int:当選、str:転落)
                if jackpot is False:
                    continue
                # 当選or転落
                else:
                    break
        return jackpot

    # 確率変動
    def bonus_time_flow(self):
        Pachinko.num_of_rotations = 0  # 回転数初期化
        print('確率変動に突入します!! 確率変動は"転落当たり"を引くまで継続します。')
        # 転落を引くまでループ
        while True:
            print(f'\n< 確率変動: {Pachinko.total_bonus}回目 >')
            Pachinko.firing_balls(self)
            jackpot = Hokuto._rush_mode_lottery_flow(self)
            # 当選
            if isinstance(jackpot, int):
                Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                Pachinko.display_rotational_count_hyper(self, jackpot)  # 情報表示(大当たり回数など)、csv保存
                Pachinko.num_of_rotations = 0  # 回転数初期化
                continue
            # 転落
            else:
                Pachinko.result(self)  # 確変終了後のリザルト画面表示
                Pachinko.do_after_losing()  # 回転数初期化、ボーナス回数初期化、csv保存
                break

# =========== メイン ============
    def main(self):
        Pachinko.seated_flow(self)
        # 所持金500円未満/持ち玉０玉/遊技終了を選択/ までループ
        while (self.money >= Hokuto.min_amount) or (self.balls > 0):
            playing = Pachinko.lend_flow(self)  # 遊戯玉取得(現金->遊戯玉 or 貯玉->遊戯玉)
            # 遊技を終了する
            if playing is False:
                Pachinko.end_of_game(self)
                return False
            else:
                Pachinko.firing_balls(self)
                jackpot = Hokuto.lottery_flow(self)  # 通常時の抽選(当選したらループを抜けてint型を返す)
                if isinstance(jackpot, bool):
                    Pachinko.display_rotational_count()  # '遊技玉が無くなりました'
                    # 再プレイ中に持ち玉を使い切った場合にループを抜ける
                    if (Pachinko.replay != 0) and (self.balls == 0):
                        break
                    continue
                # 確変突入
                else:
                    Pachinko.do_after_winning(self, jackpot)  # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存
                    print(f'{Pachinko.num_of_rotations}回転目で大当りを引きました。おめでとうございます\n')
                    Hokuto.bonus_time_flow(self)  # 確変(転落を引くまでループ)
                    replay = Pachinko.check_for_replay_first(self)  # 持ち玉を使用して遊技を継続するか確認
                    Pachinko.num_of_rotations = 0  # 回転数初期化
                    # 持ち玉を使用して再プレイする
                    if replay is True:
                        Pachinko.replay += 1
                        return Hokuto.main(self)
                    # 結果を表示後にStoreメニューに戻る
                    else:
                        print('遊戯を終了します。')
                        Pachinko.end_of_game(self)  # 遊戯台の初期化、換金 >>> 収支表示 >>> 遊戯履歴保存 >>> 出玉推移グラフ表示
                        return False

        # 所持金を使い切った場合
        if self.money < Hokuto.min_money:
            return Pachinko.continue_or_not(self)  # 戻り値('*':退店、それ以外:メニューに戻る)
        # 持ち玉を使い切った場合
        elif (self.money >= Hokuto.min_money) and (self.balls == 0):
            choice = Pachinko.continue_or_not_for_replay(self)  # 戻り値('=':所持金で再遊技、'#':storeメニュー、'*':退店、)
            if choice == '=':
                Pachinko.replay = 0
                return Hokuto.main(self)
            else:
                return choice
