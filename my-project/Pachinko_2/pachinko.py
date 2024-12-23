import random
from account import Account
from game_info import GameData
from hokuto import Hokuto
from operate_db import DataBase
from eva import Eva
from madokamagika import MadokaMagika
from store import Store


# パチンコクラス
#  ・パチンコの共通機能(玉変換、ヘソ入賞判定(通常・確変)、回転数表示(通常・確変)、Bonus結果表示、換金)
class Pachinko(Store):
    def __init__(self, name, age, money, model):
        super().__init__(name, age, money, model)
        self.get_big_bonus_balls = 1500  # BigBonus獲得出玉
        self.get_bonus_balls = 450  # Bonus獲得出玉(エヴァ、まどマギ)
        self.get_bonus_balls_h = 300  # Bonus獲得出玉(北斗)
        self.total_bonus_count = 0  # 総大当り回数
        self.big_bonus_count = 0  # BigBonus回数(内訳)
        self.bonus_count = 0  # Bonus回数(内訳)
        self.exchange_rate = 4  # 換金率

    # 回転数の加算(遊戯中データ、出玉推移データ用)　<<< 玉入賞時に実行
    def _add_rotational_count(self):
        self.rotational_count += 1
        self.total_rotational_count += 1

    # 出玉の減少(遊戯玉、出玉推移データ用) <<< 玉入賞失敗時に実行
    def _decreased_balls(self):
        self.balls -= 1
        self.total_balls -= 1

    # 所持金をパチンコ玉に変換(500円 -> 125玉) <<< playing_game.py[GGF]から実行(遊戯開始前)
    def lend(self, amount=500, ball=125):
        print(f'\n{amount}円をパチンコ玉{ball}玉に交換できます。交換しますか？', end='')
        y_n = Store.input_yer_or_no()  # (y/n)
        if y_n == 'n':
            return False  # メニュー画面に戻る
        else:
            self.money -= amount  # 所持金から引く
            self.investment_amount += amount  # 総投資額加算
            self.balls += 125  # 遊戯玉を追加
            print('交換完了：[現金:500円 ＞＞＞ 持ち玉:125玉]')
            return self.balls

    # パチンコ玉を発射する <<< playing_game.py[GGF]から実行(遊戯開始時)
    def firing_balls(self):
        print('Enterキーを押すとパチンコ玉を発射します。', end='')
        Store.input_enter()
        self.play_check += 1  # 遊戯チェック:一度でも玉を発射していれば、遊戯履歴を残す

    # ヘソ入賞(通常時) 入賞確率7%{1000円(250玉)で約17回転} <<< playing_game.py[GGF]から実行(遊戯中)
    def ball_goes_in(self, probability=7/100):
        if random.random() <= probability:
            Pachinko._add_rotational_count(self)  # 回転数、総回転数を加算
            return True
        else:
            Pachinko._decreased_balls(self)  # 遊戯玉減少、出玉推移減少
            return False

    # ヘソ入賞(確変時) 入賞確率90%  playing_game.py[GGF]から実行(遊戯中)
    def ball_goes_in_hyper(self, probability=9/10):
        if random.random() <= probability:
            Pachinko._add_rotational_count(self)  # 回転数、総回転数を加算
            return True
        else:
            Pachinko._decreased_balls(self)  # 遊戯玉減少、出玉推移減少
            return False

    # 遊戯中の情報表示(通常時):回転数 <<< playing_game.py[GGF]から実行(遊戯通常タイム)
    def display_rotational_count(self):
        print(f'>>> 現在の回転数: {self.rotational_count}回転')

    # 遊戯中の情報表示(確変時):回転数、獲得出玉、総出玉、ボーナス回数 <<< playing_game.py[GGF]から実行(遊戯確変中)
    # 大当り獲得時の処理(回転数初期化、遊戯玉追加、獲得出玉追加、出玉推移をcsvに保存)
    def display_rotational_count_hyper(self, jackpot):  # 引数:jackpot >>> 出玉(300 or 450 or 1500 or False)
        if isinstance(jackpot, (int, float)):  # 当たり
            jackpot = int(jackpot)  # エヴァ、まどマギでfloat型を受け取る場合があるため、intに変換する
            before = self.balls
            Pachinko.data_update(self, jackpot)  # 大当り獲得時の処理(遊戯玉加算、総出玉加算、回転数初期化, csvファイルにデータ保存)
            print(f'== information ==')
            print(f'回転数:{self.rotational_count}回転')
            print(f'大当り{self.total_bonus_count}回目獲得!(BIG-BONUS:{self.big_bonus_count}回、BONUS:{self.bonus_count}')
            print(f'獲得出玉:{jackpot}玉、　総獲得出玉:{before} >>> {self.get_balls}玉')
            print()
        elif isinstance(jackpot, str):  # ハズレ(北斗の拳用)
            print(f'= information ==')
            print(f'転落当たり{self.rotational_count}回転')
            Pachinko.result(self)  # 大当り情報を表示
            Pachinko.data_rewrite(self)  # # 大当り終了後の処理(回転数初期化、ボーナス数初期化、csvファイルに保存)
            print()
        else:
            return None

    # 大当り獲得時の処理(遊戯玉加算、総出玉加算、回転数初期化, csvファイルにデータ保存) <<< playing_game.py[GGF]から実行(大当たり引いた時)
    def data_update(self, jackpot):  # 引数:jackpot >>> 出玉
        jackpot = int(jackpot)  # エヴァ、まどマギでfloat型を受け取る場合があるため、intに変換する
        self.balls += jackpot  # エヴァ、まどマギでfloat型を受け取る場合があるため、intに変換する
        self.get_balls += jackpot
        self.rotational_count = 0  # 回転数
        GameData.add_data(self.total_rotational_count, self.total_balls)  # csvファイルに情報追加(玉推移、回転数)

    # 大当り終了後の処理(回転数初期化、ボーナス数初期化、csvファイルに保存)  <<< playing_game.py[GGF]から実行(確変終了or単発or遊戯終了)
    def data_rewrite(self):
        self.rotational_count = 0  # 回転数
        self.total_bonus_count = 0
        self.big_bonus_count = 0
        self.bonus_count = 0
        GameData.add_data(self.total_rotational_count, self.total_balls)  # csvファイルに情報追加(玉推移、回転数)

    # 大当り情報を表示  <<< <<< <<< playing_game.py[GGF]から実行(確変終了)
    def result(self):
        print('\n', '大当り結果を表示します。', end='')
        Store.input_enter()
        print('='*8, '大当り結果', '='*8)
        print(f'総ボーナス数:{self.total_bonus_count}回', end=' ')
        print(f'(BIG-BONUS:{self.big_bonus_count}回/BONUS:{self.bonus_count}回)')
        print(f'総獲得出玉:{self.get_balls}')
        print(f'現在の持ち玉:{self.total_balls}')
        print('='*26)

    # 遊戯終了後に遊戯玉を換金
    def _cashing(self):
        amount = self.balls * self.exchange_rate
        before = self.money
        self.money += amount  # 所持金更新
        print('\n', '持ち玉の換金を行います。', end='')
        Store.input_enter()
        print('='*8, '換金', '='*8)
        print(f'現在の換金率:{self.exchange_rate}円/玉')
        print(f'持ち玉:{self.balls} >>> 金額:{amount}円')
        print(f'所持金:{before}円 >>> {self.money}円')
        print('='*26)
        self.balls = 0
        return amount

    # 収益判定
    @staticmethod
    def _judgement(income):
        if income >= 0:
            print(f'・収支:{income}円')
            print('='*26)
            if income != 0:
                print('おめでとうございます。', end='')
            Store.input_enter()
        else:
            print(f'・収支:ー{-income}円')
            print('='*26)
            print('残念でしたね。', end='')
            Store.input_enter()

    # 収支の計算と表示 <<< playing_game.py[GGF]から実行(遊戯終了後)
    def revenue(self):
        money_when_entry = DataBase.get_money_when_entry(self.name, self.age)  # 入店時の所持金をデータベースから取得
        amount = Pachinko._cashing(self)  # 換金
        income_and_expenditure = amount - self.investment_amount  # 収支
        print('\n', '収支を表示します。', end='')
        Store.input_enter()
        print('='*8, '収支', '='*8)
        print(f'・入店時の所持金:{money_when_entry}円')
        print(f'・総投資金額:{self.investment_amount}円')
        print('\n', f'・換金後の所持金:{self.money}')
        Pachinko._judgement(income_and_expenditure)
        DataBase.save_data_to_history_table(self.name, self.age, self.models_to_play, income_and_expenditure)  # 遊戯履歴保存
        GameData.information(self.name, self.models_to_play)
        self.models_to_play = ''  # 台を離れる際に遊戯台を初期化
