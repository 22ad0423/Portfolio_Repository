import pymel.core as pm
import maya.cmds as cmds

def update_light(*args):
    # 選択されたオブジェクトを取得し、ライトであることを確認
    selection = pm.ls(selection=True, type="transform")
    if not selection:
        pm.warning("ライトを選択してください。")
        return
    light = selection[0].getShape()
    color_attr = "color"
    # Arnoldライトの場合、色は「color」属性ではなく「aiColor」属性にあります。
    #if light.nodeType() == "aiAreaLight" or light.nodeType() == "aiSkyDomeLight" or light.nodeType() == "directionalLight":
    #    color_attr = "color"
    #else:
    #    color_attr = "aiColor"
    # カラースライダーと輝度スライダーの値を取得
    color = pm.colorSliderGrp(color_field, query=True, rgb=True)
    intensity = pm.floatSliderGrp(intensity_slider, query=True, value=True)

    # ライトのカラー属性と輝度属性を設定
    light.attr(color_attr).set(color)
    light.intensity.set(intensity)
    #pm.mel.eval('setAttr "'+str(light)+'.intensity" '+str(intensity))
    print("pymel----------------------------------------------------")
    print(light)
    

def update_ui(*args):
    # 選択されたオブジェクトがライトである場合、カラースライダーと輝度スライダーの値を更新
    selection = pm.ls(selection=True, type="transform")
    if not selection:
        return
    light = selection[0].getShape()

    color_attr = "color"
    # Arnoldライトの場合、色は「color」属性ではなく「aiColor」属性にあります。
    #if light.nodeType() == "aiAreaLight" or light.nodeType() == "aiSkyDomeLight":
    #    color_attr = "color"
    #else:
    #    color_attr = "aiColor"
    pm.colorSliderGrp(color_field, edit=True, rgb=light.attr(color_attr).get())
    pm.floatSliderGrp(intensity_slider, edit=True, value=light.intensity.get())

window_name = 'light_attributes_window'
if cmds.window(window_name, exists=True):
    cmds.deleteUI(window_name)

cmds.window(window_name, title='ライトの簡易編集', sizeable=False)

layout = pm.columnLayout()

color_field = pm.colorSliderGrp(label='カラー', rgb=(1, 1, 1), parent=layout, changeCommand=update_light)
intensity_slider = pm.floatSliderGrp(label='輝度', field=True, minValue=0, maxValue=10, value=1.0, step=0.1, parent=layout, changeCommand=update_light)

pm.separator(height=10, style='none', parent=layout)
pm.button(label='更新', command=update_light, parent=layout)
pm.separator(height=10, style='none', parent=layout)

pm.showWindow()

# 初期選択のライトを編集可能にするためにUIを更新
update_ui()
pm.scriptJob(event=("SelectionChanged", update_ui))
