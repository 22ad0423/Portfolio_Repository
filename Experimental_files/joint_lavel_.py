from maya import cmds;

# 選択したボーンから下の階層にあるボーンをすべて選択する
def GetBoneNames(root):
    cmds.select(root, hierarchy=True);
    return cmds.ls(sl=True);

# buttonに登録するコマンド
#Jointの階層選択
def select_joints():
    nodes = cmds.ls(selection=True, dag=True);
    joints = [];
    for node in nodes:
        if cmds.nodeType(node) == "joint":
            joints.append(node);
    cmds.select(joints);
    return None;
    
# buttonに登録するコマンド
# ラベルの表示
def Joint_lavel_enaable():
    root_joint = cmds.ls(selection=True);
    GetBoneNames(root_joint[0]);
    cmds.select(cmds.ls(selection=True, dagObjects=True, type='joint'));
    all_joint_select = cmds.ls(sl=True)
    for i in all_joint_select:
        cmds.setAttr( i +'.drawLabel', 1 );
        if '_L' in i:
            cmds.setAttr( i +'.side', 1 );
        elif '_R' in i:
            cmds.setAttr( i +'.side', 2 );
        else:
            cmds.setAttr( i +'.side', 0 );
        cmds.setAttr( i +'.type', 18 );
        cmds.setAttr( i +'.otherType', i ,type="string");
    return None
    
# buttonに登録するコマンド
# ラベルの非表示
def Joint_lavel_disable():
    root_joint = cmds.ls(selection=True);
    GetBoneNames(root_joint[0]);
    cmds.select(cmds.ls(selection=True, dagObjects=True, type='joint'));
    all_joint_select = cmds.ls(sl=True);
    for i in all_joint_select:
        cmds.setAttr( i +'.drawLabel', 0 );
    return None;

def joint_lavel_addon():
    # ボタン付きGUIの生成
    button_window = cmds.window("joint_lavel_Addon");
    button_layout = cmds.columnLayout(adjustableColumn=True, parent=button_window);
    Joint_lavel_enaable_button = cmds.button(label="Joint lavel enaable", command="Joint_lavel_enaable()", parent=button_layout);
    Joint_lavel_disable_button = cmds.button(label="Joint lavel disable", command="Joint_lavel_disable()", parent=button_layout);
    select_joints_button = cmds.button(label="Select Joints", command="select_joints()", parent=button_layout);
    cmds.showWindow(button_window);
        
joint_lavel_addon()