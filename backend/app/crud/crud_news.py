from sqlalchemy.orm import Session
from ..models.news import NewsArticle
from ..schemas.fmp_schemas import FMPArticle
from datetime import datetime

def create_article(db: Session, article_data: FMPArticle, symbol: str) -> NewsArticle:
    db_article = NewsArticle(
        symbol=symbol,
        title=article_data.title,
        url=article_data.link,
        site=article_data.site,
        content=article_data.content,
        author=article_data.author,
        image_url=article_data.image,
        published_date=datetime.strptime(article_data.date, '%Y-%m-%d %H:%M:%S')
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_articles_by_symbol(db: Session, symbol: str, limit: int = 20):
    return db.query(NewsArticle).filter(NewsArticle.symbol == symbol).order_by(NewsArticle.published_date.desc()).limit(limit).all()