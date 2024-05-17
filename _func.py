import numpy as np
import sys

def TableCheck(result, Abbr, N, BO):
	for i in range(N):
		print("| ", end = "")
		for j in range(N):
			if result[i][j] == -1 and result[j][i] == -1:
				print("    | ", end = "")
			elif result[i][j] == -1 or result[j][i] == -1:
				print()
				raise ValueError(f"Only one side of the crosstable is filled: {Abbr[i]} vs {Abbr[j]}")
			elif result[i][j] > ((BO + 1) / 2) or result[j][i] > ((BO + 1) / 2):
				print()
				raise ValueError(f"Map count exceeding given maximum: {Abbr[i]} vs {Abbr[j]}")
			elif i != j:
				print(f"{result[i][j]}-{result[j][i]} | ", end = "")
			else:
				print("--- | ", end = "")
		print(Abbr[i])
	print("  ", end = "")
	[print(i + " " * (6 - len(i)), end = "") for i in Abbr]
	print("\n")
	

def get_standings(result, N):
	wins = [0] * N    # 勝利数
	#勝数の計算
	for i in range(N-1):
		for j in range(i+1, N):
			# i:チーム A vs. j:チーム B
			if result[i][j] == -1: # まだ対戦していないとき
				continue
			u = result[i][j] # チームA取得ラウンド数
			v = result[j][i] # チームB取得ラウンド数

			# 勝敗によって勝ち点の分配
			if u > v:
				wins[i] += 1
			else:
				wins[j] += 1

	# とりあえずの順位
	standings = [[] for _ in range(N)]
	for i in range(N):
		# 得マップ数は横方向に和をとる
		# 失マップ数は縦方向に和をとる
		# maxを入れて-1を0にしておく
		map_win = sum([max(_, 0) for _ in result[i]])
		map_lost = sum([max(_, 0) for _ in result[:, i]])

		# 得失マップ差
		map_diff = map_win - map_lost

		# 0:チーム番号 1:得失マップ差 2:勝利数
		standings[i].extend([i, map_diff, wins[i]])
	
	# 一旦暫定順位でソート
	standings = sorted(standings, key = lambda x: tuple(-x[i] for i in range(2, max([len(i) for i in standings]))))

	#　タイブレーク関数
	def resolve_ties(i, j):
		'''
		standingsのうちi番目のチームからj番目のチームまでのタイブレークをする
		2チームの場合: 内部のH2H
		3チームの場合: 内部のH2H -> 得失マップ差 -> ランダム
		4チーム以上の場合: 得失マップ差 -> ランダム
		
		引き分けているチームの数が減った瞬間return
		チームに対応する配列に適切なソート用のkeyを足していく
		'''

		# 1チームの場合
		if i == j:
			return
		
		# 2チームの場合
		if j == i + 1:
			# H2H
			if result[standings[i][0]][standings[j][0]] > result[standings[j][0]][standings[i][0]]:
				standings[i].append(1)
				standings[j].append(0)
			else:
				standings[i].append(0)
				standings[j].append(1)
			return
		
		# 3チームの場合
		if j == i + 2:
			# H2H
			a, b, c = 0, 0, 0 # 引き分けている3チームのH2H勝利数
			# a vs b
			if result[standings[i][0]][standings[i + 1][0]] > result[standings[i + 1][0]][standings[i][0]]:
				a += 1
			else:
				b += 1
			# b vs c
			if result[standings[i + 1][0]][standings[i + 2][0]] > result[standings[i + 2][0]][standings[i + 1][0]]:
				b += 1
			else:
				c += 1
			# c vs a
			if result[standings[i + 2][0]][standings[i][0]] > result[standings[i][0]][standings[i + 2][0]]:
				c += 1
			else:
				a += 1
			# これで順位がつくならappendしてreturn
			if a != b or b != c:
				standings[i].append(a)
				standings[i + 1].append(b)
				standings[i + 2].append(c)
				return
			# 得失マップ差
			# これで順位がつくならappendしてreturn
			if standings[i][1] != standings[i + 1][1] or standings[i + 1][1] != standings[i + 2][1]:
				standings[i].append(standings[i][1])
				standings[i + 1].append(standings[i + 1][1])
				standings[i + 2].append(standings[i + 2][1])
				return
			# ランダム
			# 巨大な範囲の乱数を生成して、それに応じて順位をつける
			for k in range(i, j + 1):
				standings[k].append(np.random.randint(0, sys.maxsize))
			return
		
		# 4チーム以上の場合
		# 得失マップ差
		# これで順位がつくならappendしてreturn
		if not all(standings[i][1] == standings[j][1] for j in range(i, j + 1)):
			for k in range(i, j + 1):
				standings[k].append(standings[k][1])
			return 
		# ランダム
		# 巨大な範囲の乱数を生成して、それに応じて順位をつける
		for k in range(i, j + 1):
			# standings[k].append(random.randint(0, sys.maxsize))
			standings[k].append(np.random.randint(0, sys.maxsize))
		
	# resolve_ties関数を引き分けているチームがいなくなるまで繰り返す
	while True:
		i = 0
		j = 0
		# 一通りタイブレイカーを適応する
		while True:
			tied = len(standings[i]) == len(standings[j + 1]) and all(standings[i][k] == standings[j + 1][k] for k in range(2, len(standings[i])))
			if tied:
				j += 1
			else:
				resolve_ties(i, j)
				i = j + 1
				j = i
			if j == N - 1:
				resolve_ties(i, j)
				break

		# standingsの長さを揃える
		maxlen = max([len(i) for i in standings])
		for i in range(N):
			while len(standings[i]) < maxlen:
				standings[i].append(0)
		
		# standingsをソートしておく
		standings = sorted(standings, key = lambda x: tuple(-x[i] for i in range(2, max([len(i) for i in standings]))))
	
		# すべてのタイブレイカーが固有なら終わり
		c = set()
		for i in range(N):
			tiebreaker = str([standings[i][k] for k in range(2, len(standings[i]))])
			c.add(tiebreaker)
		if len(c) == N:
			break

	# standingsを返す、[チーム番号、得失マップ差、勝利数]以外の情報は不要
	return [tuple(standings[i][:3]) for i in range(N)]

	
