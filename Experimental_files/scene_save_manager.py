import pymel.core as pm

def save_scene(*args):
	# ファイルを保存するたびに行う処理
	import os
	import csv
	import datetime
	import pymel.core as pm
	
	# 保存先のパスを作成
	scene_name = pm.sceneName()
	file_name = scene_name.basename()
	project_path = pm.workspace(q=True, rd=True)
	scene_folder = "scenes"
	project_scene_path = os.path.join(project_path, scene_folder)
	if not os.path.exists(project_scene_path):
		os.makedirs(project_scene_path)
	save_log_path = os.path.join(project_scene_path, "save_log.csv")
	
	# 保存ログを作成
	now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	save_log = [now, file_name, project_scene_path]
	
	# CSVに保存
	with open(save_log_path, mode='a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(save_log)
	print("Scene saved!")

def start_up():
	pm.scriptJob(e=['SceneSaved', save_scene])