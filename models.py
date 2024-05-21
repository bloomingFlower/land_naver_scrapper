from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Date

Base = declarative_base()

class ArticleTable(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title_area = Column(String)
    price_area = Column(String)
    information_area = Column(String)
    tag_area = Column(String)
    merit_area = Column(Date)
    full_url = Column(String)
    article_number = Column(String)

    def __str__(self):
        return f"ArticleTable(id={self.id}, title_area={self.title_area}, price_area={self.price_area}, information_area={self.information_area}, tag_area={self.tag_area}, merit_area={self.merit_area}, full_url={self.full_url}, article_number={self.article_number})"