def randomscore(BO):
	u = 0 # チームAの取得ラウンド
	v = 0 # チームBの取得ラウンド
	while True:
		if u == (BO + 1)/2 or v == (BO + 1)/2:
			break # 試合結果が決まったらループを出る
		
		b = np.random.randint(1, 3)	# 1:チームAのラウンド取得, 2:チームBのラウンド取得
		
		if b == 1:
			u+=1 # チームAのマップ勝利
		if b == 2:
			v+=1 # チームBのマップ勝利
			
	return u, v

def settings():
	# 試行回数設定
	
	l = 5000 # 5000
	DIV = 40 # 40
	while True:
		horl = input("Heavy simulation or light? (h/l): ")
		if horl == "h" or horl == "l": break

	if horl == "h":
		l = 1000000
		DIV = 100

	# シミュレーション
	GAP = (DIV - 24) // 4
	print("0 %/" + "-" * GAP + "/25%/" + "-" * GAP + "/50%/" + "-" * GAP + "/75%/" + "-" * GAP + "/100%")

	return (l, DIV)
	
def matchFill(result, remaining_match, BO, N):
	if remaining_match == []:
		standings = get_standings(result, N)
		standings = sorted(standings, key = lambda x: tuple(-x[i] for i in range(2, max([len(i) for i in standings]))))
		count = np.zeros((N, N + 1))

		'''
		Abbr = ["DFM","DRX","GEN","GE","PRX","RRQ","T1","TLN","TS","ZETA"]
		
		if standings[PLACEMENT][0] == Abbr.index("TEAMNAME"):
			TableCheck(result, Abbr, N, BO)
			print(standings)
		'''
		
		for i in range(N):
			count[standings[i][0]][i] += 1

		return count

	twozero = result.copy()
	twoone = result.copy()
	onetwo = result.copy()
	zerotwo = result.copy()

	m = remaining_match[0]
		
	twozero[m[0]][m[1]] = 2
	twozero[m[1]][m[0]] = 0

	twoone[m[0]][m[1]] = 2
	twoone[m[1]][m[0]] = 1

	onetwo[m[0]][m[1]] = 1
	onetwo[m[1]][m[0]] = 2

	zerotwo[m[0]][m[1]] = 0
	zerotwo[m[1]][m[0]] = 2

	tz = matchFill(twozero, remaining_match[1:], BO, N)
	to = matchFill(twoone, remaining_match[1:], BO, N)
	ot = matchFill(onetwo, remaining_match[1:], BO, N)
	zt = matchFill(zerotwo, remaining_match[1:], BO, N)

	summed = np.zeros((N, N + 1))

	for i in range(N):
		for j in range(N + 1):
			summed[i][j] += (tz[i][j] + to[i][j] + ot[i][j] + zt[i][j])
	
	return summed
