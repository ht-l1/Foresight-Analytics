from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
from pathlib import Path

Base = declarative_base()

# Define the table structure
class Transaction(Base):
    """Transaction model for database storage"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(DateTime, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    department = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'transaction_date': self.transaction_date,
            'transaction_amount': self.transaction_amount,
            'department': self.department,
            'category': self.category,
            'account_type': self.account_type,
            'created_at': self.created_at
        }

# Manage database operations: insert, query data
class DatabaseManager:
    """Database management class"""
    
    def __init__(self, db_path: str = "data/foresight_analytics.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Create engine and session
        self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def insert_dataframe(self, df: pd.DataFrame) -> int:
        """Insert DataFrame into database"""
        try:
            # Map DataFrame columns to model
            transactions = []
            for _, row in df.iterrows():
                transaction = Transaction(
                    transaction_date=pd.to_datetime(row['Transaction Date']),
                    transaction_amount=float(row['Transaction Amount']),
                    department=str(row['Department']),
                    category=str(row['Category']),
                    account_type=self._get_account_type(row['Category'])
                )
                transactions.append(transaction)
            
            # Bulk insert
            self.session.bulk_save_objects(transactions)
            self.session.commit()
            
            return len(transactions)
            
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database insert failed: {str(e)}")
    
    def get_all_transactions(self) -> pd.DataFrame:
        """Get all transactions as DataFrame"""
        try:
            query = self.session.query(Transaction).all()
            
            if not query:
                return pd.DataFrame()
            
            data = [t.to_dict() for t in query]
            df = pd.DataFrame(data)
            
            # Rename columns to match original format
            df = df.rename(columns={
                'transaction_date': 'Transaction Date',
                'transaction_amount': 'Transaction Amount',
                'department': 'Department',
                'category': 'Category'
            })
            
            return df[['Transaction Date', 'Transaction Amount', 'Department', 'Category']]
            
        except Exception as e:
            raise Exception(f"Database query failed: {str(e)}")
    
    def filter_by_department(self, department: str) -> pd.DataFrame:
        """Filter transactions by department"""
        try:
            query = self.session.query(Transaction).filter(
                Transaction.department == department
            ).all()
            
            if not query:
                return pd.DataFrame()
            
            data = [t.to_dict() for t in query]
            df = pd.DataFrame(data)
            
            df = df.rename(columns={
                'transaction_date': 'Transaction Date',
                'transaction_amount': 'Transaction Amount',
                'department': 'Department',
                'category': 'Category'
            })
            
            return df[['Transaction Date', 'Transaction Amount', 'Department', 'Category']]
            
        except Exception as e:
            raise Exception(f"Database filter failed: {str(e)}")
    
    def get_departments(self) -> list:
        """Get unique departments"""
        try:
            result = self.session.query(Transaction.department).distinct().all()
            return [dept[0] for dept in result]
        except Exception as e:
            raise Exception(f"Failed to get departments: {str(e)}")
    
    def get_categories(self) -> list:
        """Get unique categories"""
        try:
            result = self.session.query(Transaction.category).distinct().all()
            return [cat[0] for cat in result]
        except Exception as e:
            raise Exception(f"Failed to get categories: {str(e)}")
    
    def _get_account_type(self, category: str) -> str:
        """Map category to account type"""
        account_mapping = {
            'Assets': 'Assets',
            'Loans': 'Liabilities',
            'Salaries': 'Expenses',
            'Supplies': 'Expenses',
            'Utilities': 'Expenses',
            'Rent': 'Expenses',
            'Royalties': 'Expenses',
            'Product Sales': 'Revenue',
            'Service Revenue': 'Revenue'
        }
        return account_mapping.get(category, 'Unknown')
    
    def close(self):
        """Close database session"""
        self.session.close()