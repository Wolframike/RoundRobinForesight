import requests
from bs4 import BeautifulSoup

def fetch_liquipedia_content(page_title):
	# Send a GET request to the URL
	headers = {
		'User-Agent': "RoundRobinScorePrediction/1.0 (https://twitter.com/Wolframike; https://liquipedia.net/valorant/User:Wolfram76)"
	}

	url = "https://liquipedia.net/valorant/api.php"

	# Define the parameters for the API request
	params = {
		"action": "query",
		"prop": "revisions",
		"titles": page_title,
		"rvprop": "content",
		"format": "json"
	}

	# Send the GET request to the API with custom headers
	response = requests.get(url, params=params, headers=headers)

	# Check if the request was successful
	if response.status_code == 200:
		data = response.json()
		pages = data.get("query", {}).get("pages", {})
		for page_id, page_data in pages.items():
			if "revisions" in page_data:
				content = page_data["revisions"][0]["*"]
				return content
			else:
				return "Page content not found"
	else:
		return f"Failed to retrieve content, status code: {response.status_code}"

# Example usage
page_title = "VCL/2024/Japan/Split_1/Regular_Season"  # Replace with the desired page title on Liquipedia
content = fetch_liquipedia_content(page_title)
print(content)
