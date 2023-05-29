#https://www.youtube.com/watch?v=rhtLC5kKoBI
#https://tech-art.online/maya-python14/
#https://hexadrive.jp/hexablog/program/29864/

#import myrigingtool
#import importlib
#importlib.reload(myrigingtool)
##reload(widget)
#widget = myrigingtool.main()
#widget.show()

import os 
from maya import cmds 
import pymel.core as pm
import math

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QLineEdit
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

# 現在のファイルパスを取得
CURRENT_FILE = os.path.normpath(__file__)
# ファイルパスと拡張子を分ける
path, ext = os.path.splitext(CURRENT_FILE)
# UIファイルのパスを設定
UI_FILE = path + ".ui"

# MyRigging_toolsクラスを定義し、MayaQWidgetBaseMixinとQtWidgets.QMainWindowを継承
class main(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    # コンストラクタ
    def __init__(self, *args, **kwargs):
        # 親クラスのコンストラクタを呼び出す
        super(main, self).__init__(*args,**kwargs)

        # UIファイルをロードしてウィジェットを取得し、ウィンドウに設定
        self.widget = QUiLoader().load(UI_FILE)
        self.setCentralWidget(self.widget)
        # ウィジェットのウィンドウタイトルを設定
        self.setWindowTitle(self.widget.windowTitle())

        # ボタンがクリックされた時のイベントを設定
        #self.widget.pB_Create_Curve_2.clicked.connect(self.buttonClicked)
        

    # Translate属性を接続する関数
    def clicked_connect_translate(self):
        # 選択中のオブジェクトを取得
        src ,dst= cmds.ls(os=True)
        # Translate属性を接続
        cmds.connectAttr("{}.translate".format(src),"{}.translate".format(dst))

    # デバック用 # ボタンがクリックされた時に呼び出される関数 
    def buttonClicked(self):
        lineEdit = self.findChild(QLineEdit, "lineEditNumber")
        number = float(lineEdit.text())

        # コンソールにメッセージを表示
        print(number)
        print("Button clicked!")
    
    def generate_curve_1(self):
        try:
            # Qtのラインエディットウィジェットから入力値を取得する
            lineEdit = self.findChild(QLineEdit, "lEN_generate_curve_1")
            # 入力値をint型に変換する
            n = int(lineEdit.text())
        except ValueError:
            # 入力値が数値ではない場合には警告を表示して処理を終了する
            pm.warning('Please enter a valid integer.')
            return
        
        if n < 3:
            # 頂点の数が3未満の場合には警告を表示して処理を終了する
            pm.warning("Invalid input: The number of vertices should be greater than or equal to 3")
            return
        
        # N角形の頂点の座標を計算する
        points = []
        for i in range(n):
            x = math.cos(i * 2 * math.pi / n)
            y = math.sin(i * 2 * math.pi / n)
            z = 0
            points.append([x, z, y])
        # 最後の頂点と最初の頂点が同じ座標を持つようにする
        points.append(points[0])
        # 頂点座標からカーブを作成する
        curve = pm.curve(name="npolygonCurve", p=points, d=1)
        # カーブを選択する
        pm.select(curve)

        # コンソールにメッセージを表示する
        print('Curve created.')

    #def generate_curve_2(self):