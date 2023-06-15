# -*- coding: utf-8 -*-

# PEP8 ガイドラインに準拠しているかのチェック
# https://pep8-ja.readthedocs.io/ja/latest/


# インポート -------------------------------------------------------
import os
import re
import pymel.core as pm
import maya.cmds as cmds
import pymel.core.datatypes as dt
from functools import partial
# -----------------------------------------------------------------

# テスト用のファイルパス
FILE_PATH = ''

# 追加したいファイル名
additional_file_name = "curve_info.txt"

# 追加したい相対パス 先頭に "/" をつけない
additional_path = "scenes/data/"


# 絶対パスを生成する関数
def create_absolute_data_file_path(additional_path, additional_file_name):
    # プロジェクトのパスを取得
    project_path = pm.workspace(q=True, rd=True)
    print("プロジェクトパス: ", project_path)

    # 追加の相対パスとファイル名を組み合わせて相対パスを作成
    relative_path = os.path.join(additional_path, additional_file_name)
    print("相対パス: ", relative_path)

    # 絶対パスを作成
    absolute_path = os.path.join(project_path, relative_path)
    print("絶対パス: ", absolute_path)

    return absolute_path


def get_open_windows():
    open_windows = []
    for window in pm.lsUI(type='window'):
        if pm.window(window, query=True, exists=True):
            open_windows.append(window)
    return open_windows


# 絶対パスを生成
absolute_path = create_absolute_data_file_path(
        additional_path,
        additional_file_name
    )

# 連想配列 宣言
data = {}


# カーブ情報を保存するクラス
class CurveData:
    # コンストラクタ
    def __init__(self, name, transform_str, cv_positions_str):
        # カーブ名
        self.name = name
        # カーブのトランスフォーム情報
        self.transform_str = transform_str
        # CV（コントロールバーテックス）の座標
        self.cv_positions_str = cv_positions_str

    # カーブ情報を追加する関数
    def add_curve_information(self, curve):
        # カーブのトランスフォーム情報を追加
        transform_matrix = curve.getMatrix()
        # Matrixデータ型に変換
        transform_str = str(transform_matrix)

        # CV（コントロールバーテックス）の座標を追加
        cv_positions = []
        # カーブのCVを取得
        for cv in curve.cv:
            # カーブのCVの座標を取得
            position = cv.getPosition(space='world')
            # カーブのCVの座標をリストに追加
            cv_positions.append(position)
        # カーブのCVの座標を文字列に変換
        cv_positions_str = str(cv_positions)

        # 既存の情報と結合
        self.transform_str += '\n' + transform_str
        self.cv_positions_str += '\n' + cv_positions_str

    def remove_curve_information(self, curve_name):
        # トランスフォーム情報とCVの座標を削除
        transform_lines = self.transform_str.split('\n')
        # カーブのCVの座標を文字列からリストに変換
        cv_positions_lines = self.cv_positions_str.split('\n')
        # 初期化
        index = -1
        # カーブのトランスフォーム情報とCVの座標を削除
        for i, line in enumerate(transform_lines):
            if line.strip() == curve_name:
                index = i
                break
        # カーブのトランスフォーム情報とCVの座標を削除
        if index >= 0:
            # 該当のデータの3行削除
            del transform_lines[index:index+3]
            del cv_positions_lines[index:index+3]

        # 削除後の情報を更新
        self.transform_str = '\n'.join(transform_lines)
        self.cv_positions_str = '\n'.join(cv_positions_lines)


