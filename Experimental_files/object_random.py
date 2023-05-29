import random
import pymel.core as pm

def create_random_objects():
    # オブジェクトを削除する
    pm.delete(pm.ls(type='transform', name='random_sphere*'))

    # スライダーの値を取得する
    x_min = pm.intSliderGrp('x_min_slider', query=True, value=True)
    x_max = pm.intSliderGrp('x_max_slider', query=True, value=True)
    y_min = pm.intSliderGrp('y_min_slider', query=True, value=True)
    y_max = pm.intSliderGrp('y_max_slider', query=True, value=True)
    z_min = pm.intSliderGrp('z_min_slider', query=True, value=True)
    z_max = pm.intSliderGrp('z_max_slider', query=True, value=True)

    # ランダムな位置にオブジェクトを生成する
    for i in range(10):
        x_pos = random.uniform(x_min, x_max)
        y_pos = random.uniform(y_min, y_max)
        z_pos = random.uniform(z_min, z_max)

        # 球体を生成して位置を設定する
        sphere = pm.polySphere(radius=1, name='random_sphere{}'.format(i+1))[0]
        sphere.setTranslation([x_pos, y_pos, z_pos])

# UIを作成する
with pm.window(title='Random Object Placement'):
    with pm.columnLayout(adjustableColumn=True):
        pm.text(label='X axis')
        x_min_slider = pm.intSliderGrp('x_min_slider', field=True, label='Minimum', min=-10, max=10, value=-5)
        x_max_slider = pm.intSliderGrp('x_max_slider', field=True, label='Maximum', min=-10, max=10, value=5)

        pm.text(label='Y axis')
        y_min_slider = pm.intSliderGrp('y_min_slider', field=True, label='Minimum', min=-10, max=10, value=-5)
        y_max_slider = pm.intSliderGrp('y_max_slider', field=True, label='Maximum', min=-10, max=10, value=5)

        pm.text(label='Z axis')
        z_min_slider = pm.intSliderGrp('z_min_slider', field=True, label='Minimum', min=-10, max=10, value=-5)
        z_max_slider = pm.intSliderGrp('z_max_slider', field=True, label='Maximum', min=-10, max=10, value=5)

        pm.button(label='Create Random Objects', command=create_random_objects)

    pm.showWindow()