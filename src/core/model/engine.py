from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.model.base import Base
from core.model.light_stability import LightStabilityResult


class DB:
    def __init__(self):
        self.engine = create_engine(
            "sqlite+pysqlite:///my.db",
            connect_args={
                "autocommit": False,
            },
            echo=True,
        )
        self.Session = sessionmaker(self.engine, autoflush=True)

        Base.metadata.create_all(self.engine)

    def session(self):
        return self.Session()


db = DB()

if __name__ == "__main__":
    print("hello")
