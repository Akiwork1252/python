import logging
from account import Account
from database import DataBase


class Main:
    # ロギングの設定  >>> ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    logging.basicConfig(level=logging.DEBUG, format='%(time)s - %(name)s - %(level)s - %(message)s')

    @staticmethod
    def main():
        DataBase.create_pachinko_db()  # データベースpachinko.db(ユーザー情報、遊戯履歴)がなければカレントディレクトリに作成
        DataBase.check_and_add_spec_db()  # データベースspec.db(機種情報)をカレントディレクトリに作成、更新
        check = Account.check_account()  # アカウントの確認と作成
        if check is not None:
            pass
        else:
            print('またのご来店をお待ちしています。')


Main.main()
