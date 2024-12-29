import random
from Pachinko_store.data_processing.game_data import GameData
from Pachinko_store.data_processing.operate_db import WorkingWithDatabase
from Pachinko_store.store.store import Store


# パチンコ機能(内部機能、表示、ユーザーアクション)
class Pachinko(Store):
    balls_for_replay = 0  # 持ち玉遊戯用
    get_balls = 0  # 純増出玉(リザルト画面で使用)
    total_num_of_balls = 0  # 遊戯台の出玉数(出玉推移グラフ用)

    num_of_rotations = 0  # 遊技台回転数
    total_num_of_rotations = 0  # 遊戯台の総回転数(出玉推移グラフで使用)

    total_get_balls = 0  # 確率変動中の総獲得出玉(リザルト画面で使用)
    total_bonus = 0  # 総獲得ボーナス(リザルト画面で使用)
    big_bonus_count = 0  # 確率変動中に獲得したBigBonus数(リザルト画面で使用)
    bonus_count = 0  # 確率変動中に獲得したBonus数(リザルト画面で使用)

    exchange_rate = 4  # 換金率
    replay = 0  # 再プレイ(持ち玉遊技確認)
    min_money = 500  # 遊技に必要な金額
    min_balls = 125

    # 再プレイで持ち玉を使い切った場合に表示
    menu = {
        '=': '所持金を使用して遊技を継続する',
        '#': 'Storeメニューに戻る',
        '*': '退店',
    }
# =========== パチンコ内部処理 ============
    # 回転数の加算 <<< ヘソ入賞時に実行
    @staticmethod
    def _add_rotational_count():
        Pachinko.num_of_rotations += 1
        Pachinko.total_num_of_rotations += 1

    # 遊技玉の減少  <<< ヘソ未入賞時に実行
    def _decreased_balls(self):
        # 再プレイ(持ち玉遊技)判定
        if Pachinko.replay == 0:
            self.balls -= 1
        else:
            Pachinko.balls_for_replay -= 1
        Pachinko.total_num_of_balls -= 1

    # 遊技玉追加、獲得玉追加、ボーナスカウント、csv保存 <<< gameメインから実行
    def do_after_winning(self, jackpot, big=1500):
        jackpot = int(jackpot)  # エヴァ、まどマギでfloat型を受け取る場合があるため、intに変換
        self.balls += jackpot  # 遊戯玉増
        Pachinko.get_balls += jackpot  # 獲得出玉増
        Pachinko.total_num_of_balls += jackpot
        Pachinko.total_bonus += 1
        if jackpot == big:
            Pachinko.big_bonus_count += 1
        else:
            Pachinko.bonus_count += 1
        GameData.add_data(Pachinko.total_num_of_rotations, Pachinko.total_num_of_balls)  # 遊戯履歴

    # ボーナス回数初期化 <<< ゲームmain(hokuto,eva,madomagi)から実行(確変終了後、遊技終了後)
    @staticmethod
    def do_after_losing():
        Pachinko.total_bonus = 0
        Pachinko.big_bonus_count = 0
        Pachinko.bonus_count = 0

    # 出玉推移グラフ用のデータを削除する  <<< revenueで実行
    @staticmethod
    def delete_game_data():
        Pachinko.total_num_of_rotations = 0
        Pachinko.total_num_of_balls = 0

    # ヘソ入賞判定(通常):入賞確率7% <<< CommonFlowから実行
    def ball_goes_in(self, probability=7/100):
        if random.random() <= probability:
            Pachinko._add_rotational_count()
            return True
        else:
            Pachinko._decreased_balls(self)
            return False

    # ヘソ入賞判定(確変):入賞確率90% <<< CommonFlowから実行
    def ball_goes_in_rush(self, probability=9/10):
        if random.random() <= probability:
            Pachinko._add_rotational_count()
            return True
        else:
            Pachinko._decreased_balls(self)
            return False

    # 貯玉 <<< gameメインから実行(持ち玉遊技決定時)
    def processing_for_replay_first(self):
        Pachinko.saving_balls = self.balls
        self.balls = 0

