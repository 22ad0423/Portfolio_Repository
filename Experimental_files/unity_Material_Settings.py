import pymel.core as pm
import json
import os

# マテリアル情報を格納する辞書
materials_dict = {"Material": {}}

# マテリアル情報を格納する辞書
def add_material(materials_dict, material_name):
    # 既に存在するマテリアル名の場合はエラーを表示
    if material_name in materials_dict["Material"]:
        print(f"Error: Material '{material_name}' already exists!")
        return

    # マテリアル名をキーとして、空のテクスチャ情報リストを追加
    materials_dict["Material"][material_name] = {"textures": []}


# マテリアルにテクスチャ情報を追加する関数
def add_texture(materials_dict, material_name, texture_type, texture_path):
    # マテリアル名が存在しない場合はエラーを表示
    if material_name not in materials_dict["Material"]:
        print(f"Error: Material '{material_name}' does not exist!")
        return

    # テクスチャ情報を辞書形式で作成
    texture_info = {"type": texture_type, "path": texture_path}

    # マテリアル名に対応するテクスチャ情報リストに追加
    materials_dict["Material"][material_name]["textures"].append(texture_info)


def attribute_to_string(attribute):
    
        return str(attribute)

# マテリアル情報を格納する辞書
def export_materials_to_json(materials_dict, file_name):
    # 現在のプロジェクトの絶対パスを取得
    project_path = pm.workspace.path
    
    # 保存するフォルダーのパスを作成
    save_folder_path = os.path.join(project_path, "json")
    
    # 保存するファイルのパスを作成
    save_file_path = os.path.join(save_folder_path, file_name)
    
    # フォルダーが存在しない場合は作成する
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)
    
    # ファイルを書き込みモードで開く
    with open(save_file_path, "w") as json_file:
        json.dump(materials_dict, json_file, indent=4)
    
    # ログを出力
    print(f"File saved: {save_file_path}")




