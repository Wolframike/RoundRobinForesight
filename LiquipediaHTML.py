import requests
from bs4 import BeautifulSoup

# これまでの試合結果とチーム名を取得する関数
def fetch_result(url, N):
	# チーム名を抽出する関数
	def extract_teamnames(teamnames):
		seen_names = set()
		unique_names = []

		for name in teamnames:
			if name not in seen_names:
				unique_names.append(name)
				seen_names.add(name)

		if len(unique_names) != N:
			raise ValueError("Number of unique team names is not equal to N.")
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
			# Extract text within <b> tags from the table
			match_result = [b.text for b in table.find_all('b')]

			# Extract alt texts of <img> tags from the table
			teamnames = [img['alt'] for img in table.find_all('img') if 'alt' in img.attrs]
			
			# Print the extracted text
			print("Match Results:")
			i = 0
			for text in match_result:
				print(text)
				i += 1
				if i % (N - 1) == 0:
					print("------")
			print("Team Names:")
			teamnames = extract_teamnames(teamnames)
			for name in teamnames:
				print(name)
		else:
			print("No table found.")
	else:
		print("Failed to fetch URL. Status code:", response.status_code)

# Example usage:
url = "https://liquipedia.net/valorant/VCL/2023/Japan/Split_1/Regular_Season"  # Replace with the desired URL
fetch_result(url, 8)
