import datetime
import random
from info import InformationDisplay
from operate_db import DB
from hokuto import h_lottery, h_lottery_bonus
from eva import e_lottery, e_lottery_chance, e_lottery_bonus
from madomagi import m_lottery, m_lottery_bonus, m_lottery_bonus_plus


# ===============================================================
# パチンコ店のクラス　
# <機能>
#  ・インスタンス作成、・入場制限、・機種の表示、・スペックの表示、・収益の表示、日付の入手(DB保存用)
#  ・パチンコの共通機能(玉変換、ヘソ入賞判定(通常・確変)、当たり抽選(通常・確変)、回転数表示(通常・確変)、Bonus結果表示、換金)
#  ・遊技台の出玉推移グラフの作成と表示(csvファイル作成 → DataFrame作成 → グラフ作成 → 表示、pngファイルで保存)
class Store:
    # コンストラクタ
    def __init__(self, name, age, money=0):
        self.name = name
        self.age = age  # 入店時とデータベースの操作に使用
        self.money = money  # 所持金
        self.money_at_time_of_entry = 0  # 入店時の所持金を記録
        self.ball = 0  # 入店後の初遊技で所持金からパチンコ玉に変換する。退店時は現金に戻す
        self.investment_amount = 0  # 総投資額を計算する
        self.play = 0  # 遊技確認で使用。１回でも玉を発射すると＋１して、データベースに遊技履歴を残す。
        self.gaming_machine = ''  # 遊技機種を保存(遊技履歴保存のため)

    # エントランス (戻り値　>>> None:20歳未満/所持金500円未満お断り）
    def entrance(self):
        min_age = 20
        min_money = 500
        if self.age < min_age:
            print(f'パチンコは{min_age}歳からです。')
        elif self.money < min_money:
            print(f'パチンコで遊ぶには{min_money}円以上必要です。')
        else:
            print('いらっしゃいませ!!')
            self.money_at_time_of_entry = self.money
            InformationDisplay.create_csvfile()  # csvファイル作成(出玉推移グラフ用) + 初期データ(回転数:0, 出玉:0)を入力
            return self.age

    # 選択機種の表示  (戻り値：choice)
    def display(self):
        # 設置機種
        game = {
            'H': '・CR北斗の拳 (1/349)',
            'E': '・CRエヴァンゲリオン (1/319)',
            'M': '・CR魔法少女まどかマギカ (1/199)',
            '#': '・各機種のスペックを一覧表示する。',
            '=': '・過去の遊技履歴を表示する。',
            '$': '・お金を追加する。',
            '*': '・店を出る。',
            'aki': '管理者操作(パスワード必要)'
        }
        while True:
            input('Enterキーを押すとメニュー画面が表示されます。'
                  'メニューから遊技台の選択、もしくはその他アクションを選択して、対応キーを入力してください。')

            print('-'*10, 'メニュー', '-'*10)
            for k, v in game.items():
                if k == 'H':
                    print('＜遊技台＞')
                if k == '#':
                    print('＜その他メニュー＞')
                print(f'{v} >>> キー：{k}')
            print('-'*20)

            choice = Pachinko.user_action('user_choice')  # ユーザーがEnterキーを入力するまで待機
            # 遊技台を選択
            if (choice == 'H') or (choice == 'E') or (choice == 'M'):
                if self.money < 500:
                    input('お金がないので遊べません。Enterキーを押してください。')
                else:
                    print(f'あなたは{game[choice]}を選びました。')
                    break

            # 機種スペックを表示
            elif choice == '#':
                Store.display_spec()

            # 遊技履歴を表示
            elif choice == '=':
                DB.check_history(self.name, self.age)

            # 所持金を追加
            elif choice == '$':
                print(f'これまでの投資額：{self.investment_amount}円,  所持金:{self.money}')
                print('お金を追加します。金額を半角英数字で入力してください。')
                money = int(input('(例:5000): '))
                self.money += money  # 所持金を増やす
                input(f'あなたの所持金は{self.money}円になりました。Enterキーを押してください。')

            # 退店
            elif choice == '*':
                self.investment_amount = 0  # 退店時に投資額を初期化
                return None

            # 管理者操作
            elif choice == 'aki':
                menu = {
                    1: '顧客確認',
                    2: '遊技履歴',
                }
                password = 'hoge'
                print('管理者専用の操作です。パスワードを入力してください。')
                text = input('password: ')
                if text == password:
                    while True:
                        print('以下から操作を選択して対応キーを入力してください。')
                        for k, v in menu.items():
                            print(f'{v}：キー >>> {k}')
                        choice = int(input('管理者: '))
                        if choice in menu:
                            Pachinko.check_the_db(choice)
                        choice = input('操作を繰り返しますか？(y/n)')
                        if choice == 'y':
                            continue
                        else:
                            print('管理者操作を終了します。')
                            break
                else:
                    print('パスワードが一致しませんでした。メニュー画面に戻ります。')

            # メニュー以外の入力
            else:
                print('入力されたキーが正しくありません。')

        return choice

    # 機種スペックの表示
    @staticmethod
    def display_spec():
        # ゲームスペック　[通常時大当り確率、初当たり出玉、RUSH突入率、RUSH時の大当り確率、RASH時の出玉振り分け]
        input('\n各機種のスペックを表示します。Enterキーを押してください。')
        print('*'*20, 'スペック一覧', '*'*20)
        DB.get_game_specs_from_db()  # データベースからスペックを取得
        print('*'*50)
        while True:  # ユーザーの応答を待つ
            enter = input('Enterキーを押すとメニュー画面に戻ります。')
            if type(enter) is str:
                break

    def check_the_game(self):
        self.play += 1

    # パチンコ玉に変換する
    def lend(self):
        self.play += 1  # 遊技確認。一回でもプレイしたらデータベースに履歴を残す。
        while True:
            # print('\n500円で125玉と交換できます。')
            choice = input('\n500円で125玉と交換できます。交換しますか？(y/n): ')
            if choice == 'n':
                return None
            elif choice == 'y':
                self.money -= 500  # ユーザーの残金から５００円を引く
                self.investment_amount += 500  # 総投資額加算
                self.ball += 125  # パチンコ玉１２５玉
                return self.ball
            else:
                print('入力が正しくありません。')

    # パチンコ玉をヘソに入れる（通常時）　ヘソに入る確率：約7%　＞＞　１０００円２５０玉で平均１７回転
    @staticmethod
    def ball_goes_in():
        n = random.randint(1, 14)
        # ７でヘソに入賞
        if n == 7:
            Pachinko.add_total_count()  # 玉がヘソに入る度に加算(データ推移用)
            return n
        else:
            return None

    # パチンコ玉をヘソに入れる（確率変動時）　ヘソに入る確率：90%
    @staticmethod
    def ball_goes_in_bonus():
        n = random.randint(1, 10)
        # ７以外でヘソに入賞
        if n != 7:
            Pachinko.add_total_count()  # 玉がヘソに入る度に加算(データ推移用)
            return n
        else:
            return None

    # 回転数の表示（通常時）
    @staticmethod
    def num_of_rotations(count):
        print(f'>>> 現在の回転数：{count}回転', end=' ')
        print()

    # 確変時の情報表示
    @staticmethod
    def bonus_info(jackpot_b):
        if type(jackpot_b) is str:
            print(f' info:(転落当たり：{Pachinko.count_b+1}回転目)')
        else:
            print(f' info:(回転数：{Pachinko.count_b+1}回転)')
            print(f'     :(大当り{Pachinko.total_bonus_count}回目獲得! 総出玉:{Pachinko.bonus_pt-jackpot_b}玉 ＋ "{jackpot_b}玉")')

    # 大当り終了時の結果を表示
    @staticmethod
    def result():
        print('\n', '='*8, '大当り結果', '='*8)
        print(f'総ボーナス数：{Pachinko.total_bonus_count}回'
              f'(BigBonus:{Pachinko.big_bonus_count}回、Bonus:{Pachinko.small_bonus_count}回)')
        print(f'ボーナス獲得出玉：{Pachinko.bonus_pt}玉')
        print(f'現在の持ち玉：{Pachinko.bonus_balls}玉')
        print('='*26)
        while True:  # ユーザーの応答を待つ
            enter = input('Enterキーを入力してください。')
            if type(enter) is str:
                break

    # 獲得した出玉をお金に変換して結果を表示する。
    @staticmethod
    def cashing():
        income = Pachinko.bonus_balls * 4
        input(f'持ち玉<{Pachinko.bonus_balls}玉>を1玉4円で換金します。Enterキーを押してください。')
        print('\n', '='*8, '換金', '='*8)
        print(f'持ち玉:{Pachinko.bonus_balls}玉　>>> {income}円')
        print('='*23)
        Pachinko.bonus_balls = 0  # ボーナス出玉を０にする。
        return income

    # 遊技した日付を取得（データベース保存用）
    @staticmethod
    def get_date():
        dt = datetime.datetime.now()
        today = f'{dt.year}/{dt.month}/{dt.day}'
        return today

    # 収益の計算と表示、データベース(TABLE<history>)に遊技履歴を保存、出玉推移グラフの表示
    def revenue(self, income):
        input('収支を表示します。Enterキーを押してください。')
        before = self.money
        self.money += income  # 出玉を現金換算して所持金に加算
        revenue = income - self.investment_amount  # 収益 = 所得 - 投資額
        print('\n', '='*8, '収支', '='*8)
        print(f'入店時：{self.money_at_time_of_entry}円')
        print(f'総投資額:{self.investment_amount}円')
        print(f'現在の所持金：{before}円 + {income}円　>>> {self.money}円')
        if revenue > 0:
            print(f'プラス{revenue}円でした。')
            print('='*23)
            print('おめでとうございます。', end='')
            revenue = '+' + str(revenue)  # DB保存用として文字列に変換
        else:
            print(f'マイナス{-revenue}円でした。')
            print('='*23)
            print('残念でしたね。', end='')
            revenue = str(revenue)  # DB保存用として文字列に変換
        date = Store.get_date()  # 日付を取得
        # history(date CHAR(20), name CHAR(20), age INT, machine CHAR(20), income INT)
        DB.save_when_exit(date, self.name, self.age, self.gaming_machine, revenue)  # 遊技履歴作成
        Store.transition(self)
        # 台を離れたら、総回転数、出玉推移初期化される。
        Pachinko.total_count = 0
        Pachinko.total_balls = 0

    # ユーザーの入力(ユーザーが入力するまでループして待機する)
    @staticmethod
    def user_action(user):
        action = 0

        # ユーザー入力判定(遊技確認は必ずyes/no)
        def input_judge(txt):
            if (txt != 'y') and (txt != 'n'):
                print('入力が正しくありません')
                return None
            else:
                return txt
        while True:
            if user == 'firing':
                action = input('Enterキーを押すと玉が発射されます。')
            elif user == 'menu':
                action = input('Enterキーを入力すると次の画面に進みます。')
            elif user == 'bonus_start':
                action = input('<確率変動>に突入します。Enterキーを押してください。')
            elif user == 'bonus_end':
                action = input('<確率変動>を終了します。Enterを押すと結果画面が表示されます。\n')
            elif user == 'replay_choice':
                while True:
                    action = input('\n獲得出玉で遊技を続けますか？ (y/n): ')
                    n = input_judge(action)
                    if n is not None:
                        break
            elif user == 'replay':
                while True:
                    action = input('\n持ち玉を使用して遊技を行いますか？(y/n): ')
                    n = input_judge(action)
                    if n is not None:
                        break
            elif user == 'replay_again':
                while True:
                    action = input('持ち玉を使い切りました。現金を使って遊技を継続しますか。(y/n)')
                    n = input_judge(action)
                    if n is not None:
                        break
            elif user == 'finished':
                action = input('お疲れ様でした。Enterキーを押すとメニュー画面が表示されます。')
            elif user == 'user_choice':
                action = input('user:')
            # ユーザーが入力するまでループして待機する
            if type(action) is str:
                return action

    # 通常時の値
    @staticmethod
    def value_normal():
        Pachinko.count = 0

    # 確変終了後の初期化
    @staticmethod
    def after_bonus():
        Pachinko.count_b = 0  # 回転数
        Pachinko.bonus_pt  = 0  # 獲得出玉（ボーナス終了後の結果表示で使用）
        Pachinko.total_bonus_count = 0  # 結果表示で使用
        Pachinko.big_bonus_count = 0  # 結果表示（内訳）で使用
        Pachinko.small_bonus_count = 0  # 結果表示（内訳）で使用

    # 再プレイ時（持ち玉遊技）の値
    @staticmethod
    def value_re():
        Pachinko.replay = 0  # 再プレイ時に使用
        Pachinko.replay_balls = 0  # 持ち玉遊技に使用

    # 出玉推移データの作成、表示、ファイル保存
    def transition(self):
        # DataFrame作成
        df = InformationDisplay.create_dataframe()

        # 出玉推移グラフをpngファイルで保存する。　
        # ファイル名 >>> "{ユーザー名(英字３文字or匿名)}_{日付(４桁)_{遊技台(イニシャル)}}.png"
        # 日付を取得　>>> 戻り値：month, day
        month, day = InformationDisplay.date()
        # ユーザー名が英字か判定　>>> 戻り値：英字 → 最初３文字、英字ではない → anonymous(アノニマス)
        name = InformationDisplay.name_judge(self.name)
        # 遊技台をイニシャルで返す　>>> 戻り値：文字列
        model_initial = InformationDisplay.convert_to_initials(self.gaming_machine)
        # 名前、日付、遊技台を使用してファイル名を作成 >>> 戻り値：文字列
        filename = InformationDisplay.make_filename(name, month, day, model_initial)

        # 遊技台・ユーザー名・日付から、グラフのタイトルを作成 >>> 戻り値：文字列
        title = InformationDisplay.make_title_name(self.gaming_machine, name, month, day)
        # グラフ作成、表示(10秒)、pngファイルで保存
        InformationDisplay.view_graph(df, title, filename)  # 引数：DataFrame, グラフタイトル、ファイル名

    # データベースの確認（使用にはパスワードが必要）
    @staticmethod
    def check_the_db(n):  # 引数n:操作メニュー >>> 1:ユーザー情報、 2:遊技履歴
        DB.check_db(n)
        print('データは以上です。')


