from sqlalchemy.orm import Session

from . import JobDefinition, Base

from sqlalchemy import create_engine, MetaData

if __name__ == "__main__":
    user = "automation"
    password = "neN8gnShMSpFC5rq"
    database = "automation"
    connection_url = f"postgresql+psycopg2://{user}:{password}@localhost:5432/{database}"
    engine = create_engine(connection_url, echo=True, future=True)
    Base.metadata.create_all(bind=engine)

    # job = JobDefinition.create(engine, 2, {}, "hello there", {}, {})
    items = JobDefinition.find_all(engine)
    for item in items:
        print(item)
