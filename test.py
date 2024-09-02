from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
request = requests.get(url)
soup = BeautifulSoup(request.content, 'html.parser')

table = soup.find(class_='wikitable')
body = table.find('tbody')
rows = body.find_all('tr')[1:]

mutable_types = []
immutable_types = []

for row in rows:
    parts = row.find_all('td')
    name = parts[0].find('code').text
    type = parts[1].text.strip()
    if type == 'immutable':
        immutable_types.append(name)
    else: mutable_types.append(name)

print(mutable_types)
print(immutable_types)