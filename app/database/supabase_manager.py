from supabase import create_client, Client
import pandas as pd
from typing import List, Dict, Any, Optional
from app.config.settings import AppConfig
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)

class SupabaseManager:
    """Supabase database manager for cloud operations"""
    
    def __init__(self):
        if not AppConfig.get_supabase_url() or not AppConfig.get_supabase_key():
            raise ValueError("Supabase credentials not found in environment variables")
        self.client: Client = create_client(
            AppConfig.get_supabase_url(),
            AppConfig.get_supabase_key()
        )
        self.table_name = 'transactions'
        
    def create_table_if_not_exists(self) -> bool:
        """Create transactions table if it doesn't exist"""
        try:
            # Check if table exists by trying to fetch one record
            result = self.client.table(self.table_name).select("*").limit(1).execute()
            logger.info("Transactions table already exists")
            return True
        except Exception as e:
            logger.info(f"Table might not exist: {str(e)}")
            # Table creation is done via Supabase dashboard
            # This is just a check - actual table creation happens in Supabase UI
            return False
    
    def insert_dataframe(self, df: pd.DataFrame) -> int:
        """Insert DataFrame into Supabase table"""
        try:
            # Convert DataFrame to list of dictionaries
            records = []
            for _, row in df.iterrows():
                record = {
                    'row_id': int(row['Row ID']),
                    'order_id': str(row['Order ID']),
                    'order_date': pd.to_datetime(row['Order Date'], format='%d/%m/%Y').isoformat(),
                    'ship_date': pd.to_datetime(row['Ship Date'], format='%d/%m/%Y').isoformat(),
                    'ship_mode': str(row['Ship Mode']),
                    'customer_id': str(row['Customer ID']),
                    'customer_name': str(row['Customer Name']),
                    'segment': str(row['Segment']),
                    'country': str(row['Country']),
                    'city': str(row['City']),
                    'state': str(row['State']),
                    'postal_code': str(row['Postal Code']) if pd.notna(row['Postal Code']) else None,
                    'region': str(row['Region']),
                    'product_id': str(row['Product ID']),
                    'category': str(row['Category']),
                    'sub_category': str(row['Sub-Category']),
                    'product_name': str(row['Product Name']),
                    'sales': float(row['Sales'])
                }
                records.append(record)
            
            # Insert in batches to avoid API limits
            batch_size = 1000
            total_inserted = 0
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                result = self.client.table(self.table_name).insert(batch).execute()
                total_inserted += len(batch)
                logger.info(f"Inserted batch {i//batch_size + 1}: {len(batch)} records")
            
            logger.info(f"Successfully inserted {total_inserted} records into Supabase")
            return total_inserted
            
        except Exception as e:
            logger.error(f"Failed to insert data into Supabase: {str(e)}")
            raise Exception(f"Supabase insert failed: {str(e)}")
    
    def has_data(self) -> bool:
        """Check if table has any data"""
        try:
            result = self.client.table(self.table_name).select("*").limit(1).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error checking data existence: {str(e)}")
            return False
    
    def get_all_transactions(self) -> pd.DataFrame:
        """Get all transactions as DataFrame"""
        try:
            # Fetch all data with pagination
            all_data = []
            offset = 0
            limit = 1000  # Supabase default limit per request
            while True:
                result = self.client.table(self.table_name).select("*").range(offset, offset + limit - 1).execute()
                if not result.data:
                    break
                all_data.extend(result.data)
                offset += limit
                if len(result.data) < limit:
                    break
            
            if not all_data:
                return pd.DataFrame()
            
            df = pd.DataFrame(all_data)
            
            # Convert date strings back to datetime
            if 'order_date' in df.columns:
                df['order_date'] = pd.to_datetime(df['order_date'])
            if 'ship_date' in df.columns:
                df['ship_date'] = pd.to_datetime(df['ship_date'])
            
            # Return only required columns
            required_cols = ['row_id', 'order_date', 'sales', 'region', 'category', 
                        'sub_category', 'segment', 'ship_mode', 'product_name', 
                        'city', 'state', 'postal_code']
            
            return df[required_cols]
            
        except Exception as e:
            logger.error(f"Error fetching all transactions: {str(e)}")
            raise Exception(f"Supabase query failed: {str(e)}")
    
    def filter_by_region(self, region: str) -> pd.DataFrame:
        """Filter transactions by region"""
        try:
            result = self.client.table(self.table_name).select("*").eq('region', region).execute()
            
            if not result.data:
                return pd.DataFrame()
            
            df = pd.DataFrame(result.data)
            
            # Convert date strings back to datetime
            if 'order_date' in df.columns:
                df['order_date'] = pd.to_datetime(df['order_date'])
            if 'ship_date' in df.columns:
                df['ship_date'] = pd.to_datetime(df['ship_date'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error filtering by region: {str(e)}")
            raise Exception(f"Supabase filter failed: {str(e)}")
    
    def get_regions(self) -> List[str]:
        """Get unique regions"""
        try:
            result = self.client.table(self.table_name).select("region").execute()
            regions = list(set([item['region'] for item in result.data]))
            return sorted(regions)
        except Exception as e:
            logger.error(f"Error getting regions: {str(e)}")
            return []
    
    def get_segments(self) -> List[str]:
        """Get unique segments"""
        try:
            result = self.client.table(self.table_name).select("segment").execute()
            segments = list(set([item['segment'] for item in result.data]))
            return sorted(segments)
        except Exception as e:
            logger.error(f"Error getting segments: {str(e)}")
            return []
    
    def get_categories(self) -> List[str]:
        """Get unique categories"""
        try:
            result = self.client.table(self.table_name).select("category").execute()
            categories = list(set([item['category'] for item in result.data]))
            return sorted(categories)
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return []
    
    def close(self):
        """Close connection (not needed for Supabase client)"""
        pass