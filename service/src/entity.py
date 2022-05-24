from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import declarative_base, relationship

from config.engine import InternalDatabaseConfiguration

Base = declarative_base()


class Bioobject(Base):
    __tablename__ = "bioobject"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)

    analysis = relationship("Analysis")


class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True)
    bioobject_id = Column(Integer, ForeignKey("bioobject.id"), nullable=False)
    content = Column(JSON, nullable=False)


Base.metadata.create_all(InternalDatabaseConfiguration.get_engine())
