from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


connection_url = f"postgresql://postgres:kUMAR_66231456@db.azcnbbsxiugpmncqhxcn.supabase.co:5432/postgres"


engine = create_engine(connection_url)


Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()