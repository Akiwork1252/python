from operate_db import DB
from store import Store, Pachinko


# メインクラス
# 入店（アカウント確認・作成）、遊技関数の呼び出し、退店（遊技記録をDBに保存）
class Main:
    # 遊技台の関数ディクショナリー
    func_dict = {
        'H': Pachinko.hokuto,
        'E': Pachinko.eva,
        'M': Pachinko.madomagi,
    }

    @staticmethod
    def account_check():
        print('名前,年齢,所持金を半角英数字で入力してください。')
        name = input('名前: ')
        while True:
            try:
                age = int(input('年齢： '))
            except ValueError:
                print('半角英数字で入力してください。(例:32)')
            else:
                break
        # 名前と年齢でデータベースを検索。データがあれば、前回の所持金を返す。データが無ければアカウントを作成する。
        user = DB.user_search_and_add(name, age)  # 戻り値 >>> データあり:int(money)、データなし:tuple(name, age, money)
        if type(user) is tuple:
            # char:インスタンス作成
            char = Store(user[0], user[1], user[2])
        else:
            # char:インスタンス作成(前回の所持金を利用)
            char = Store(name, age, user)
        judge = char.entrance()
        if judge is None:
            return None
        else:
            print('下記のアカウントで入店します。')
            print('-'*20)
            print(f'名前: {char.name}')
            print(f'年齢: {char.age}歳')
            print(f'所持金: {char.money}円')
            print('-'*20)
            while True:
                action = input('確認したらEnterキーを押してください。')
                if type(action) is str:
                    break
            return char

    @staticmethod
    def main():
        DB.create_table()  # テーブルがなければ作成
        char = Main.account_check()
        if char is not None:
            while True:
                choice = char.display()  # 予期せぬ値を受け取らないようにdisplay()で対応済
                if choice is None:
                    DB.updating_money(char.name, char.age, char.money, char.play)  # 遊技していたら所持金を更新
                    print('またのご来店をお待ちしております。')
                    break
                else:
                    ex = Main.func_dict[choice](char)  # 関数dictionaryから選択された関数を呼び出す
                    if ex == '*':
                        break
        else:
            print('またのご来店をお待ちしております。')


if __name__ == '__main__':
    Main.main()
