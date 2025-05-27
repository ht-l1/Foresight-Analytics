from dotenv import load_dotenv
from app.database.supabase_manager import SupabaseManager
from app.config.settings import AppConfig
import os

# Load environment variables from .env
load_dotenv()

# Debug: Print environment variables and AppConfig
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_KEY: {os.getenv('SUPABASE_KEY')}")
print(f"DATABASE_MODE: {os.getenv('DATABASE_MODE')}")
print(f"AppConfig.get_supabase_url(): {AppConfig.get_supabase_url()}")
print(f"AppConfig.get_supabase_key(): {AppConfig.get_supabase_key()}")
print(f"AppConfig.get_database_mode(): {AppConfig.get_database_mode()}")

# Test Supabase connection and data
try:
    mgr = SupabaseManager()
    print("Connection successful!")
    has_data = mgr.has_data()
    print(f"Has data: {has_data}")
    if has_data:
        df = mgr.get_all_transactions()
        print(f"Rows fetched: {len(df)}")
        print("Sample data:")
        print(df.head())
    else:
        print("No data found in Supabase.")
except Exception as e:
    print(f"Connection or data fetch failed: {str(e)}")