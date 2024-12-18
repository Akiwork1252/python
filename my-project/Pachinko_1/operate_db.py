import sqlite3


class DB:
    # 機種のスペックをデータベースに保存
    @staticmethod
    def create_spec_db():
        con = sqlite3.connect('spec.db')
        cursor = con.cursor()
        create_table_txt = '''Name TEXT, Probability_Normal TEXT, Payout_First TEXT, 
        Distribution_First TEXT, Probability_Rush TEXT, Distribution_Rush TEXT, 
        Continuation_Probability TEXT, Supplement TEXT'''
        cursor.execute(f'CREATE TABLE spec({create_table_txt})')
        values_hokuto = '''
        'CR北斗の拳', '1/349', '+300(80%) or +1500(20%)', 
        '確変:100%','当:1/25 or 転落:1/180[回転数:いずれか引くまで]', '+300(25%) or +1500(75%)', '88%', 'なし'
        '''
        values_eva = '''
        'CRエヴァンゲリオン', '1/319', '+450(75%) or +1500(25%)', 
        '確変:70%、チャンスタイム:30%','当:1/90[回転数:170回]', 'ALL+1500', '85%', 'なし'
        '''
        values_madomagi = '''
        'CR魔法少女まどかマギカ', '1/199', '+450(90%) or +1500(10%)', 
        '確変:50%、通常:50%', '当:1/70[回転数:80回]、<上位>当:1/80[回転数:120回]', 'ALL+1500', 
        '68% or 86%<上位>', '確率変動中の当たり1/4で確率変動<上位>に突入'
        '''
        cursor.execute(f'INSERT INTO spec VALUES({values_hokuto})')
        cursor.execute(f'INSERT INTO spec VALUES({values_eva})')
        cursor.execute(f'INSERT INTO spec VALUES({values_madomagi})')
        con.commit()

    # 機種スペックを取り出し表示
    @staticmethod
    def get_game_specs_from_db():
        con = sqlite3.connect('spec.db')
        cursor = con.cursor()
        itr = cursor.execute('SELECT * FROM spec')
        for row in itr:
            model, normal_p, payout_f, dist_f, rush_p, dist_r, conti_p, supp = row
            print(f'''
            --{model}--
            (通常時の大当り確率): {normal_p}, (初当たり出玉): {payout_f},
            (初当たり振り分け): {dist_f}, (確率変動時の大当り確率): {rush_p},
            (確率変動時の出玉振り分け): {dist_r}, (大当り継続率): {conti_p},
            (補足): {supp}
            ''')
        con.close()

    # テーブル作成(初回のみ）
    @staticmethod
    def create_table():
        # <pachinko.db>
        # userテーブル(名前、年齢、所持金)
        # historyテーブル(日付、名前、年齢、遊技台、収支(文字列のためsort不可))
        db_instruction = '''
        CREATE TABLE IF NOT EXISTS history(date CHAR(20), name CHAR(20), age INT, machine CHAR(20), income CHAR(10))
        '''
        con = sqlite3.connect('pachinko.db')
        cursor = con.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user(name CHAR(20), age INT, money INT)')
        cursor.execute(db_instruction)
        con.commit()

    # テーブル削除（プログラムの試行でデータが増えた時に使用）
    @staticmethod
    def del_table():
        con = sqlite3.connect('pachinko.db')
        cursor = con.cursor()
        cursor.execute('DROP TABLE user')
        cursor.execute('DROP TABLE history')
        con.commit()

    # 来店時　ユーザー情報を確認、履歴が無ければデータベースに作成
    @staticmethod
    def user_search_and_add(name, age):
        min_age = 20
        count = 0
        money = 0
        con = sqlite3.connect('pachinko.db')  # userTABLE(name, age, money)
        cursor = con.cursor()
        itr = cursor.execute('SELECT * FROM user WHERE (name=(?)) and (age=(?))', [name, age])
        for row in itr:
            name, age, money = row
            count += 1
        # WHEREでデータがヒットしない
        if count == 0:
            if age >= min_age:
                print('初めてのご来店ですね。所持金を入力してください。')
            else:
                pass
            while True:
                try:
                    money = int(input('所持金: '))
                    cursor.execute('INSERT INTO user VALUES(?, ?, ?)', [name, age, money])
                    con.commit()
                except ValueError:
                    print('半角英数字で入力してください。(例:5000)')
                else:
                    break
            return name, age, money
        else:
            if age < min_age:  # データはヒットしたが前回入店できていない
                print('来店できません。')
            else:
                while True:
                    user = input(f'来店履歴が確認できました。前回の所持金{money}円を使用して遊技ができます。Enterキーを押してください。')
                    if type(user) is str:
                        break
            return money

    # ユーザーの遊技履歴を表示する
    @staticmethod
    def check_history(name, age):
        count = 0
        con = sqlite3.connect('pachinko.db')
        cursor = con.cursor()
        itr = cursor.execute('SELECT * FROM history WHERE (name == (?)) and (age == (?))', [name, age])
        for user in itr:
            count += 1
            print(user)
        if count == 0:
            print('遊技履歴が存在しませんでした。')
        con.commit()

    # 遊技終了後のデータをテーブル(history)に追加する　history{日付、名前、年齢、遊技台、収支}
    @staticmethod
    def save_when_exit(date, name, age, machine, income):
        con = sqlite3.connect('pachinko.db')
        cursor = con.cursor()
        cursor.execute('INSERT INTO history VALUES(?, ?, ?, ?, ?)', [date, name, age, machine, income])
        con.commit()

    # 退店時にテーブル(user)の所持金を更新する user(名前、年齢、所持金)
    @staticmethod
    def updating_money(name, age, money, check):
        con = sqlite3.connect('pachinko.db')
        cursor = con.cursor()
        if check != 0:  # 遊技確認
            cursor.execute('UPDATE user SET money = (?) WHERE (name == (?)) and (age == (?))', [money, name, age])
            print('所持金の更新を行いました。次回来店時にご利用できます。')
            while True:
                action = input('Enterキーを押してください。')
                if type(action) is str:
                    break
        con.commit()

    # データベースの確認（管理者用）パスワード必要にする
    @staticmethod
    def check_db(n):  # 引数n:操作メニュー >>> 1:ユーザー情報、 2:遊技履歴
        con = sqlite3.connect('pachinko.db')
        cursor = con.cursor()
        instruction_1 = 'SELECT * FROM user'
        instruction_2 = 'SELECT * FROM history'
        count = 1
        if n == 1:
            itr = cursor.execute(instruction_1)  # user(名前、年齢、所持金)
            for row in itr:
                name, age, money = row
                print(f'ユーザー[{count}]', end=' ')
                print(f'>>> (名前){name}、(年齢){age}、(所持金){money}')
                count += 1
        elif n == 2:
            itr = cursor.execute(instruction_2)  # history{日付、名前、年齢、遊技台、収支}
            for row in itr:
                date, name, age, model, income = row
                print(f'(日付){date}、(名前){name}、(年齢){age}、(遊技台){model}、(収支){income}')
        else:
            print('入力が正しくありません。')
        con.close()


# con = sqlite3.connect('spec.db')
# cursor = con.cursor()
# DB.create_spec_db()
# con.commit()
# # DB.get_game_specs_from_db()
# con.close()
