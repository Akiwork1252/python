from Pachinko_store.data_processing.operate_db import WorkingWithDatabase


# アカウント作成、メニュー選択、メニュー実行(機種情報の表示、遊戯履歴確認、所持金追加、管理者メニュー)
class Store:
    menu = {
        'H': 'CR北斗の拳',
        'E': 'CRエヴァンゲリオン',
        'M': 'CR魔法少女まどかマギカ',
        '#': '機種情報を表示',
        '=': '自身の遊技履歴を表示',
        '$': '所持金を追加',
        '*': '退店',
        'master': '管理者メニュー(パスワード必要)',
    }
    master_top_menu = {
        1: 'データベースの確認',
        2: '今後実装予定',
    }
    master_db_menu = {
        1: '顧客情報の確認',
        2: '遊技履歴の確認',
    }

    def __init__(self, name, age, money):
        self.name = name
        self.age = age
        self.money = money
        self.balls = 0  # 遊技で使用
        self.total_investment_amount = 0  # 総投資額
        self.model_played = ''  # 遊技機種
        self.play_check = 0  # 遊技確認(DB保存用)
        self.add_money = 0

# =========== アカウント作成 ============
    # 名前と年齢の入力
    @staticmethod
    def _input_name_and_age(min_age=18):
        print('名前と年齢を入力してください。')
        name = input('Name: ')
        while True:
            try:
                age = int(input('Age: '))
                if age < min_age:
                    print(f'パチンコは{min_age}歳からです。')
                    age = None
                    break
            except ValueError:
                print('半角英数字で入力してください。(例:20)')
            else:
                break
        return name, age

# =========== ユーザー入力 ============
    # Enter
    @staticmethod
    def input_enter():
        input('Enter: ')

    # Yes/No
    @staticmethod
    def input_yes_or_no():
        while True:
            y_n = input('(y/n): ')
            if (y_n == 'y') or (y_n == 'n'):
                break
            else:
                print('入力が正しくありません。')
        return y_n

    # 金額入力
    @staticmethod
    def input_amount():
        while True:
            try:
                amount = int(input('Amount: '))
            except ValueError:
                print('半角英数字で入力してください。')
            else:
                judge = Store.amount_judge(amount)
                if judge is False:
                    continue
                else:
                    break
        return amount

    # 金額判定
    @staticmethod
    def amount_judge(amount, min_amount=500, max_amount=10000):
        judge = True
        if amount < min_amount:
            print(f'遊技には最低{min_amount}円必要です。')
            judge = False
        elif amount > max_amount:
            print(f'一度に追加できる金額は{max_amount}円です。')
            judge = False
        return judge

    # メニュー選択
    @staticmethod
    def input_choice():
        while True:
            choice = input('User: ')
            if choice in Store.menu:
                return choice
            else:
                print('入力が正しくありません。')

# =========== ユーザーアクション ============
    # 所持金の追加
    def _add_money(self):
        before = self.money
        print(f'・現在の所持金: {before}円')
        print(f'・現在の投資金額: {self.total_investment_amount}円')
        print(f'追加する金額を入力してください。')
        amount = Store.input_amount()
        self.money += amount
        self.add_money += amount  # 追加金額
        print(f'・所持金: {before}円 >>> {self.money}円')
        print(f'{amount}円を追加しました。')

