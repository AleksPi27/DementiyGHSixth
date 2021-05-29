from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    params = dict(request.query.decode())
    label = params['label']
    id = params['id']
    print(id)
    s = session()
    article = s.query(News).get(id)
    article.label = label
    s.commit()
    print(article.label)
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    news = get_news("https://news.ycombinator.com/")
    freshest_news_from_site = news[0]

    s = session()

    freshed_news_from_db = s.query(News).first()
    if not freshed_news_from_db is None:
        if freshed_news_from_db.title == freshest_news_from_site['title'] and freshed_news_from_db.author == freshest_news_from_site['author']:
            print('All news are fresh')
            redirect("/news")
        else:
            isFresh = True
            news_i = 2
            i = 0
            while isFresh and news_i < 27:
                print("news i is "+str(news_i))
                while isFresh and i < len(news):
                    print('i' + str(i))
                    if news[i]['title'] == freshed_news_from_db.title and news[i]['author'] == freshed_news_from_db.author:
                        isFresh = False
                    else:
                        entry = News()
                        entry.title=news[i]['title']
                        entry.author = news[i]['author']
                        entry.url = news[i]['url']
                        entry.comments = news[i]['comments']
                        entry.points = news[i]['points']
                        s.add(entry)
                        i += 1
                    print(isFresh)
                if isFresh:
                    news = get_news("https://news.ycombinator.com/news?p=" + str(news_i))

        s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
