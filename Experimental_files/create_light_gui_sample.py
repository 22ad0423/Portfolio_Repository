import pymel.core as pm
import maya.cmds as cmds

def create_light(*args):
    light_type = pm.optionMenu(light_type_menu, query=True, value=True)
    color = pm.colorSliderGrp(color_field, query=True, rgb=True)
    intensity = pm.floatSliderGrp(intensity_slider, query=True, value=True)
    shadows_enabled = pm.checkBoxGrp(shadow_checkbox, query=True, value1=True)

    if light_type == 'Point Light':
        light = pm.pointLight(intensity=intensity)
    elif light_type == 'Directional Light':
        light = pm.directionalLight(intensity=intensity)
    elif light_type == 'Spot Light':
        light = pm.spotLight(intensity=intensity)

    light.setColor(color)
    light.setCastShadows(shadows_enabled)

window_name = 'light_attributes_window'
if cmds.window(window_name, exists=True):
    cmds.deleteUI(window_name)

cmds.window(window_name, title='Light Attributes', sizeable=False)

layout = pm.columnLayout()

light_type_menu = pm.optionMenu(label='Light Type', parent=layout)
pm.menuItem(label='Point Light')
pm.menuItem(label='Directional Light')
pm.menuItem(label='Spot Light')

color_field = pm.colorSliderGrp(label='Color', rgb=(1, 1, 1), parent=layout)
intensity_slider = pm.floatSliderGrp(label='Intensity', field=True, minValue=0, maxValue=10, value=1.0, step=0.1, parent=layout)
shadow_checkbox = pm.checkBoxGrp(label='Shadow', numberOfCheckBoxes=1, label1='Enabled', parent=layout)

pm.separator(height=10, style='none', parent=layout)
pm.button(label='Create Light', command=create_light, parent=layout)
pm.separator(height=10, style='none', parent=layout)

pm.showWindow()
