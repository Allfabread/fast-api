from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание экземпляра FastAPI
app = FastAPI()

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Здесь используется SQLite, но вы можете использовать другую базу данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определение базовой модели SQLAlchemy
Base = declarative_base()

# Определение модели данных
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Создание таблицы в базе данных (если она еще не существует)
Base.metadata.create_all(bind=engine)

# Маршрут для создания нового пользователя
@app.post("/users/")
def create_user(user_name: str):
    db = SessionLocal()
    user = User(name=user_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "user_name": user.name}