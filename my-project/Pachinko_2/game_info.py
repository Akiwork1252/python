import csv
import datetime
import re
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd


# 遊戯台の出玉推移グラフの作成、表示
# csvファイル作成 > 遊戯データ(回転数、出玉)を保存 > データフレイム作成 > グラフ作成、保存(png) > 表示
class GameData:
    model_name_h = 'CR北斗の拳'
    model_name_e = 'CRエヴァンゲリオン'
    model_name_m = 'CR魔法少女まどかマギカ'

    # =============================== 遊戯データの保存 ===============================
    # csvファイルをカレントディレクトリに作成 <<< Accountから実行(来店時) ※台移動の時を検討する
    # カラム(rotations:回転数、 balls:出玉)
    @staticmethod
    def create_csv():
        with open('game_data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['rotations', 'balls'])

    # 遊戯データの収集 <<< Pachinkoから実行(大当り時)、PlayGamesから実行(遊戯前,初当たり時,確変終了時、遊戯終了時)
    @staticmethod
    def add_data(roll, ball):
        with open('game_data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([roll, ball])

    # データフレイムに変換
    @staticmethod
    def _create_df():
        try:
            game_df = pd.read_csv('game_data.csv')
        except FileNotFoundError as e:
            print(e)
        else:
            return game_df

    # =============================== ファイル名、グラフタイトルの作成 ===============================
    # ファイル名 >>> {name(3文字) or 'anonymous'}_{date(0000)}_{model_initial}.png
    # グラフ名 >>> {model}(user:{user}、 date:{date(0000/00/00)})

    # ユーザー名がアルファベットか判定して、ファイル名用の文字列に変換(アルファベット>>>頭３文字使用、以外>>>'anonymous'を使用)
    @staticmethod
    def _check_username(name):
        pattern = '^([A-Z]|[a-z]){3}'
        pattern = re.compile(pattern)
        res = pattern.search(name)
        if res is not None:
            return name[:3]
        else:
            return 'anonymous'

    # 遊戯日を取得(ファイル名用、グラフタイトル用)
    @staticmethod
    def _get_date():
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        file_name_date = f'{month}{day}'  # ファイル名
        graph_title_date = f'{year}/{month}/{day}'  # グラフタイトル
        return file_name_date, graph_title_date

    # 遊戯モデルを取得してイニシャルに変換
    @staticmethod
    def _get_model_initial(model_name, initial=''):
        if model_name == GameData.model_name_h:
            initial = 'h'
        elif model_name == GameData.model_name_e:
            initial = 'e'
        elif model_name == GameData.model_name_m:
            initial = 'm'
        else:
            print('入力が正しくありません。')
        return initial

    # ファイル名を作成
    @staticmethod
    def _create_filename(name, date, model, extension='png'):
        file_name = f'{name}_{date}_{model}.{extension}'
        return file_name

    # グラフのタイトル名を作成
    @staticmethod
    def _create_graph_title(model, name, date):
        graph_title = f'{model}(User: {name}、date: {date})'
        return graph_title

    # =============================== グラフ作成、表示 ===============================
    @staticmethod
    def _create_and_view_graph(dataframe, graph_title, file_name):
        x_txt = 'rotations'
        y_txt = 'balls'
        x = dataframe[x_txt]
        y = dataframe[y_txt]
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', markersize=3, markerfacecolor='r')
        ax.set_title(graph_title)
        ax.set_xlabel(x_txt)
        ax.set_ylabel(y_txt)
        fig.savefig(f'{file_name}')
        while True:
            action = input('Enterキーを押すとグラフが表示されます。')
            if type(action) is str:
                break
        plt.show()
        plt.close(fig)

    # 遊戯データからグラフを作成して表示 <<< Pachinkoから実行(収支提示時)
    @staticmethod
    def information(user_name, model):
        game_df = GameData._create_df()  # 遊戯データ(csv)からデータフレイムを作成
        name = GameData._check_username(user_name)  # ユーザー名取得(ファイル名) 英字３文字orアノニマス
        file_name_data, graph_title_data = GameData._get_date()  # 日付取得(ファイル名、グラフタイトル)
        model_initial = GameData._get_model_initial(model)  # 遊戯台のイニシャル取得
        file_name = GameData._create_filename(name, file_name_data, model_initial)  # 出玉推移グラフを保存するためのファイル名作成
        graph_title = GameData._create_graph_title(model, user_name, graph_title_data)  # グラフタイトル作成
        GameData._create_and_view_graph(game_df, graph_title, file_name)


if __name__ in '__main__':
    GameData.create_csv()
    GameData.add_data(0, 0)
    GameData.add_data(135, -5000)
    GameData.add_data(250, -3000)
    GameData.add_data(420, 1000)
    GameData.add_data(520, 2500)
    GameData.information('akinori', GameData.model_name_h)



