from bs4 import BeautifulSoup
import requests
import csv
import time, re

def reading():
    s = open('partial_url_crawl_list.txt', 'r').read()
    urls = s.split("\n")
    return urls

urls_list = reading()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

target = open('reviews_part2.txt', 'w', encoding="UTF-8")

for review_url in urls_list:
    page = 1
    r = requests.get(review_url + "?page=" + str(page), headers=headers)
    # print r.text
    while True:
        r = requests.get(review_url + "?page=" + str(page), headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html5lib")
            movie_name = soup.find("meta",{"name":"movieTitle"})['content']
            rotten_tomato_movie_id = review_url.split("/")[4]
            reviews_on_page = soup.findAll("div",{"class":"review_container"})

            for review in reviews_on_page:
                # print(review)
                review_info = review.find("div",{"class":"the_review"}).text
                if review_info.strip() == "":
                    continue
                fresh = review.find("div", {"class":"fresh"})
                rotten = review.find("div", {"class":"rotten"})

                score_rating = review.find("div", {"class":"review_desc"}).find("div", {"class":"subtle"}).text
                rating = None
                try:
                    rating = score_rating.split("Original Score:",1)[1]
                except (ValueError,IndexError):
                    print()
                    #DO NOTHING


                output_to_file = rotten_tomato_movie_id + " || " + movie_name + " || " + review_info

                if fresh == None:
                    output_to_file = output_to_file + " || " + "NEGATIVE"
                else:
                    output_to_file = output_to_file + " || " + "POSITIVE"

                if rating != None:
                    output_to_file = output_to_file + " || " + rating.strip()



                output_to_file = output_to_file + "\n"
                target.write(output_to_file)

            print(review_url + "?page=" + str(page))
            page += 1
        else:
            break
