import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

page1 = 'https://www.bikeradar.com/reviews/bikes/'
r = requests.get(page1, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
pages = [page1]

urls = []
#find all links
for url in soup.find_all('a'):
    webpage = url.get('href')
    if webpage is not None:
        if re.search("https:\/\/www\.bikeradar\.com\/reviews\/bikes\/(?!.*page).*\/.*\/$", webpage):
            if webpage not in urls:
                urls.append(webpage)

print(urls)