class CurveManager:
    def __init__(self):
        self.curve_data_list = []

    def add_curve_information(self, curve):
        # CurveDataオブジェクトを作成してリストに追加
        name = curve.nodeName()
        # カーブのトランスフォーム情報を追加
        transform_matrix = curve.getMatrix()
        transform_str = str(transform_matrix)
        # CV（コントロールバーテックス）の座標を追加
        cv_positions = [cv.getPosition(space='world') for cv in curve.cv]
        cv_positions_str = str(cv_positions)
        # CurveDataオブジェクトを作成してリストに追加
        curve_data = CurveData(name, transform_str, cv_positions_str)
        # CurveDataオブジェクトをリストに追加
        self.curve_data_list.append(curve_data)

    # カーブ情報を削除する関数
    def remove_curve_information(self, curve_name):
        # CurveDataオブジェクトを削除
        for curve_data in self.curve_data_list:
            if curve_data.name == curve_name:
                self.curve_data_list.remove(curve_data)
                break

    # カーブ情報を保存する関数
    def save_to_file(self, save_path):
        # CurveDataリストを保存
        with open(save_path, 'w') as f:
            for curve_data in self.curve_data_list:
                f.write(curve_data.name + '\n')
                f.write(curve_data.transform_str + '\n')

                f.write(curve_data.cv_positions_str + '\n')
                f.write('---\n')

    # カーブ情報をファイルから読み込む関数
    def load_from_file(self, load_path):
        with open(load_path, 'r') as f:
            curve_data_list = []
            curve_data = None

            for line in f:
                line = line.strip()

                if line == '---':
                    if curve_data is not None:
                        curve_data_list.append(curve_data)
                    curve_data = None
                elif curve_data is None:
                    name = line
                    transform_str = f.readline().strip()
                    cv_positions_str = f.readline().strip()
                    curve_data = CurveData(
                        name,
                        transform_str,
                        cv_positions_str
                    )

            if curve_data is not None:
                curve_data_list.append(curve_data)

        self.curve_data_list = curve_data_list

    # カーブ情報を出力する関数
    def print_curve_information(self, curve_name=None):
        for curve_data in self.curve_data_list:
            if curve_name is None or curve_data.name == curve_name:
                print("Curve Name:", curve_data.name)
                print("Transform Information:")
                print(curve_data.transform_str)
                print("CV Positions:")
                print(curve_data.cv_positions_str)
                print("---")

    # カーブ情報を追加する関数
    def add_selected_curve_information(self):
        # 選択されたカーブを取得
        selected_curves = pm.ls(selection=True)
        print(selected_curves)

        for curve in selected_curves:
            self.add_curve_information(curve)

    # 名前からカーブ情報を取得する関数
    def get_curve_data_by_name(self, curve_name):
        for curve_data in self.curve_data_list:
            if curve_data.name == curve_name:
                return curve_data
        return None

    # 指定したファイルに新しいカーブの情報を追記する関数
    def append_selected_curve_information(self, file_path):
        # 選択されたカーブを取得
        selected_curves = pm.ls(selection=True)

        # ファイルを追記モードで開く
        with open(file_path, 'a') as f:
            for curve in selected_curves:
                # CurveDataオブジェクトを作成
                name = curve.nodeName()
                transform_matrix = curve.getMatrix()
                transform_str = str(transform_matrix)
                cv_positions = [
                    cv.getPosition(space='world') for cv in curve.cv
                ]
                cv_positions_str = str(cv_positions)
                curve_data = CurveData(name, transform_str, cv_positions_str)

                # CurveDataの情報をファイルに追記
                f.write(curve_data.name + '\n')
                f.write(curve_data.transform_str + '\n')
                f.write(curve_data.cv_positions_str + '\n')
                f.write('---\n')


# データファイル##################################################
def load_data(f_path):
    # ファイルの読み込み
    with open(f_path, 'r') as file:
        file_data = file.read()

    curves = re.split(r'---\n', file_data)
    # カーブ情報の読み込み
    for curve in curves:
        # カーブ情報を改行で分割
        curve_data = curve.split('\n')
        # カーブ情報が2つ以上ある場合
        if len(curve_data) >= 2:
            curve_name = curve_data[0]
            curve_info = curve_data[1]

            # カーブ情報の文字列をリストに変換
            curve_info = eval(curve_info)

            data[curve_name] = {
                "Name": curve_name,
                "Curve_Info": curve_info
            }


##################################################################
# 初期設定 ファイルロード
# カーブ情報の管理クラスのインスタンスを作成
curve_manager = CurveManager()

