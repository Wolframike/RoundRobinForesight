import tkinter as tk
from tkinter import messagebox, ttk

# URLを入力するためのGUIを作成
def gui(root):
	# 文字列を格納するための変数
	url_var = tk.StringVar()

	# ドロップダウンメニューの選択肢を格納するための変数
	mode_var = tk.StringVar()
	mode_var.set("Light")  # Default selection

	bestof_var = tk.StringVar()
	bestof_var.set("3")  # Default selection

	# Submitボタンがクリックされたかどうかを格納する変数
	submitted = False

	# Submitボタンがクリックされたときの処理
	def on_submit():
		nonlocal submitted
		submitted = True
		root.quit()

	# Pasteボタンがクリックされたときの処理
	def paste_from_clipboard():
		clipboard_content = root.clipboard_get()
		url_var.set(clipboard_content)
		on_submit()

	# GUI本体
	label = tk.Label(root, text="Enter Liquipedia URL:")
	label.pack(pady=10)
	entry = tk.Entry(root, width=50, textvariable=url_var)
	entry.pack(pady=5)

	# ドロップダウンメニューフレーム
	dropdown_frame = tk.Frame(root)
	dropdown_frame.pack(pady=5)

	mode_label = tk.Label(dropdown_frame, text="Simulation weight:")
	mode_label.pack(side=tk.LEFT, padx=5)
	mode_dropdown = tk.OptionMenu(dropdown_frame, mode_var, "Light", "Heavy")
	mode_dropdown.pack(side=tk.LEFT, padx=5)

	bestof_label = tk.Label(dropdown_frame, text="Best of:")
	bestof_label.pack(side=tk.LEFT, padx=5)
	bestof_dropdown = tk.OptionMenu(dropdown_frame, bestof_var, "3", "5")
	bestof_dropdown.pack(side=tk.LEFT, padx=5)

	# ボタンフレーム
	button_frame = tk.Frame(root)
	button_frame.pack(pady=5)

	# Clipboardから貼り付けるボタン
	paste_button = tk.Button(button_frame, text="Paste and Go", command=paste_from_clipboard)
	paste_button.pack(side=tk.LEFT, padx=5)

	# Submitボタン
	submit_button = tk.Button(button_frame, text="Submit", command=on_submit)
	submit_button.pack(side=tk.LEFT, padx=5)

	log_text_widget = None  # Log text widget placeholder

	# 正しいURLが入力されるまでループ
	while True:
		# イベントループ
		root.mainloop()

		# 入力されたURLを取得
		url = url_var.get()

		# Submitボタンがクリックされていない場合
		if not submitted:
			return None  # Return None if the window was closed

		# URLが空文字か、LiquipediaのURLでない場合
		if url == "" or not url.startswith("https://liquipedia.net"):
			messagebox.showerror("Invalid URL", "Please enter a valid Liquipedia URL.\n\nGiven URL:\n" + url)
			url_var.set("")
			submitted = False
		# 正しいURLが入力された場合
		else:
			# Create a progress bar
			progress_bar = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate", maximum=97.5)
			progress_bar.pack(pady=10)

			# Create a massive log text field
			log_label = tk.Label(root, text="Results")
			log_label.pack(pady=10)
			log_text_widget = tk.Text(root, height=20, width=80, font=("Courier New", 16), spacing1=5, spacing2=5, spacing3=5, padx=10, pady=10)
			log_text_widget.pack(pady=5, expand=True, fill=tk.BOTH)

			return url, mode_var.get() == "Heavy", int(bestof_var.get()), log_text_widget, progress_bar # Return the URL and log widget if valid

def print_log(log_text_widget, message, end="\n"):
	if log_text_widget:
		log_text_widget.config(state=tk.NORMAL)
		log_text_widget.insert(tk.END, str(message) + end)
		log_text_widget.see(tk.END)
		log_text_widget.config(state=tk.DISABLED)
	else:
		messagebox.showerror("Log Error", "Log widget not initialized")

def update_progress(progress_bar, value):
	if progress_bar:
		progress_bar.configure(value=value)
		progress_bar.update()
	else:
		messagebox.showerror("Progress Error", "Progress bar not initialized")