#ジョイントを作成:
import pymel.core as pm

# ジョイントを作成
joint = pm.joint()

#指定位置にジョイントを作成:
import pymel.core as pm

# ジョイントを指定位置に作成
position = (1, 0, 0)  # 例: (x, y, z) の座標
joint = pm.joint(p=position)


#親子関係のあるジョイントを作成:
import pymel.core as pm

# 親ジョイントを作成
parent_joint = pm.joint()

# 子ジョイントを作成し、親ジョイントに接続
child_joint = pm.joint()
pm.parent(child_joint, parent_joint)


#ジョイントを移動:
import pymel.core as pm

# 移動前のジョイントの取得
joint = pm.PyNode('joint1')

# ジョイントを新しい位置に移動
new_position = (2, 0, 0)  # 例: (x, y, z) の座標
joint.setTranslation(new_position, space='world')


#親と子それぞれのジョイントの座標を setTranslation() メソッドを使用して指定
import pymel.core as pm

# 親ジョイントを作成
parent_position = (0, 0, 0)  # 親ジョイントの座標
parent_joint = pm.joint()
parent_joint.setTranslation(parent_position, space='world')

# 子ジョイントを作成し、親ジョイントに接続
child_position = (2, 0, 0)  # 子ジョイントの座標
child_joint = pm.joint()
child_joint.setTranslation(child_position, space='world')
pm.parent(child_joint, parent_joint)

