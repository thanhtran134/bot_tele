from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Generation(Base):
    __tablename__ = "generations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    prompt = Column(String)
    image_url = Column(String)

engine = create_engine("sqlite:///generations.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)