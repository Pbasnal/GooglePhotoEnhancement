import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, query, Session, declarative_base

BASE = declarative_base()

class SqlConnection(object):
    def __init__(self, connectionStr):
        self.engine = db.create_engine(connectionStr, echo=True)
        self.connection = self.engine.connect()

    def __enter__(self):
        BASE.metadata.create_all(self.engine)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


class SqlEngine(object):
    session = Session()

    def __init__(self, connection: SqlConnection):
        self.connection = connection
        self.engine = connection.engine

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        self.session.expire_on_commit = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.commit()

    def add(self, row):
        self.session.add(row)
        return self

    def select(self, table) -> query.Query:
        return self.session.query(table)


    def execute(self, query):
        return self.connection.execute(query)