# ============================================================================================
# パチンコ台のクラス（3機種）
# ・CR北斗の拳(1/349)、・CRエヴァンゲリオン(1/319)、・CR魔法少女まどかマギカ(1/199)
class Pachinko(Store):
    total_count = 0  # 遊技を通した全ての回転数(出玉推移グラフで使用)
    total_balls = 0  # 遊技を通した出玉(出玉推移グラフで使用)
    count_hokuto = 0  # 通常時回転数(北斗)
    count_eva = 0  # 通常時回転数(エヴァ)
    count_madoka = 0  # 通常時回転数(まどか)
    count_b = 0  # 確率変動時の回転数
    total_bonus_count = 0  # ボーナス数のカウント
    big_bonus_count = 0  # ボーナス内訳
    small_bonus_count = 0  # ボーナス内訳
    bonus_balls = 0  # ボーナス時の純増出玉（確変時の抽選で使用するため減少する）
    bonus_pt = 0  # ボーナスでの獲得出玉（ボーナスで獲得した出玉量。確変終了後の結果表示で使用する）
    before_bonus_balls = 0  # 持ち玉遊技時に使用した玉数の計算で使用
    replay = 0  # 大当り終了後に再プレイするときに使用
    replay_balls = 0  # 持ち玉遊技で使用
    bonus_list = []  # ボーナスを記録

    # 遊技中に回転数を受け取り、集計する
    @staticmethod
    def add_total_count():
        Pachinko.total_count += 1

    # 遊技中にパチンコ玉の増減を集計する
    @staticmethod
    def add_total_balls(balls):
        Pachinko.total_balls += balls

