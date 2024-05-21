from sqlalchemy.orm import Session
from database import SessionLocal
from models import ArticleTable


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def store_data(db: Session, article: ArticleTable):
    existing_article = db.query(ArticleTable).filter(
        ArticleTable.title_area == article.title_area,
        ArticleTable.price_area == article.price_area,
        ArticleTable.information_area == article.information_area,
        ArticleTable.tag_area == article.tag_area,
        ArticleTable.merit_area == article.merit_area
    ).first()
    if existing_article is None:
        # If the article does not exist in the database, create a new one
        db.add(article)
        db.commit()
        db.refresh(article)
        return article
    else:
        # If the article already exists in the database, update it
        existing_article.full_url = article.full_url
        existing_article.article_number = article.article_number
        db.commit()
        db.refresh(existing_article)
        return existing_article
