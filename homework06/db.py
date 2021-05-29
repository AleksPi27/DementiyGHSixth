from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

# s=session()
#
# news=get_news("https://news.ycombinator.com/",26)
#
# for i in range(len(news)):
#     entry=News(title=news[i]['title'],
#               author=news[i]['author'],
#               url=news[i]['url'],
#               comments=news[i]['comments'],
#               points=news[i]['points'])
#     s.add(entry)
# s.commit()