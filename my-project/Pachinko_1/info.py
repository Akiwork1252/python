import csv
import datetime
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import re
import seaborn as sns
import pandas as pd


# 遊技台の出玉推移グラフの作成と表示(csvファイル作成、DataFrame作成、グラフ作成、表示、pngファイルで保存)
class InformationDisplay:
    # 出玉推移グラフ作成のためのcsvファイル作成 >>> カラム(num_of_rotations:回転数、balls:出玉)
    # csvファイルは使い回す。
    @staticmethod
    def create_csvfile():
        with open('game_data.csv', mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['num_of_rotations', 'balls'])

    # csvファイルに遊技データを追加
    # (記録タイミング >>> 初打ち(回転数０,玉０)、遊技玉が無くなった時、初当たり時、大当り毎、確率変動終了後、遊技終了後)
    @staticmethod
    def add_data_to_csvfile(count, balls):  # count:回転数、balls:玉数
        with open('game_data.csv', mode='a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([count, balls])

    # csvファイルからデータフレイム作成
    @staticmethod
    def create_dataframe():
        df = pd.read_csv('game_data.csv')
        return df

    # 遊技日を取得し、月と日にちを返す(ファイル名とグラフのタイトルに使用)
    @staticmethod
    def date():
        today = datetime.datetime.now()
        return today.month, today.day

    # ユーザーの名前が英字か調べる。
    # 英字であれば最初３文字を遊技データのファイル名に使用。英字でなければをanonymousを使用。
    @staticmethod
    def name_judge(username):
        pt = '^([A-Z]|[a-z]){3}'
        pattern = re.compile(pt)
        res = pattern.search(username)
        if res is not None:
            return username[:3]
        else:
            return 'anonymous'

    # 遊技台のイニシャルを返す（ファイル名に使用）
    @staticmethod
    def convert_to_initials(model):
        model_initial = None
        if model == 'CR北斗の拳':
            model_initial = 'h'
        elif model == 'CRエヴァンゲリオン':
            model_initial = 'e'
        elif model == 'CR魔法少女まどかマギカ':
            model_initial = 'm'
        return model_initial

    # ユーザー名、日付、遊技台のイニシャルを使用してファイル名を作成
    @staticmethod
    def make_filename(username, month, day, model):
        date_in_filename = f'{month}{day}'
        file_name = f'{username}_{date_in_filename}_{model}.png'
        return file_name

    # 遊技台とユーザー名と日付を受け取り、タイトル用の文字列を作成
    @staticmethod
    def make_title_name(machine, username, month, day):
        graph_title = f'{machine}(user:{username},  date:{month}/{day})'
        return graph_title

    # グラフ作成、表示、グラフの保存(png)
    @staticmethod
    def view_graph(df, title, filename):  # title:遊技台
        # カラム指定
        col_nums = 'num_of_rotations'
        col_balls = 'balls'
        x = df[col_nums]
        y = df[col_balls]
        # グラフの表示
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', markersize=3, markerfacecolor='r')
        ax.set_title(title)
        ax.set_xlabel('回転数')
        ax.set_ylabel('玉数')
        # グラフを保存
        fig.savefig(f'{filename}')
        while True:
            action = input('Enterキーを押すとグラフが表示されます。')
            if type(action) is str:
                break
        plt.show()
        plt.close(fig)

    # 統計データ計算、表示
    @staticmethod
    def statistics():
        pass


if __name__ == '__main__':
    # with open('game_data/game_data.csv', 'r', encoding='utf-8') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)

    df = InformationDisplay.create_dataframe()
    x = df['num_of_rotations']
    y = df['balls']
    plt.plot(x, y, marker='o', markersize=3, markerfacecolor='r')
    plt.show()
