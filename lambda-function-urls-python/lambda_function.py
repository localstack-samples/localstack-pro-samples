import json
import requests
from bs4 import BeautifulSoup as bs

def trending():
    url = "https://github.com/trending"
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    data = {}
    repo_list = soup.find_all('article', attrs={'class':'Box-row'})
    for repo in repo_list:
        full_repo_name = repo.find('h1').find('a').text.strip().split('/')
        developer_name = full_repo_name[0].strip()
        repo_name = full_repo_name[1].strip()
        data[developer_name] = repo_name
    return data

def lambda_handler(event, context):
    data = trending()
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
