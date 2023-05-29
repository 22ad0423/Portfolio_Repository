import pymel.core as pm
from functools import partial
from maya import utils

JNT_name_dic = {
    'head': 'head_JNT',
    'neck': 'neck_JNT',
    'chest ': 'chest_JNT',
    'spine': 'spine_JNT',
    'hips': 'hips_JNT',
    'root': 'root_JNT',
    'Shoulder': 'Shoulder_JNT',
    'Upper_Arm': 'Upper_Arm_JNT',
    'Lower_Arm': 'Lower_Arm_JNT',
    'Hand': 'Hand_JNT',
    'thumb_proximal': 'thumb_proximal_JNT',
    'thumb_intermediate': 'thumb_intermediate_JNT',
    'thumb_distal': 'thumb_distal_JNT',
    'index_proximal': 'index_proximal_JNT',
    'index_intermediate': 'index_intermediate_JNT',
    'index_distal': 'index_distal_JNT',
    'middle_proximal': 'middle_proximal_JNT',
    'middle_intermediate': 'middle_intermediate_JNT',
    'middle_distal': 'middle_distal_JNT',
    'ring_proximal': 'ring_proximal_JNT',
    'ring_intermediate': 'ring_intermediate_JNT',
    'ring_distal': 'ring_distal_JNT',
    'littele_proximal': 'littele_proximal_JNT',
    'littele_intermediate': 'littele_intermediate_JNT',
    'littele_distal': 'littele_distal_JNT',
    'upper_leg': 'upper_leg_JNT',
    'lower_leg': 'lower_leg_JNT',
    'foot': 'foot_JNT',
    'toes': 'toes_JNT'
}

def get_value_from_dict(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None

def button1_command(*args):
    print("Button 1 clicked!")

def rename_func(name):
    # 選択したオブジェクトを取得
    selection = pm.selected()
    
    if selection:
        for obj in selection:
            # オブジェクトの名前を変更
            obj.rename(name)
            print("Name changed to '"+ name +"':", obj)
    else:
        print("Please select an object.")

def button_action(button_name):
    # ボタンごとの処理を実行するコードを記述する
    switcher = {
        'Button1': lambda: rename_func(get_value_from_dict(JNT_name_dic, "head")),
        'Button2': lambda: rename_func(get_value_from_dict(JNT_name_dic, "neck")),
        'Button3': lambda: rename_func(get_value_from_dict(JNT_name_dic, "chest "))
    }
    switcher.get(button_name, lambda: None)()

with pm.window(title='Button Layout Example'):
    # ボタンを配置するレイアウトを作成
    with pm.formLayout() as main_layout:
        # ボタンの座標を指定
        button_positions = {'Button1': (50, 50), 'Button2': (150, 100), 'Button3': (250, 150)}

        # ボタンを格納する辞書
        buttons = {}

        #旧
        #for button_name, pos in button_positions.items():
        #    button = pm.button(label=button_name, width=100, height=50, align='center')
        #    buttons[button_name] = button
        #    pm.formLayout(main_layout, edit=True, attachForm=[(button, 'top', pos[1]), (button, 'left', pos[0])])

        #新
        # ボタンを配置
        for button_name, pos in button_positions.items():
            # ボタンを作成
            button = pm.button(label=button_name, width=100, height=50, align='center', command=lambda *args, name=button_name: button_action(name))
            # ボタンを辞書に追加
            buttons[button_name] = button
            # ボタンをレイアウトに配置
            pm.formLayout(main_layout, edit=True, attachForm=[(button, 'top', pos[1]), (button, 'left', pos[0])])

        # 2番目のボタンを赤色に設定
        #button_to_color = buttons.get('Button2')
        #if button_to_color:
        #    button_to_color.setBackgroundColor((1, 0, 0))  # 赤色に設定



pm.showWindow()