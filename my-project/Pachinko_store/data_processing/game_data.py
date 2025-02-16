import csv
import datetime
import re
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
from Pachinko_store.store.store import Store


class GameData:
    model_name_h = 'CR北斗の拳'
    model_name_e = 'CRエヴァンゲリオン'
    model_name_m = 'CR魔法少女まどかマギカ'

# =========== データ作成 ============
    # csvファイル作成 <<< Storeから実行(アカウント作成時)
    @staticmethod
    def create_csvfile():
        with open('game_data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Num_of_Rotations', 'Num_of_balls'])

    # 遊戯データの保存  <<< Pachinkoから実行(遊戯前, 初当たり時, 大当り時, 確変終了時、遊戯終了時)
    @staticmethod
    def add_data(rotations, balls):
        with open('game_data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([rotations, balls])

    # DataFrame作成
    @staticmethod
    def _create_df():
        df = pd.read_csv('game_data.csv')
        return df

# =========== データ表示の準備 ============
    # グラフファイル名作成　{ユーザー名:3文字}_{日付:4文字}_{遊技台:1文字}.png
    # ユーザー名が英字３文字か判定 英字でなければ"anonymous"を使用
    @staticmethod
    def _validate_user_name_format(username):
        pattern = '^([A-Z]|[a-z]){3}'
        pattern = re.compile(pattern)
        res = pattern.search(username)
        if res is not None:
            return username[:3]
        else:
            return 'anonymous'

    # 日付を取得(ファイル名用、グラフタイトル用)
    @staticmethod
    def _get_datetime():
        date = datetime.datetime.now()
        date_for_file = f'{date.month}{date.day}'
        date_for_graph = f'{date.year}/{date.month}/{date.day}'
        return date_for_file, date_for_graph

    # 遊技モデルをイニシャルに変換
    @staticmethod
    def _get_model_initial(model, initial=''):
        if model == GameData.model_name_h:
            initial = 'h'
        elif model == GameData.model_name_e:
            initial = 'e'
        elif model == GameData.model_name_m:
            initial = 'm'
        return initial

    # ファイル名を作成
    @staticmethod
    def _create_filename(username, date, model, extension='png'):
        file_name = f'{username}_{date}_{model}.{extension}'
        return file_name

    # グラフのタイトル名を作成
    @staticmethod
    def _create_graph_title(model, username, date):
        graph_title = f'{model}(遊技者:{username}, 遊技日: {date})'
        return graph_title

# =========== データ表示 ============
    @staticmethod
    def _show_graph(df, file_name, graph_title):
        x_col = 'Num_of_Rotations'
        y_col = 'Num_of_balls'
        x = df[x_col]
        y = df[y_col]
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', markersize=3, markerfacecolor='r')
        ax.set_xlim(0, 2000)
        ax.set_ylim(-30000, 30000)
        ax.set_title(graph_title)
        ax.set_xlabel('回転数')
        ax.set_ylabel('出玉')
        fig.savefig(f'{file_name}')
        print('Enterキーを押すと出玉推移グラフが表示されます。確認したら閉じてください。。', end='')
        Store.input_enter()
        plt.show()
        plt.close(fig)

# =========== ゲームデータメイン ============
    # 出玉推移グラフの表示、保存 <<< Pachinkoから実行(収益計算後)
    @staticmethod
    def show_game_data(username, model):
        game_df = GameData._create_df()  # csvファイルをDataFrameに変換
        username_for_file = GameData._validate_user_name_format(username)  # pngファイル用のユーザー名を取得
        date_for_file, date_for_graph = GameData._get_datetime()  # pngファイル名、グラフタイトル用の日付を取得
        model_initial = GameData._get_model_initial(model)  # pngファイル名用の遊技台イニシャルを取得
        file_name = GameData._create_filename(username_for_file, date_for_file, model_initial)  # pngファイル名作成
        graph_title = GameData._create_graph_title(model, username, date_for_graph)  # グラフタイトル作成
        GameData._show_graph(game_df, file_name, graph_title)  # グラフ表示、pngファイル保存


if __name__ == '__main__':
    name = GameData._validate_user_name_format('akinori')
    print(name)
    # GameData.create_csvfile()
    # GameData.add_data(125, -5000)
    # GameData.add_data(155, -2500)
    # GameData.add_data(180, -500)
    # GameData.add_data(225, 1000)
    # GameData.add_data(245, 2500)
    # GameData.add_data(325, 7000)
    # GameData.show_game_data('aki', GameData.model_name_h)
