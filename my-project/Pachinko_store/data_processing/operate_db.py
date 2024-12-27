import datetime
import sqlite3


class WorkingWithDatabase:
    # 機種スペック情報
    hokuto_specs = ['CR北斗の拳', '1/349', '+300(80%) or +1500(20%)',
                    '確変:100%', '当:1/25 or 転落:1/180[回転数:いずれか引くまで]',
                    '+300(25%) or +1500(75%)', 'なし']
    eva_specs = ['CRエヴァンゲリオン', '1/319', '+450(75%) or +1500(25%)',
                 '確変:70%、チャンスタイム:30%', '当:1/90[回転数:170回]',
                 'ALL+1500', 'なし']
    madomagi_specs = ['CR魔法少女まどかマギカ', '1/199', '+450(90%) or +1500(10%)',
                      '確変:50%、通常:50%', '当:1/70[回転数:80回]、<上位>当:1/80[回転数:120回]',
                      'ALL+1500', '確率変動中の当たり1/4で確率変動<上位>に突入']
    insert_values_text = "?, ?, ?, ?, ?, ?, ?"
    models = [hokuto_specs, eva_specs, madomagi_specs]

# ========================== spec.db ==========================
    # spec(Model_Name, Probability_Normal, Payout_Normal, Mode_Allocation, Probability_Rush, Payout_Rush, Addition)
    # テーブルに値を挿入
    @staticmethod
    def _create_spec_db():
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            for model in WorkingWithDatabase.models:
                model = list(model)
                cursor.execute(f'INSERT INTO spec VALUES({WorkingWithDatabase.insert_values_text})', model)

    # テーブルチェック >>> 戻り値(None:空、True:既存データ、False:新規データ)
    @staticmethod
    def _check_for_spec_db(model):
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            try:
                itr = cursor.execute('SELECT * FROM spec')
            except sqlite3.OperationalError:
                create_table_text = """
                Model_Name TEXT, Probability_Normal TEXT, Payout_Normal TEXT, Mode_Allocation TEXT,
                Probability_Rush TEXT, Payout_Rush TEXT, Addition TEXT
                """
                cursor.execute(f'CREATE TABLE IF NOT EXISTS spec({create_table_text})')
            else:
                check = None
                for db_value in itr:
                    if model[0] == db_value[0]:
                        check = True
                        break
                    else:
                        check = False
                return check

    # spec.dbメイン
    @staticmethod
    def spec_db_main():
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            for model in WorkingWithDatabase.models:
                check = WorkingWithDatabase._check_for_spec_db(model)
                # 新規作成
                if check is None:
                    WorkingWithDatabase._create_spec_db()
                # 追加
                elif check is False:
                    model = list(model)
                    cursor.execute(f'INSERT INTO spec VALUES({WorkingWithDatabase.insert_values_text})', model)
            conn.commit()

    # スペック情報の取り出し　<<< Storeから実行(Userアクション)
    @staticmethod
    def show_spec_db():
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            try:
                models = cursor.execute('SELECT * FROM spec')
            except sqlite3.OperationalError as e:
                print(e)
            else:
                for model in models:
                    model = list(model)
                    print(f" ・{model[0]} ")
                    print(f'(大当たり確率):{model[1]},  (初当たり出玉割合):{model[2]},  (モード移行割合):{model[3]}')
                    print(f'(確変時大当たり確率):{model[4]},  (確変時出玉割合):{model[5]},  (補足):{model[6]}')
                    print()

# ========================== store.db TABLE(user, history)==========================
    @staticmethod
    def _create_store_db():
        create_table_user_text = 'Name TEXT, Age INT, Money INT'
        create_table_history_text = """
        Date TEXT, User_Name TEXT, User_Age INT, Model_Name TEXT, Income_and_Expenditure INT
        """
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS user({create_table_user_text})')
            cursor.execute(f'CREATE TABLE IF NOT EXISTS history({create_table_history_text})')
            conn.commit()

