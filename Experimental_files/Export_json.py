import json

def export_materials_to_json(materials):
    """
    マテリアル情報をJson形式で出力する

    Args:
        materials (list): マテリアル情報のリスト。各要素は辞書形式で、以下のキーを持つ。
            "material_name" (str): マテリアルの名前
            "textures" (list): テクスチャ情報のリスト。各要素は辞書形式で、以下のキーを持つ。
                "type" (str): テクスチャの種類
                "path" (str): テクスチャのファイルパス

    Returns:
        None
    """
    # マテリアル情報を格納する辞書
    materials_dict = {}
    for material in materials:
        material_name = material.get("material_name")
        textures = material.get("textures")
        materials_dict[material_name] = textures
    
    # JSON形式で出力
    with open("materials.json", "w") as json_file:
        json.dump(materials_dict, json_file, indent=4)

# マテリアル情報を含む辞書オブジェクトを作成する
materials = {
    "Material1": [
        {"type": "albedo", "path": "albedo.png"},
        {"type": "normal", "path": "normal.png"},
        {"type": "metallic", "path": "metallic.png"},
        {"type": "smoothness", "path": "smoothness.png"},
        {"type": "emission", "path": "emission.png"},
        {"type": "occlusion", "path": "occlusion.png"}
    ],
    "Material2": [
        {"type": "albedo", "path": "albedo.png"},
        {"type": "normal", "path": "normal.png"},
        {"type": "metallic", "path": "metallic.png"},
        {"type": "smoothness", "path": "smoothness.png"},
        {"type": "emission", "path": "emission.png"},
        {"type": "occlusion", "path": "occlusion.png"}
    ]
}


import json
# マテリアル情報を格納する辞書
def add_material(materials_dict, material_name):
    # 既に存在するマテリアル名の場合はエラーを表示
    if material_name in materials_dict:
        print(f"Error: Material '{material_name}' already exists!")
        return

    # マテリアル名をキーとして、空のテクスチャ情報リストを追加
    materials_dict[material_name] = []

# マテリアルにテクスチャ情報を追加する関数
def add_texture(materials_dict, material_name, texture_type, texture_path):
    # マテリアル名が存在しない場合はエラーを表示
    if material_name not in materials_dict:
        print(f"Error: Material '{material_name}' does not exist!")
        return

    # テクスチャ情報を辞書形式で作成
    texture_info = {"type": texture_type, "path": texture_path}

    # マテリアル名に対応するテクスチャ情報リストに追加
    materials_dict[material_name].append(texture_info)


# マテリアル情報を格納する辞書
materials_dict = {}

# マテリアル1の追加
add_material(materials_dict, "Material1")

# マテリアル2の追加
add_material(materials_dict, "Material2")

# マテリアル1にテクスチャ情報を追加
add_texture(materials_dict, "Material1", "Diffuse", "textures/diffuse1.jpg")
add_texture(materials_dict, "Material1", "Specular", "textures/specular1.jpg")

# マテリアル2にテクスチャ情報を追加
add_texture(materials_dict, "Material2", "Diffuse", "textures/diffuse2.jpg")
add_texture(materials_dict, "Material2", "Normal", "textures/normal2.jpg")

# マテリアル情報をJSON形式で出力
with open("materials.json", "w") as json_file:
    json.dump(materials_dict, json_file, indent=4)
