import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

#params = {"q": "dji", "hl": "en", 'gl': 'us', 'tbm': 'shop'}
 
# Gather links on first page
url = 'https://www.bikeradar.com/reviews/bikes/'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
urls = [url]

links = []
#find all links
for link in soup.find_all('a'):
    webpage = link.get('href')
    if webpage is not None:
        if re.search("https://www.bikeradar.com/reviews/bikes/.*/.*/", webpage):
            if webpage not in links:
                links.append(webpage)

# Add links in next 50 pages
for i in range(2,51):
    url = 'https://www.bikeradar.com/reviews/bikes/page/' + str(i)
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        break
    else:
        urls.append(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        for link in soup.find_all('a'):
            webpage = link.get('href')
            if webpage is not None:
                if re.search("https://www.bikeradar.com/reviews/bikes/.*/.*/", webpage):
                    if webpage not in links:
                        links.append(webpage)
    
print(links)

#while r.status_code == 200:


#if r.status_code == 404:
 #   print("status is 404")
 
# print request object
#print(r.url)