# =========== 管理者アクション　============
    # パスワードの確認
    @staticmethod
    def _check_password(text, master=False):
        password = 'aki'
        if text == password:
            master = True
        else:
            print('パスワードが正しくありません。')
        return master

    # 管理者メニューを表示
    @staticmethod
    def _show_master_top_menu():
        print('管理者メニューを表示します。')
        print('メニュー画面から行動を選択して、対応キーを入力してください。')
        print('-'*5, '<Master Menu> ', '-'*5)
        for key, menu in Store.master_top_menu.items():
            print(f'・{menu} >>> キー:({key})')
        print('-'*30)

    # 管理者データベースメニューを表示
    @staticmethod
    def _show_master_db_menu():
        print('管理者データベースメニューを表示します。')
        print('メニュー画面から行動を選択して、対応キーを入力してください。')
        print('-'*5, '<DataBase Menu>', '-'*5)
        for key, menu in Store.master_db_menu.items():
            print(f'・{menu} >>> キー:({key})')
        print('-'*30)

    # 入力
    @staticmethod
    def _input_master(menu='Top'):
        while True:
            try:
                choice = int(input('Master: '))
            except ValueError:
                print('半角英数字で入力してください。')
            else:
                judge = Store._check_master_input(choice, menu)
                if judge is False:
                    continue
                else:
                    break
        return choice

    # 入力判定
    @staticmethod
    def _check_master_input(choice, menu, judge=False):
        if menu == 'Top':
            if choice in Store.master_top_menu:
                judge = True
            else:
                print('入力が正しくありません。')
        elif menu == 'DB':
            if choice in Store.master_db_menu:
                judge = True
            else:
                print('入力が正しくありません。')
        return judge

    # 管理者Topメニュー選択
    @staticmethod
    def _master_choice_top_menu():
        Store._show_master_top_menu()
        choice = Store._input_master()
        return choice

    # 管理者DBメニュー選択
    @staticmethod
    def _master_choice_db_menu():
        Store._show_master_db_menu()
        choice = Store._input_master('DB')
        return choice

    # 管理者DBメニュー
    @staticmethod
    def _master_check_db():
        choice = Store._master_choice_db_menu()
        if choice == 1:
            print('='*5, ' <顧客情報> ', '='*5)
            WorkingWithDatabase.show_user_table_of_store_db()
        elif choice == 2:
            print('='*5, ' <遊技履歴> ', '='*5)
            WorkingWithDatabase.show_history_tabel_of_store_db(master=True)
        else:
            print('今後実装予定です。')
        print('='*8, ' END ', '='*8)
        Store.input_enter()

    # 管理者メニューメイン
    @staticmethod
    def _master_main():
        print('パスワードを入力してください。')
        text = input('User: ')
        master = Store._check_password(text)
        if master is True:
            while True:
                choice = Store._master_choice_top_menu()
                if choice == 1:
                    Store._master_check_db()
                else:
                    print('今後実装予定です。')
                print('操作を継続しますか？', end='')
                y_n = Store.input_yes_or_no()
                if y_n == 'y':
                    continue
                else:
                    print('管理者操作を終了します。')
                    break
        else:
            print('操作を終了します。')

# =========== Storeメイン ============
    # メニュー表示
    @staticmethod
    def _show_menu():
        print('メニュー画面を表示します。', end='')
        Store.input_enter()
        print('-'*8, ' Store Menu ', '-'*8)
        print('<遊技>')
        for key, menu in Store.menu.items():
            if key == '#':
                print('<その他メニュー>')
            print(f'・{menu} >>> キー:({key})')
        print('-'*20)

    # メニュー選択 <<< Mainで実行
    # 戻り値choice(None:退店、False:アクション後にメニューに戻る、str：遊技関数呼び出し)
    def action_selection(self):
        Store._show_menu()
        print('上記メニューから行動を選択して、対応キーを入力してください。')
        choice = Store.input_choice()
        print(f'あなたは "{Store.menu[choice]}" を選択しました。')
        if (choice == 'H') or (choice == 'E') or (choice == 'M'):
            self.model_played = Store.menu[choice]
        elif choice == '#':
            print('===== <遊技台スペック情報> =====')
            WorkingWithDatabase.show_spec_db()
            choice = False
        elif choice == '=':
            print('===== <遊技履歴> =====')
            WorkingWithDatabase.show_history_tabel_of_store_db(self.name, self.age)
            choice = False
        elif choice == '$':
            print('===== <所持金追加> =====')
            Store._add_money(self)
            choice = False
        elif choice == 'master':
            print('===== <管理者メニュー> =====')
            Store._master_main()
            choice = False
        else:
            print('ご来店ありがとうございました。')
            choice = None
        if choice is not None:
            print('='*30)
            Store.input_enter()
        return choice

    # 顧客情報を返す <<< Mainで実行
    @staticmethod
    def customer():
        name, age = Store._input_name_and_age()
        if age is None:
            money = None
        else:
            money = WorkingWithDatabase.user_table_of_store_db_main(name, age)  # DB確認(データ無:所持金入力, データ有:所持金取出)
        return name, age, money

# =========== パチンコ処理 ============
    # 遊戯玉の貸し出し
    def _ball_rental(self, amount, balls):
        self.money -= amount
        self.balls += balls
        self.total_investment_amount += amount