# 初期ファイルパス
FILE_PATH = absolute_path
load_data(FILE_PATH)
curve_manager.load_from_file(FILE_PATH)
print("データ保存パス: ", FILE_PATH)
##################################################################


# 連想配列 ボタン コールバック関数
def button_callback(asset_name, asset_data, *args):
    # ボタンが押されたときの処理
    # asset_name: ボタンの名前
    # asset_data: ボタンのデータ
    print("Clicked asset:", str(asset_name))
    print("Clicked data:", asset_data)

    # create_curve(asset_name, asset_data)
    print("カーブを生成しました。")

    # CurveDataを読み込み
    curve_manager.load_from_file(absolute_path)
    curve_data = curve_manager.get_curve_data_by_name(str(asset_name))

    if curve_data:
        # トランスフォーム情報を復元
        transform_matrix = eval(curve_data.transform_str)
        # Matrixデータ型に変換
        transform_matrix = dt.Matrix(transform_matrix)
        # CVの座標情報を復元
        cv_positions = eval(curve_data.cv_positions_str)

        # 最後のCVを最初に追加
        cv_positions.insert(0, cv_positions[-1])

        # 新しいカーブを生成（1次のCVカーブ）
        curve = pm.curve(d=1, p=cv_positions, n=str(asset_name))

        # トランスフォームを適用
        curve.setMatrix(transform_matrix, worldSpace=True)

        print("Created curve:", curve)
    else:
        print("Curve not found.")


# Assetウィンドウを作成する
# create_asset_window(data)
# dataの出力
# print(data)


# カーブ保存機能タブ
#  ボタン
#   ファイルの読み込み
#   ファイルの書き出し
#   カーブの保存
#   カーブの削除
#   カーブの出力
#   保存されているカーブのリスト
#    → GUIで一覧表示

# 自動セットアップ
#  ジョイントの名前によってジョイントの原点に指定されたカーブを生成する。
#  ブレンドノードの構築
#  コンストレイントの構築


