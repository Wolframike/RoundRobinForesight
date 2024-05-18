import numpy as np
import random
import time
import os
import sys
from gui import *
from LiquipediaHTMLparser import *
from utils import *

# 出力時の幅
w = 13

# 繰上げ桁
r = w - 4

def simulation(root):
	# URL取得
	try:
		url, heavy, BO, log_text_widget, progress_bar = gui(root)
	except:
		return
	if url == None:
		return
	
	# 試合結果とチーム名を取得
	result_linear, Abbr = fetch_result(url)

	# チーム数
	N = len(Abbr)

	# ボーダー
	border = np.zeros((N, N + 1))

	# 取得ラウンドのテーブル
	# 試合には-1,同じチームがクロスするところには0
	XX = -1
	DD = 0
	result = np.array([[XX if i != j else DD for j in range(N)] for i in range(N)])

	# Result_linearをresultに変換
	index = 0
	for i in range(N):
		for j in range(N):
			if i == j:
				continue
			print(f"{Abbr[i]} vs {Abbr[j]}: {result_linear[index]}")
			score = result_linear[index]
			won = int(score[0])
			lost = int(score[2])
			if won == 0 and lost == 0:
				index += 1
				continue
			result[i][j] = won
			result[j][i] = lost
			index += 1


	#クロステーブル確認
	table_check(result, Abbr, N, BO, log_text_widget)

	# それぞれのチームがどの順位になったかをカウント
	count = np.zeros((N, N + 1))

	# 未実施の試合をremaining_matchへ格納
	remaining_match = []
	for i in range(N - 1):
		for j in range(i + 1, N):
			if result[i][j] == -1:
				remaining_match.append((i, j))

	s = time.time()

	fullsearch = len(remaining_match) <= 10

	if fullsearch:
		print(f"Performing full search on {len(remaining_match)} matches...")
		print_log(log_text_widget, f"Performing full search on {len(remaining_match)} matches...")
		count = matchFill(result, remaining_match, BO, N)
		
	else:
		print("Performing Monte Carlo simulation...")
		print_log(log_text_widget, "Performing Monte Carlo simulation...")

		# l, DIV = settings()# 試行回数設定とプログレスバーのヘッダー表示
		if heavy:
			l = 1000000
			DIV = 100
		else:
			l = 5000
			DIV = 40
		
		for _ in range(l):
			if _%(l/DIV) == 0:
				sys.stdout.write('█')
				sys.stdout.flush()
			# update progress bar for every 2.5% of the total iterations
			if _%(l/40) == 0:
				update_progress(progress_bar, _/(l/100))
			
			newtable = np.array(result)# クロステーブルをコピー

			# 残りの試合について、ランダムに試合結果を生成すして、対戦表を埋めていく
			for i, j in remaining_match: # チーム i vs. チーム j について
				p, q = randomscore(BO)
				newtable[i][j] = p
				newtable[j][i] = q
				
			standings = get_standings(newtable, N)

			for i in range(N):
				team_num = standings[i][0] # (i+1)位のチーム番号
				count[team_num][i] += 1
			'''
			if standings[7][0] == 9:
				print()
				TableCheck(newtable, Abbr, N, BO)
				for i in standings:
					print(f"{Abbr[i[0]]}: {i[2]} - {9 - i[2]}")
			'''
			
	e = time.time()
	t = int(e - s)

	# 試行回数で割って、パーセントに直す
	if fullsearch:
		prob = count / (4 ** len(remaining_match)) * 100
	else:
		prob = count / l * 100

	place = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th"]
	print("")
	print_log(log_text_widget, "")

	# 確率出力
	for i in place:
		print(i, end = "")
		print_log(log_text_widget, i, end="")
		l = w - len(i)
		print(" " * (l + 1), end = "")
		print_log(log_text_widget, " " * (l + 1), end = "")
		if int(i[:-2]) == N:
			print("Team Name")
			print_log(log_text_widget, "Team Name")
			break

	m = 0 
	for i in prob:
		n = 0
		for j in i:
			if n == N:
				print(Abbr[m])
				print_log(log_text_widget, Abbr[m])
				continue
			print(round(j, r), end = "")
			print_log(log_text_widget, round(j, r), end="")
			l = w - len(str(round(j, r)))
			print("%"+ " " * l, end = "")
			print_log(log_text_widget, "%" + " " * l, end = "")
			n+=1
		m+=1

	print(f"\nTime taken: {t // 60}m{t % 60}s")
	print_log(log_text_widget, f"\nTime taken: {t // 60}m{t % 60}s")

	# ボーダー出力
	'''
	for i in place:
		print(i, end = "")
		l = w - len(i)
		print(" " * (l + 1), end = "")
		if int(i[:-2]) == N:
			print("W/L")
			break

	m = 1
	for i in border:
		n = 0
		for j in i:
			pct = round(j * 100 / sum(i), r)
			if n == N:
				print(f"{N - m}W{m - 1}L")
				continue
			print(pct, end = "")
			l = w - len(str(pct))
			print("%" + " " * l, end = "")
			n+=1
		m+=1
	'''
	print("\n" + url)
	print_log(log_text_widget, "\n" + url)
	os.system('afplay /System/Library/Sounds/Blow.aiff')
