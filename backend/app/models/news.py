from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint, Index
from ..core.database import Base
from .company import TimestampMixin

class NewsArticle(Base, TimestampMixin):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True, nullable=False)
    title = Column(String(500), nullable=False)
    image_url = Column(String(1000))
    url = Column(String(1000), nullable=False)
    published_date = Column(DateTime, nullable=False, index=True)
    author = Column(String(255))
    site = Column(String(100))
    content = Column(Text)

    __table_args__ = (
        UniqueConstraint('symbol', 'url', name='_symbol_url_uc'),
        Index('idx_news_symbol_date', 'symbol', 'published_date'),
    )