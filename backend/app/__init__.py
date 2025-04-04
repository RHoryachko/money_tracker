from app.database import Base, SessionLocal, engine
from app.dependencies import get_db

Base.metadata.create_all(bind=engine)