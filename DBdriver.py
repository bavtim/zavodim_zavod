from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

from config import settings

engine = create_engine(settings.bot_db, future=True, echo=False)
Base = declarative_base()


class UsersData(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    pSQL_dbname = Column(String)
    pSQL_dbuser = Column(String)
    pSQL_dbpassword = Column(String)
    pSQL_dbhost = Column(String)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    def get_col(self):
        return [c.name for c in self.__table__.columns]

Base.metadata.create_all(engine)