import numpy as np
import random
import time
import os
import sys
from _func import *

# チーム数
N = 8

# Best of
BO = 3

# ボーダー
border = np.zeros((N, N + 1))

# 出力時の幅
w = 13

# 繰上げ桁
r = w - 4

# 取得ラウンドのテーブル
# まだ戦ってない試合には-1,同じチームがクロスするところには0
XX = -1
DD = 0
result = np.array([
	[DD, XX, XX, XX, XX, XX, XX, XX],#FL
	[XX, DD, XX, XX, XX, XX, XX, XX],#SZ
	[XX, XX, DD, XX, XX, XX, XX, XX],#IGZ
	[XX, XX, XX, DD, XX, XX, XX, XX],#RC
	[XX, XX, XX, XX, DD, XX, XX, XX],#VL
	[XX, XX, XX, XX, XX, DD, XX, XX],#SG
	[XX, XX, XX, XX, XX, XX, DD, XX],#MRG
	[XX, XX, XX, XX, XX, XX, XX, DD],#NTH
#	 FL  SZ  IGZ RC  VL  SG  MRG NTH
])


# 略称
Abbr = [
	"FL",
	"SZ",
	"IGZ",
	"RC",
	"VL",
	"SG",
	"MRG",
	"NTH"
]

#クロステーブル確認用
while True:
	yorn = input("Check the cross table? (y/n): ")
	if yorn == "y" or yorn == "n": break
	
if yorn == "y":
	TableCheck(result, Abbr, N, BO)

# それぞれのチームがどの順位になったかをカウント
count = np.zeros((N, N+1))

# 未実施の試合をremaining_matchへ格納
remaining_match = []
for i in range(N-1):
	for j in range(i+1, N):
		if result[i][j] == -1:
			remaining_match.append((i, j))

s = time.time()

fullsearch = len(remaining_match) <= 10

if fullsearch:
	print(f"Performing full search on {len(remaining_match)} matches...\n")
	count = matchFill(result, remaining_match, BO, N)
	
else:
	print("Performing Monte Carlo simulation...\n")

	l, DIV = settings()# 試行回数設定とプログレスバーのヘッダー表示
	
	for _ in range(l):
		if _%(l/DIV) == 0:
			sys.stdout.write('█')
			sys.stdout.flush()
		
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
print("\n")

# 確率出力

for i in place:
	print(i, end = "")
	l = w - len(i)
	print(" " * (l + 1), end = "")
	if int(i[:-2]) == N:
		print("Team Name")
		break

m = 0 
for i in prob:
	n = 0
	for j in i:
		if n == N:
			print(Abbr[m])
			continue
		print(round(j, r), end = "")
		l = w - len(str(round(j, r)))
		print("%"+ " " * l, end = "")
		n+=1
	m+=1

print(f"\nTime taken: {t // 60}m{t % 60}s\n")

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
print("\n" + __file__)
os.system('afplay /System/Library/Sounds/Blow.aiff')
