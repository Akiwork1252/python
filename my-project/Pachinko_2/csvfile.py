import csv
import datetime
import re
import matplotlib.pyplot as plt
import pandas as pd


# 遊戯台の出玉推移グラフの作成、表示
# csvファイル作成 > 遊戯データ(回転数、出玉)を保存 > データフレイム作成 > グラフ作成、保存(png) > 表示
class Information:
    model_hokuto = 'CR北斗の拳'
    model_eva = 'CRエヴァンゲリオン'
    model_madokamagika = 'CR魔法少女まどかマギカ'

    # =============================== 遊戯データの作成 ===============================
    # csvファイルをカレントディレクトリに作成(rotations:回転数、 balls:出玉)
    @staticmethod
    def create_csv():
        with open('game_data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['rotations', 'balls'])

    # 遊戯データをcsvファイルに保存
    # 保存タイミング >>> 遊戯前(回転数0、玉0)、持ち玉消化時、初当たり時、当たり、確変終了後、遊戯終了時)
    @staticmethod
    def add_data(roll, ball):
        with open('game_data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([roll, ball])

    # データフレイムに変換
    @staticmethod
    def create_df():
        try:
            df = pd.read_csv('game_data.csv')
        except FileNotFoundError as e:
            print(e)
        else:
            return df

    # =============================== ファイル名、グラフタイトルの作成 ===============================
    # ファイル名 >>> {name(3文字) or 'anonymous'}_{date(0000)}_{model_initial}.png
    # グラフ名 >>> {model}(user:{user}、 date:{date(0000/00/00)})

    # ユーザー名がアルファベットか判定して、ファイル名用の文字列に変換(アルファベット>>>頭３文字使用、以外>>>'anonymous'を使用)
    @staticmethod
    def check_username(name):
        pattern = '^([A-Z]|[a-z]){3}'
        pattern = re.compile(pattern)
        res = pattern.search(name)
        if res is not None:
            return name[:3]
        else:
            return 'anonymous'

    # 遊戯日を取得(ファイルネーム用、グラフ提示用)
    @staticmethod
    def get_date(str_):
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        if str_ == 'file':
            f_date = f'{month}{day}'
            return f_date
        elif str_ == 'graph':
            g_date = f'{year}/{month}/{day}'
            return g_date
        else:
            print('入力が正しくありません。')

    # 遊戯モデルを取得してイニシャルに変換
    @staticmethod
    def convert_name_to_initials(model_name, initial=''):
        if model_name == Information.model_hokuto:
            initial = 'h'
        elif model_name == Information.model_eva:
            initial = 'e'
        elif model_name == Information.model_madokamagika:
            initial = 'm'
        else:
            print('入力が正しくありません。')
        return initial

    # ファイル名を作成
    @staticmethod
    def create_filename(name, date, model, extension='png'):
        file_name = f'{name}_{date}_{model}.{extension}'
        return file_name

    # グラフのタイトル名を作成
    @staticmethod
    def create_graphtitle(model, name, date):
        graph_title = f'{model}(User: {name}、date: {date})'
        return graph_title

    # =============================== グラフ作成、表示 ===============================
    @staticmethod
    def create_and_view_graph(dataframe, graph_title, file_name):
        x_txt = 'rotations'
        y_txt = 'balls'
        x = dataframe[x_txt]
        y = dataframe[y_txt]
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', markersize=3, markerfacecolor='r')
        ax.set_title(graph_title)
        ax.set_xlabel(x_txt)
        ax.set_ylabel(y_txt)
        plt.show()


if __name__ in '__main__':
    # Information.create_csv()
    # Information.add_data(100, 10)
    # Information.create_df()
    # f = Information.check_username('ローレン')
    # print(f)
    # f = Information.get_date('graph')
    # print(f)
    # i = Information.convert_name_to_initials('CR北斗の拳')
    # print(i)
    Information.create_csv()
    Information.add_data(0, 0)
    Information.add_data(400, -3500)
    Information.add_data(420, -2000)
    Information.add_data(450, 500)
    Information.add_data(700, 2500)
    df = Information.create_df()
    print(df)


