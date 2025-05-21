from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from models import SessionLocal
import uvicorn
app = FastAPI()

class GenerationCreate(BaseModel):
    user_id: int
    prompt: str
    image_url: str

class GenerationOut(BaseModel):
    id: int
    user_id: int
    prompt: str
    image_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generations/", response_model=GenerationOut)
def create_generation(generation: GenerationCreate, db: Session = Depends(get_db)):
    db_generation = models.Generation(**generation.dict())
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation

@app.get("/generations/{user_id}", response_model=list[GenerationOut])
def read_generations(user_id: int, db: Session = Depends(get_db)):
    generations = db.query(models.Generation).filter(models.Generation.user_id == user_id).all()
    return generations

@app.put("/generations/{generation_id}", response_model=GenerationOut)
def update_generation(generation_id: int, generation: GenerationCreate, db: Session = Depends(get_db)):
    db_generation = db.query(models.Generation).filter(models.Generation.id == generation_id).first()
    if not db_generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    for key, value in generation.dict().items():
        setattr(db_generation, key, value)
    db.commit()
    db.refresh(db_generation)
    return db_generation

@app.delete("/generations/{generation_id}")
def delete_generation(generation_id: int, db: Session = Depends(get_db)):
    db_generation = db.query(models.Generation).filter(models.Generation.id == generation_id).first()
    if not db_generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    db.delete(db_generation)
    db.commit()
    return {"message": "Generation deleted"}
