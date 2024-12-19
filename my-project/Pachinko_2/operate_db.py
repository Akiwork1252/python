import logging
import sqlite3
import datetime
import textwrap


# データベース作成、操作
class DataBase:
    # ロギングの設定
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')  # オプション: 日付フォーマット

    # ======================================  spec.db(機種情報)  ======================================
    # 遊戯データ [機種名、通常時当たり確率、初当たり出玉、初当たり振り分け、確変時振り分け、確変時出玉、大当り継続率、補足」
    values_hokuto = ['CR北斗の拳', '1/349', '+300(80%) or +1500(20%)',
                     '確変:100%', '当:1/25 or 転落:1/180[回転数:いずれか引くまで]',
                     '+300(25%) or +1500(75%)', '88%', 'なし']
    values_eva = ['CRエヴァンゲリオン', '1/319', '+450(75%) or +1500(25%)',
                  '確変:70%、チャンスタイム:30%', '当:1/90[回転数:170回]',
                  'ALL+1500', '85%', 'なし']
    values_madokamagika = ['CR魔法少女まどかマギカ', '1/199', '+450(90%) or +1500(10%)',
                           '確変:50%、通常:50%', '当:1/70[回転数:80回]、<上位>当:1/80[回転数:120回]',
                           'ALL+1500', '68% or 86%<上位>', '確率変動中の当たり1/4で確率変動<上位>に突入']
    # 遊戯台リスト
    model_list = [values_hokuto, values_eva, values_madokamagika]

    # 遊戯データがデータベースに存在するか確認
    @staticmethod
    def _check_spec_db(model):
        count = 0
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            try:
                itr = cursor.execute('SELECT * FROM spec')
            except sqlite3.OperationalError as e:
                # テーブル作成
                create_table_txt = '''
                Name TEXT, Probability_Normal TEXT, Payout_First TEXT, 
                Distribution_First TEXT, Probability_Rush TEXT, Distribution_Rush TEXT, 
                Continuation_Probability TEXT, Supplement TEXT
                '''
                cursor.execute(f'CREATE TABLE IF NOT EXISTS spec({create_table_txt})')
            else:
                check = False
                for db_data in itr:
                    count += 1
                    if model[0] != db_data[0]:
                        check = True
                    else:
                        continue
                if count != 0:
                    return check
                else:
                    return None

    # データベース(spec.db)新規作成
    # spec(Name, Probability_Normal, Payout_First, Distribution_First,
    #      Probability_Rush, Distribution_Rush, Continuation_Probability, Supplement)
    @staticmethod
    def _create_spec_db_first():
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            for model in DataBase.model_list:
                model, p_n, p_f, d_f, p_r, d_r, c_p, s = model
                cursor.execute(f'INSERT INTO spec VALUES(?, ?, ?, ?, ?, ?, ?, ?)', [model, p_n, p_f, d_f, p_r, d_r, c_p, s])
            conn.commit()

    # データベース:spec.db(機種スペックデータ)作成 <<< Mainから実行(来店時)
    @staticmethod
    def check_and_add_spec_db():
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            for model in DataBase.model_list:
                check = DataBase._check_spec_db(model)  # データベースを確認
                # データベース(specテーブル)が空
                if check is None:
                    DataBase._create_spec_db_first()
                # データベース(specテーブル)に(model)の情報がない
                elif check is False:
                    model, p_n, p_f, d_f, p_r, d_r, c_p, s = model
                    cursor.execute(f'INSERT INTO spec VALUES(?, ?, ?, ?, ?, ?, ?, ?)', [model, p_n, p_f, d_f, p_r, d_r, c_p, s])
                # 既存データ
                else:
                    continue
            conn.commit()

    # 機種のスペック情報を表示 <<< Storeから実行(ユーザー選択時)
    @staticmethod
    def show_spec_db():
        with sqlite3.connect('spec.db') as conn:
            cursor = conn.cursor()
            try:
                itr = cursor.execute('SELECT * FROM spec')
            except sqlite3.OperationalError:
                print('テーブルが存在しません。')
            else:
                for model in itr:
                    model, normal_p, payout_f, dist_f, rush_p, dist_r, conti_p, supp = model
                    print(textwrap.dedent(f'''
                    --{model}--
                    (通常時の大当り確率): {normal_p}, (初当たり出玉): {payout_f},
                    (初当たり振り分け): {dist_f}, (確率変動時の大当り確率): {rush_p},
                    (確率変動時の出玉振り分け): {dist_r}, (大当り継続率): {conti_p},
                    (補足): {supp}
                    '''))

    # ======================================  pachinko.db(ユーザー情報)  ======================================
    # データベース:pachinko.db(顧客情報、遊戯履歴)作成 <<< Mainから実行(来店時)
    # user(Name, Age, Money), history(Data, Name, Age, Model, Income)
    @staticmethod
    def create_pachinko_db():
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user(
            Name TEXT NOT NULL,
            Age INTEGER,
            Money INTEGER
            )''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS history(
            Date TEXT NOT NULL,
            Name TEXT,
            Age INTEGER,
            Model TEXT,
            Income INTEGER
            )''')
            conn.commit()

    # アカウント確認 <<< Accountから実行(来店時)
    @staticmethod
    def account_check(name, age):
        count = 0
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            itr = cursor.execute('SELECT * FROM user WHERE (name==(?)) and (age==(?))', [name, age])
            for user in itr:
                name, age, money = user
                count += 1
        if count == 0:
            return None
        else:
            return money

    # 新規客の情報をuserテーブルに追加する <<< Accountから実行(来店時)
    @staticmethod
    def add_account_to_db(name, age, money):
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user VALUES(?, ?, ?)', [name, age, money])
            conn.commit()

    # 所持金を取得 <<< Pachinkoから実行(収益計算時)
    @staticmethod
    def get_money_when_entry(name, age):
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            itr = cursor.execute('SELECT money FROM user WHERE (name==(?)) and (age==(?))', [name, age])
            for user_money, in itr:  # アンパック
                return user_money

    # 自身の遊戯履歴を表示する <<< Storeから実行(ユーザー選択時)
    @staticmethod
    def show_history(name, age):  # 引数(name==self.name)でなければ観覧できないようにする
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            itr = cursor.execute('SELECT * FROM history WHERE (name==(?)) and (age==(?))', [name, age])
            for idx, history in enumerate(itr):
                data, name, age, model, income = history
                if idx == 0:
                    print(f'＜{name}({age})の遊戯履歴＞')
                print(f'{idx+1} >>>', end='')
                print(f'\t(日付){data}, (遊戯台){model}, (収支){income}')
            print('>>> End')

    # 現在時刻を取得
    @staticmethod
    def _get_date():
        date = datetime.datetime.now()
        date = f'{date.year}/{date.month}/{date.day}'
        return date

    # 遊戯データをhistoryテーブルに保存 <<< Pachinkoから実行(収益計算後)
    @staticmethod
    def save_data_to_history_table(name, age, model, income):
        date = DataBase._get_date()
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO history VALUES(?, ?, ?, ?, ?)', [date, name, age, model, income])
            conn.commit()

    # userテーブルの所持金を更新 <<< Storeから実行(退店時)
    @staticmethod
    def update_user_table(name, age, money, playing_check):  # playing_check >>> 遊戯確認(一度でも玉を発射するとカウント)
        if playing_check != 0:
            with sqlite3.connect('pachinko.db') as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE user SET money=(?) WHERE (name==(?)) and (age==(?))', [money, name, age])
                conn.commit()
        else:
            pass

    # ======================================  メニュー画面から操作  ======================================
    # userテーブル(name, age, money)の情報を表示
    @staticmethod
    def _master_show_user(itr):
        count = 1
        print('ユーザー情報を表示します。')
        print('='*20)
        for user in itr:
            name, age, money = user
            print(f'ユーザー[{count}]', end=' ')
            print(f'>>> (名前){name}、(年齢){age}、(所持金){money}')
            count += 1
        print('='*20)

    # historyテーブル(date, name, age, model, income)の情報を表示
    @staticmethod
    def _master_show_history(itr):
        print('顧客の遊戯履歴を確認します。')
        print('='*20)
        for history in itr:
            date, name, age, model, income = history
            print(f'(日付){date}、(名前){name}、(年齢){age}、(遊技台){model}、(収支){income}')
        print('='*20)

    # 管理人のデータベース確認 <<< Storeから実行(管理人選択時)
    @staticmethod
    def master_only_check_pachinko_db(num):  # num(int) >>> 1:ユーザー情報確認、2:history:遊戯履歴確認
        instruction_dict = {
            1: 'SELECT * FROM user',
            2: 'SELECT * FROM history',
        }
        with sqlite3.connect('pachinko.db') as conn:
            cursor = conn.cursor()
            if num in instruction_dict:
                instruction = instruction_dict[num]
                itr = cursor.execute(instruction)
                if num == 1:
                    DataBase._master_show_user(itr)
                elif num == 2:
                    DataBase._master_show_history(itr)
            else:
                print('入力が正しくありません。')


if __name__ == '__main__':
    DataBase.get_money_when_entry('aki', 33)
    # ---spec.db---
    # 新規作成
    #DataBase.create_spec_db_first()
    # チェック
    # check_h = DataBase.check_spec_db(DataBase.values_hokuto)
    # check_e = DataBase.check_spec_db(DataBase.values_eva)
    # check_m = DataBase.check_spec_db(DataBase.values_madokamagika)
    # print(check_h, check_e, check_m)
    # 確認、追加
    # DataBase.check_and_add_spec_db()

    # ---pachinko.db---
    # DataBase.save_data_to_history_table('aki', 33, 'CR北斗の拳', -17500)
    # DataBase.show_history('aki', 33)

    # ---管理人操作---
    # DataBase.check_pachinko_db(2)