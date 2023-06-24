import sqlalchemy

from core.config import db_url

engine = sqlalchemy.create_engine(db_url)
