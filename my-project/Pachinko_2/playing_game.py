from pachinko import Pachinko
from game_info import GameData
from store import Store
from eva import Eva
from hokuto import Hokuto
from madokamagika import MadokaMagika


class GameGeneralFlow(Pachinko):
    def __init__(self, name, age, money, model):
        super().__init__(name, age, money, model)
        self.balls_for_replay = 0  # 持ち玉遊戯用

    # 通常時の抽選判定
    normal_lottery_list = {
        'CR北斗の拳': Hokuto.h_lottery,
        'CRエヴァンゲリオン': Eva.e_lottery,
        'CR魔法少女まどかマギカ': MadokaMagika.m_lottery,
    }

    # 持ち玉遊戯確認
    def _check_for_replay(self):
        print('持ち玉で遊戯を継続しますか？', end='')
        y_n = Store.input_yer_or_no()
        if y_n is True:
            GameGeneralFlow._processing_for_replay(self)
            return True
        else:
            return False

    # 大当たり終了後の持ち玉遊戯を行う場合    # ※125玉使いきるまでに当たりを引いたら残玉をballsに足す必要あり
    def _processing_for_replay(self, min_balls=125):
        if self.balls <= min_balls:
            self.balls_for_replay = self.balls
            print(f'持ち玉を全て払い出します。[持ち玉:{self.balls}玉 >>> 0玉]')
        else:
            before = self.balls
            self.balls -= 125
            self.balls_for_replay += 125
            print(f'持ち玉から{min_balls}玉を払い出します。[持ち玉:{before}玉 >>> {self.balls}玉]')

    # 遊戯終了後の処理
    def _end_of_game(self):
        Pachinko.data_rewrite(self)  # 遊戯台の初期化、csv保存
        Pachinko.revenue(self)  # 換金 >>> 収支表示 >>> 遊戯履歴保存 >>> 出玉推移グラフ表示
        Pachinko.input_enter()

    # 遊戯開始準備  <<< GameMainから実行
    def seated(self):
        print('-'*20)
        print(f'{self.models_to_play}で遊びます。')
        GameData.add_data(self.rotational_count, self.balls)  # 遊戯データを記録(0/0)

    # 遊戯開始(現金>>>遊戯玉 or 持ち玉>>>遊戯玉)  <<< GameMainから実行
    def start_playing(self, min_amount=500):
        # 現金 >>> 遊戯玉
        if self.balls == 0:
            Pachinko.lend(self)
        # 持ち玉 >>> 遊戯玉
        else:
            y_n = GameGeneralFlow._check_for_replay(self)
        # 現金or持ち玉>>>遊戯玉に交換しなければ遊戯を終了
        if (self.balls == 0) or (self.balls_for_replay == 0):
            print('遊戯を終了します。', end='')
            Store.input_enter()
            GameGeneralFlow._end_of_game(self)
            return False
        else:
            Pachinko.firing_balls(self)
            return True

    # 遊戯(通常時: ヘソ入賞〜)  <<< GameMainから実行
    def game_normal_mode(self):
        while self.balls > 0:
            did_enter = Pachinko.ball_goes_in(self)
            if did_enter is False:
                continue
            else:
                jackpot = GameGeneralFlow.normal_lottery_list[self.models_to_play]()
                if jackpot is False:
                    continue
                else:
                    return jackpot


class GameMain(GameGeneralFlow):
    def __init__(self, name, age, money, model):
        super().__init__(name, age, money, model)

    # 北斗の拳
    def fist_of_the_north_star(self, model='CR北斗の拳'):
        GameGeneralFlow.seated(self)
        while True:
            exchange_for_balls = GameGeneralFlow.start_playing(self)  # 現金or持ち玉 >>> 遊戯玉
            if exchange_for_balls is False:
                break
            jackpot = GameGeneralFlow.game_normal_mode(self)  # ヘソ入賞判定 >>> 抽選(Trueを返したら当たり)
            if jackpot is False:
                continue

    # エヴァンゲリオン
    def neon_genesis_evangelion(self, model='CRエヴァンゲリオン'):
        GameData.add_data(self.rotational_count, self.balls)  # (回転数:0/玉推移:0)

    # 魔法少女まどかマギカ
    def puella_magi_madoka_magika(self, model='魔法少女まどかマギカ'):
        GameData.add_data(self.rotational_count, self.balls)  # (回転数:0/玉推移:0)


if __name__ == '__main__':
    pass
    # GameMain.fist_of_the_north_star(aki)