# GUIベース クラス
class GUIProgram(object):
    def __init__(self):
        # "MyRigging_tool_2"のウィンドウを削除する
        open_windows = get_open_windows()
        if "MyRigging_tool_2" in open_windows:
            pm.deleteUI("MyRigging_tool_2")
        else:
            print("ウィンドウは存在しません。")

        self.window = cmds.window(
            "MyRigging_tool_2",
            title="MyRigging_tool_2",
            w=600, h=400
            # widthHeight=(600, 400)
        )

        # メニューバーの作成
        self.menu_bar = pm.menuBarLayout()

        # ファイルメニューの作成
        self.file_menu = pm.menu(label='File')
        pm.menuItem(label='Inport', command=self.button_curve_inport)
        pm.menuItem(label='Export', command=self.button_curve_export)
        pm.menuItem(divider=True)

        # タブレイアウトの作成
        self.tab_layout = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

        # エクスポートタブの作成
        self.curve_manage_tab = pm.columnLayout(adjustableColumn=True)
        '''
        pm.text(label="前処理", width=100, align='left')

        # レイアウトの作成 ロー
        self.layout = pm.rowLayout(numberOfColumns=2, width=400)

        # カーブの保存
        self.button1 = pm.button(
            label="中点にピボットポイントを移動",
            width=150, align='left',
            command=self.button_pivot
        )
        # カーブの出力
        self.button2 = pm.button(
            label="トランスフォームのフリーズ",
            width=150, align='left',
            command=self.button_trns_f
        )
        '''
        # タブレイアウトにペアレント
        pm.setParent(self.curve_manage_tab)

        pm.text(label="カーブ管理", width=100, align='left')

        # レイアウトの作成 ロー
        self.layout = pm.rowLayout(numberOfColumns=3, width=300)

        # カーブの保存
        self.button1 = pm.button(
            label="選択したカーブの追加",
            width=120, align='left',
            command=self.button_curve_add
        )
        # カーブの出力
        self.button2 = pm.button(
            label="カーブリスト",
            width=100, align='left',
            command=self.button_curve_list
        )
        pm.text(label="再読み込みをするにはプログラムを再実行してください", align='left')
        '''
        # カーブの再読み込み
        self.button2 = pm.button(
            label="再読み込み",
            width=100, align='left',
            command=self.button_curve_reload
        )
        '''

        # タブレイアウトにペアレント
        pm.setParent(self.curve_manage_tab)

        # asset_dict にデータを入れる
        asset_dict = data
        self.asset_dict = asset_dict
        print("asset_dict: ", asset_dict)
        
        '''
        # レイアウトの作成 ロー
        self.layout = pm.rowLayout(numberOfColumns=3, width=300)

        # 入力要素: テキストボックス
        self.input_textfield = pm.textFieldGrp(
            label="削除するカーブ名:",
            columnWidth=[50, 250]
        )
        # カーブの削除
        self.button2 = pm.button(
            label="削除",
            width=100, align='left',
            command=self.button_curve_delete
        )
        '''
        # タブレイアウトにペアレント
        pm.setParent(self.curve_manage_tab)

        # layoutの作成
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.text(label="カーブ リスト", width=70, align='left')

        # 連想配列　ボタン
        row_layout = None  # ロー（行）レイアウトの変数を初期化

        for index, (asset_name, asset_data) in enumerate(asset_dict.items()):
            if index % 4 == 0:
                # 新しいロー（行）レイアウトを作成
                row_layout = pm.rowLayout(
                    numberOfColumns=4, parent=self.layout)

            # ボタンの作成
            asset_button = pm.button(
                label=asset_name,
                command=partial(button_callback, asset_name, asset_data),
                annotation=asset_name,
                parent=row_layout,
                width=120
            )

        # タブレイアウトにペアレント
        pm.setParent(self.tab_layout)

        # セットアップタブの作成
        # self.setup_tab = pm.columnLayout(adjustableColumn=True)
        # pm.text(label="\nセットアップ", width=70, align='left')
        # セットアップのコントロールを追加する場合はここに記述

        # タブレイアウトにペアレント
        # pm.setParent(self.tab_layout)

        # タブの追加
        pm.tabLayout(
            self.tab_layout,
            edit=True,
            tabLabel=(
                (self.curve_manage_tab, "カーブライブラリ"),
                # (self.setup_tab, "セットアップ")
            )
        )

    # カーブファイル インポート
    def button_curve_inport(self, *args):
        print("カーブファイルをインポートします。")

    # カーブファイル エクスポート
    def button_curve_export(self, *args):
        print("カーブファイルをエクスポートします。")

    # 選択したカーブの追加
    def button_curve_add(self, *args):
        print("選択したカーブを追加します。")
        curve_manager.append_selected_curve_information(FILE_PATH)

    # カーブの生成
    def button_curve_list(self, *args):
        print("カーブリスト")
        curve_manager.print_curve_information()

    # 中点にピボットポイントを移動
    # def button_pivot(self, *args):
    #    print("中点にピボットポイントを移動")

    # トランスフォームのフリーズ
    # def button_trns_f(self, *args):
    #    print("トランスフォームのフリーズ")

    # カーブの再読み込
    '''
    def button_curve_reload(self, *args):
        print("カーブの再読み込み")
        if pm.window(self.window, exists=True):

            # 再起動
            curve_manager.load_from_file(absolute_path)
            load_data(absolute_path)
            print("データ保存パス: ", absolute_path)
            program = GUIProgram()
            program.run()
    '''

    # カーブの削除
    def button_curve_delete(self, *args):
        print("カーブを削除します。")
        # テキストフィールドからカーブ名を取得
        input_text = self.input_textfield.getText()
        # カーブ情報を削除
        print("入力値: {}".format(input_text))
        self.input_textfield.setText("")

    def run(self):
        # ウィンドウを表示
        #  self.window.show()  pm での書き方
        cmds.showWindow(self.window)


# GUIプログラムの実行
program = GUIProgram()
program.run()