def print_material_and_texture_info(obj):
    #
    #選択したオブジェクトのマテリアルとテクスチャの情報をPrintで表示する関数
    #:param obj: PyMELのオブジェクト

    #変数名
    #obj:選択したオブジェクト
    #shape_node:オブジェクトの形状ノード
    #shading_engine_list:形状ノードのシェーディングエンジン
    #shader_list:シェーディングエンジンに接続されているマテリアルノード
    #shader:マテリアルノード
    #file_nodes:マテリアルノードに接続されたファイルノード
    #file_node:ファイルノード
    #file_path:ファイルノードのファイルパス
    #rel_file_path:ファイルパスをプロジェクトの相対パスに変換
    #connections:file_nodeの接続先情報
    #bump_nodes:マテリアルノードに接続されたbump2dノード
    #bump_node:bump2dノード
    #bump_type:bump2dノードのbumpInterpの値
    #bump_value:bump2dノードのbumpValueの値
    #project_path:現在のプロジェクトの絶対パス

    # 現在のプロジェクトの絶対パスを取得
    project_path = pm.workspace.path
    
    # 絶対パスを表示
    print("現在のプロジェクトの絶対パス：", project_path)
    
    # オブジェクトの形状ノードを取得
    shape_node = obj.getShape()
    # 形状ノードのシェーディングエンジンを取得
    shading_engine_list = shape_node.listConnections(type='shadingEngine')
    # シェーディングエンジンが存在する場合
    if shading_engine_list:
        print("Object: {}".format(obj.name()))
        print("Material and Texture Info:")
        # シェーディングエンジンの数だけループ
        for shading_engine in shading_engine_list:
            # シェーディングエンジンに接続されているマテリアルノードを取得
            shader_list = shading_engine.listConnections(type='lambert') + \
                          shading_engine.listConnections(type='blinn') + \
                          shading_engine.listConnections(type='aiStandardSurface')
            # マテリアルノードが存在する場合
            if shader_list:
                
                # マテリアルノードの数だけループ
                for shader in shader_list:
                    # マテリアルノードの名前を表示
                    print("    Material: {}".format(shader.name()))
                    # マテリアル情報を格納する辞書にマテリアル名を追加
                    add_material(materials_dict, attribute_to_string(shader.name()))

                    # マテリアルノードがAiStandardSurfaceノードの場合
                    if isinstance(shader, pm.nt.AiStandardSurface):
                        # マテリアルノードの接続先情報を取得して一番最後の要素のみ表示
                        file_nodes = shader.listConnections(type='file')
                        # マテリアルノードに接続されたファイルノードが存在する場合
                        if file_nodes:
                            # マテリアルノードに接続されたファイルノードの数だけループ
                            for file_node in file_nodes:
                                # ファイルノードのファイルパスを取得
                                file_path = file_node.fileTextureName.get()
                                # ファイルパスをプロジェクトの相対パスに変換
                                rel_file_path = os.path.relpath(file_path, pm.workspace.path)
                                # ファイルノードの名前とファイルパスを表示
                                print("        Texture: {}, File Path: {}".format(file_node.name(), rel_file_path))
                                

                                # file_nodeの接続先情報を取得して一番最後の要素のみ表示
                                connections = file_node.listConnections(destination=True, plugs=True)
                                # ファイルノードに接続されている場合
                                if connections:
                                    # ファイルノードに接続されている接続先情報を表示
                                    print("            Connection: {}".format(connections[-1]))
                                
                                add_texture(materials_dict, attribute_to_string(shader.name()), attribute_to_string(connections[-1]), attribute_to_string(rel_file_path))
                        # マテリアルノードに接続されたbump2dノードを取得
                        bump_nodes = shader.listConnections(type='bump2d')

                        # bump2dノードが存在する場合
                        if bump_nodes:
                            # bump2dノードの数だけループ
                            for bump_node in bump_nodes:
                                # bump2dノードの情報を表示
                                bump_type = bump_node.bumpInterp.get()
                                # bump2dノードのbumpValueの値を取得
                                bump_value = bump_node.bumpValue.get()
                                # bump2dノードの名前とbumpValueの値を表示
                                print("        Bump: {}, Type: {}, Value: {}".format(bump_node.name(), bump_type, bump_value))

                                # bump_nodeの接続先情報を取得して一番最後の要素のみ表示
                                connections = bump_node.listConnections(destination=True, plugs=True)
                                
                                # bump_nodeに接続されている場合
                                if connections:
                                    # bump_nodeに接続されている接続先情報を表示
                                    print("            Connection: {}".format(connections[-1]))
                                    # bump_nodeに接続されたファイルノードを取得して表示
                                    file_nodes = pm.listConnections(bump_node.bumpValue, type='file')
                                    
                                    # ファイルノードが存在する場合
                                    if file_nodes:
                                        # ファイルノードの数だけループ
                                        for file_node in file_nodes:
                                            # ファイルノードのファイルパスを取得
                                            file_path = file_node.fileTextureName.get()
                                            # ファイルパスをプロジェクトの相対パスに変換
                                            rel_file_path = os.path.relpath(file_path, pm.workspace.path)
                                            # ファイルノードの名前とファイルパスを表示
                                            print("            Texture: {}, File Path: {}".format(file_node.name(), rel_file_path))
                                            # file_nodeの接続先情報を取得して一番最後の要素のみ表示
                                            connections = file_node.listConnections(destination=True, plugs=True)
                                            
                                            # file_nodeに接続されている場合
                                            if connections:
                                                print("                Connection: {}".format(connections[-1]))
                                                
                                                add_texture(materials_dict, attribute_to_string(shader.name()), attribute_to_string(connections[-1]), attribute_to_string(rel_file_path))
                    # マテリアルノードがblinn・lambertの場合
                    else:
                        # マテリアルノードに接続されたファイルノードを取得
                        file_nodes = shader.listConnections(type='file') + \
                                     shader.listConnections(type='aiImage')
                        
                        # マテリアルノードに接続されたファイルノードが存在する場合
                        if file_nodes:
                            # マテリアルノードに接続されたファイルノードの数だけループ
                            for file_node in file_nodes:
                                # ファイルノードのファイルパスを取得
                                file_path = file_node.fileTextureName.get()
                                # ファイルパスをプロジェクトの相対パスに変換
                                rel_file_path = os.path.relpath(file_path, pm.workspace.path)
                                # ファイルノードの名前とファイルパスを表示
                                print("        Texture: {}, File Path: {}".format(file_node.name(), rel_file_path))
                                # file_nodeの接続先情報を取得して一番最後の要素のみ表示
                                connections = file_node.listConnections(destination=True, plugs=True)
                                
                                # ファイルノードに接続されている場合
                                if connections:
                                    print("            Connection: {}".format(connections[-1]))

                                    add_texture(materials_dict, attribute_to_string(shader.name()), attribute_to_string(connections[-1]), attribute_to_string(rel_file_path))

def add_project_info(materials_dict):
    # プロジェクトパスを取得する
    w_project_path = cmds.workspace(q=True, rd=True)
    # プロジェクト名を取得する
    w_project_name = os.path.basename(w_project_path)
    # materials_dictにプロジェクトパスを追加する
    materials_dict['Project'] = {'Path': w_project_path}

# マテリアル情報をJSONファイルに出力
def material_info_to_json():
    print('処理開始\n\n')
    # 選択したオブジェクトを取得
    selected_objects = pm.ls(sl=True)

    # 選択したオブジェクトのマテリアルとテクスチャ情報を表示
    for obj in selected_objects:
        # オブジェクトのマテリアルとテクスチャ情報を表示
        print_material_and_texture_info(obj)
        print('\n')

    scene_name = pm.sceneName()
    print("現在のシーンの名前: ", scene_name)
    file_name = str(scene_name)+".json"

    #プロジェクトの情報を書き込み
    add_project_info(materials_dict)

    export_materials_to_json(materials_dict, file_name)

    print('処理終了\n\n')




material_info_to_json()