# ==================================================================================================
# スペック:CR北斗の拳:
# (通常時の大当り確率): 1/349, (初当たり出玉): +300(4/5) or +1500(1/5),
# (確率変動突入率): 100%, (確率変動時の大当り確率): 当たり:1/40, 転落:1/150,
# (確率変動時の出玉振り分け): +300(1/4) or +1500(3/4)、(大当り継続率): 88%
    def hokuto(self, ball=0):  # ball:遊戯で獲得したball (self.ballとは別) <= 貯玉での遊技で使用
        print('-'*20)
        print('CR北斗の拳で遊びます。')
        InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
        self.gaming_machine = 'CR北斗の拳'
        # 遊技準備
        while (self.money >= 500) or (Pachinko.bonus_balls > 0):
            # 再プレイではない場合(持ち玉遊技ではない場合)
            if Pachinko.bonus_balls == 0:
                ball = Store.lend(self)  # lend() >>> self.ball += 125
            # lend()で玉への変換を拒否した場合
            if ball is None:
                input('遊技を終了します。Enterキーを押すとメニュー画面に戻ります。')
                break
            else:
                if Pachinko.bonus_balls == 0:
                    print('交換完了：[現金:500円 ＞＞＞ 持ち玉:125玉]')
                # 再プレイ（持ち玉遊技）
                else:
                    re = 125  # 持ち玉遊技(=125玉)
                    replay_choice = Pachinko.user_action('replay')  # ユーザー：持ち玉を使用して遊技を行いますか？(y/n)
                    if replay_choice == 'y':
                        before = Pachinko.bonus_balls
                        if Pachinko.bonus_balls < re:
                            Pachinko.replay_balls = Pachinko.bonus_balls  #
                            print(f'{Pachinko.replay_balls}玉を払い出します。　[持ち玉:{Pachinko.bonus_balls}玉 >>> 0玉]')
                            Pachinko.bonus_balls = 0
                        else:
                            Pachinko.bonus_balls -= re  # 持ち玉から125玉引く
                            Pachinko.replay_balls += re  # 遊技玉に125玉追加する
                            print(f'{re}玉を払い出します。　＜持ち玉:{before}玉 >>> {Pachinko.bonus_balls}玉＞')
                    elif replay_choice == 'n':
                        print('遊技を終了します。')
                        income = Store.cashing()  # 戻り値:income(=ball*4)
                        Store.revenue(self, income)
                        Pachinko.user_action('finished')
                        Pachinko.replay = 0  # 再プレイを０に戻す。
                        break
                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                Store.check_the_game(self)  # 遊技確認
                # 遊技
                while (self.ball > 0) or (Pachinko.replay_balls > 0):
                    if (Pachinko.replay == 0) or (Pachinko.replay_balls > 0):
                        navel = Store.ball_goes_in()  # 戻り値{None:消化、n:ヘソ入賞}
                        # 玉の入賞判定 (通常時7%で入賞) None:ヘソ入賞なし、int型:ヘソ入賞 -> 抽選
                        if navel is None:
                            if Pachinko.replay == 0:
                                self.ball -= 1  # 持ち玉が減る
                                Pachinko.add_total_balls(-1)  # 玉推移
                                continue
                            # 持ち玉遊技の場合
                            else:
                                Pachinko.replay_balls -= 1  # 持ち玉が減る
                                Pachinko.add_total_balls(-1)  # 玉推移
                                continue
                        else:
                            Pachinko.count_hokuto += 1  # 回転数
                            jackpot = h_lottery()  # 戻り値{None:ハズレ、int型:当たり}
                            # 大当りの抽選判定
                            if jackpot is None:
                                continue
                            # 大当り！　＞＞＞ 確率変動突入
                            else:
                                Pachinko.total_bonus_count += 1  # 大当り回数をカウント
                                Pachinko.bonus_balls += jackpot  # 大当り純増出玉(確変突入時の遊技で使用＝減少していく）
                                Pachinko.bonus_pt += jackpot  # 大当りでの獲得出玉
                                Pachinko.add_total_balls(jackpot)  # 玉推移
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                if jackpot == 1500:
                                    Pachinko.big_bonus_count += 1
                                elif jackpot == 300:
                                    Pachinko.small_bonus_count += 1
                                Pachinko.bonus_list.append(jackpot)
                                input(f'{Pachinko.count_hokuto}回転目で大当りを引きました。おめでとうございます\n')
                                Pachinko.user_action('bonus_start')
                                print(f'\n*確率変動*: {Pachinko.total_bonus_count}回目')
                                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                                Pachinko.count_hokuto = 0  # 大当りを引いたら通常時の回転数を初期化
                                # 大当り(1/40)転落(1/150)どちらか引くまで確率変動ループ
                                while True:
                                    n = Store.ball_goes_in_bonus()  # 戻り値{n:ヘソ入賞、None:消化}
                                    # 玉の入賞判定　(確率変動時90%でヘソ入賞) None:ヘソ入賞なし、int型:ヘソ入賞->抽選
                                    if n is None:
                                        Pachinko.bonus_balls -= 1  # 持ち玉が減る
                                        Pachinko.add_total_balls(-1)  # 玉推移
                                        continue
                                    else:
                                        Pachinko.count_b += 1  # 回転数
                                        Pachinko.count_b += 1  # ボーナス時の回転数をカウント
                                        jackpot_b = h_lottery_bonus()  # lottery_bonus() 抽選
                                        # 大当りor転落の抽選判定  None:ハズレ、int型:大当り、str型:転落
                                        if jackpot_b is None:
                                            continue
                                        # 大当り
                                        elif type(jackpot_b) is int:
                                            Pachinko.bonus_balls += jackpot_b  # 大当り総獲得出玉
                                            Pachinko.add_total_balls(jackpot_b)  # 玉推移
                                            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                            Pachinko.bonus_pt += jackpot_b
                                            if jackpot_b == 1500:
                                                Pachinko.big_bonus_count += 1
                                            elif jackpot_b == 300:
                                                Pachinko.small_bonus_count += 1
                                            Pachinko.total_bonus_count += 1
                                            Store.bonus_info(jackpot_b)  # 情報表示
                                            print()
                                            print(f'*確率変動*: {Pachinko.total_bonus_count}回目')
                                            Pachinko.bonus_list.append(jackpot_b)
                                            Pachinko.count_b = 0  # 大当り時の回転数を初期化
                                            input('キーを押すと玉が発射されます。')
                                            continue
                                        # ハズレ（転落）
                                        elif type(jackpot_b) is str:
                                            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                            Store.bonus_info(jackpot_b)  # 情報表示
                                            Pachinko.user_action('bonus_end')  # ユーザー：Enter
                                            if Pachinko.replay == 0:
                                                Pachinko.bonus_balls += self.ball  # 大当り前の持ち玉を獲得出玉に合算
                                                self.ball = 0  # 持ち玉を初期化
                                            else:
                                                Pachinko.bonus_balls += Pachinko.replay_balls  # 大当り前の持ち玉を獲得出玉に合算
                                                Pachinko.replay_balls = 0  # 持ち玉を初期化
                                            Pachinko.before_bonus_balls = Pachinko.bonus_balls  # 再プレイで使用した玉数を計算する時に使用
                                            Store.result()
                                            Pachinko.after_bonus()  # 確変終了後の初期化
                                            Pachinko.replay += 1  # 一度遊技ループから抜ける
                                            break
                    # ボーナス終了後に一度ループを抜けてユーザーのアクション選択画面(持ち玉遊技をするか)に移行する
                    else:
                        break
                # ボーナス０回(bonus_balls=0)
                if Pachinko.replay == 0:
                    print('持ち玉が無くなりました。', end=' ')
                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                    Store.num_of_rotations(Pachinko.count_hokuto)
                # 再プレイ（持ち玉遊技）
                elif (Pachinko.replay_balls == 0) and (Pachinko.before_bonus_balls != Pachinko.bonus_balls):
                    print('玉が無くなりました。', end=' ')
                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                    Store.num_of_rotations(Pachinko.count_hokuto)
                    if Pachinko.bonus_balls == 0:
                        choice = Pachinko.user_action('replay_again')  # ユーザー：持ち玉を使い切りました。現金を使って遊技を継続しますか。(y/n)
                        if choice == 'y':
                            Pachinko.replay = 0  # 持ち玉を使い切った場合は０に戻す
                            return Pachinko.hokuto(self)
                        else:
                            input('メニュー画面に戻ります。Enterキーを押してください。')
                            break
                # ボーナス終了直後（持ち玉遊技の確認）
                elif Pachinko.replay > 0:
                    choice = Pachinko.user_action('replay_choice')  # 獲得出玉で遊技を続けますか？ (y/n):
                    # 遊技継続の場合は再度自身の関数を呼ぶ
                    if choice == 'y':
                        return Pachinko.hokuto(self)  # 再プレイなら自身の関数を呼ぶ
                    else:
                        print('遊技を終了します。')
                        income = Store.cashing()  # 戻り値:income(=ball*4)
                        Store.revenue(self, income)
                        Pachinko.replay = 0  # 再プレイを０に戻す。
                        Pachinko.user_action('finished')  # ユーザー：Enter
                        Pachinko.count_hokuto = 0  # 回転数を初期化
                        break

        if self.money == 0:
            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
            print('\nお金が無くなりました。退店したい場合は ”*” を入力してください。')
            print('それ以外のキーを入力するとメニュー画面に戻ります。メニュー画面からお金の追加を行うことができます。')
            exiting = Pachinko.user_action('user_choice')  # ユーザー：退店orメニュー画面選択
            if exiting == '*':
                DB.updating_money(self.name, self.age, self.money, self.play)
                print('またのご来店をお待ちしております。')
                self.investment_amount = 0  # 投資額の初期化
                Pachinko.count_hokuto = 0  # 回転数を初期化
                return exiting
