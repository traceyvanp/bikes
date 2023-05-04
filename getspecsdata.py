import requests
from bs4 import BeautifulSoup
import re
headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

# Gather links on first page
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

# Add links in next two pages
for i in range(2,3):
    page = 'https://www.bikeradar.com/reviews/bikes/page/' + str(i)
    r = requests.get(page, headers=headers)
    if r.status_code == 404:
        break
    else:
        urls.append(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        for url in soup.find_all('a'):
            webpage = url.get('href')
            if webpage is not None:
                if re.search("https:\/\/www\.bikeradar\.com\/reviews\/bikes\/(?!.*page).*\/.*\/$", webpage):
                    if webpage not in urls:
                        urls.append(webpage)  

#get specs for each link
print('urls gathered.')
productspecsdata = []
for url in urls:
    # Make a GET request
    try:
        r = requests.get(url, headers=headers)
    except:
        specs = []
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    productspecs = soup.find('div', attrs = {'id':'product-specs__content'})
    #creation of specs table
    specs = {'url': url}

    #add date to specs
    try:
        for i in soup.findAll('time'):
                if i.has_attr('datetime'):
                    reviewdate = (i['datetime'])
        specs['reviewdate'] = reviewdate
    except:
        specs['reviewdate'] = None

    #add author of review to specs
    try:
        reviewer = soup.find('a', attrs={'author-name__name'}).string
        specs['reviewer'] = reviewer
    except:
        specs['reviewer'] = None

    #add star rating to specs
    try:
        stars = soup.find('span', attrs = {'class':'ratings-stars__value'})
        rating = stars.span.next_sibling.string.strip()
        specs['star_rating'] = rating
    except:
        specs['star_rating'] = None

    #get currency values
    try:
        prices = []
        spans = productspecs.find_all('span')
        for span in spans:
            if (span.string is not None):
                prices.append(span.string)
    except:
        prices = None
    # print(prices)

    #get specs from spec table
    try:
        tdlabels = productspecs.find_all('td', attrs={"class" : "spec-table__label"})
        tdvalues = productspecs.find_all('td', attrs={"class" : "spec-table__value"})
        #assign the key and value pairs
        for i in range(len(tdlabels)):
            try:
                specs[tdlabels[i].string] = tdvalues[i].string
            except:
                specs[tdlabels[i].string] = None
    except:
        tdlabels = None
        tdvalues = None

    #replace empty prices with currencies
    specs['Price'] = prices

    #add review
    reviewtext = ""
    try:
        words = soup.find('section', {'class': 'template-article__editor-content editor-content'})
        pgraphs = words.findAll('p')
        for pg in pgraphs:
            if (pg.string is not None):
                reviewtext += (pg.string)
    except:
        reviewtext = None

    specs['reviewtext'] = reviewtext

    productspecsdata.append(specs)

print(productspecsdata)