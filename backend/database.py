from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:rsmmsr@localhost:3306/online_pharmacy"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ MySQL connection successful!")
    except Exception as e:
        print("❌ MySQL connection failed!")
        print(e)