# =========== 表示 ============
    # 遊戯中の情報表示(通常時):回転数 <<< gameのメインから実行(遊戯通常タイム)
    @staticmethod
    def display_rotational_count():
        print(f'遊技玉が無くなりました。 >>> 現在の回転数: {Pachinko.num_of_rotations}回転')
        GameData.add_data(Pachinko.total_num_of_rotations, Pachinko.total_num_of_balls)  # 遊戯履歴(回転数/出玉)

    # 遊戯中の情報表示(確変時):回転数、獲得出玉、総出玉、ボーナス回数 <<< gameのメインから実行(遊戯確変中)
    # 大当り獲得時の処理(回転数初期化、遊戯玉追加、獲得出玉追加)
    def display_rotational_count_hyper(self, jackpot):  # 引数:jackpot >>> 出玉(300 or 450 or 1500 or False)
        if isinstance(jackpot, (int, float)):  # 当たり
            jackpot = int(jackpot)  # エヴァ、まどマギでfloat型を受け取る場合があるため、intに変換する
            before = self.balls - jackpot
            print(f'・大当たり情報')
            print(f'(回転数):{Pachinko.num_of_rotations}回転', end='\t')
            print(f'大当り"{Pachinko.total_bonus}回目"獲得!(BigBonus:{Pachinko.big_bonus_count}回、Bonus:{Pachinko.bonus_count})')
            print(f'(獲得出玉):{jackpot}玉', end='\t')
            print(f'(持ち玉):{before}玉 >>> {self.balls}玉')
        elif isinstance(jackpot, str):  # ハズレ(北斗の拳用)
            print(f'*information*')
            print(f'・(回転数):{Pachinko.num_of_rotations}回転')
            Pachinko.result(self)  # 大当り情報を表示
        Store.input_enter()

    # 大当り情報を表示  <<< gameメインから実行(確変終了後)
    def result(self):
        print('\n大当り結果を表示します。', end='')
        Store.input_enter()
        print('='*8, '大当り結果', '='*8)
        print(f'総ボーナス数:{Pachinko.total_bonus}回', end=' ')
        print(f'(BigBonus:{Pachinko.big_bonus_count}回/Bonus:{Pachinko.bonus_count}回)')
        print(f'総獲得出玉:{Pachinko.get_balls}玉')
        print(f'現在の持ち玉:{self.balls}玉')
        print('='*26)
        Store.input_enter()

    # 遊戯終了後に遊戯玉を換金
    def _cashing(self):
        amount = self.balls * Pachinko.exchange_rate
        before = self.money
        self.money += amount  # 所持金更新
        print('\n持ち玉の換金を行います。', end='')
        Store.input_enter()
        print('='*8, '換金', '='*8)
        print(f'・現在の換金率:{Pachinko.exchange_rate}円/玉')
        print(f'・持ち玉:{self.balls}玉 >>> 金額:{amount}円')
        print(f'・所持金:{before}円 >>> {self.money}円')
        print('='*26)
        self.balls = 0
        Store.input_enter()
        return amount

    # 収益判定
    @staticmethod
    def _judge(income):
        if income >= 0:
            print()
            print(f'・収支: プラス{income}円')
            print('='*26)
            if income != 0:
                print('おめでとうございます。', end='')
            Store.input_enter()
        else:
            print()
            print(f'・収支: マイナス{-income}円')
            print('='*26)
            print('残念でしたね。', end='')
            Store.input_enter()

    # 収支の計算と表示 <<< CommonFlowから実行(遊戯終了後)
    def revenue(self):
        money_when_entry = WorkingWithDatabase.get_money(self.name, self.age)  # 入店時の所持金をデータベースから取得
        if self.balls != 0:
            amount = Pachinko._cashing(self)  # 換金
        else:
            amount = 0
        income_and_expenditure = amount - self.total_investment_amount  # 収支
        print()
        print('収支を表示します。')
        Store.input_enter()
        print('='*8, '収支', '='*8)
        print(f'・遊技台:{self.model_played}')
        print(f'・投資金額:{self.total_investment_amount}円 (メニュー画面での追加金額:{self.add_money}円)')
        print(f'・獲得金額:{amount}円')
        print(f'・入店時の所持金:{money_when_entry}円')
        print(f'・現在の所持金:{self.money}円')
        Pachinko._judge(income_and_expenditure)  # 収益を判定してコメントを表示
        WorkingWithDatabase.insert_history(self.name, self.age, self.model_played, income_and_expenditure)  # 遊戯履歴保存
        GameData.show_game_data(self.name, self.model_played)  # 出玉推移グラフを表示
        WorkingWithDatabase.update_user_table_money(self.name, self.age, self.money)  # DB所持金更新
        GameData.create_csvfile()  # csvファイル初期化
        Pachinko.replay = 0  # 再遊技初期化
        Pachinko.delete_game_data()  # 出玉推移グラフ用のデータを初期化
        self.model_played = ''  # 遊戯台を初期化
        self.total_investment_amount = 0  # 総投資額を初期化

    # 遊戯終了後の処理  <<< gameメインから実行
    def end_of_game(self):
        Pachinko.do_after_losing()  # 遊戯台の初期化、csv保存
        Pachinko.revenue(self)  # 換金 >>> 収支表示 >>> 遊戯履歴保存 >>> 出玉推移グラフ表示
        Pachinko.input_enter()