# ========= user(Name, Age, Money) =========
    # userテーブルの確認 >>> 戻り値(False:データなし、True:既存データ)
    @staticmethod
    def _check_for_user_table(name, age):
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            try:
                users = cursor.execute('SELECT * FROM user')
            except sqlite3.OperationalError as e:
                print(e)
            else:
                check = False
                for user in users:
                    if (name == user[0]) and (age == user[1]):
                        check = True
                    else:
                        continue
                return check

    # 所持金の入力 <<< 新規客に実行
    @staticmethod
    def _input_money(min_money=500):
        print('初めてのご来店ですね。所持金を半角英数字で入力してください。')
        while True:
            try:
                while True:
                    money = int(input('Money: '))
                    if money < min_money:
                        print(f'遊技には最低{min_money}円必要です。入力を変更してください。')
                    else:
                        break
            except ValueError:
                print('半角英数字で入力してください。(例:5000)')
            else:
                return money

    # ユーザーの所持金を取り出す <<< 既存客に実行
    @staticmethod
    def get_money(name, age):
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            itr = cursor.execute('SELECT Money FROM user WHERE (Name==(?)) and (Age==(?))', [name, age])
            for money, in itr:
                return money

    # userテーブルの確認 <<< Storeから実行(Masterアクション)
    @staticmethod
    def show_user_table_of_store_db():
        count = 1
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            users = cursor.execute('SELECT * FROM user')
            for user in users:
                name, age, money = user
                print(f'ユーザー({count})', end='')
                print(f'>>> (名前):{name}、(年齢):{age}、(所持金):{money}')
                count += 1

    # 退店前に所持金を更新 <<< Storeから実行(退店時)
    @staticmethod
    def update_user_table_money(name, age, money):
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user SET Money=(?) WHERE (Name==(?)) and (Age==(?))', [money, name, age])
            conn.commit()
        print('\nデータベースの所持金を更新しました。次回来店時に使用できます。')

    # userテーブルメイン <<< Storeから実行
    @staticmethod
    def user_table_of_store_db_main(name, age, min_money=500):
        WorkingWithDatabase._create_store_db()  # DBがなければ作成
        account_check = WorkingWithDatabase._check_for_user_table(name, age)  # 来店履歴があるか確認
        # データなし
        if account_check is False:
            money = WorkingWithDatabase._input_money()  # 所持金を入力
            with sqlite3.connect('store.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO user VALUES(?, ?, ?)', [name, age, money])
                conn.commit()
        # データあり
        else:
            money = WorkingWithDatabase.get_money(name, age)  # 前回退店時の所持金を取り出す
            print(f'来店履歴が確認できました。', end='')
            if money < min_money:
                print(f'前回の所持金は{money}円です。')
            else:
                print(f'前回の所持金{money}円が使用できます。')
        return money

# ========= history(Date, Name, Age, Model, Income_and_Expenditure) =========
    # 時刻取得
    @staticmethod
    def _get_datetime():
        date = datetime.datetime.now()
        date = f'{date.year}/{date.month}/{date.day}'
        return date

    # 遊戯履歴を保存 <<< Pachinkoから実行(収益計算時)
    @staticmethod
    def insert_history(name, age, model, amount):
        date = WorkingWithDatabase._get_datetime()
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO history VALUES(?, ?, ?, ?, ?)', [date, name, age, model, amount])
            conn.commit()

    # 遊技履歴を確認(master=True:全データ、False:自身のデータ) <<< Storeから実行
    @staticmethod
    def show_history_tabel_of_store_db(name=None, age=None, master=False):
        with sqlite3.connect('store.db') as conn:
            cursor = conn.cursor()
            if master is False:
                itr = cursor.execute('SELECT * FROM history WHERE (User_Name==(?)) and (User_Age==(?))', [name, age])
                print(f'--{name}({age})--')
                for history in itr:
                    date, name, age, model, amount = history
                    print(f'>>> (日付):{date}、(遊技台):{model}、(収支):{amount}')
            else:
                itr = cursor.execute('SELECT * FROM history')
                for history in itr:
                    date, name, age, model, amount = history
                    print(f'(日付):{date}、(名前):{name}、(年齢):{age}、(遊技台):{model}、(収支):{amount}')


if __name__ == '__main__':
    pass
    # WorkingWithDatabase.show_history_tabel_of_store_db('aki', 33)
    # WorkingWithDatabase.update_user_table_money('aki', 33, 10000, 1)
    # WorkingWithDatabase.show_user_table_of_store_db()
    # WorkingWithDatabase.show_history_tabel_of_store_db('aki', 33)
    # WorkingWithDatabase.insert_history('luffy', 19, 'CR北斗の拳', 100000)
    # WorkingWithDatabase.insert_history('aki', 33, 'CRエヴァンゲリオン', -60000)
    # WorkingWithDatabase.show_user_table_of_store_db()
    WorkingWithDatabase.spec_db_main()
    WorkingWithDatabase.show_spec_db()