# ==================================================================================================
# CRエヴァンゲリオン:
# (通常時の大当り確率): 1/319, (初当たり出玉): +450(75%) or +1500(25%),
# (初当たり振り分け): 確率変動:70%, チャンスタイム(100回転:大当り確率1/170):30%, (確率変動時の大当り確率): 当選:1/90 回転数:170回転,
# (確率変動時の出玉振り分け): ALL+1500、(大当り継続率): 85%
    def eva(self, ball=0):
        # チャンスタイム引き戻し対策
        chance_time = 0
        navel = 0
        jackpot = 0

        print('-'*20)
        print('CRエヴァンゲリオンで遊びます。')
        InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
        self.gaming_machine = 'CRエヴァンゲリオン'
        # 遊技準備
        while (self.money >= 500) or (Pachinko.bonus_balls > 0):
            # 再プレイではない場合(持ち玉遊技ではない場合)
            if Pachinko.bonus_balls == 0:
                ball = Store.lend(self)  # lend() >>> self.ball += 125
            # lend()で玉への変換を拒否した場合
            if ball is None:
                input('遊技を終了します。Enterキーを押すとメニュー画面に戻ります。')
                break
            else:
                if Pachinko.bonus_balls == 0:
                    print('交換完了：[現金:500円 ＞＞＞ 持ち玉:125玉]')
                # 再プレイ（持ち玉遊技）
                else:
                    re = 125  # 持ち玉遊技(=125玉)
                    replay_choice = Pachinko.user_action('replay')  # ユーザー：持ち玉を使用して遊技を行いますか？(y/n)
                    if replay_choice == 'y':
                        before = Pachinko.bonus_balls
                        # 持ち玉＜125玉であれば、持ち玉全てを遊技用に払い出す
                        if Pachinko.bonus_balls < re:
                            Pachinko.replay_balls = Pachinko.bonus_balls  #
                            print(f'{Pachinko.replay_balls}玉を払い出します。　[持ち玉:{Pachinko.bonus_balls}玉 >>> 0玉]')
                            Pachinko.bonus_balls = 0
                        else:
                            Pachinko.bonus_balls -= re  # 持ち玉から125玉引く
                            Pachinko.replay_balls += re  # 遊技玉に125玉追加する
                            print(f'{re}玉を払い出します。　＜持ち玉:{before}玉 >>> {Pachinko.bonus_balls}玉＞')
                    elif replay_choice == 'n':
                        print('遊技を終了します。')
                        income = Store.cashing()  # cashing_out() >>> 戻り値:income(=ball*4)
                        Store.revenue(self, income)
                        print('お疲れ様でした。Enterキーを押すとメニュー画面に戻ります。。')
                        Pachinko.replay = 0  # 再プレイを０に戻す。
                        break
                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                Store.check_the_game(self)  # 遊技確認
                # 遊技開始
                while (self.ball > 0) or (Pachinko.replay_balls > 0):
                    if (Pachinko.replay == 0) or (Pachinko.replay_balls > 0):
                        if chance_time == 0:  # チャンスタイム引き戻しの場合はスルー
                            navel = Store.ball_goes_in()  # 戻り値{None:消化、n:ヘソ入賞}
                        # 玉の入賞判定 (通常時7%で入賞) None:ヘソ入賞なし、int型:ヘソ入賞 -> 抽選
                        if navel is None:
                            if Pachinko.replay == 0:
                                self.ball -= 1  # 持ち玉が減る
                                Pachinko.add_total_balls(-1)  # 玉推移
                                continue
                            # 持ち玉遊技の場合
                            else:
                                Pachinko.replay_balls -= 1  # 持ち玉が減る
                                Pachinko.add_total_balls(-1)  # 玉推移
                                continue
                        # 大当りの抽選判定
                        else:
                            Pachinko.count_eva += 1 # 回転数
                            if chance_time == 0:  # チャンスタイム引き戻しの場合はスルー
                                jackpot = e_lottery()  # 戻り値{None:ハズレ、int型:当たり+確変、float型:当たり+チャンスタイム}
                            if jackpot is None:
                                continue
                            # チャンスタイム(100回転)
                            elif type(jackpot) is float:
                                chance_time = 100
                                Pachinko.bonus_balls += int(jackpot)  # 大当り純増出玉(確変突入時の遊技で使用＝減少していく）
                                Pachinko.add_total_balls(jackpot)  # 玉推移
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                Pachinko.bonus_pt += jackpot  # 大当りでの獲得出玉
                                Pachinko.total_bonus_count += 1  # 大当り回数をカウント
                                Pachinko.small_bonus_count += 1  # ボーナス内訳をカウント
                                print(f'{Pachinko.count_eva}回転目で小当りを引きました。{chance_time}回転の<チャンスタイム>に突入します。')
                                print('チャンスタイム中に大当りを引くと確率変動に突入します。')
                                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                                Pachinko.count_eva = 0  # 通常時の回転数を初期化
                                # チャンスタイム（入賞90%、抽選1/170)
                                while Pachinko.count_b <= 100:
                                    navel = Store.ball_goes_in_bonus()  # 戻り値{None:消化、n:ヘソ入賞}
                                    # 玉の入賞判定 (通常時7%で入賞) None:ヘソ入賞なし、int型:ヘソ入賞 -> 抽選
                                    if navel is None:
                                        Pachinko.bonus_balls -= 1  # 持ち玉が減る
                                        Pachinko.add_total_balls(-1)  # 玉推移
                                        continue
                                    else:
                                        Pachinko.count_b += 1  # ボーナス時の回転数をカウント
                                        jackpot_c = e_lottery_chance()
                                        if jackpot_c is None:
                                            continue
                                        else:
                                            print(f'チャンスタイム{Pachinko.count_b}回転目で大当りを引きました。おめでとうございます。')
                                            Pachinko.count_b = 0
                                            # loopを抜けて確変に行くための変数
                                            chance_time = 7
                                            navel = 7
                                            jackpot = jackpot_c  # 確変(loop外のelse文で持ち玉に加算する）
                                            Pachinko.replay_balls = Pachinko.bonus_balls
                                            break

                                # チャンスタイム終了
                                if Pachinko.count_b != 0:
                                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                    input(f'\nチャンスタイム{chance_time}回中に大当りを引けませんでした。<通常>に戻ります。Enterを押してください。')
                                    Pachinko.bonus_balls += self.ball  # 獲得出玉に小当たり前の持ち玉を足す
                                    self.ball = 0
                                    Pachinko.result()  # 結果表示
                                    Pachinko.total_bonus_count = 1  # 大当り回数を初期化
                                    Pachinko.small_bonus_count = 0  # ボーナス内訳を初期化
                                    Pachinko.count_b = 0  # 大当り時の回転数を初期化
                                    Pachinko.replay += 1
                                    break
                            # 確率変動
                            else:
                                bonus_time = 170
                                if chance_time == 7:  # チャンスタイム引き戻しの場合
                                    Pachinko.bonus_balls = Pachinko.replay_balls
                                    chance_time = 0
                                Pachinko.count_eva = 0  # 通常時の回転数を初期化
                                Pachinko.bonus_balls += int(jackpot)  # 大当り純増出玉(確変突入時の遊技で使用＝減少していく）
                                Pachinko.add_total_balls(jackpot)  # 玉推移
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                Pachinko.bonus_pt += jackpot  # 大当りでの獲得出玉
                                Pachinko.total_bonus_count += 1  # 大当り回数をカウント
                                # 大当り内訳をカウント（初回）
                                if jackpot == 1500:
                                    Pachinko.big_bonus_count += 1
                                elif jackpot == 300:
                                    Pachinko.small_bonus_count += 1
                                Pachinko.user_action('bonus_start')
                                print(f'\n*確率変動*: {Pachinko.total_bonus_count}回目')
                                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                                while Pachinko.count_b <= 170:
                                    n = Store.ball_goes_in_bonus()  # 戻り値{n:ヘソ入賞、None:消化}
                                    # ヘソ入賞判定
                                    if n is None:
                                        Pachinko.bonus_balls -= 1  # 持ち玉が減る
                                        Pachinko.add_total_balls(-1)  # 玉推移
                                        continue
                                    else:
                                        Pachinko.count_b += 1  # 回転数
                                        jackpot_b = e_lottery_bonus()  # lottery_bonus() 抽選
                                        # 大当りor転落の抽選判定  None:ハズレ、int型:大当り
                                        if jackpot_b is None:
                                            continue
                                        # 大当り
                                        else:
                                            Pachinko.bonus_balls += jackpot_b  # 大当り純増出玉
                                            Pachinko.add_total_balls(jackpot_b)  # 玉推移
                                            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                            Pachinko.bonus_pt += jackpot_b  # 大当り獲得出玉
                                            Pachinko.total_bonus_count += 1
                                            Pachinko.big_bonus_count += 1
                                            Store.bonus_info(jackpot_b)  # 情報表示
                                            print()
                                            print(f'*確率変動*: {Pachinko.total_bonus_count}回目')
                                            Pachinko.bonus_list.append(jackpot_b)
                                            Pachinko.count_b = 0  # 大当り時の回転数を初期化
                                            input('キーを押すと玉が発射されます。')
                                            continue
                                # 確率変動終了
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                print(f'\n確率変動{bonus_time}回転中に大当りを引く事ができませんでした。')
                                Pachinko.user_action('bonus_end')  # ユーザー：Enter
                                if Pachinko.replay == 0:
                                    Pachinko.bonus_balls += self.ball  # 大当り前の持ち玉を獲得出玉に合算
                                    self.ball = 0  # 持ち玉を初期化
                                else:
                                    Pachinko.bonus_balls += Pachinko.replay_balls  # 大当り前の持ち玉を獲得出玉に合算
                                    Pachinko.replay_balls = 0  # 持ち玉を初期化
                                Pachinko.before_bonus_balls = Pachinko.bonus_balls  # 再プレイで使用した玉数を計算する時に使用
                                Store.result()
                                Pachinko.after_bonus()  # 確変終了後の初期化
                                Pachinko.replay += 1
                                break
                    # ボーナス終了後ループから抜ける
                    else:
                        break
                # ボーナス０回(bonus_balls=0)
                if Pachinko.replay == 0:
                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                    print('持ち玉が無くなりました。', end=' ')
                    Store.num_of_rotations(Pachinko.count_eva)
                elif (Pachinko.replay_balls == 0) and (Pachinko.before_bonus_balls != Pachinko.bonus_balls):
                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                    print('玉が無くなりました。', end=' ')
                    Store.num_of_rotations(Pachinko.count_eva)
                    if Pachinko.bonus_balls == 0:
                        choice = Pachinko.user_action('replay_again')  # ユーザー：持ち玉を使い切りました。現金を使って遊技を継続しますか。(y/n)
                        if choice == 'y':
                            Pachinko.replay = 0  # 持ち玉を使い切った場合は０に戻す
                            return Pachinko.eva(self)
                        else:
                            input('メニュー画面に戻ります。Enterキーを押してください。')
                            break
                # ボーナスが終了
                elif Pachinko.replay > 0:
                    choice = Pachinko.user_action('replay_choice')  # ユーザー：獲得出玉で遊技を続けますか？ (y/n):
                    # 遊技継続の場合は再度自身の関数を呼ぶ
                    if choice == 'y':
                        return Pachinko.eva(self)  # 再プレイなら自身の関数を呼ぶ
                    else:
                        print('遊技を終了します。')
                        income = Store.cashing()  # 戻り値:income(=ball*4)
                        Store.revenue(self, income)
                        Pachinko.replay = 0  # 再プレイを初期化。
                        Pachinko.count_eva = 0  # 回転数を初期化
                        Pachinko.user_action('finished')  # ユーザー：Enter
                        break

        if self.money == 0:
            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
            print('\nお金が無くなりました。退店したい場合は ”*” を入力してください。')
            print('それ以外のキーを入力するとメニュー画面に戻ります。メニュー画面からお金の追加を行うことができます。')
            exiting = Pachinko.user_action('user_choice')  # ユーザー：退店orメニュー画面選択
            if exiting == '*':
                DB.updating_money(self.name, self.age, self.money, self.play)
                print('またのご来店をお待ちしております。')
                self.investment_amount = 0  # 投資額の初期化
                Pachinko.count_eva = 0
                return exiting
