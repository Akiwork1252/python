import logging
from database import DataBase


# アカウントの作成、確認
class Account:
    # ロギングの設定  >>> ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    logging.basicConfig(level=logging.DEBUG, format='%(time)s - %(name)s - %(level)s - %(message)s')

    def __init__(self, name, age, money):
        self.name = name
        self.age = age
        self.money = money

    # 年齢入力
    @staticmethod
    def input_age():
        while True:
            try:
                user_age = int(input('年齢:'))
            except ValueError:
                print('半角英数字で入力してください。')
            except KeyboardInterrupt:
                print('予期せぬエラーが発生しました。')
                logging.error('これはエラーメッセージです')
            else:
                return user_age

    # 所持金入力(初来店の客のみ）
    @staticmethod
    def input_money():
        print('初めてのご来店ですね。所持金を入力してください。')
        while True:
            try:
                user_money = int(input('所持金: '))
            except ValueError:
                print('半角英数字で入力してください。')
            except KeyboardInterrupt:
                print('予期せぬエラーが発生しました。')
                logging.error('これはエラーメッセージです')
            else:
                return user_money

    # 年齢チェック
    @staticmethod
    def check_age(age, min_age=18):
        if min_age <= age:
            return age
        else:
            print(f'パチンコは{min_age}歳からです。')

    # 所持金チェック
    @staticmethod
    def check_money(money):
        min_money = 500
        if min_money < money:
            return money
        else:
            print(f'遊戯には{min_money}円以上必要です。')
            print('遊戯したい場合は、メニュー画面からお金を追加してください。')
            return money

    # アカウント表示
    @staticmethod
    def view_account(name, age, money):
        print('-'*20)
        print(f'名前: {name}')
        print(f'年齢: {age}')
        print(f'所持金: {money}')
        print('-'*20)

    # アカウント作成
    @staticmethod
    def create_account(name, age):
        money = Account.check_money(Account.input_money())  # check_money():所持金の入力と判定 500未満はNoneを返す
        DataBase.add_account_to_db(name, age, money)  # データベースに新規客の情報を追加
        char = Account(name, age, money)  # インスタンス作成
        return char

    # アカウント確認、作成
    @staticmethod
    def check_account():
        print('名前、年齢、所持金を入力してください。')
        user_name = input('名前:')
        user_age = Account.check_age(Account.input_age())  # check_age():年齢取得 >>> 18歳未満ならNoneを返す
        if user_age is not None:
            db_money = DataBase.account_check(user_name, user_age)  # account_check():データベースを確認
            if db_money is None:
                char = Account.create_account(user_name, user_age)  # アカウント作成
                print('アカウントを作成しました。')
                Account.view_account(char.name, char.age, char.money)
                return char
            else:
                char = Account(user_name, user_age, db_money)  # インスタンス作成
                print(f'前回の所持金({char.money}円)を使用して、下記のアカウントで入店します。')
                Account.view_account(char.name, char.age, char.money)
                return char
        else:
            return None


if __name__ == '__main__':
    Account.check_account()
