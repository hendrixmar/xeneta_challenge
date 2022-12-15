from sqlalchemy.orm import sessionmaker
from app.db.settings import Settings
from sqlalchemy import create_engine, text
import psycopg2

engine = create_engine(Settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
