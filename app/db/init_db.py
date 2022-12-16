from sqlalchemy.orm import sessionmaker
from app.tools.settings import Settings
from sqlalchemy import create_engine

engine = create_engine(Settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
