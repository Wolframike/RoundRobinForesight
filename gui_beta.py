import tkinter as tk
from tkinter import messagebox, ttk

def get_config():
	# ウィンドウ作成
	root = tk.Tk()
	root.title("Round Robin Score Prediction Configuration")
	root.geometry("+1000+500")

	# 入力格納用の変数
	team_number_var = tk.IntVar()
	url_var = tk.StringVar()
	team_name_entries = []
	team_numbers = [i for i in range(1, 13)]

	# 入力はDict型で格納
	stored_data = {}

	# チーム数を回収、チーム数に応じてチーム名入力欄を作成
	def submit_team_number():
		try:
			team_number = team_number_var.get()
			if team_number <= 0:
				raise ValueError("Team number must be a positive integer")
			create_team_name_entries(team_number)
		except ValueError as e:
			messagebox.showerror("Invalid Input", str(e))
	
	# チーム名とURLを回収
	def create_team_name_entries(team_number):
		# 
		for widget in frame_team_names.winfo_children():
			widget.destroy()
		
		del team_name_entries[:]
		
		for i in range(team_number):
			label = tk.Label(frame_team_names, text=f"Team {i + 1} abbreviation:")
			label.grid(row=i, column=0, padx=10, pady=5)
			entry = tk.Entry(frame_team_names)
			entry.grid(row=i, column=1, padx=10, pady=5)
			team_name_entries.append(entry)

			if i == 0:
				entry.focus_set()
		
		tk.Label(frame_team_names, text="Liquipedia URL:").grid(row=team_number, column=0, padx=10, pady=5)
		tk.Entry(frame_team_names, textvariable=url_var).grid(row=team_number, column=1, padx=10, pady=5)
		tk.Button(frame_team_names, text="Submit", command=submit_team_names).grid(row=team_number + 1, columnspan=2, pady=10)

	# 全引数をdictに格納
	def submit_team_names():
		stored_data["team_number"] = team_number_var.get()
		stored_data["team_names"] = [entry.get() for entry in team_name_entries]
		stored_data["url"] = url_var.get()
		
		# チーム名を回収したらウィンドウを閉じる
		root.quit()
	
	# チーム数入力欄
	tk.Label(root, text="Team Number:").grid(row=0, column=0, padx=10, pady=5)
	team_number_dropdown = ttk.Combobox(root, textvariable=team_number_var, values=team_numbers, state="readonly")
	team_number_dropdown.grid(row=0, column=1, padx=10, pady=5)
	tk.Button(root, text="Submit", command=submit_team_number).grid(row=1, columnspan=2, pady=10)
 
	# チーム名入力欄
	frame_team_names = tk.Frame(root)
	frame_team_names.grid(row=2, columnspan=2, pady=10)

	# ウィンドウを表示
	root.mainloop()

	# ウィンドウを閉じる際Xボタンを押した場合もハンドリング
	try:
		root.destroy()
	except tk.TclError:
		pass

	# (チーム数、チーム名、URL)のｔupleを返す
	return stored_data.get("team_number", None), stored_data.get("team_names", None), stored_data.get("url", None)

# 使用例
N, Abbr, URL = get_config()
if all([i is not None for i in (N, Abbr, URL)]):
	print(f"Team Number: {N}")
	print(f"Team Names: {Abbr}")
	print(f"String: {URL}")
else:
	print("No data entered.")
