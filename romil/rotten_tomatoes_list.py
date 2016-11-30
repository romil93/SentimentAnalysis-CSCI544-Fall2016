from bs4 import BeautifulSoup
import requests
import csv
import time

def write_to_file(url_list):
    target = open('url_list.txt', 'w')
    for url in url_list:
    	target.write(url + "\n")

url = "https://www.rottentomatoes.com/sitemap.xml"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data, "html5lib")
list_of_urls = []
for url in soup.findAll("loc"):
    list_of_urls.append(url.text)

print(list_of_urls)

review_urls = []

for sitemap_url in list_of_urls:
    r = requests.get(sitemap_url)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    list_of_urls = []
    for url in soup.findAll("loc"):
        if "/reviews/" in url.text:
            review_urls.append(url.text)
    time.sleep(1)

write_to_file(review_urls)