# =========== ユーザーアクション ============
    # 遊技玉の貸し出し(500円 >>> 125玉) <<< CommonFLowから実行
    def lend(self, amount=500, balls=125):
        print(f'\n{amount}円をパチンコ玉{balls}玉に交換できます。交換しますか？', end='')
        y_n = Store.input_yes_or_no()
        if y_n == 'y':
            Store._ball_rental(self, amount, balls)
            print(f'交換完了[500円 >>> 遊技玉:125玉]　(残金:{self.money}円)')
            return self.balls
        else:
            return None

    # パチンコ玉を発射する <<<gameメインから実行(遊戯開始時)
    def firing_balls(self):
        print('Enterキーを押すとパチンコ玉を発射します。', end='')
        self.play_check += 1
        Store.input_enter()

    # メニュー選択
    @staticmethod
    def input_choice():
        while True:
            choice = input('User: ')
            if choice in Pachinko.menu:
                return choice
            else:
                print('入力が正しくありません。')

# =========== 持ち玉遊技 ============
    # 大当たり終了後の持ち玉遊戯を行う場合    # ※125玉使いきるまでに当たりを引いたら残玉をballsに足す必要あり
    def _processing_for_replay(self):
        if self.balls <= Pachinko.min_balls:
            Pachinko.balls_for_replay = self.balls
            self.balls = 0
            print(f'持ち玉を全て払い出します。[持ち玉:{Pachinko.balls_for_replay}玉 >>> {self.balls}玉]')
        else:
            before = self.balls
            self.balls -= 125
            Pachinko.balls_for_replay += 125
            print(f'持ち玉{Pachinko.min_balls}玉を払い出します。[持ち玉:{before}玉 >>> {self.balls}玉]')

    # 持ち玉遊戯確認
    def _check_for_replay(self):
        print(f'\n持ち玉{Pachinko.min_balls}を払い出しますか？', end='')
        y_n = Store.input_yes_or_no()
        if y_n == 'y':
            Pachinko._processing_for_replay(self)  # 持ち玉 >>> 遊戯玉

    # 持ち玉遊技を行うか確認  <<< gameメインから実行
    def check_for_replay_first(self, replay=False):
        print(f'持ち玉{self.balls}玉を使用して遊技を継続しますか。', end='')
        y_n = Store.input_yes_or_no()
        if y_n == 'y':
            Pachinko.replay += 1
            replay = True
        return replay

# =========== 共通Flow ============
    def seated_flow(self):
        print()
        print('-'*20)
        print(f'"{self.model_played}" で遊びます。')
        GameData.add_data(Pachinko.total_num_of_rotations, Pachinko.total_num_of_balls)  # 遊戯履歴(回転数:0/出玉:0)

    # 遊戯玉の貸し出し
    def lend_flow(self):
        if Pachinko.replay == 0:
            Pachinko.lend(self)
        else:
            # if Pachinko.replay != 0:
            Pachinko._check_for_replay(self)  # 持ち玉遊技の確認(No >>> False)
        # 遊戯玉に交換(所持金->遊戯玉 or 持ち玉->遊戯玉)していなければ, Falseを返す
        if ((Pachinko.replay == 0) and (self.balls == 0)) or ((Pachinko.replay != 0) and (Pachinko.balls_for_replay == 0)):
            print('遊戯を終了します。', end='')
            Pachinko.input_enter()
            return False
        else:
            return True

    # 遊技終了確認(所持金なし)
    def continue_or_not(self):
        print('\nお金が無くなりました。退店したい場合は ”*” を入力してください。')
        print('それ以外のキーを入力するとメニュー画面に戻ります。メニュー画面から "所持金を追加" が選択できます。')
        choice = input('user: ')
        if choice == '*':
            Pachinko.revenue(self)
            GameData.create_csvfile()  # csvファイル初期化
        return choice

    # 遊技終了確認(持ち玉なし)
    def continue_or_not_for_replay(self):
        print('\n持ち玉を使い切りました。以下のメニューから行動を選択して対応キーを入力してください。')
        Store.input_enter()
        print('-'*8, ' Menu ', '-'*8)
        for key, menu in Pachinko.menu.items():  # menu("=":所持金で遊技継続、 "#":Storeメニューに戻る、"*":退店)
            print(f'・{menu} >>> キー:({key})')
        print('-'*20)
        print('(※ Storeメニューに戻ると今回の遊技データーは初期化されます。)')
        choice = Pachinko.input_choice()
        if choice == '*':
            Pachinko.revenue(self)
            GameData.create_csvfile()  # csvファイル初期化
        return choice
