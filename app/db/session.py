from sqlalchemy.orm import sessionmaker
from app.db.engine import engine


SessionLocal = sessionmaker(engine, expire_on_commit=False)