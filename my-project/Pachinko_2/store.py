import random
from account import Account
from operate_db import DataBase


# パチンコ店のクラス　
# <機能>
#  ・アクションメニューの選択、・収益を表示、
#  ・選択アクション(遊戯台の選択、遊戯台のスペックを表示、自身の遊戯履歴表示、所持金追加、管理者メニュー、退店)
#  ・遊技台の出玉推移グラフを表示
class Store(Account):
    # 顧客選択メニュー
    menu = {
        'H': 'CR北斗の拳',
        'E': 'CRエヴァンゲリオン',
        'M': 'CR魔法少女まどかマギカ',
        '#': '遊戯台のスペックを確認',
        '=': '自身の遊戯履歴を表示',
        '$': '所持金を追加',
        '*': '退店',
        'master': '管理者メニュー(パスワード必要)',
    }

    # 管理者メニュー(TOP)表示用
    master_top_menu = {
        1: 'データベースの確認',
        2: '今後追加予定'
    }
    # 管理者メニュー(DB)表示用
    master_db_menu = {
        1: '顧客情報の確認',
        2: '遊戯履歴の確認',
    }

    def __init__(self, name, age, money):
        super().__init__(name, age, money)
        self.investment_amount = 0  # 総投資額
        self.play_check = 0

    # メニュー画面を表示
    @staticmethod
    def _menu_display():
        print('メニュー画面を表示します。', end='')
        Store.input_enter()
        print('-'*8, '<MENU>', '-'*8)
        print('＜遊戯台＞')
        for key, menu in Store.menu.items():
            if key == '#':
                print('＜その他メニュー＞')
            print(f'  {menu} >>> キー({key})')
        print('-'*20)

    # メニューの選択
    @staticmethod
    def _user_choice():
        Store._menu_display()  # メニュー画面を表示
        while True:
            print('アクションを選択して対応キーを入力してください。')
            choice = Store.input_choice()
            if choice not in Store.menu:
                print('入力が正しくありません。')
                continue
            else:
                break
        print(f'\nあなたは" {Store.menu[choice]} "を選択しました。')
        return choice

    # アクションの振り分け 戻り値 >>> choice:遊戯、 False:アクション後メニュー画面に戻る、None:ループから抜ける(退店)
    def _user_action(self, choice, min_money=500):
        if (choice == 'H') or (choice == 'E') or (choice == 'M'):  # 遊戯
            if self.money < min_money:
                print(f'遊戯は{min_money}円以上必要です。メニュー画面で「所持金を追加」を選択してください。')
                return False
            else:
                return choice
        elif choice == '#':  # 遊戯台のスペックを表示
            Store._show_spec()
            return False
        elif choice == '=':  # 自身の遊戯履歴を表示
            Store._show_history(self)
            return False
        elif choice == '$':  # 所持金を追加
            Store._add_money(self)
            return False
        elif choice == '*':  # 退店
            print('ご来店ありがとうございました。', end='')
            Store.input_enter()
            return None
        elif choice == 'master':
            print('管理者メニューの操作にはパスワードが必要です。パスワードを入力して下さい。')
            master = Store._check_password()
            if master is False:
                return False
            else:
                while True:
                    Store._master_action()
                    print('操作を継続しますか?', end='')
                    y_n = Store.input_yer_or_no()  # 戻り値: y >>>True, n >>>False
                    if y_n is True:
                        continue
                    else:
                        print('管理者操作を終了します。')
                        break
                return False

    # 機種スペックの表示
    @staticmethod
    def _show_spec():
        print('遊戯台のスペックを表示します。', end='')
        Store.input_enter()
        print('-'*40)
        DataBase.show_spec_db()
        print('-'*40)

    # 過去の遊戯履歴を表示
    def _show_history(self):
        print('過去の遊戯履歴を表示します。', end='')
        Store.input_enter()
        print('-'*40)
        DataBase.show_history(self.name, self.age)
        print('-'*40)

    # 所持金を追加
    def _add_money(self, min_amount=500, max_amount=10000):
        print('所持金を追加します。', end='')
        Store.input_enter()
        print('-'*40)
        print(f'これまでの投資金額:{self.investment_amount}円')
        while True:
            try:
                amount = int(input('金額を半角英数字で入力してください。'))
            except ValueError:
                print('入力された値が正しくありません。')
            else:
                if amount < min_amount:
                    print(f'遊戯には{min_amount}円以上必要です。')
                elif max_amount < amount:
                    print(f'一度に追加できる上限金額は{max_amount}円です')
                else:
                    print(f'所持金は{amount}円になりました。', end='')
                    Store.input_enter()
                    break
        print('-'*40)

    # 管理者メニュー(TOP)の表示、選択
    @staticmethod
    def _show_master_top_menu():
        while True:
            print('メニューから操作を選択してください。')
            print('-'*8, '<TOP-MENU>', '-'*8)
            for key, menu in Store.master_top_menu.items():
                print(f'{menu} >>> キー({key})')
            print('-'*20)
            choice = int(Store.input_choice())
            if choice in Store.master_db_menu:
                return choice
            else:
                print('入力が正しくありません。')

    # 管理者メニュー(DB)の表示
    @staticmethod
    def _show_master_db_menu():
        while True:
            print('データベースの確認をします。メニューから操作を選択してください。')
            print('-'*8, '<DataBase-MENU>', '-'*8)
            for key, menu in Store.master_db_menu.items():
                print(f'{menu} >>> キー({key})')
            print('-'*20)
            choice = int(Store.input_choice())
            if choice in Store.master_db_menu:
                return choice
            else:
                print('入力が正しくありません。')

    # 管理者アクション
    @staticmethod
    def _master_action():
        top_menu_action = Store._show_master_top_menu()
        if top_menu_action == 1:
            db_menu_action = Store._show_master_db_menu()
            DataBase.master_only_check_pachinko_db(db_menu_action)
        else:
            print('他メニューは今後実装予定です。')

    # パスワード確認
    @staticmethod
    def _check_password(master_ward='hoge'):
        user = input('パスワード：　')
        if user != master_ward:
            print('入力されたパスワードは正しくありません。')
            return False

    # ユーザーの確認を待つ
    @staticmethod
    def input_enter():
        while True:
            enter = input('Enterキーを押してください。')
            if isinstance(enter, str):
                break

    # ユーザーの選択を待つ
    @staticmethod
    def input_choice():
        while True:
            choice = input('User: ')
            if isinstance(choice, str):
                return choice
            else:
                continue

    # 入力(y/n)と入力判定
    @staticmethod
    def input_yer_or_no():
        while True:
            yes_or_no = input('(y/n): ')
            if yes_or_no == 'y':
                return True
            elif yes_or_no == 'n':
                return False
            else:
                print('入力が正しくありません。(YES -> "y", NO -> "n")')
                continue

    # Storeメイン
    def store(self):
        while True:
            choice = Store._user_choice()
            user_action = Store._user_action(self, choice)
            # その他アクションの実行後にメニュー画面に戻る
            if user_action is False:
                continue
            # 退店
            elif user_action is None:
                DataBase.update_user_table(self.name, self.age, self.money, self.play_check)
                break
            # 遊戯
            elif isinstance(user_action, str):  # 遊戯
                return choice


if __name__ == '__main__':
    aki = Store('aki', 33, 5000)
    Store.store(aki)