# ==================================================================================================
# CR魔法少女まどかマギカ:
# (通常時の大当り確率): 1/199, (初当たり出玉): +450(90%) or +1500(10%),
# (初当たり振り分け): 確率変動:50%, 通常:50%, (確率変動時の大当り確率): 1/70 回転数:70回転, (確率変動<上位>時の確率): 1/60: 回転数:120回転,
# (確率変動時の出玉振り分け): ALL+1500、(大当り継続率):68% or 86%, (補足)確率変動中の当たり1/3で確率変動<上位>に突入
    def madomagi(self, ball=0):
        print('-'*20)
        print('CR魔法少女まどかマギカで遊びます。')
        InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
        self.gaming_machine = 'CR魔法少女まどかマギカ'
        # 遊技準備
        while (self.money >= 500) or (Pachinko.bonus_balls > 0):
            # 再プレイではない場合(持ち玉遊技ではない場合)
            if Pachinko.bonus_balls == 0:
                ball = Store.lend(self)  # lend() >>> self.ball += 125
            # lend()で玉への変換を拒否した場合
            if ball is None:
                input('遊技を終了します。Enterキーを押すとメニュー画面に戻ります。')
                break
            else:
                if Pachinko.bonus_balls == 0:
                    print('交換完了：[現金:500円 ＞＞＞ 持ち玉:125玉]')
                # 再プレイ（持ち玉遊技）
                else:
                    re = 125  # 持ち玉遊技(=125玉)
                    replay_choice = Pachinko.user_action('replay')  # ユーザー：持ち玉を使用して遊技を行いますか？(y/n)
                    if replay_choice == 'y':
                        before = Pachinko.bonus_balls
                        # 持ち玉＜125玉であれば、持ち玉全てを遊技用に払い出す
                        if Pachinko.bonus_balls < re:
                            Pachinko.replay_balls = Pachinko.bonus_balls
                            print(f'{Pachinko.replay_balls}玉を払い出します。　[持ち玉:{Pachinko.bonus_balls}玉 >>> 0玉]')
                            Pachinko.bonus_balls = 0
                        else:
                            Pachinko.bonus_balls -= re  # 持ち玉から125玉引く
                            Pachinko.replay_balls += re  # 遊技玉に125玉追加する
                            print(f'{re}玉を払い出します。　＜持ち玉:{before}玉 >>> {Pachinko.bonus_balls}玉＞')
                    elif replay_choice == 'n':
                        print('遊技を終了します。')
                        income = Store.cashing()  # cashing_out() >>> 戻り値:income(=ball*4)
                        Store.revenue(self, income)
                        Pachinko.user_action('finished')
                        Pachinko.replay = 0  # 再プレイを０に戻す。
                        break
                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                Store.check_the_game(self)  # 遊技確認
                # 遊技
                while (self.ball > 0) or (Pachinko.replay_balls > 0):
                    if (Pachinko.replay == 0) or (Pachinko.replay_balls > 0):
                        navel = Store.ball_goes_in()  # 戻り値{None:消化、n:ヘソ入賞}
                        # 玉の入賞判定 (通常時7%で入賞) None:ヘソ入賞なし、int型:ヘソ入賞 -> 抽選
                        if navel is None:
                            if Pachinko.replay == 0:
                                self.ball -= 1  # 持ち玉が減る
                                Pachinko.add_total_balls(-1)  # 玉推移
                                continue
                            # 持ち玉遊技の場合
                            else:
                                Pachinko.replay_balls -= 1  # 持ち玉が減る
                                Pachinko.add_total_balls(-1)  # 玉推移
                                continue
                        # 大当りの抽選判定
                        else:
                            Pachinko.count_madoka += 1 # 回転数
                            jackpot = m_lottery()  # 戻り値{None:ハズレ、int型:当たり+確変、float型:当たり+通常}
                            if jackpot is None:
                                continue
                            # bonus(+450玉) >>> 通常
                            elif type(jackpot) is float:
                                Pachinko.bonus_balls += int(jackpot)  # 大当り純増出玉(確変突入時の遊技で使用＝減少していく）
                                Pachinko.add_total_balls(jackpot)  # 玉推移
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                Pachinko.bonus_pt += jackpot  # 大当りでの獲得出玉
                                Pachinko.total_bonus_count += 1  # 大当り回数をカウント
                                Pachinko.small_bonus_count += 1  # ボーナス内訳をカウント
                                Pachinko.count_madoka = 0  # 通常時の回転数を初期化
                                Pachinko.bonus_balls += self.ball  # 獲得出玉に小当たり前の持ち玉を足す
                                self.ball = 0
                                Pachinko.bonus_balls = int(Pachinko.bonus_balls)  # 結果をfloatで表示しないため
                                Pachinko.result()  # 結果表示
                                Pachinko.total_bonus_count = 0  # 大当り回数を初期化
                                Pachinko.small_bonus_count = 0  # ボーナス内訳を初期化
                                Pachinko.count_madoka = 0  # 通常時の回転数を初期化
                                Pachinko.count_b = 0  # 大当り時の回転数を初期化
                                Pachinko.bonus_pt = 0  # 大当りでの獲得出玉を初期化
                                Pachinko.before_bonus_balls = Pachinko.bonus_balls  # 再プレイ（持ち玉遊技）の判定で使用
                                Pachinko.replay += 1

                                break
                            # 確率変動
                            else:
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                bonus_time = 80
                                Pachinko.count_madoka = 0  # 通常時の回転数を初期化
                                Pachinko.bonus_balls += jackpot  # 大当り純増出玉(確変突入時の遊技で使用＝減少していく）
                                Pachinko.add_total_balls(jackpot)  # 玉推移
                                InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                Pachinko.bonus_pt += jackpot  # 大当りでの獲得出玉
                                Pachinko.total_bonus_count += 1  # 大当り回数をカウント
                                # ボーナス内訳をカウント
                                if jackpot == 1500:
                                    Pachinko.big_bonus_count += 1
                                elif jackpot == 450:
                                    Pachinko.small_bonus_count += 1
                                Pachinko.user_action('bonus_start')
                                print(f'\n*確率変動*: {Pachinko.total_bonus_count}回目')
                                Pachinko.user_action('firing')  # ユーザー：Enterキーを押すと玉が発射されます。
                                while Pachinko.count_b <= 80:
                                    n = Store.ball_goes_in_bonus()  # 戻り値{n:ヘソ入賞、None:消化}
                                    # ヘソ入賞判定
                                    if n is None:
                                        Pachinko.bonus_balls -= 1  # 持ち玉が減る
                                        Pachinko.add_total_balls(-1)  # 玉推移
                                        continue
                                    else:
                                        Pachinko.count_b += 1  # 回転数
                                        jackpot_b = m_lottery_bonus()  # lottery_bonus() 抽選
                                        # 大当りor転落の抽選判定  None:ハズレ、int型:大当り、float型:大当り+確変上位突入
                                        if jackpot_b is None:
                                            continue
                                        # 確変当たり
                                        elif type(jackpot_b) is int:
                                            Pachinko.bonus_balls += jackpot_b  # 大当り純増出玉
                                            Pachinko.add_total_balls(jackpot_b)  # 玉推移
                                            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                            Pachinko.bonus_pt += jackpot_b  # 大当り獲得出玉
                                            Pachinko.total_bonus_count += 1
                                            Pachinko.big_bonus_count += 1
                                            Store.bonus_info(jackpot_b)  # 情報表示
                                            print()
                                            print(f'*確率変動*: {Pachinko.total_bonus_count}回目')
                                            Pachinko.bonus_list.append(jackpot_b)
                                            Pachinko.count_b = 0  # 大当り時の回転数を初期化
                                            Pachinko.user_action('firing')
                                            continue
                                        # 確変当たり＋確率変動<上位>に突入
                                        elif type(jackpot_b) is float:
                                            jackpot_b = int(jackpot_b)  # int型に戻す
                                            bonus_time = 120
                                            Pachinko.bonus_balls += jackpot_b  # 大当り純増出玉(確変突入時の遊技で使用＝減少していく）
                                            Pachinko.add_total_balls(jackpot_b)  # 玉推移
                                            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                            Pachinko.bonus_pt += jackpot_b  # 大当りでの獲得出玉
                                            Pachinko.total_bonus_count += 1  # 大当り回数をカウント
                                            Pachinko.big_bonus_count += 1  # 大当り内訳をカウント
                                            big_bonus_plus_count = 0  # 大当り内訳（まどマギ上位用）
                                            Store.bonus_info(jackpot_b)  # 情報表示
                                            print()
                                            print('おめでとうございます。上位突入大当りを引いたので、確率変動<上位>に突入します。')
                                            print('確率：1/70 -> 1/60、　回転数：80回転　-> 120回転')
                                            input('<確率変動(上位)>に突入します。Enterキーを押すと玉が発射されます。')
                                            while Pachinko.count_b <= 120:
                                                n = Store.ball_goes_in_bonus()  # 戻り値{n:ヘソ入賞、None:消化}
                                                # ヘソ入賞判定
                                                if n is None:
                                                    Pachinko.bonus_balls -= 1  # 持ち玉が減る
                                                    Pachinko.add_total_balls(-1)  # 玉推移
                                                    continue
                                                else:
                                                    Pachinko.count_b += 1  # 回転数
                                                    jackpot_b_plus = m_lottery_bonus_plus()  # lottery_bonus() 抽選
                                                    # 大当りor転落の抽選判定  None:ハズレ、int型:大当り
                                                    if jackpot_b is None:
                                                        continue
                                                    elif type(jackpot_b_plus) is int:
                                                        Pachinko.bonus_balls += jackpot_b  # 大当り純増出玉
                                                        Pachinko.add_total_balls(jackpot_b)  # 玉推移
                                                        InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                                        Pachinko.bonus_pt += jackpot_b  # 大当り獲得出玉
                                                        Pachinko.total_bonus_count += 1
                                                        big_bonus_plus_count += 1
                                                        Store.bonus_info(jackpot_b)  # 情報表示
                                                        print()
                                                        print(f'*確率変動<上位>*: {big_bonus_plus_count}回目')
                                                        Pachinko.bonus_list.append(jackpot_b_plus)
                                                        Pachinko.count_b = 0  # 大当り時の回転数を初期化
                                                        input('キーを押すと玉が発射されます。')
                                                        continue
                                            # 確変<上位>転落　>>> 通常
                                            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                            print(f'\n確率変動<上位>{bonus_time}回転中に大当りを引く事ができませんでした。')
                                            Pachinko.user_action('bonus_end')  # ユーザー：Enter
                                            # 持ち玉を初期化
                                            if Pachinko.replay == 0:
                                                Pachinko.bonus_balls += self.ball  # 大当り前の持ち玉を獲得出玉に合算
                                                self.ball = 0
                                            else:
                                                Pachinko.bonus_balls += Pachinko.replay_balls  # 大当り前の持ち玉を獲得出玉に合算
                                                Pachinko.replay_balls = 0
                                            Pachinko.before_bonus_balls = Pachinko.bonus_balls  # 再プレイで使用した玉数を計算する時に使用
                                            Pachinko.bonus_balls = int(Pachinko.bonus_balls)  # 結果をfloatで表示しないため
                                            Store.result()
                                            Pachinko.after_bonus()  # 確変終了後の初期化
                                            Pachinko.replay += 1
                                            break
                                # 確変転落　>>> 転落
                                if Pachinko.replay == 0:
                                    bonus_time = 80
                                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                                    print(f'\n確率変動{bonus_time}回転中に大当りを引く事ができませんでした。')
                                    Pachinko.user_action('bonus_end')  # ユーザー：Enter
                                    # 持ち玉を初期化
                                    if Pachinko.replay == 0:
                                        Pachinko.bonus_balls += self.ball  # 大当り前の持ち玉を獲得出玉に合算
                                        self.ball = 0
                                    else:
                                        Pachinko.bonus_balls += Pachinko.replay_balls  # 大当り前の持ち玉を獲得出玉に合算
                                        Pachinko.replay_balls = 0
                                    Pachinko.before_bonus_balls = Pachinko.bonus_balls  # 再プレイで使用した玉数を計算する時に使用
                                    Pachinko.bonus_balls = int(Pachinko.bonus_balls)  # 結果をfloatで表示しないため
                                    Store.result()
                                    Pachinko.after_bonus()  # 確変終了後の初期化
                                    Pachinko.replay += 1
                                    break
                # ボーナス０回(bonus_balls=0)
                if Pachinko.replay == 0:
                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                    print('持ち玉が無くなりました。', end=' ')
                    Store.num_of_rotations(Pachinko.count_madoka)
                elif (Pachinko.replay_balls == 0) and (Pachinko.before_bonus_balls != Pachinko.bonus_balls):
                    InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
                    print('玉が無くなりました。', end=' ')
                    Store.num_of_rotations(Pachinko.count_madoka)
                    if Pachinko.bonus_balls == 0:
                        choice = Pachinko.user_action('replay_again')  # ユーザー：持ち玉を使い切りました。現金を使って遊技を継続しますか。(y/n)
                        if choice == 'y':
                            Pachinko.replay = 0  # 持ち玉を使い切った場合は０に戻す
                            return Pachinko.madomagi(self)
                        else:
                            input('メニュー画面に戻ります。Enterキーを押してください。')
                            break
                # ボーナスが終了
                elif Pachinko.replay > 0:
                    choice = Pachinko.user_action('replay_choice')  # ユーザー：獲得出玉で遊技を続けますか？ (y/n):
                    # 遊技継続の場合は再度自身の関数を呼ぶ
                    if choice == 'y':
                        return Pachinko.madomagi(self)  # 再プレイなら自身の関数を呼ぶ
                    else:
                        print('遊技を終了します。')
                        income = Store.cashing()  # 戻り値:income(=ball*4)
                        Store.revenue(self, income)
                        Pachinko.replay = 0  # 再プレイを初期化。
                        Pachinko.count_eva = 0  # 回転数を初期化
                        Pachinko.user_action('finished')  # ユーザー：Enter
                        break

        if self.money == 0:
            InformationDisplay.add_data_to_csvfile(Pachinko.total_count, Pachinko.total_balls)  # csv
            print('\nお金が無くなりました。退店したい場合は ”*” を入力してください。')
            print('それ以外のキーを入力するとメニュー画面に戻ります。メニュー画面からお金の追加を行うことができます。')
            exiting = Pachinko.user_action('user_choice')  # ユーザー：退店orメニュー画面選択
            if exiting == '*':
                DB.updating_money(self.name, self.age, self.money, self.play)
                print('またのご来店をお待ちしております。')
                self.investment_amount = 0  # 投資額の初期化
                Pachinko.count_eva = 0
                return exiting
