import requests
from bs4 import BeautifulSoup

import json


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    # news=requests.get("https://news.ycombinator.com/newest")
    tbl_list = parser.table.findAll('table')
    entries = tbl_list[1].findAll('td')
    i = 0
    while i + 4 < len(entries):
        author = str(entries[i + 4].a.text)
        points = str(entries[i + 4].span.text)
        title = str(entries[i + 2].a.text)
        url = str(entries[i + 2].a['href'])
        comments = str(entries[i + 4].findAll('a')[-1].text)
        if points.__eq__('discuss'):
            points = str(0)
        else:
            points = points.split('p')[0][:-1]

        if comments.__eq__('discuss'):
            comments = str(0)
        else:
            comments = comments.split('c')[0][:-1]
        entry = dict(author=f'{author}', comments=f'{comments}', points=f'{points}', title=f'{title}', url=f'{url}')
        news_list.append(entry)
        i += 5
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    tbl_list = parser.table.findAll('table')
    entries = tbl_list[1].findAll('td')
    print(entries[-1].a['href'])
    return entries[-1].a['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news



