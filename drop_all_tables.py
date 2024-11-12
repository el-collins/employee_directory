from sqlmodel import create_engine, SQLModel
from sqlalchemy import text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)

def drop_all_tables():
    with engine.connect() as connection:
        # Disable foreign key checks
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        # Get all table names
        result = connection.execute(text("SHOW TABLES;"))
        tables = result.fetchall()
        
        # Drop all tables
        for table in tables:
            table_name = table[0]
            connection.execute(text(f"DROP TABLE IF EXISTS `{table_name}`;"))
        
        # Enable foreign key checks
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

if __name__ == "__main__":
    drop_all_tables()