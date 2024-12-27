from Pachinko_store.store.store import Store
from Pachinko_store.data_processing.operate_db import WorkingWithDatabase
from Pachinko_store.data_processing.game_data import GameData
from Pachinko_store.game.eva import Eva
from Pachinko_store.game.hokuto import Hokuto
from Pachinko_store.game.madomagi import MadoMagi


class Main:
    min_money = 500

    game_func_dict = {
        'H': Hokuto.main,
        'E': Eva.main,
        'M': MadoMagi.main
    }

    # アカウント確認
    @staticmethod
    def _show_account(name, age, money):
        print('下記のアカウントで入店します。')
        print('-'*20)
        print(f'名前: {name}')
        print(f'年齢: {age}歳')
        print(f'所持金: {money}円')
        print('-'*20)
        if money < Main.min_money:
            print(f'遊技には{Main.min_money}円必要です。メニュー画面から "所持金を追加" を選択してください。')

    @staticmethod
    def main():
        name, age, money = Store.customer()
        # age < 18
        if age is None:
            print('入店できませんでした。')
        else:
            char = Store(name, age, money)  # インスタンス作成
            GameData.create_csvfile()  # 遊技情報を記録するためのcsvファイルを作成
            print('いらっしゃいませ')
            Main._show_account(char.name, char.age, char.money)  # アカウント表示
            while True:
                choice = Store.action_selection(char)  # 行動選択
                # 退店
                if choice is None:
                    break
                # メニューアクション(機種情報の表示、自身の遊技履歴確認、所持金の追加、管理者メニュー)
                elif choice is False:
                    continue
                # 遊技
                else:
                    continue_or_not = Main.game_func_dict[choice](char)  # ゲームメイン
                    # メニュー選択に戻る
                    if continue_or_not != '*':
                        continue
                    # 退店
                    else:
                        print('ご来店ありがとうございました。')
                        break


if __name__ == '__main__':
    Main.main()
