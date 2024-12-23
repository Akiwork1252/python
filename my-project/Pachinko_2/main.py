import logging
from account import Account
from operate_db import DataBase
from playing_game import GameMain
from store import Store


class Main:
    # ロギングの設定  >>> ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    logging.basicConfig(level=logging.DEBUG, format='%(time)s - %(name)s - %(level)s - %(message)s')
    logging.getLogger('matplotlib').setLevel(logging.WARNING)

    # ゲーム関数ディクショナリー
    game_menu = {
        'H': GameMain.fist_of_the_north_star,
        'E': GameMain.neon_genesis_evangelion,
        'M': GameMain.puella_magi_madoka_magika,
    }

    @staticmethod
    def main():
        DataBase.create_pachinko_db()  # データベースpachinko.db(ユーザー情報、遊戯履歴)をカレントディレクトリに作成(あればスルー)
        DataBase.check_and_add_spec_db()  # データベースspec.db(機種情報)をカレントディレクトリに作成、更新
        char = Account.check_account()  # アカウントの確認と作成 >>> インスタンスオブジェクトを返す
        # 年齢判定 >>> None:退店
        if char is not None:
            game_choice = Store.store_main(char)  # 退店:Noneを返す、　遊戯:str型を返す　その他アクション:関数内でループ
            if game_choice is not None:
                Main.game_menu[game_choice](char)
            else:
                print('またのご来店をお待ちしています。')
        else:
            print('またのご来店をお待ちしています。')


Main.main()
