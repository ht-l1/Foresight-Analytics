from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
from pathlib import Path
from app.config.settings import AppConfig
from app.database.supabase_manager import SupabaseManager

Base = declarative_base()

class Transaction(Base):
    """Transaction model for Superstore dataset"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer, nullable=False)
    order_id = Column(String(50), nullable=False)
    order_date = Column(DateTime, nullable=False)
    ship_date = Column(DateTime, nullable=False)
    ship_mode = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    customer_name = Column(String(100), nullable=False)
    segment = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=True)
    region = Column(String(50), nullable=False)
    product_id = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    sub_category = Column(String(100), nullable=False)
    product_name = Column(String(200), nullable=False)
    sales = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'row_id': self.row_id,
            'order_id': self.order_id,
            'order_date': self.order_date,
            'ship_date': self.ship_date,
            'ship_mode': self.ship_mode,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'segment': self.segment,
            'country': self.country,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'region': self.region,
            'product_id': self.product_id,
            'category': self.category,
            'sub_category': self.sub_category,
            'product_name': self.product_name,
            'sales': self.sales,
            'created_at': self.created_at
        }

# Manage database operations: insert, query data
class DatabaseManager:
    """Database management class that supports both local SQLite and cloud Supabase"""
    
    def __init__(self, db_path: str = "data/foresight_analytics.db"):
        if AppConfig.is_cloud_mode():
            self.db_manager = SupabaseManager()
            self.mode = 'cloud'
        else:
            # Existing SQLite logic
            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(exist_ok=True)
            
            self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
            Base.metadata.create_all(self.engine)
            
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.mode = 'local'
    
    def insert_dataframe(self, df: pd.DataFrame) -> int:
        """Insert DataFrame - delegates to appropriate manager"""
        if self.mode == 'cloud':
            return self.db_manager.insert_dataframe(df)
        else:
            # SQLite logic
            try:
                transactions = []
                for _, row in df.iterrows():
                    transaction = Transaction(
                        row_id=int(row['Row ID']),
                        order_id=str(row['Order ID']),
                        order_date=pd.to_datetime(row['Order Date'], format='%d/%m/%Y'),
                        ship_date=pd.to_datetime(row['Ship Date'], format='%d/%m/%Y'),
                        ship_mode=str(row['Ship Mode']),
                        customer_id=str(row['Customer ID']),
                        customer_name=str(row['Customer Name']),
                        segment=str(row['Segment']),
                        country=str(row['Country']),
                        city=str(row['City']),
                        state=str(row['State']),
                        postal_code=str(row['Postal Code']) if pd.notna(row['Postal Code']) else None,
                        region=str(row['Region']),
                        product_id=str(row['Product ID']),
                        category=str(row['Category']),
                        sub_category=str(row['Sub-Category']),
                        product_name=str(row['Product Name']),
                        sales=float(row['Sales'])
                    )
                    transactions.append(transaction)
                
                self.session.bulk_save_objects(transactions)
                self.session.commit()
                return len(transactions)
                
            except Exception as e:
                self.session.rollback()
                raise Exception(f"Database insert failed: {str(e)}")
    
    def has_data(self) -> bool:
        """Check if database has data"""
        if self.mode == 'cloud':
            return self.db_manager.has_data()
        else:
            try:
                count = self.session.query(Transaction).count()
                return count > 0
            except Exception as e:
                raise Exception(f"Database check failed: {str(e)}")
    
    def get_all_transactions(self) -> pd.DataFrame:
        """Get all transactions"""
        if self.mode == 'cloud':
            return self.db_manager.get_all_transactions()
        else:
            # SQLite logic
            try:
                query = self.session.query(Transaction).all()
                if not query:
                    return pd.DataFrame()
                
                data = [t.to_dict() for t in query]
                df = pd.DataFrame(data)
                
                return df[['row_id', 'order_date', 'sales', 'region', 'category', 'sub_category', 'segment', 'ship_mode', 'product_name', 'city', 'state', 'postal_code']]
            except Exception as e:
                raise Exception(f"Database query failed: {str(e)}")
    
    def filter_by_region(self, region: str) -> pd.DataFrame:
        """Filter by region"""
        if self.mode == 'cloud':
            return self.db_manager.filter_by_region(region)
        else:
            # SQLite logic 
            try:
                query = self.session.query(Transaction).filter(
                    Transaction.region == region
                ).all()
                
                if not query:
                    return pd.DataFrame()
                
                data = [t.to_dict() for t in query]
                return pd.DataFrame(data)
            except Exception as e:
                raise Exception(f"Database filter failed: {str(e)}")
    
    def get_regions(self) -> list:
        """Get unique regions"""
        if self.mode == 'cloud':
            return self.db_manager.get_regions()
        else:
            try:
                result = self.session.query(Transaction.region).distinct().all()
                return [region[0] for region in result]
            except Exception as e:
                raise Exception(f"Failed to get regions: {str(e)}")
    
    def get_segments(self) -> list:
        """Get unique segments"""
        if self.mode == 'cloud':
            return self.db_manager.get_segments()
        else:
            try:
                result = self.session.query(Transaction.segment).distinct().all()
                return [segment[0] for segment in result]
            except Exception as e:
                raise Exception(f"Failed to get segments: {str(e)}")
    
    def get_categories(self) -> list:
        """Get unique categories"""
        if self.mode == 'cloud':
            return self.db_manager.get_categories()
        else:
            try:
                result = self.session.query(Transaction.category).distinct().all()
                return [category[0] for category in result]
            except Exception as e:
                raise Exception(f"Failed to get categories: {str(e)}")
    
    def close(self):
        """Close database connections"""
        if self.mode == 'cloud':
            self.db_manager.close()
        else:
            self.session.close()