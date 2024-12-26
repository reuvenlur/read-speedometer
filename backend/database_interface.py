from sqlalchemy import create_engine, text
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger('DatabaseInterface')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - DatabaseInterface - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Database credentials from .env file
user = os.getenv('DATABASE_USER', 'root')  # Default to 'root' if not defined
password = os.getenv('DATABASE_PASSWORD', 'example')  # Default password
host = os.getenv('DATABASE_HOST', 'localhost')  # Default to localhost
port = int(os.getenv('DATABASE_INTERNAL_PORT', 3306))  # Convert to int, default to 3306
database = os.getenv('DATABASE_NAME', 'read_speedometer')  # Default database name

# Get SQLAlchemy connection
def get_connection():
    try:
        # Build the database URL
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url)
        logger.info("Database connection created successfully.")
        return engine
    except Exception as e:
        logger.error(f"Error creating database connection: {e}")
        raise

# Insert data into the table
def save_page_data(engine, username, page_number, time_spent, reading_speed):
    try:
        with engine.begin() as connection:  # Use engine.begin() to enable transactions
            query = text("""
                INSERT INTO page_data (username, page_number, time_spent, reading_speed)
                VALUES (:username, :page_number, :time_spent, :reading_speed)
            """)
            connection.execute(query, {
                "username": username,
                "page_number": page_number,
                "time_spent": time_spent,
                "reading_speed": reading_speed
            })
            logger.info(f"Data saved successfully: User={username}, Page={page_number}, Time={time_spent}, Speed={reading_speed}")
            return {"message": "Data saved successfully!"}
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return {"error": str(e)}

# Read data from the table
def read_table_data(engine):
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM page_data")
            result = connection.execute(query)
            rows = [row for row in result]
            logger.info(f"Data retrieved from the database: {rows}")
            return rows
    except Exception as e:
        logger.error(f"Error reading data: {e}")
        return {"error": str(e)}
