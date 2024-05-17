import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

# これまでの試合結果とチーム名を取得する関数
def fetch_result(url):
	result = []
	names = []
	# チーム名を抽出する関数
	def extract_teamnames(teamnames):
		seen_names = set()
		unique_names = []

		for name in teamnames:
			if name not in seen_names:
				unique_names.append(name)
				seen_names.add(name)

		return unique_names
	
	# URLからHTMLを取得
	response = requests.get(url)
	
	# リクエストが成功した場合
	if response.status_code == 200:
		html_content = response.text
		
		# BeautifulSoupでHTMLを解析
		soup = BeautifulSoup(html_content, 'html.parser')
		
		# テーブルのみを取得
		table = soup.find('table', class_='wikitable wikitable-bordered crosstable')
		
		# テーブルが存在する場合
		if table:
			# テーブル内の<b>タグのテキストを取得、試合結果を抽出
			match_result = [b.text for b in table.find_all('b')]

			# テーブル内の<img>タグのalt属性を取得、チーム名を抽出
			teamnames = [img['alt'] for img in table.find_all('img') if 'alt' in img.attrs]

			# 試合結果を抽出
			for r in match_result:
				result.append(r)
			# チーム名を抽出
			names = extract_teamnames(teamnames)
		# テーブルが存在しない場合
		else:
			messagebox.showerror("Invalid URL", "No cross table found on the given URL.")
	# リクエストが失敗した場合
	else:
		messagebox.showerror("Request Failed", "Failed to fetch data from the given URL with status code: " + str(response.status_code))
	
	return result, names